from sqlalchemy.exc import SQLAlchemyError

from backend.app.api.v1.tag.repository import TagRepository
from backend.app.models.tag import Tag, TagCreate
from backend.app.service.pagination import PaginatedResponse, paginated_query

class DatabaseError(Exception):
    pass

class TagAlreadyExistsError(Exception):
    pass

class TagService:
    def __init__(self, repository: TagRepository):
        self.repository= repository

    def create_tag(self, tag_create: TagCreate, user_id: int) -> Tag:
        try:
            if self.repository.get_tag_by_name(tag_create.name):
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
