from contextlib import contextmanager
from typing import Optional
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.db import engine
from ..models.tag import Tag
from ..models.user import User
from .. import models
from .data.tags import TAGS
from .data.users import USERS


def hash_password(plain: str) -> str:
    return PasswordHash.recommended().hash(plain)

@contextmanager
def atomic(db: Session):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise

def _user_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalars().first()


def _tag_by_name(db: Session, name: str) -> Optional[Tag]:
    return db.execute(select(Tag).where(Tag.name == name)).scalars().first()


def seed_users(db: Session) -> None:
    with atomic(db=db):
        for data in USERS:
            obj = _user_by_email(db=db, email=data.get("email"))
            if obj:
                changed = False
                if obj.full_name != data.get("full_name"):
                    obj.full_name = data.get("full_name")
                    changed = True
                if data.get("password") and not PasswordHash.recommended().verify(data.get("password"), obj.hashed_password):
                    obj.hashed_password = hash_password(plain=data.get("password"))
                    changed = True
                if data.get("role"):
                    obj.role = data.get("role")
                    changed = True
                if changed:
                    db.add(obj)
            else:
                db.add(User(
                    email=data.get("email"),
                    full_name=data.get("full_name"),
                    hashed_password=hash_password(plain=data.get("password")),
                    role=data.get("role")
                ))


def seed_tags(db: Session) -> None:
    admin_email= USERS[0].get("email")
    admin_user= _user_by_email(db=db, email=admin_email)
    
    if not admin_user:
        raise Exception("Error: No se encontro al usuario administrador. Ejecutar seed_users primero")
    
    with atomic(db=db):
        for data in TAGS:
            obj = _tag_by_name(db=db, name=data.get("name"))
            if not obj:
                db.add(Tag(
                    name=data.get("name"),
                    owner_id=admin_user.id
                ))


def run_all() -> None:
    with Session(engine) as db:
        seed_users(db=db)
        seed_tags(db=db)


def run_users() -> None:
    with Session(engine) as db:
        seed_users(db=db)


def run_tags() -> None:
    with Session(engine) as db:
        seed_tags(db=db)