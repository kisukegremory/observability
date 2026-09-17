import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.trace import StatusCode

logger = logging.getLogger(__name__)


def _format_id(value: int, width: int) -> str:
    return format(value, f"0{width}x")


def get_trace_context() -> dict[str, str]:
    span = trace.get_current_span()
    ctx = span.get_span_context()

    if not ctx.is_valid:
        return {}

    return {
        "trace_id": _format_id(ctx.trace_id, 32),
        "span_id": _format_id(ctx.span_id, 16),
    }


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    span = trace.get_current_span()
    span.record_exception(exc)
    span.set_status(StatusCode.ERROR, str(exc))

    trace_context = get_trace_context()

    logger.exception(
        "Unhandled exception on %s %s [trace_id=%s]",
        request.method,
        request.url.path,
        trace_context.get("trace_id", "none"),
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", **trace_context},
        headers={"X-Trace-Id": trace_context.get("trace_id", "")},
    )
