from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from backend.app.api.v1.auth.repository import UserRepository
from backend.app.core.db import get_session
from backend.app.core.security import decode_token
from backend.app.models.user import User
import jwt

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(db: Annotated[Session, Depends(get_session)], token: Annotated[str,Depends(ouath2_scheme)]) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload= decode_token(token=token)
        user_id= int(payload.get("sub"))
    except jwt.PyJWTError: 
        raise credentials_exc

    repository = UserRepository(db=db)
    user= repository.get_by_id(user_id=user_id)
    
    if not user:
        raise credentials_exc

    return user