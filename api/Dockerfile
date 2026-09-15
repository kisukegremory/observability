FROM python:3.14-slim AS builder

# Copia apenas o binário do UV
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Camadas de dependência
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copia Aplicação
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev \
 && python -m compileall -q -x '/\.venv/' /app # main.py nunca é compilado, portanto deixar ele leve e modularizar o que for possível é o ideal

 # Runtime
FROM python:3.14-slim AS base

 # remove uso do 'uv run' + não reescreve bytecode
 ENV PATH="/app/.venv/bin:$PATH" \
     PYTHONUNBUFFERED=1 \
     PYTHONDONTWRITEBYTECODE=1

# nonroot user
RUN groupadd --system --gid 10001 app \
&& useradd --system --uid 10001 --gid app --no-create-home \
    --shell /usr/sbin/nologin app # Não tem acesso a shell e nem home

EXPOSE 8000

WORKDIR /app

# ---------- dev (código gravável pelo usuário app) ----------
FROM base AS dev
COPY --from=builder --chown=app:app /app /app
USER app
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# ---------- runtime (produção, código somente leitura) ----------
FROM base AS runtime
COPY --from=builder /app /app
USER app
CMD ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
