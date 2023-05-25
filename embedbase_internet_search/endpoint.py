import os
from pydantic import BaseModel, validator
from fastapi import Request
from fastapi.responses import JSONResponse
import logging
from embedbase_internet_search.bing import BingSearchRequestHandler


s = BingSearchRequestHandler(os.environ["BING_SUBSCRIPTION_KEY"])

logger = logging.getLogger(__name__)


class InternetSearchRequest(BaseModel):
    query: str
    top_k: int = 6
    engine: str = "bing"  # TODO google etc

    @validator("query")
    def query_must_not_be_empty(cls, v):
        assert v, "Query must not be empty"
        return v

    @validator("engine")
    def engine_is_in_supported_ones(cls, v):
        assert v in ["bing"], f"Engine {v} is not supported"
        return v


async def internet_search(
    _: Request,
    request_body: InternetSearchRequest,
):
    query = request_body.query

    if not query:
        return JSONResponse(
            status_code=400,
            # pylint: disable=protected-access TODO: expose public?
            content={"error": "No query provided"},
        )
    results = s.search(query, 5)

    logger.debug("Got results from internet: %s", results)

    return JSONResponse(
        status_code=200,
        content=results,
    )
