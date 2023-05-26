
# embedbase-internet-search

<div align="center">

embedbase-internet-search - internet search extension for [Embedbase](https://github.com/different-ai/embedbase)
<br>
<br>
⚠️ Status: Alpha release ⚠️
<br>
<br>
<a href="https://discord.gg/pMNeuGrDky"><img alt="Discord" src="https://img.shields.io/discord/1066022656845025310?color=black&style=for-the-badge"></a>
<a href="https://badge.fury.io/py/embedbase-internet-search"><img alt="PyPI" src="https://img.shields.io/pypi/v/embedbase-internet-search?color=black&style=for-the-badge"></a>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/different-ai/embedbase)](https://github.com/different-ai/embedbase-internet-search/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

</div>

The point of internet search in embedbase is to combine your private information with latest public information.

Also remember that AIs like ChatGPT have limited knowledge to a certain date, for example try to ask ChatGPT about GPT4 or about Sam Altman talk with the senate (which happened few days ago), it will not know about it.


https://github.com/different-ai/embedbase-internet-search/assets/25003283/3131450f-93e2-46b1-8dcb-30673e5abe70


Please check [examples](./examples/answer-question/README.md) for usage or keep reading.

## Quick tour

Here's an example to answer general purpose questions.

The recommended workflow is like this:
1. search your question using internet endpoint
2. (optional) add results to embedbase
3. (optional) search embedbase with the question
4. use `.generate()` to get your question answered

```ts
import { createClient } from 'embedbase-js'

const formatInternetResultsInPrompt = (internetResult: any) =>
    `Name: ${internetResult.name}
Snippet: ${internetResult.snippet}
Url: ${internetResult.url}`


const system = `You are an AI assistant that can answer questions.
When a user send a question, we will answer its question following these steps:
1. we will search the internet with the user's question.
2. we will ask you to answer the question based on the internet results.`

const fn = async () => {
    const embedbase = createClient('https://api.embedbase.xyz', process.env.EMBEDBASE_API_KEY)

    // get question from process.argv
    const question = process.argv[2]

    const internetSearchResponse = await fetch('https://api.embedbase.xyz/v1/internet-search', {
        method: 'POST',
        body: JSON.stringify({
            query: question,
            engine: 'bing'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const internetSearchJson = await internetSearchResponse.json()
    const results = internetSearchJson.webPages.value
    const answerQuestionPrompt = `Based on the following internet search results:
${results.map(formatInternetResultsInPrompt).join('\n')}
\n
Please answer the question: ${question}`

    for await (const result of embedbase.generate(answerQuestionPrompt, {
        history: [{
            role: 'system',
            content: system
        }],
    })) {
        console.log(result)
    }
}

fn()
```

```bash
EMBEDBASE_API_KEY="<get me here https://app.embedbase.xyz>" npx tsx answer.ts "What did Sam Altman say to to US Senate lately?"
```

## Self-hosted usage

Just add two lines to your original embedbase entrypoint:

```py
import os
import uvicorn
from embedbase import get_app
from embedbase.database.memory_db import MemoryDatabase
from embedbase.embedding.openai import OpenAI
# import this
from embedbase_internet_search import internet_search

app = get_app().use_db(MemoryDatabase()).use_embedder(OpenAI(os.environ["OPENAI_API_KEY"])).run()
# add the new endpoint
app.add_api_route("/internet-search", internet_search, methods=["POST"])

if __name__ == "__main__":
    uvicorn.run(app)
```

If you have any feedback or issues, please let us know by opening an issue or contacting us on [discord](https://discord.gg/pMNeuGrDky).

Regarding the SDK, please refer to the [documentation](https://docs.embedbase.xyz/sdk).
