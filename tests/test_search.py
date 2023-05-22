import pytest
from httpx import AsyncClient
from embedbase_internet_search.main import app

unit_testing_dataset = "unit_test"

@pytest.mark.asyncio
async def test_search():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(
            f"/v1/{unit_testing_dataset}/search",
            json={
                "query": "test",
            }
        )
        assert response.status_code == 200
        json_response = response.json()
        print(json_response)