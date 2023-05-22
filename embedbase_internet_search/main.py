import os
from embedbase import get_app
import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
from embedbase.database.memory_db import MemoryDatabase
import logging
from embedbase_internet_search.sentence_embedder import LocalEmbedder
from embedbase_internet_search.bing import BingSearchRequestHandler
from starlette.concurrency import iterate_in_threadpool
import json

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

    query = body.get("query")

    if not query:
        await set_body(request, await request.body())
        return await call_next(request)

    results = list(s.search(query, 5))
    await set_body(request, await request.body())

    # todo ask llm to extract context from these results
    logger.debug("Got results from bing: %s", results)

    response = await call_next(request)
    response_body = [section async for section in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    response_body = json.loads(response_body[0].decode())
    response_body["similarities"] += results
    return JSONResponse(
        status_code=200,
        content={**response_body},
    )


app = (
    get_app()
    .use_db(MemoryDatabase(dimensions=384))
    .use_embedder(LocalEmbedder())
    .use_middleware(search)
)

app = app.run()

if __name__ == "__main__":
    uvicorn.run(app)
