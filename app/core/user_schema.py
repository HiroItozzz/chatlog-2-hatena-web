from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from app.core.user_crud import get_user_by_id


class UserBase(BaseModel):
    """
    ユーザアカウントスキーマの共通部分
    """

    email: str = Field(min_length=2, max_length=255)


class UserCreate(UserBase):
    """
    ユーザアカウント作成時のリクエスト用
    email: str
    password: str
    """

    password: str = Field(min_length=8, max_length=100)


class UserAuth(UserBase):
    id: int
    disabled: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_db_user(cls, user):
        """
        authenticate_user_by_emailでのユーザー情報取得用ユーティリティメソッド
        """
        return cls(id=user.id, email=user.email, disabled=user.disabled)


class UserResponse(UserBase):
    """レスポンス用スキーマ"""

    id: int
    username: Optional[str] = None
    created_at: datetime
    disabled: bool

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


def get_user_for_response(id: int, db: Session) -> Optional[UserResponse]:
    user = get_user_by_id(id, db)
    if user is None:
        return None
    user_for_response = UserResponse.model_validate(user)
    return user_for_response
