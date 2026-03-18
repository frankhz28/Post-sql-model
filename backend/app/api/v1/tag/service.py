from sqlalchemy.exc import SQLAlchemyError

from backend.app.api.v1.tag.repository import TagRepository
from backend.app.models.tag import Tag, TagCreate

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