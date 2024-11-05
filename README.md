# Perplexity-Like System

This is a Python-based web search and analysis system inspired by **Perplexity**. It leverages search engines, web
crawlers, and a large language model (LLM) to process user queries, retrieve relevant information from the web, and
return concise answers with confidence scores and source citations. The system is built using **FastAPI**, and it
integrates asynchronous tasks to ensure fast and efficient processing of multiple search and analysis requests.

## Features

- **Search term analysis**: Uses a generative AI model (google gemini 1.5 Alpha) to extract relevant search terms from
  the user query.
- **Web Search**: Searches the web using a search engine API (e.g., Google Custom Search).
- **Web Crawling**: Fetches and sanitizes content from the web using an asynchronous web crawler.
- **LLM-Based Analysis**: Uses an LLM backend to analyze the crawled content and generate an answer to the user's query.
- **Confidence Score & Source**: Returns a list of top results sorted by confidence, with citations (URLs) of the
  original sources.

## Architecture Overview

- **FastAPI**: Provides the API endpoints for submitting search queries and returning results.
- **Async Task Handling**: Asynchronous processing of search, crawl, and analysis tasks using Python's `asyncio`.
- **Search Engine Integration**: Uses the Google custom JSON search engine API to find relevant web pages.
- **Web Crawler**: An asynchronous web crawler that fetches and sanitizes web content (removes HTML tags, scripts,
  etc.).
- **Generative AI Model (GenAI)**: A language model backend (e.g., Google Gemini or similar) that analyzes crawled
  content and provides answers.

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry (as a package manager)
- Access to the required APIs:
    - **Generative AI API** (e.g., Google Gemini API)
    - **Search Engine API** (e.g., Google Custom Search)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/perplexity-like-system.git
    cd perplexity-like-system
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

3. Configure your API keys:

    - **GenAI API Key**: Set up your API credentials for the generative AI model (e.g., Google Gemini).
    - **Search Engine API Key**: Set up your search engine API key (e.g., Google Custom Search). 
   You can add these to environment variables or directly in the code (for development).
   ```
    GEMINI_API_KEY=<GEMINI_API_KEY>
    SEARCH_API_KEY=<GOOGLE_CUSTOM_JSON_SEARCH_API_KEY>
    SEARCH_ENGINE_ID=<GOOGLE_CUSTOM_JSON_SEARCH_ENGINE_ID>
    ```
    

### Running the Application

To run the FastAPI application locally:

```bash
poetry run uvicorn main:app --reload
```

### Sample request

```bash
curl -X POST "http://127.0.0.1:8000/search/" \
-H "Content-Type: application/json" \
-d '{"query": "What is the capital of France?"}'
```

### Sample Response
```
[
    {
        "answer": "The 2026 FIFA World Cup will be jointly hosted by 16 cities in three North American countries: Canada, Mexico, and the United States.",
        "confidence": 1.0,
        "source_url": "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup"
    },
    {
        "answer": "Canada, Mexico, and the USA",
        "confidence": 1.0,
        "source_url": "https://www.fifa.com/.../worldcup/canadamexicousa2026/.../world-cup-202..."
    },
    {
        "answer": "The 2026 World Cup will be held in Mexico, Canada, and the United States.",
        "confidence": 1.0,
        "source_url": "https://olympics.com/.../fifa-world-cup-2026-full-list-stadiums-mexico-cana..."
    },
    {
        "answer": "Canada, Mexico and USA",
        "confidence": 0.9,
        "source_url": "https://www.fifa.com/en/.../worldcup/canadamexicousa2026/host-cities"
    }
]
```

### sample error

```
{"detail":"Unable to search or analyse results"}
```