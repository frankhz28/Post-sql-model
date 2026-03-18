from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from backend.app.models.post_tag_link import PostTagLink
from backend.app.models.tag import TagPublic

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
    owner_id: int = Field(
        foreign_key="user.id",
        index=True,
    )
    tags: list["Tag"] = Relationship(
        back_populates="posts",
        link_model=PostTagLink
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
    owner_id: int
    tags: list[TagPublic] = Field(
        default_factory=[]
    )
    model_config = {"from_attributes": True}

class PostUpdate(SQLModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,  
    )
    content: str | None = Field(
        default=None,
        min_length=1 
    )