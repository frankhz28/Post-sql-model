from os import name

from backend.app.api.v1.posts.repository import PostRepository
from backend.app.models.post import Post, PostCreate, PostUpdate
from sqlalchemy.exc import SQLAlchemyError
from backend.app.api.v1.tag.repository import TagRepository
from backend.app.models.tag import Tag
from backend.app.models.user import User
from backend.app.service.pagination import PaginatedResponse, paginated_query

class DatabaseError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def user_can_edit(self,user: User, post: Post) -> bool:
        if user.id == post.owner_id:
            return True
        return user.is_staff

    def user_can_delete(self,user: User, post: Post) -> bool:
        if user.id == post.owner_id:
            return True
        return user.is_admin

    def get_posts(
            self,
            query: str | None,
            page: int,
            per_page: int,
            order_by: str,
            direction: str,
            user_id: int | None = None
        ) -> PaginatedResponse:

        try:
            base_query = self.repository.get_base_query(title_query=query, user_id=user_id)

            return paginated_query(
                db=self.repository.db,
                model=Post,
                base_query=base_query, 
                page=page, 
                per_page=per_page,
                order_by=order_by,
                direction=direction,
                allowed_order={"id": Post.id, "title": Post.title}
            )
        except SQLAlchemyError:
            raise DatabaseError("Error al buscar post")

    def create_post(self, post_create: PostCreate, user_id: int) -> Post:
        try:
            post = Post(
                owner_id=user_id,
                title=post_create.title,
                content=post_create.content
            )
            tag_repository = TagRepository(db=self.repository.db)
            for tag in post_create.tags:
                clean_tag_name= tag.name.lower().strip()
                tag_obj = tag_repository.get_tag_by_name(name=clean_tag_name)
                if tag_obj:
                    post.tags.append(tag_obj)
                else:
                    tag_obj = Tag(name=clean_tag_name, owner_id=user_id)
                    post.tags.append(tag_obj)
            return self.repository.create_post(post=post)
        except SQLAlchemyError:
            raise DatabaseError("Error al crear el post")

    def get_posts_by_user(self, user_id: int, query: str | None) -> list[Post]:
        try:
            return self.repository.get_posts_by_user(user_id=user_id, title_query=query)
        except SQLAlchemyError:
            raise DatabaseError("Error al buscar post")

    def update_post(self, post_id: int, user: User, payload: PostUpdate) -> Post | None:
        post = self.repository.get_post_by_id(post_id=post_id)

        if not post:
            raise NotFoundError("El post no existe")

        if not self.user_can_edit(user=user, post=post):
            raise ForbiddenError("No tienes permisos para editar este post")

        updates= payload.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(post,key,value)

        try:
            return self.repository.update_post(post=post)
        except SQLAlchemyError:
            raise DatabaseError("Error al actualizar el post en la base de datos")

    def delete_post(self, post_id: int, user: User) -> None:
        post = self.repository.get_post_by_id(post_id=post_id)
        if not post:
            raise NotFoundError("El post no existe")

        if not self.user_can_delete(user=user, post=post):
            raise ForbiddenError("No tienes permisos para eliminar este post")

        try:
            self.repository.delete_post(post=post)
        except SQLAlchemyError:
            raise DatabaseError("Error al eliminar el post en la base de datos")