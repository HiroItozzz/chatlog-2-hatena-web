from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# web/__init__.py があるディレクトリの絶対パスを取得
current_dir = Path(__file__).parent
static_dir = current_dir / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory="templates")


from web.router import views

app.include_router(views)
