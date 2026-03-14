import re
from pydantic import field_validator
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field

class Role(str, Enum):
    USER= "user"
    EDITOR= "editor"
    ADMIN= "admin"

class UserBase(SQLModel):
    email: str = Field(
        max_length=255,
        index=True,
        unique=True
    )
    full_name: str = Field(
        max_length=255
    )

class User(UserBase, table=True):
    id: int = Field(
        default=None,
        primary_key=True,
        index=True
    )
    hashed_password: str
    role: Role = Field(
        default=Role.USER
    )
    is_active: bool = Field(
        default=True
    )
    created_at: datetime = Field(
        default_factory= lambda: datetime.now(timezone.utc)
    )

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    @property
    def is_editor(self) -> bool:
        return self.role == Role.EDITOR
    
    @property
    def is_staff(self) -> bool:
        return self.is_admin or self.is_editor

class UserCreate(UserBase):    
    password: str = Field(
        description="Contraseña alpha numerico",
        min_length=6,
        max_length=72
    )

    model_config= {
        "json_schema_extra" : {
            "example": {
                "email": "user@gmail.com",
                "full_name": "User example",
                "password": ""
            }
        }
    }

    @field_validator("password")
    def validate_password_complexity(cls, value: str) -> str:
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]+$"
        if not re.match(pattern, value):
            raise ValueError("El password debe contener al menos una letra, un numero y ser estrictamente alfanumerico")
        return value

class UserPublic(UserBase):
    id : int
    role : Role
    is_active: bool
    created_at: datetime
    model_config= {"from_attributes": True}