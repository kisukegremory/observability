export OTEL_SERVICE_NAME=obs-api
export OTEL_LOGS_EXPORTER=none
export OTEL_PYTHON_LOG_FORMAT="%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s"
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=debug
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# uv run uvicorn main:app --host 0.0.0.0 --port 8000
uv run opentelemetry-instrument uvicorn main:app --host 0.0.0.0 --port 8000
