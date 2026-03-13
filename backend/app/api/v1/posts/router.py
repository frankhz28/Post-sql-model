from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.app.api.v1.posts.repository import PostRepository
from backend.app.api.v1.posts.service import DatabaseError, PostService
from backend.app.core.db import get_session
from backend.app.api.v1.deps import get_current_user
from backend.app.models.post import PostCreate, PostPublic
from backend.app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])

def database_error(e: DatabaseError):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )

@router.post("", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User,Depends(get_current_user)]
):
    try:
        service = PostService(PostRepository(db))
        return service.create_post(user_id=user.id, post_create=post)
    except DatabaseError as e:
        raise database_error(e)

@router.get("/search", response_model=list[PostPublic], status_code=status.HTTP_200_OK)
def get_post_by_tittle(
    title: str,
    db: Annotated[Session, Depends(get_session)]
):
    try:
        service = PostService(PostRepository(db))
        return service.get_post_by_title(title=title)
    except DatabaseError as e:
        raise database_error(e)

@router.get("/me", response_model=list[PostPublic])
def get_posts_by_user(
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        service = PostService(PostRepository(db=db))
        return service.get_posts_by_user(user_id=user.id)
    except DatabaseError as e:
        raise database_error(e)