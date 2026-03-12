from typing import Annotated
from fastapi import Depends
from pwdlib import PasswordHash
from sqlmodel import Session
from backend.app.api.v1.deps import ouath2_scheme
from backend.app.core.db import get_session
from backend.app.models.user import User

pwd_contex = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_contex.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_contex.verify(plain_password, hashed_password)

async def get_current_user(db: Annotated[Session, Depends(get_session)], token: Annotated[str,Depends(ouath2_scheme)]) -> User:
    return db.get(User,int(token))