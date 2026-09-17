export OTEL_SERVICE_NAME=obs-single-file
export OTEL_LOGS_EXPORTER=otlp
export OTEL_PYTHON_LOG_FORMAT="%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s"
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=debug
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=none
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317


uv run opentelemetry-instrument python main_traced.py
