.PHONY: check-status

check-status:
	curl -i http://localhost:8000/health

install-avaiable-otel:
	uv run opentelemetry-bootstrap -a requirements > otel-requirements.txt
	uv add -r otel-requirements.txt
	rm otel-requirements.txt

default-run:
	uv run uvicorn main:app --reload

instrument-run:
	uv run opentelemetry-instrument --traces_exporter console --metrics_exporter console uvicorn main:app --reload
