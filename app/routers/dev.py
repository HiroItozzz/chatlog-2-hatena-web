from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import DEBUG
from app.core import user_crud, user_schema
from app.database import get_db
from app.models.users import User

if DEBUG:
    router = APIRouter(prefix="/dev", tags=["dev"])

    @router.get("/users/", response_model=list[user_schema.UserResponse])
    def read_users(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100):
        """
        ユーザー一覧を取得（ページネーション対応）

        Args:
            db: データベースセッション
            skip: スキップするレコード数（オフセット）
            limit: 取得する最大レコード数

        Returns:
            ユーザーオブジェクトのリスト
        """

        users = user_crud.get_users(db, skip=skip, limit=limit)
        return users

    @router.delete("/users/{user_id}")
    def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"message": f"ID: {user.id} 番のユーザーをDBから削除しました"}
        return {"message": "削除対象のユーザーが見つかりません"}
