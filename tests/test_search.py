import pytest
from httpx import AsyncClient
from embedbase_internet_search.main import app

unit_testing_dataset = "unit_test"

@pytest.mark.asyncio
async def test_search():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(
            f"/v1/{unit_testing_dataset}",
            json={
                "documents": [
                    {
                        "data": "The lion is the king of the jungle.",
                    },
                    {
                        "data": "The giraffe is the tallest animal in the world.",
                    },
                    {
                        "data": "The hippo is the heaviest animal in the world.",
                    },
                ]
            }
        )
        assert response.status_code == 200
        json_response = response.json()
        print(json_response)
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(
            f"/v1/{unit_testing_dataset}/search",
            json={
                "query": "African animals",
            }
        )
        assert response.status_code == 200
        json_response = response.json()
        assert len(json_response["similarities"]) >= 8
        print(json_response)