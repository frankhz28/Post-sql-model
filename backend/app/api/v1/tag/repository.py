from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from backend.app.models import tag
from backend.app.models.tag import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db= db

    def get_tag_by_id(self, tag_id: int) -> Tag | None:
        return self.db.get(Tag,tag_id)

    def get_tag_by_name(self, name: str) -> Tag | None:
        stmt = select(Tag).where(
            Tag.name == name
        )
        return self.db.exec(stmt).first()

    def create_tag(self, tag: Tag) -> Tag:
        try:
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
            return tag
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_base_query(self, name_query: str | None, user_id: int | None):
        try:
            stmt= select(Tag)
            if user_id:
                stmt= stmt.where(Tag.owner_id == user_id)
            if name_query:
                stmt= stmt.where(
                    func.lower(func.trim(Tag.name)).like(f"%{name_query}%")
                )
            return stmt
        except SQLAlchemyError:
            raise