import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import async_engine
from src.main import app
from src.models import ShortUrl
from tests.factories.short_url import ShortUrlFactory


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    yield session
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def short_url_instance(async_session) -> ShortUrl:
    async with async_session() as session:
        instance = ShortUrlFactory()
        session.add(instance)
        await session.commit()
    yield instance


@pytest_asyncio.fixture(scope="function")
async def removed_short_url_instance(async_session) -> ShortUrl:
    async with async_session() as session:
        instance = ShortUrlFactory(is_removed=True)
        session.add(instance)
        await session.commit()
    yield instance
