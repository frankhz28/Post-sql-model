from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from backend.app.api.v1.deps import get_current_user
from backend.app.api.v1.tag.repository import TagRepository
from backend.app.api.v1.tag.service import DatabaseError, TagAlreadyExistsError, TagService
from backend.app.core.db import get_session
from backend.app.models.tag import TagCreate, TagPublic
from backend.app.models.user import User


router = APIRouter(prefix="/tag", tags=["Tag"])

def database_error(e: DatabaseError):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )

@router.post("", response_model=TagPublic, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagCreate,
    db: Annotated[Session, Depends(get_session)],
    user: Annotated[User,Depends(get_current_user)]
):
    try:
        service = TagService(TagRepository(db=db))
        return service.create_tag(
            tag_create=tag,
            user_id=user.id
        )
    except SQLAlchemyError as e:
        raise database_error(e)
    except TagAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
