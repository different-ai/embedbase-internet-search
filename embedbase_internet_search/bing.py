import requests
import os


TIMEOUT = os.environ.get("EMBEDBASE_TIMEOUT", 10)

# to optimize the response for LLMs, check how LLM prefer it here https://github.com/facebookresearch/ParlAI


class BingSearchRequestHandler:
    bing_search_url = "https://api.bing.microsoft.com/v7.0/search"

    def __init__(self, bing_subscription_key, use_description_only=False):
        self.subscription_key = bing_subscription_key
        self.use_description_only = use_description_only

    def search(
        self,
        q: str,
        n: int,
    ) -> dict:
        types_to_search = ["News", "Entities", "Places", "Webpages"]
        promote = ["News"]

        print(f"n={n} responseFilter={types_to_search}")
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        params = {
            "q": q,
            "textDecorations": False,
            "textFormat": "HTML",
            "responseFilter": types_to_search,
            "promote": promote,
            "answerCount": 5,
        }
        response = requests.get(
            BingSearchRequestHandler.bing_search_url,
            headers=headers,
            params=params,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        search_results = response.json()

        return search_results
