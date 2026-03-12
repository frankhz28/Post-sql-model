from backend.app.api.v1.posts.repository import PostRepository
from backend.app.models.post import Post, PostCreate
from sqlalchemy.exc import SQLAlchemyError

class DatabaseError(Exception):
    pass

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository


    def get_post_by_title(self, title:str) -> list[Post]:    
        try:
            title = title.lower().strip()
            return self.repository.get_by_title(title=title)
        except SQLAlchemyError:
            raise DatabaseError("Error interno al acceder a la base de datos para buscar posts")


    def create_post(self, post_create: PostCreate) -> Post:
        try:
            post = Post(**post_create.model_dump())
            return self.repository.create_post(post=post)
        except SQLAlchemyError:
            raise DatabaseError("Error al crear el post")