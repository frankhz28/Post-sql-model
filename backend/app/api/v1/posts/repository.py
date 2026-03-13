from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.post import Post


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


    def get_by_title(self, title: str) -> list[Post]:
        try:
            query = select(Post).where(func.lower(func.trim(Post.title)).like(f"%{title}%"))
            return self.db.exec(query).all()
        except SQLAlchemyError:
           raise

    def get_posts_by_user(self, user_id: int) -> list[Post]:
        try:
            query = select(Post).where(Post.owner_id == user_id)
            return self.db.exec(query).all()
        except SQLAlchemyError:
            raise