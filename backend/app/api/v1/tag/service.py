from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.app.api.v1.tag.repository import TagRepository
from backend.app.models.tag import Tag, TagCreate, TagUpdate
from backend.app.models.user import User
from backend.app.service.pagination import PaginatedResponse, paginated_query

class DatabaseError(Exception):
    pass

class TagAlreadyExistsError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class TagService:
    def __init__(self, repository: TagRepository):
        self.repository= repository

    def user_can_edit(self,user: User, tag: Tag) -> bool:
        if user.id == tag.owner_id:
            return True
        return user.is_staff


    def user_can_delete(self,user: User, tag: Tag) -> bool:
        if user.id == tag.owner_id:
            return True
        return user.is_admin

    def create_tag(self, tag_create: TagCreate, user_id: int) -> Tag:
        try:
            setattr(tag_create, "name", tag_create.name.lower().strip())
            if self.repository.get_tag_by_name(name=tag_create.name):
                raise TagAlreadyExistsError("Tag ya registrado")
            tag = Tag(owner_id=user_id, **tag_create.model_dump())
            return self.repository.create_tag(tag=tag)
        except SQLAlchemyError:
            raise DatabaseError("Error al crear el tag")

    def get_tags(
            self,
            query: str | None,
            page: int,
            per_page: int,
            order_by: str,
            direction: str,
            user_id: int | None = None
        ) -> PaginatedResponse:

        try:
            base_query = self.repository.get_base_query(name_query=query, user_id=user_id)

            return paginated_query(
                db=self.repository.db,
                model=Tag,
                base_query=base_query, 
                page=page, 
                per_page=per_page,
                order_by=order_by,
                direction=direction,
                allowed_order={"id": Tag.id, "name": Tag.name}
            )
        except SQLAlchemyError:
            raise DatabaseError("Error al buscar tag")

    def update_tag(self, tag_id: int, user: User, payload: TagUpdate) -> Tag | None:
        tag = self.repository.get_tag_by_id(tag_id=tag_id)

        if not tag:
            raise NotFoundError("El tag no existe")

        if not self.user_can_edit(user=user, tag=tag):
            raise ForbiddenError("No tienes permisos para editar este tag")

        updates= payload.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(tag,key,value)

        try:
            return self.repository.update_tag(tag=tag)
        except IntegrityError:
            raise TagAlreadyExistsError("Ya existe un tag con este nombre")
        except SQLAlchemyError:
            raise DatabaseError("Error al actualizar el tag en la base de datos")

    def delete_tag(self, tag_id: int, user: User) -> None:
        tag = self.repository.get_tag_by_id(tag_id=tag_id)
        if not tag:
            raise NotFoundError("El tag no existe")

        if not self.user_can_delete(user=user, tag=tag):
            raise ForbiddenError("No tienes permisos para eliminar este tag")

        try:
            self.repository.delete_tag(tag=tag)
        except SQLAlchemyError:
            raise DatabaseError("Error al eliminar el tag en la base de datos")