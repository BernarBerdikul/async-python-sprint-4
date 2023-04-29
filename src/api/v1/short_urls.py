import http

from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.models import ShortUrlCreate, ShortUrlDetail
from src.services import ShortUrlService, get_short_url_service

router = APIRouter(
    prefix="/short-urls",
    tags=["short-urls"],
)


@router.post(
    path="/",
    response_model=ShortUrlDetail,
    summary="Create short url",
    status_code=http.HTTPStatus.CREATED,
)
async def create_short_url(
    *,
    data: ShortUrlCreate,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
) -> ShortUrlDetail:
    """Create short url."""
    return await short_url_service.create(data=data)


@router.delete(
    path="/{short_url}/",
    response_model=None,
    summary="Create short url",
    status_code=http.HTTPStatus.NO_CONTENT,
)
async def delete_short_url(
    *,
    short_url: str,
    short_url_service: ShortUrlService = Depends(get_short_url_service),
):
    """Delete short url."""
    await short_url_service.delete(short_url=short_url)
    return Response(content=None, status_code=http.HTTPStatus.NO_CONTENT)
