FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

# ソースコードのコピー
COPY . .

# アプリの自動起動
CMD ["uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]