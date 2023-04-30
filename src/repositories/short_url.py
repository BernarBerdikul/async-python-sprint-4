from sqlalchemy import select, update

from src.models import ShortUrl, ShortUrlBulkCreate, ShortUrlCreate
from src.repositories import AbstractRepository
from src.utils import shortuuid

__all__ = ("ShortUrlRepository",)


class ShortUrlRepository(AbstractRepository):
    model: type[ShortUrl] = ShortUrl  # type: ignore

    async def get(self, short_url: str) -> ShortUrl | None:  # type: ignore
        """Get short url by short url."""
        result = await self.session.execute(
            select(self.model).where(
                self.model.short_url == short_url,
            )
        )
        return result.scalars().first()

    async def add(self, data: ShortUrlCreate) -> ShortUrl:
        """Add short url."""
        new_short_url = self.model(
            short_url=await shortuuid.uuid(),
            original_url=data.original_url,
        )
        self.session.add(new_short_url)
        await self.session.commit()
        await self.session.refresh(new_short_url)
        return new_short_url

    async def bulk_add(self, data: ShortUrlBulkCreate) -> list[ShortUrl]:
        """Bulk add short urls."""
        new_short_urls = [
            self.model(
                short_url=await shortuuid.uuid(),
                original_url=url,
            )
            for url in data.urls
        ]
        self.session.add_all(new_short_urls)
        await self.session.commit()
        return new_short_urls

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        await self.session.execute(update(self.model).where(self.model.short_url == short_url).values(is_removed=True))
        await self.session.commit()
