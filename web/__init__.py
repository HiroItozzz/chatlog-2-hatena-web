import logging
from logging.handlers import RotatingFileHandler
import sys

from web.main import app

logger = logging.getLogger(__name__)

parent = logging.getLogger("web")
parent.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(level_name)s | %(name)s:%(funcname)s:%(lineno)s | %(massage)s"))
console_handler.setLevel(logging.WARNING)
parent.addHandler(console_handler)

file_hanlder = RotatingFileHandler(filename="app.log", maxBytes=1*1024*1024, backupCount=2, encoding="utf-8")
file_hanlder.setFormatter(logging.Formatter("%(asctime)s:%(level_name)s | %(name)s:%(funcname)s:%(lineno)s | %(massage)s "))
file_hanlder.setLevel(logging.DEBUG)
parent.addHandler(file_hanlder)