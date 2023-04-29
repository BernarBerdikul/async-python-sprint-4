from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.models import ShortUrlCreate, ShortUrlDetail
from src.repositories import ShortUrlRepository
from src.services import ServiceMixin

__all__ = (
    "ShortUrlService",
    "get_short_url_service",
)


@dataclass
class ShortUrlService(ServiceMixin):
    """Short url service."""

    async def create(self, data: ShortUrlCreate) -> ShortUrlDetail:
        """Create short url."""
        return ShortUrlDetail.from_orm(await self.repository.add(data=data))

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        await self.repository.delete(short_url=short_url)


async def get_short_url_service(
    session: AsyncSession = Depends(get_async_session),
) -> ShortUrlService:
    """Get short url service."""
    repository = ShortUrlRepository(session=session)
    return ShortUrlService(repository=repository)
