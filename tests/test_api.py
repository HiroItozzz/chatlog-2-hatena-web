import pytest


@pytest.mark.asyncio
async def test_summarize_endpoint(client, mock_gemini_get_summary):
    """FastAPIエンドポイントのテスト"""

    # files = {"files":("test.txt", open("sample/ChatGPT-sample.json", "rb"), "text/plain"), }
    files = {
        "files": [
            ("ChatGPT-sample.json", open("sample/ChatGPT-sample.json", "rb"), "text/plain"),
            ("Claude-sample.json", open("sample/Claude-sample.json", "rb"), "text/plain"),
        ]
    }
    # URLパスを指定
    response = await client.post("/", files=files)

    assert response.status_code == 200
    assert response.json()["title"] == "モックタイトル"
