import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.users import Base
from app.config import DEBUG

DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy側だけの設定（DBにはまだ働きかけない）
engine = create_engine(DATABASE_URL, echo=DEBUG)

# `with SessionLocal()`でセッションを開始できるCallableなインスタンスの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

# Depends用のラッパー：Dependsで参照することで自動で閉じてくれる
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 既存テーブルがなければテーブルを作成、あれば何もしない
# 開発のとき専用。本番はAlembic（マイグレーションツール(バージョン管理ツール)）
Base.metadata.create_all(bind=engine)
