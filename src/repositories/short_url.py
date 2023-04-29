from sqlalchemy import update

from src.models import ShortUrl, ShortUrlCreate
from src.repositories import AbstractRepository
from src.utils import shortuuid

__all__ = ("ShortUrlRepository",)


class ShortUrlRepository(AbstractRepository):
    model: type[ShortUrl] = ShortUrl  # type: ignore

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

    async def delete(self, short_url: str) -> None:
        """Soft delete short url."""
        await self.session.execute(update(self.model).where(self.model.short_url == short_url).values(is_removed=True))
        await self.session.commit()
