FROM python:3.13-slim

# uvのダウンロード+インストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /workspace

COPY pyproject.toml uv.lock* ./
RUN uv sync --dev --frozen

# ソースコードのコピー
COPY . .

# アプリの自動起動
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
