import logging
import os

import yaml
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import DEBUG
from cha2hatena import DeepseekClient, LlmConfig, blog_post, json_loader
from cha2hatena.llm.llm_stats import TokenStats

logger = logging.getLogger(__name__)

router = APIRouter()

with open("config.yaml", encoding="utf-8") as f:
    config_dict = yaml.safe_load(f)


templates = Jinja2Templates(directory="app/templates")


async def _generate_summary(conversation: str) -> tuple[dict, TokenStats]:
    """共通のLLM要約処理"""
    config = LlmConfig(
        prompt=config_dict["ai"]["prompt"],
        model=config_dict["ai"]["model"],
        temperature=config_dict["ai"]["temperature"],
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        conversation=conversation,
    )
    return await DeepseekClient(config).get_summary()


async def _post_to_blog(llm_outputs: dict, preset_categories: list[str], is_draft: bool) -> dict:
    """はてなブログ投稿処理（内部関数）"""
    hatena_secret_keys = {
        "client_id": os.environ.get("HATENA_CONSUMER_KEY"),
        "client_secret": os.environ.get("HATENA_CONSUMER_SECRET"),
        "token": os.environ.get("HATENA_ACCESS_TOKEN"),
        "token_secret": os.environ.get("HATENA_ACCESS_TOKEN_SECRET"),
        "hatena_entry_url": os.getenv("HATENA_ENTRY_URL"),
    }
    return await blog_post(
        **llm_outputs, hatena_secret_keys=hatena_secret_keys, preset_categories=preset_categories, is_draft=is_draft
    )


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # templates/top.html を読み込んで返す
    return templates.TemplateResponse("top.html", {"request": request})


@router.post("/")
async def generate(files: list[UploadFile] = File(), preset_categories: list[str] = Form([])):
    single_log_text = await json_loader(files)
    llm_outputs, llm_stats = await _generate_summary(single_log_text)

    hatena_response = await _post_to_blog(llm_outputs, preset_categories=preset_categories, is_draft=DEBUG)
    return hatena_response
