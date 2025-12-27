__version__ = "0.1.0"

import logging

from cha2hatena.hatenablog_poster import blog_post
from cha2hatena.llm.conversational_ai import LlmConfig
from cha2hatena.llm.deepseek_client import DeepseekClient

logger = logging.getLogger("cha2hatena")
logger.setLevel(logging.WARNING)
logger.propagate = False
