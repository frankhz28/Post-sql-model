from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from backend.app.models.post_tag_link import PostTagLink

if TYPE_CHECKING:
    from .post import Post

class TagBase(SQLModel):
    name: str = Field(
        min_length=1,
        max_length=50,
        index=True,
        unique=True
    )

class Tag(TagBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True
    )
    posts: list[Post] = Relationship(
        back_populates="tags",
        link_model=PostTagLink
    ) 

class TagPublic(TagBase):
    id: int