"""
まずこれだけ実装すれば動く！
get_user_by_email()     # ログイン時に必要
create_user()           # 登録時に必要
authenticate_user()     # 認証時に必要
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.models.users import User

logger = logging.getLogger(__name__)


def get_user_by_id(id: int, db: Session) -> Optional[User]:
    """IDでユーザー取得"""
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """メールでユーザー取得"""

    return db.query(User).filter(User.email == email).first()


# 開発用関数
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """
    ユーザー一覧を取得（ページネーション対応）

    Args:
        db: データベースセッション
        skip: スキップするレコード数（オフセット）
        limit: 取得する最大レコード数

    Returns:
        ユーザーオブジェクトのリスト
    """
    return db.query(User).order_by(User.id).offset(skip).limit(limit).all()
