export OTEL_SERVICE_NAME=nina-service-worker
export OTEL_LOGS_EXPORTER=console
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none

uv run opentelemetry-instrument python main.py
