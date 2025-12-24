import os

import yaml
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import httpx
from authlib.integrations.httpx_client import AsyncOAuth1Client

from cha2hatena import DeepseekClient, LlmConfig, blog_post

views = APIRouter()

with open("config.yaml", encoding="utf-8") as f:
    config_dict = yaml.safe_load(f)


templates = Jinja2Templates(directory="web/templates")

# @views.get("/")
# async def root():
#     return {"message": "Hello World"}

@views.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # templates/top.html を読み込んで返す
    return templates.TemplateResponse("top.html", {"request": request})

@views.post("/upload")
async def post(file: UploadFile = File(), preset_categories: list[str] = Form([])):
    conversation = (await file.read()).decode("utf-8")
    config = LlmConfig(
        prompt=config_dict["ai"]["prompt"],
        model=config_dict["ai"]["model"],
        temperature=config_dict["ai"]["temperature"],
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        conversation=conversation,
    )

    llm_outputs, llm_stats = await DeepseekClient(config).get_summary()

    import json
    preset_cats = preset_categories
    
    hatena_secret_keys = {
    "client_id": os.environ.get("HATENA_CONSUMER_KEY"),
    "client_secret": os.environ.get("HATENA_CONSUMER_SECRET"),
    "token": os.environ.get("HATENA_ACCESS_TOKEN"),
    "token_secret": os.environ.get("HATENA_ACCESS_TOKEN_SECRET"),
    "hatena_entry_url": os.getenv("HATENA_ENTRY_URL")}

    hatena_response = await blog_post(
        **llm_outputs, hatena_secret_keys=hatena_secret_keys, preset_categories=preset_cats, is_draft=False
    )
    return hatena_response
    # url = hatena_response.get("link_alternate","")
    # url_edit = hatena_response.get("link_edit_user","")
    # return { "記事URL":url, "編集用URL":url_edit}
