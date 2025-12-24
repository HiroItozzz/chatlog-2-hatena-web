import pytest


@pytest.mark.asyncio
async def test_summarize_endpoint(client, mock_gemini_get_summary):
    """FastAPIエンドポイントのテスト"""

    files = {"file": ("test.txt", open("sample/sample.txt", "rb"), "text/plain")}
    # URLパスを指定
    response = await client.post("/", files=files)

    assert response.status_code == 200
    assert response.json()["title"] == "モックタイトル"
