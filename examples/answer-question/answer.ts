import { createClient } from 'embedbase-js'

// Usage:
// EMBEDBASE_API_KEY="<get me here https://app.embedbase.xyz>" npx tsx answer.ts "What is GPT4?"

// Name: name
// Snippet: snippet
// Url: url
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

    console.log(`Answering question: ${question}`)
    console.log('I will search internet first')


    const internetSearchResponse = await fetch('http://localhost:8000/internet-search', {
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
    console.log('Internet search response:')
    console.log(internetSearchJson)

    const results = internetSearchJson.webPages.value

    const answerQuestionPrompt = `Based on the following internet search results:
${results.map(formatInternetResultsInPrompt).join('\n')}
\n
Please answer the question: ${question}`

    console.log('The prompt for .generate is:')
    console.log(answerQuestionPrompt)
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

