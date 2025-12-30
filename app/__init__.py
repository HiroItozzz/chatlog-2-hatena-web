import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import DEBUG
from app.main import app

logger = logging.getLogger(__name__)

if DEBUG:
    parent = logging.getLogger("app")
    parent.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s:%(funcName)s:%(lineno)s | %(message)s"))
    console_handler.setLevel(logging.DEBUG)
    parent.addHandler(console_handler)

    file_hanlder = RotatingFileHandler(
        filename="/workspace/app/app.log", maxBytes=1 * 1024 * 1024, backupCount=2, encoding="utf-8"
    )
    file_hanlder.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s | %(name)s:%(funcName)s:%(lineno)s | %(message)s")
    )
    file_hanlder.setLevel(logging.DEBUG)
    parent.addHandler(file_hanlder)
    logger.info("loggerの設定終了")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)  # 必要に応じて

    print(f"✅ Logger setup complete for '{parent.name}' and children")
