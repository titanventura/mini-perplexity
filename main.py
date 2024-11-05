import asyncio
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from gen_ai import GenAi, get_gen_ai
from search_engine import SearchEngine, get_search_engine
from web_crawler import WebCrawler, get_web_crawler
from functools import reduce

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    answer: str
    confidence: float
    source_url: str


@app.post("/search/", response_model=List[SearchResult])
async def search(
        req: SearchRequest,
        gen_ai: Annotated[GenAi, Depends(get_gen_ai)],
        search_engine: Annotated[SearchEngine, Depends(get_search_engine)],
        web_crawler: Annotated[WebCrawler, Depends(get_web_crawler)]
):
    # Step 1: Get search terms from Gen AI for the user query
    search_terms = gen_ai.get_search_terms(req.query)

    # Step 2: Perform web searches for each search term (Async)
    search_tasks = [search_engine.search(term) for term in search_terms]
    search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
    search_results_flattened = list(
        reduce(lambda x, y: x + y[:4] if not isinstance(y, Exception) else x, search_results, []))

    # Step 3: Crawl the top results from the search engine (Async)
    # We associate each crawl result with its corresponding URL
    crawl_tasks = [(web_crawler.crawl(sr["formattedUrl"]), sr["formattedUrl"]) for sr in search_results_flattened]
    crawl_results = await asyncio.gather(*[task[0] for task in crawl_tasks], return_exceptions=True)
    crawl_urls = [task[1] if not isinstance(task[1], Exception) else None for task in crawl_tasks]
    crawl_urls = list(filter(lambda u: u is not None, crawl_urls))

    # Step 4: Analyse the crawled content with Gen AI (Async)
    # We associate each analysis result with its corresponding URL
    analyse_tasks = [(gen_ai.analyse(content, req.query), url) for content, url in zip(crawl_results, crawl_urls)]
    analyse_results = await asyncio.gather(*[task[0] for task in analyse_tasks], return_exceptions=True)
    analyse_urls = [task[1] if not isinstance(task[1], Exception) else None for task in analyse_tasks]
    analyse_urls = list(filter(lambda u: u is not None, analyse_urls))

    # Step 5: Combine analysis results with URLs and sort by confidence level
    combined_results = []
    for res, url in zip(analyse_results, analyse_urls):
        if res.get("answer") and res.get("confidence"):
            combined_results.append({"answer": res["answer"], "confidence": res["confidence"], "source_url": url})

    # Sort the results by confidence level in descending order and return the top 5
    combined_results = sorted(combined_results, key=lambda res: res["confidence"], reverse=True)

    if len(combined_results) == 0:
        raise HTTPException(status_code=500, detail="Unable to search or analyse results")

    return combined_results
