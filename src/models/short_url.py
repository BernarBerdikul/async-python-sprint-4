from pydantic import HttpUrl
from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import UUIDMixin

__all__ = (
    "ShortUrl",
    "ShortUrlCreate",
    "ShortUrlDetail",
)


class ShortUrlBase(SQLModel):
    """Short URL base model."""

    short_url: str = Field(
        nullable=False,
        unique=True,
        index=True,
    )


class ShortUrlCreate(SQLModel):
    """Short URL create model."""

    original_url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "original_url": "https://www.google.com/",
            },
        }


class ShortUrlDetail(ShortUrlBase, UUIDMixin):
    """Short URL detail model."""


class ShortUrl(UUIDMixin, ShortUrlBase, table=True):  # type: ignore
    """Short URL model in database."""

    __tablename__ = "short_url"  # noqa

    original_url: str = Field(nullable=False)
    usage_count: int = Field(
        title="Short URL usage count",
        default=0,
        nullable=False,
    )
    is_removed: bool = Field(
        title="Deleted flag",
        default=False,
        nullable=False,
    )
    short_url_logs: list["ShortUrlLog"] = Relationship(  # type: ignore
        back_populates="short_url",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )
