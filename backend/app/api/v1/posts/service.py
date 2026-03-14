from backend.app.api.v1.posts.repository import PostRepository
from backend.app.models.post import Post, PostCreate, PostUpdate
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.user import User

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

    def get_post_by_title(self, title:str) -> list[Post]:    
        try:
            title = title.lower().strip()
            return self.repository.get_by_title(title=title)
        except SQLAlchemyError:
            raise DatabaseError("Error interno al acceder a la base de datos para buscar posts")


    def create_post(self, post_create: PostCreate, user_id: int) -> Post:
        try:
            post = Post(owner_id=user_id,**post_create.model_dump())
            return self.repository.create_post(post=post)
        except SQLAlchemyError:
            raise DatabaseError("Error al crear el post")

    def get_posts_by_user(self, user_id: int) -> list[Post]:
        try:
            return self.repository.get_posts_by_user(user_id=user_id)
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