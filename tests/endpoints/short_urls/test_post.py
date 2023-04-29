import http

import pytest


@pytest.mark.asyncio
async def test_create_success_short_url(async_client):
    response = await async_client.post(
        url="/api/v1/short-urls/",
        json={"original_url": "https://www.google.com/"},
    )
    data = response.json()
    assert response.status_code == http.HTTPStatus.CREATED, data
