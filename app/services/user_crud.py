"""
# まずこれだけ実装すれば動く！
get_user_by_email()     # ログイン時に必要
create_user()           # 登録時に必要
authenticate_user()     # 認証時に必要
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.models.users import User
from app.security import get_password_hash, verify_password
from app.services.user_schema import Token, UserCreate

logger = logging.getLogger(__name__)


def get_user(user_id: int, db: Session) -> Optional[User]:
    """IDでユーザー取得"""
    return db.query(User).filter(User.id == user_id).first()


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


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """メールでユーザー取得"""

    logger.debug("関数実行：get_user_by_email")
    logger.debug(f"  email: {email}")
    logger.debug(f"  db type: {type(db)}")
    logger.debug(f"  db repr: {repr(db)[:100]}")

    return db.query(User).filter(User.email == email).first()


def create_user(user_input: UserCreate, db: Session) -> User:
    """ユーザアカウント作成"""
    # パスワードをハッシュ化
    hashed = get_password_hash(user_input.password)
    new_user = User(email=user_input.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# emailでのログイン用
def authenticate_user_by_email(email: str, password: str, db: Session):
    """ログイン用（ユーザー認証）"""

    logger.debug("関数実行：authenticate_user_by_email")
    logger.debug(f"  email: {email}")
    logger.debug(f"  password length: {len(password)}")
    logger.debug(f"  db type: {type(db)}")

    user = get_user_by_email(email, db)

    if not user or not verify_password(password, user.hashed_password):
        return None

    logger.debug(f"Userが見つかりました: id={user.id}, email={user.email}")

    return user


# Googleからのログイン用
def authenticate_user_by_google(db: Session):
    pass
