import os
from embedbase import get_app
import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
from embedbase.database.memory_db import MemoryDatabase
import logging
from sentence_embedder import LocalEmbedder
from bing import BingSearchRequestHandler
from starlette.middleware.base import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
s = BingSearchRequestHandler(os.environ["BING_SUBSCRIPTION_KEY"])


logger = logging.getLogger(__name__)


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.json()
    await set_body(request, body)
    return body


async def search(request: Request, call_next, _, __):
    await set_body(request, await request.body())

    body = await get_body(request)

    # search the query
    results = list(s.search(body["query"], 5))

    print(f"Got {len(results)} results from bing")

    response = await call_next(request)
    # response.headers["X-bing"] = ",".join(results)
    print("Setting response")
    # todo
    # return JSONResponse(
    #     status_code=200,
    #     content={
    #         **response.body
    #         "results": results},
    # )
    return response


app = (
    get_app()
    .use_db(MemoryDatabase(dimensions=384))
    .use_embedder(LocalEmbedder())
    .use_middleware(search)
)

app = app.run()

if __name__ == "__main__":
    uvicorn.run(app)
