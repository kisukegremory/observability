export OTEL_SERVICE_NAME=obs-single-file
export OTEL_LOGS_EXPORTER=console
export OTEL_PYTHON_LOG_LEVEL=debug
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317


uv run opentelemetry-instrument python main_base.py
