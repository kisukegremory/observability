# API
Para APIs teremos armadilhas na instrumentação automática, principalmente em servidores de aplicação como uvicorn e health checks.

Começamos com a aplicação da instalação da distro:

```sh
uv add fastapi uvicorn # Aplicação
uv add opentelemetry-distro opentelemetry-exporter-otlp
```

Agora a leitura dos frameworks ativos e a adição deles nas dependências

```sh
uv run opentelemetry-bootstrap -a requirements > otel-requirements.txt
uv add -r otel-requirements.txt && rm otel-requirements.txt
```

Agora a instrumentação será feita em tempo de execução, sendo controlada via variáveis de ambiente:
```sh
export OTEL_SERVICE_NAME=obs-api
export OTEL_LOGS_EXPORTER=console # Habilita para stdout
export OTEL_TRACES_EXPORTER=none # Não recomendo uso para console, use otlp
export OTEL_METRICS_EXPORTER=none # Não recomendo uso para console, use otlp
uv run opentelemetry-instrument uvicorn main:app --host 0.0.0.0 --port 8000
```

> Nesse repositório temos o run.sh, só rodar ./run.sh, se não funcionar por falta de permissão (chmod +x run.sh)

Quero utilizar via docker, ao invés de instalar coisas na minha máquina, nesse caso temos um Dockerfile com multistage building mais otimizado para produção

```sh
docker build -t obs-api:latest .
docker run --rm \
  -p 8000:8000 \
  -e OTEL_SERVICE_NAME=obs-api \
  -e OTEL_LOGS_EXPORTER=console \
  -e OTEL_TRACES_EXPORTER=none \
  -e OTEL_METRICS_EXPORTER=none \
  obs-api:latest
```
