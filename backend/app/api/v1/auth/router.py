from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.app.api.v1.auth.repository import UserRepository
from backend.app.api.v1.auth.service import DatabaseError, UserAlreadyExistsError, UserService
from backend.app.core.db import get_session
from backend.app.models.user import UserCreate, UserPublic


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic)
def register(payload: UserCreate, db: Session = Depends(get_session)):
    service = UserService(UserRepository(db))
    try:
        return service.register(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )