from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class PostTagLink(SQLModel, table=True):
    __tablename__="post_tag_link"
    __table_args__= (UniqueConstraint(
        "post_id",
        "tag_id",
        name="uq_post_tag"
    ),)

    post_id: int = Field(
        foreign_key="post.id",
        primary_key=True
    )
    tag_id: int = Field(
        foreign_key="tag.id",
        primary_key=True
    )