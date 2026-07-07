import logging
from collections.abc import Awaitable, Callable
from time import perf_counter

from fastapi import FastAPI, Request, Response

from app.core.config import settings
from app.observability.metrics import metrics_collector

logger = logging.getLogger("app.observability.requests")


def register_observability_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start_time = perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception:
            logger.exception(
                "method=%s path=%s status_code=%s duration_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                (perf_counter() - start_time) * 1000,
            )
            raise
        finally:
            duration_ms = (perf_counter() - start_time) * 1000
            if settings.enable_metrics:
                metrics_collector.record_request(
                    request.method,
                    status_code,
                    duration_ms,
                )
            logger.info(
                "method=%s path=%s status_code=%s duration_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
            )
