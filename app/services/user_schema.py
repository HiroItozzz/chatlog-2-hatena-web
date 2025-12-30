from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Token(BaseModel):
    """"""

    access_token: str
    token_type: str


class UserBase(BaseModel):
    """
    ユーザアカウントスキーマの共通部分 /
    TokenData取得用
    """

    email: str


class UserCreate(UserBase):
    """ユーザアカウント作成時のリクエスト用"""

    password: str = Field(min_length=8, max_length=100)


class UserResponse(UserBase):
    """レスポンス用スキーマ"""

    id: int
    username: Optional[str] = None
    created_at: datetime

    @field_validator("username")
    @classmethod
    def validate_username(cls, v, values):
        if v is None:
            email = values.data.get("email")
            if email:
                stem = email.split("@")[0]
                return stem[:50]
        return "user"


class UserViewAdmin(UserBase):
    """管理者閲覧用"""

    id: int
    hashed_password: Optional[str] = None
    email_verified: bool = False
    google_id: Optional[str] = None
    disabled: bool = False
    avatar_url: Optional[str] = None
    auth_method: str

    created_at: datetime
    updated_at: datetime
