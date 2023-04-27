import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src import settings
from src.middlewares import add_process_time_header


def create_app() -> FastAPI:
    current_app = FastAPI(
        title=settings.app.project_name,
        description=settings.app.description,
        version=settings.app.version,
        # Адрес документации в красивом интерфейсе
        docs_url="/api/openapi",
        redoc_url="/api/redoc",
        # Адрес документации в формате OpenAPI
        openapi_url=f"{settings.app.api_doc_prefix}/openapi.json",
        debug=settings.app.debug,
        default_response_class=ORJSONResponse,
    )
    # Middlewares
    current_app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)

    # Подключаем роутеры к серверу
    return current_app


app = create_app()


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
    )
