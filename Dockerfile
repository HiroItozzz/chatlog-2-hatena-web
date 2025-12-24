FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# ソースコードのコピー
COPY . .

COPY pyproject.toml uv.lock* ./
RUN uv sync --dev --frozen

# アプリの自動起動
CMD ["uv", "run", "uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8080"]