from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    title: str = Field(
        index=True,
        min_length=1,
        max_length=255,
        
    )
    content: str = Field(
        min_length=1,
    )

class Post(PostBase, table=True):
    id: int = Field(
        default=None,
        primary_key=True,
        index=True,
    )
    created_at: datetime = Field(
        default_factory= lambda : datetime.now(timezone.utc),
        nullable=False,
    )

class PostCreate(PostBase):
    model_config= {
        "json_schema_extra" : {
            "example": {
                "title": "El asombroso mundo de Gumball",
                "content": "Serie de animacion britanico-estadounidense de comedia familiar"
            }
        }
    } 

class PostPublic(PostBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}