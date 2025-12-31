import logging

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import DEBUG, get_hatena_secrets, get_llm_config
from cha2hatena import DeepseekClient, LlmConfig, blog_post, json_loader

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # templates/top.html を読み込んで返す
    return templates.TemplateResponse("top.html", {"request": request})


@router.post("/")
async def generate(
    files: list[UploadFile] = File(),
    preset_categories: list[str] = Form([]),
    llm_config: LlmConfig = Depends(get_llm_config),
    hatena_secret_keys: dict = Depends(get_hatena_secrets),
):
    
    llm_config.conversation = await json_loader(files)
    llm_outputs, _ = await DeepseekClient(llm_config).get_summary()
    hatena_response: dict = await blog_post(
        **llm_outputs, hatena_secret_keys=hatena_secret_keys, preset_categories=preset_categories, is_draft=DEBUG
    )

    return hatena_response
