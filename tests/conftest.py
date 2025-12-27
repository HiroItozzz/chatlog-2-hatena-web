# tests/conftest.py

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from cha2hatena.llm.llm_stats import TokenStats
from app import app  # FastAPIアプリをインポート


@pytest_asyncio.fixture
async def client():
    """非同期テストクライアント"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_gemini_get_summary(monkeypatch):
    """GeminiClientのget_summaryをモック化"""

    async def _mock_get_summary(self):
        return (
            {"title": "モックタイトル", "content": "これはモック要約です", "categories": ["テスト", "モック"]},
            TokenStats(
                input_tokens=100,
                thoughts_tokens=0,
                output_tokens=50,
                input_letter_count=500,
                output_letter_count=200,
                model="gemini-2.5-flash",
            ),
        )

    from cha2hatena.llm import deepseek_client

    monkeypatch.setattr(deepseek_client.DeepseekClient, "get_summary", _mock_get_summary)
    return _mock_get_summary
