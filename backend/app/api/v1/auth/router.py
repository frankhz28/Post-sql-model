from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from backend.app.api.v1.auth.repository import UserRepository
from backend.app.api.v1.auth.service import DatabaseError, InvalidCredentialsError, UserAlreadyExistsError, UserService
from backend.app.core.db import get_session
from backend.app.core.security import ouath2_scheme
from backend.app.models.user import UserCreate, UserPublic


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic)
async def register(payload: UserCreate, db: Session = Depends(get_session)):
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


@router.post("/token")
async def login(db: Annotated[Session, Depends(get_session)], form :Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = form.username
    password = form.password
    service = UserService(UserRepository(db))
    try:
        token = service.login(user, password)
        return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
