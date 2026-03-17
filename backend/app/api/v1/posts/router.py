from typing import Annotated, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.app.api.v1.posts.repository import PostRepository
from backend.app.api.v1.posts.service import DatabaseError, ForbiddenError, NotFoundError, PostService
from backend.app.core.db import get_session
from backend.app.api.v1.deps import get_current_user
from backend.app.models.post import PostCreate, PostPublic, PostUpdate
from backend.app.models.user import User
from backend.app.service.pagination import PaginatedResponse

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

@router.get("", response_model=PaginatedResponse[PostPublic], status_code=status.HTTP_200_OK)
def list_posts(
    db: Annotated[Session, Depends(get_session)],
    query: Optional[str] = None,
    per_page: int = 10,
    page: int = 1,
    order_by: Literal["id","title"] = "id",
    direction: Literal["asc","desc"] = "asc"
):
    try:
        service = PostService(PostRepository(db))
        return service.get_posts(
            query=query,
            per_page=per_page,
            page=page,
            order_by=order_by,
            direction=direction
        )
    except DatabaseError as e:
        raise database_error(e)

@router.get("/me", response_model=PaginatedResponse[PostPublic], status_code=status.HTTP_200_OK)
def get_posts_by_user(
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    query: Optional[str] = None,
    per_page: int = 10,
    page: int = 1,
    order_by: Literal["id","title"] = "id",
    direction: Literal["asc","desc"] = "asc"
):
    try:
        service = PostService(PostRepository(db))
        return service.get_posts(
            query=query,
            per_page=per_page,
            page=page,
            order_by=order_by,
            direction=direction,
            user_id=user.id
        )
    except DatabaseError as e:
        raise database_error(e)

@router.put("/{post_id}",response_model=PostPublic)
def update_post(
    post_id: int,
    payload: PostUpdate,
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        service = PostService(PostRepository(db=db))
        return service.update_post(post_id=post_id,user=user,payload=payload)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DatabaseError as e:
        raise database_error(e)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        service = PostService(PostRepository(db=db))
        return service.delete_post(post_id=post_id, user=user)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DatabaseError as e:
        raise database_error(e)