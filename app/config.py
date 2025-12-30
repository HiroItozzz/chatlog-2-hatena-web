import logging
from functools import lru_cache
from pathlib import Path
from typing import Annotated

import yaml
from fastapi import Depends
from pydantic_settings import BaseSettings

from cha2hatena import LlmConfig

logger = logging.getLogger(__name__)

DEBUG = True


class SettingsEnv(BaseSettings):
    """環境変数取得"""

    # 外部APIキー
    deepseek_api_key: str
    hatena_consumer_key: str
    hatena_consumer_secret: str
    hatena_access_token: str
    hatena_access_token_secret: str
    hatena_entry_url: str
    spreadsheet_id: str

    # セキュリティ設定
    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


class SettingsAi(BaseSettings):
    """AI設定"""

    prompt: str
    model: str = "deepseek-chat"
    temperature: float = 1.3
    max_len_content: int = 1500

    @classmethod
    @lru_cache()
    def from_yaml(cls, filepath: str = "config.yaml"):
        path = Path.cwd() / filepath
        if path.exists():
            config = yaml.safe_load(path.read_text(encoding="utf-8"))
            return cls(**config["ai"])
        logger.warning("YAMLファイルを読み込めませんでした。")
        return cls()


class SettingsAuth(BaseSettings):
    """セキュリティ設定"""

    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


@lru_cache()
def get_env_settings() -> SettingsEnv:
    return SettingsEnv()


# Dependsに投入するためのラッパー関数
@lru_cache()
def get_ai_settings() -> SettingsAi:
    return SettingsAi.from_yaml()


def get_llm_config(
    env_config: Annotated[SettingsEnv, Depends(get_env_settings)],
    yaml_config: Annotated[SettingsAi, Depends(get_ai_settings)],
) -> LlmConfig:
    config = LlmConfig(
        prompt=yaml_config.prompt,
        model=yaml_config.model,
        temperature=yaml_config.temperature,
        api_key=env_config.deepseek_api_key,
        conversation="",  # json_loaderの返り値をあとで代入
    )
    return config


def get_hatena_secrets(env_config: Annotated[SettingsEnv, Depends(get_env_settings)]):
    hatena_secret_keys = {
        "client_id": env_config.hatena_consumer_key,
        "client_secret": env_config.hatena_consumer_secret,
        "token": env_config.hatena_access_token,
        "token_secret": env_config.hatena_access_token_secret,
        "hatena_entry_url": env_config.hatena_entry_url,
    }
    return hatena_secret_keys


def get_auth_config(env_config: Annotated[SettingsEnv, Depends(get_env_settings)]) -> SettingsAuth:
    auth_config = SettingsAuth(
        jwt_secret_key=env_config.jwt_secret_key,
        algorithm=env_config.algorithm,
        access_token_expire_minutes=env_config.access_token_expire_minutes,
    )
    return auth_config
