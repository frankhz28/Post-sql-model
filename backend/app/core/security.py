from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from backend.app.core.config import settings

pwd_contex = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_contex.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_contex.verify(plain_password, hashed_password)

def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes or settings.JWT_EXPIRES_MIN)
    return jwt.encode(
        payload={
            "sub" : sub,
            "exp":expire
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )

def decode_token(token: str) -> dict:
    return jwt.decode(jwt=token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALG])