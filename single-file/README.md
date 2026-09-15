# Single Files
Embora coloquei com single files, quis deixar como o formato mais simples de aplicação, que não tenha um framework como uma API plugado a eles, como um recurso de formato mais "puro". Como não haverá severas auto instrumentações, dependerá fortemente de instrumnetação manual, sendo logs como um bridge para o `logger(__name__)` e ativo para métricas e traces.

Começamos com a aplicação da instalação da distro:

```sh
uv add opentelemetry-distro opentelemetry-exporter-otlp
```

Agora a leitura dos frameworks ativos e a adição deles nas dependências

```sh
uv run opentelemetry-bootstrap -a requirements > otel-requirements.txt
uv add -r otel-requirements.txt && rm otel-requirements.txt
```

Agora a instrumentação será feita em tempo de execução, sendo controlada via variáveis de ambiente:
```sh
export OTEL_SERVICE_NAME=obs-single-file
export OTEL_LOGS_EXPORTER=console # Habilita para stdout
export OTEL_TRACES_EXPORTER=none # Não recomendo uso para console, use oltp
export OTEL_METRICS_EXPORTER=none # Não recomendo uso para console, use oltp
uv run opentelemetry-instrument python test.py
```

> Nesse repositório temos o run.sh, só rodar ./run.sh, se não funcionar por falta de permissão (chmod +x run.sh)

Quero utilizar via docker, ao invés de instalar coisas na minha máquina, nesse caso temos um Dockerfile com multistage building mais otimizado para produção

```sh
docker build -t obs-single-file:latest .
docker run --rm \
  -e OTEL_SERVICE_NAME=obs-single-file \
  -e OTEL_LOGS_EXPORTER=console \
  -e OTEL_TRACES_EXPORTER=none \
  -e OTEL_METRICS_EXPORTER=none \
  obs-single-file:latest
```
