import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.user_crud import authenticate_user_by_email, create_user, get_user_by_email
from app.services.user_schema import Token, UserCreate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register")
def register(user_input: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(user_input.email, db):
        raise HTTPException(400, "このメールアドレスはすでに登録されています")

    user = create_user(user_input, db)
    return {"message": "アカウントを作成しました", "user_id": user.id}


@router.post("/login")
def login_by_email(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):  # 第一引数がクラスの場合Dependsの引数を省略可能
    user = authenticate_user_by_email(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(401, "メールアドレスかパスワードが間違っています")
    return {"message": "ログイン成功", "user_id": user.id}
