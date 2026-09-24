# API

Em APIs a instrumentação automática faz a maior parte do trabalho, mas tem algumas armadilhas, principalmente com servidores de aplicação como o uvicorn e com health checks.

## Instalação

Instalamos a aplicação e a distro do OpenTelemetry:

```sh
uv add fastapi uvicorn
uv add opentelemetry-distro opentelemetry-exporter-otlp
```

Depois o bootstrap identifica os frameworks usados e adiciona as instrumentações correspondentes:

```sh
uv run opentelemetry-bootstrap -a requirements > otel-requirements.txt
uv add -r otel-requirements.txt && rm otel-requirements.txt
```

A instrumentação acontece em tempo de execução e é controlada por variáveis de ambiente:

```sh
export OTEL_SERVICE_NAME=obs-api
export OTEL_LOGS_EXPORTER=console # mostra os logs no stdout
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
uv run opentelemetry-instrument uvicorn main:app --host 0.0.0.0 --port 8000
```

> Cada exemplo tem um `.sh` pronto. Se der erro de permissão, rode `chmod +x *.sh`.

## A aplicação

O `main.py` tem alguns endpoints simples, cada um mostrando algo diferente:

| Endpoint | O que mostra |
| --- | --- |
| `/health` | health check, que costuma poluir traces e métricas |
| `/items/{item_id}` | rota dinâmica |
| `/topics` | rota estática |
| `/sales` | span e métrica manuais (`sales_created_total`) |
| `/unexpected` | erro aleatório, tratado em `src/errors.py` |

O `load.py` fica chamando esses endpoints a cada segundo, incluindo uma rota que não existe, para gerar tráfego.

## Passo a passo

### 1. Rodando localmente

Em um terminal suba a API e em outro rode o gerador de carga:

```sh
./run_local.sh
uv run python load.py
```

Os logs aparecem no console com `trace_id` e `span_id`.

### 2. Enviando para o otel-lgtm

Com o otel-lgtm rodando (`cd ../shared && docker compose up`), pare o `run_local.sh`, suba a versão que envia via OTLP e rode o `load.py` de novo:

```sh
./run.sh
uv run python load.py
```

O `run.sh` já tem `OTEL_PYTHON_EXCLUDED_URLS=health`. Com ela, tudo que é relacionado ao `/health` deixa de gerar traces e métricas, o que evita encher o Tempo com chamadas que não interessam. O `--no-access-log` desliga o log de acesso do uvicorn, que já fica coberto pelos traces.

### 3. Explorando os traces

No Grafana, em **Explore > Tempo**:

- Filtre o `/sales` pelos atributos do span manual, por exemplo `span.payment_type = "credit"`.
- Veja os erros do `/unexpected`. A resposta de erro devolve o `trace_id`, e isso é muito útil: quem recebeu o erro consegue passar esse id e você cai direto no trace certo.

## Métricas

No Grafana, em **Explore > Prometheus**, usando o **builder**:

1. Comece com `sum by (http_target)`. Repare que o nome dos atributos no Prometheus é diferente do que aparece no Tempo.
2. Use `http_server_duration_milliseconds_count` com `increase` e range de `5m`, some por `http_target`, aplique `round` e coloque o min step em `1m`. O resultado é a quantidade de requisições acumuladas nos últimos minutos (range), calculada a cada minuto (step).
3. Separe também por `http_status_code` e filtre só o `/unexpected`.

```promql
round(sum by (http_target, http_status_code) (increase(http_server_duration_milliseconds_count{http_target="/unexpected"}[5m])))
```

4. Para a métrica manual, use `sales_created_total` agrupando por `type`:

```promql
sum by (type) (sales_created_total)
```

## Docker

Existe um Dockerfile multistage pensado para produção:

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

Também tem um `docker-compose.yml` que sobe a API junto com o otel-lgtm e usa o `watch` para recarregar o código sem gerar uma imagem nova:

```sh
docker compose up --watch
```
