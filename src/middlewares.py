import http
import time
from ipaddress import ip_address, ip_network

from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

__all__ = (
    "add_process_time_header",
    "IPBlockMiddleware",
)


async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} sec")
    return response


class IPBlockMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, blacklist: list[str]):
        super().__init__(app)
        self.blacklist = [ip_network(subnet) for subnet in blacklist]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        client_ip = ip_address(request.client.host)

        for subnet in self.blacklist:
            if client_ip in subnet:
                return ORJSONResponse(
                    content={"detail": "Access denied"},
                    status_code=http.HTTPStatus.FORBIDDEN,
                )

        return await call_next(request)
