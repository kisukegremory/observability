import logging
import os


def is_opentelemetry_active() -> bool:
    # O CLI opentelemetry-instrument injeta opentelemetry/instrumentation/auto_instrumentation
    # no PYTHONPATH ou PYTHONSTARTUP para fazer o bootstrapping
    pythonpath = os.environ.get("PYTHONPATH", "")
    pythonstartup = os.environ.get("PYTHONSTARTUP", "")

    return "opentelemetry" in pythonpath or "opentelemetry" in pythonstartup


def clean_uvicorn_logging():
    # Repassa os handlers para os loggers internos do Uvicorn
    for uvicorn_logger_name in ("uvicorn", "uvicorn.error"):
        uv_logger = logging.getLogger(uvicorn_logger_name)
        uv_logger.handlers.clear()
        uv_logger.propagate = False
    for uvicorn_logger_name in "uvicorn.access":
        uv_logger = logging.getLogger(uvicorn_logger_name)
        uv_logger.handlers = []
        uv_logger.propagate = False
