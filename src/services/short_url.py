from dataclasses import dataclass
from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.models import ShortUrlBulkCreate, ShortUrlCreate, ShortUrlDetail, ShortUrlList
from src.repositories import ShortUrlRepository
from src.services import ServiceMixin

__all__ = (
    "ShortUrlService",
    "get_short_url_service",
)


@dataclass
class ShortUrlService(ServiceMixin):
    """Short url service."""

    async def get(self, short_url: str) -> ShortUrlDetail:
        """Get short url by short url."""
        short_url = await self.repository.get(short_url=short_url)
        if not short_url:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        elif short_url.is_removed:  # type: ignore
            raise HTTPException(status_code=HTTPStatus.GONE)
        return ShortUrlDetail.from_orm(short_url)

    async def create(self, data: ShortUrlCreate) -> ShortUrlDetail:
        """Create short url."""
        return ShortUrlDetail.from_orm(await self.repository.add(data=data))

    async def bulk_create(self, data: ShortUrlBulkCreate) -> ShortUrlList:
        """Create short urls."""
        return ShortUrlList.from_orm(await self.repository.bulk_add(data=data))

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        await self.repository.delete(short_url=short_url)


async def get_short_url_service(
    session: AsyncSession = Depends(get_async_session),
) -> ShortUrlService:
    """Get short url service."""
    repository = ShortUrlRepository(session=session)
    return ShortUrlService(repository=repository)
