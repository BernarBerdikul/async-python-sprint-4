import http

import pytest
from sqlalchemy import select

from src.models import ShortUrl
from tests.factories.short_url import ShortUrlFactory


@pytest.mark.asyncio
async def test_delete_success_short_url(async_client, async_session):
    short_url = ShortUrlFactory()

    async_session.add(short_url)
    await async_session.commit()

    response = await async_client.delete(
        url=f"/api/v1/short-urls/{short_url.short_url}/",
    )
    print(short_url)
    print(short_url.is_removed)
    print("*"*100)
    assert response.status_code == http.HTTPStatus.NO_CONTENT

    # async with async_engine.connect() as conn:
    #     result = await conn.execute(select(ShortUrl).where(
    #         ShortUrl.short_url == short_url,
    #     ))
    #     short_url = await result.fetchone()
    # assert short_url.is_removed is True

