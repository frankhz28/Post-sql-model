from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.post import Post
from backend.app.models.tag import Tag


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_post_by_id(self, post_id: int) -> Post | None:
        return self.db.get(Post, post_id)

    def create_post(self, post: Post) -> Post:
        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except SQLAlchemyError as e:
            self.db.rollback()
            raise

    def get_base_query(self, title_query: str | None, tag_query: str | None, user_id: int | None):
        try:
            stmt= select(Post)
            if user_id:
                stmt= stmt.where(Post.owner_id == user_id)
            if title_query:
                stmt= stmt.where(
                    func.lower(func.trim(Post.title)).like(f"%{title_query}%")
                )
            if tag_query:
                stmt= stmt.where(
                    Post.tags.any(func.lower(func.trim(Tag.name)).like(f"%{tag_query}%"))
                )
            
            return stmt
        except SQLAlchemyError:
            raise

    def get_posts(self, title_query: str | None) -> list[Post]:
        try:
            stmt = select(Post)
            if title_query:
                stmt = stmt.where(
                    (func.lower(func.trim(Post.title)).like(f"%{title_query}%"))
                )
            return self.db.exec(stmt).all()            
        except SQLAlchemyError:
            raise

    def get_posts_by_user(self, user_id: int, title_query: str | None) -> list[Post]:
        try:
            stmt = select(Post).where(Post.owner_id == user_id)
            if title_query:
                stmt = stmt.where(
                    func.lower(func.trim(Post.title)).like(f"%{title_query}%")
                )
            return self.db.exec(stmt).all()
        except SQLAlchemyError:
            raise

    def update_post(self, post: Post) -> Post:
        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_post(self, post: Post) -> None:
        try:
            self.db.delete(post)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise