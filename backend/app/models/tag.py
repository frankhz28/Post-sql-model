from sqlmodel import Field, Relationship, SQLModel
from backend.app.models.post_tag_link import PostTagLink

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
    owner_id: int = Field(
        foreign_key="user.id",
        index=True
    )
    posts: list["Post"] = Relationship(
        back_populates="tags",
        link_model=PostTagLink
    ) 

class TagPublic(TagBase):
    id: int
    owner_id: int

class TagCreate(TagBase):
    model_config= {
        "json_schema_extra":{
            "example":{
                "name":"dev"
            }
        }
    }

class TagUpdate(TagBase):
    model_config= {
        "json_schema_extra":{
            "example":{
                "name":"tag_actualizado"
            }
        }
    }