"""
https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#use-the-form-data
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#install-pwdlib
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.config import DEBUG, SettingsAuth, get_auth_config
from app.core import user_crud, user_schema
from app.database import get_db
from app.models.users import User

logger = logging.getLogger(__name__)

# --- security primitives ---
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_user(user_input: user_schema.UserCreate, db: Session) -> User:
    """ユーザアカウント作成"""
    # パスワードをハッシュ化
    hashed = get_password_hash(user_input.password)
    new_user = User(email=user_input.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# emailでのログイン用
def authenticate_user_by_email(email: str, password: str, db: Session) -> Optional[user_schema.UserAuth]:
    """ログイン用（ユーザー認証）"""

    user = user_crud.get_user_by_email(email, db)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user_schema.UserAuth.from_db_user(user)


def create_access_token(
    data: dict,
    auth_config: SettingsAuth,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_config.jwt_secret_key, algorithm=auth_config.algorithm)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    auth_config: Annotated[SettingsAuth, Depends(get_auth_config)],
) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_config.jwt_secret_key, algorithms=[auth_config.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        try:
            user_id = int(user_id)
        except ValueError:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = user_crud.get_user_by_id(id=user_id, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Googleからのログイン用
def authenticate_user_by_google(db: Session):
    pass
