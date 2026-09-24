# Single file

Este é o formato mais simples de aplicação: um script sem framework como uma API por trás. Como quase não há instrumentação automática aqui, dependemos mais da instrumentação manual. Os logs usam o `logging.getLogger(__name__)` normal do Python, e o OpenTelemetry faz a ponte deles junto com os traces.

## Instalação

Primeiro instalamos a distro do OpenTelemetry e o exporter OTLP:

```sh
uv add opentelemetry-distro opentelemetry-exporter-otlp
```

Depois o bootstrap identifica as bibliotecas usadas no projeto e adiciona as instrumentações correspondentes:

```sh
uv run opentelemetry-bootstrap -a requirements > otel-requirements.txt
uv add -r otel-requirements.txt && rm otel-requirements.txt
```

A instrumentação acontece em tempo de execução e é controlada por variáveis de ambiente:

```sh
export OTEL_SERVICE_NAME=obs-single-file
export OTEL_LOGS_EXPORTER=console # mostra os logs no stdout
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
uv run opentelemetry-instrument python main_base.py
```

> Cada exemplo tem um `.sh` pronto. Se der erro de permissão, rode `chmod +x *.sh`.

## Passo a passo

### 1. Log simples, sem OpenTelemetry

Abra o `main_base.py`. É um processo de extract, transform e load com logging comum e um handler próprio. Ele serve de base para comparar com o que vem depois.

```sh
uv run python main_base.py
```

### 2. Log instrumentado

Agora rode o mesmo arquivo pelo `opentelemetry-instrument`:

```sh
./run_base.sh
```

Repare que o formato no console muda e cada log vira um objeto que dá para parsear como JSON, com recurso, severidade e outros campos.

### 3. Spans em cada etapa

Abra o `main_traced.py`. Agora cada função tem seu próprio span (`process`, `extract`, `transform` e `load`), usando o decorator `@tracer.start_as_current_span`.

### 4. Traces aparecendo nos logs

Aqui existem duas formas de ver o `trace_id` e o `span_id` preenchidos:

```sh
./run_traced_console.sh  # exporter console, log em formato JSON
./run_traced_format.sh   # log em texto, com o formato que definimos
```

| Variável | console | format |
| --- | --- | --- |
| `OTEL_LOGS_EXPORTER` | `console` | `none` |
| `OTEL_PYTHON_LOG_FORMAT` | comentada | formato com `otelTraceID` e `otelSpanID` |
| `OTEL_PYTHON_LOG_CORRELATION` | `true` | `true` |
| `OTEL_PYTHON_LOG_LEVEL` | `debug` | `debug` |

Isso já ajuda bastante no debug remoto, mas existem formas melhores de visualizar. Para isso vamos subir alguns serviços.

### 5. Enviando via OTLP

Em outra aba do terminal, suba o otel-lgtm:

```sh
cd ../shared
docker compose up
```

Abra o Grafana em http://localhost:3000 e vá em **Explore**.

Agora os sinais passam a ser enviados para os serviços, e não mais só para o console. Rode algumas vezes:

```sh
./run_traced_otlp.sh
```

No Grafana:

- **Loki**: veja os logs do serviço `obs-single-file`. Pelo painel do lado esquerdo dá para adicionar campos como `trace_id` e `span_id` na visualização.
- **Tempo**: use o **Search** para ver as execuções e abra uma ou duas para ver os spans. Filtre por status `error` para achar as execuções em que o `transform` falhou.

## Docker

Se preferir não instalar nada na máquina, existe um Dockerfile multistage pensado para produção:

```sh
docker build -t obs-single-file:latest .
docker run --rm \
  -e OTEL_SERVICE_NAME=obs-single-file \
  -e OTEL_LOGS_EXPORTER=console \
  -e OTEL_TRACES_EXPORTER=none \
  -e OTEL_METRICS_EXPORTER=none \
  obs-single-file:latest
```
