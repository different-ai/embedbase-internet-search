import { createClient } from 'embedbase-js'

// Usage:
// EMBEDBASE_API_KEY="<get me here https://app.embedbase.xyz>" npx tsx answer.ts "What is GPT4?"

// Name: name
// Snippet: snippet
// Url: url
const formatInternetResultsInPrompt = (internetResult: any) =>
    `Name: ${internetResult.title}
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

    if (!question) {
        console.log('Please provide a question as argument, for example "What is GPT4?"')
        return
    }

    console.log(`Answering question: ${question}`)
    console.log('I will search internet first')


    const results = await embedbase.internetSearch(question)
    console.log('Internet search response:')
    console.log(results)

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

