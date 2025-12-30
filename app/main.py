import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import DEBUG

logger = logging.getLogger(__name__)

app = FastAPI(debug=DEBUG, docs_url="/docs" if DEBUG else None, redoc_url="/redocs" if DEBUG else None)

# app/__init__.py があるディレクトリの絶対パスを取得
current_dir = Path(__file__).parent
static_dir = current_dir / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def force_https_redirect(request: Request, call_next):
    # ローカルホストは除外（開発用）
    if "localhost" in str(request.url) or "127.0.0.1" in str(request.url):
        return await call_next(request)

    # HTTPならHTTPSにリダイレクト
    if request.url.scheme == "http":
        https_url = str(request.url).replace("http://", "https://", 1)
        return RedirectResponse(https_url, status_code=301)

    return await call_next(request)


from app.routers import auth, users, views

app.include_router(views.router)
app.include_router(auth.router)
app.include_router(users.router)
if DEBUG:
    from app.routers import dev

    app.include_router(dev.router)
