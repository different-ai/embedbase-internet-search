import os
import pytest
from httpx import AsyncClient
from embedbase_internet_search import internet_search
from embedbase.database.memory_db import MemoryDatabase
from sentence_embedder import LocalEmbedder
from embedbase import get_app


embedbase_app = (
    get_app().use_db(MemoryDatabase(dimensions=384)).use_embedder(LocalEmbedder())
)

app = embedbase_app.run()
app.add_api_route("/internet-search", internet_search, methods=["POST"])


@pytest.mark.asyncio
async def test_internet_search():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(
            "/internet-search",
            json={"query": "What is Alpaca LLM?", "engine": "bing"},
        )
        assert response.status_code == 200
        json_response = response.json()
        # {'_type': 'SearchResponse', 'queryContext': {'originalQuery': 'African animals'}, 'webPages': {'webSearchUrl': 'https://www.bing.com/search?q=African+animals', 'totalEstimatedMatches': 635000, 'value': [...], 'someResultsRemoved': True}, 'rankingResponse': {'mainline': {...}}}
        assert json_response["queryContext"]["originalQuery"] == "What is Alpaca LLM?"
        assert json_response["webPages"]["totalEstimatedMatches"] > 10
