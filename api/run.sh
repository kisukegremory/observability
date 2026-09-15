export OTEL_SERVICE_NAME=obs-api
export OTEL_LOGS_EXPORTER=console # Habilita para stdout
export OTEL_TRACES_EXPORTER=none # Não recomendo uso para console, use oltp
export OTEL_METRICS_EXPORTER=none # Não recomendo uso para console, use oltp
uv run opentelemetry-instrument uvicorn main:app --host 0.0.0.0 --port 8000
