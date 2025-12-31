import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import SettingsAuth, get_auth_config
from app.core import security, user_crud, user_schema
from app.core.security import Token, authenticate_user_by_email, create_access_token, create_user
from app.database import get_db
from app.models import users

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="ユーザー新規登録",
    description="""
    新規ユーザーを登録します。
    
    - メールアドレスは必須で一意
    - パスワードは8文字以上100文字以下
    """,
)
def register(user_input: user_schema.UserCreate, db: Annotated[Session, Depends(get_db)]) -> user_schema.UserResponse:
    if user_crud.get_user_by_email(user_input.email, db):
        raise HTTPException(400, "このメールアドレスはすでに登録されています")

    user = create_user(user_input, db)
    return user


@router.post(
    "/token",
    summary="OAuth2準拠ログイン",
    description="""
    OAuth2準拠ログイン

    - username: メールアドレスを入力
    - password: パスワードを入力
    """,
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_config: Annotated[SettingsAuth, Depends(get_auth_config)],
    db: Annotated[Session, Depends(get_db)],
) -> Token:  # 第一引数がクラスの場合Dependsの引数を省略可能
    print("username(email):", form_data.username)
    print("password:", form_data.password)
    print("grant_type:", form_data.grant_type)

    user = authenticate_user_by_email(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.debug("ユーザーの存在確認完了")

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account disabled",
        )
    access_token_expires = timedelta(minutes=auth_config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, auth_config=auth_config, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/items/", response_model=user_schema.UserResponse)
async def read_own_items(
    current_user: Annotated[users.User, Depends(security.get_current_active_user)],
):
    return current_user
