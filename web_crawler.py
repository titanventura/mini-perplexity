from functools import lru_cache
from typing import Optional

import httpx
from bs4 import BeautifulSoup
import re


# @lru_cache
def get_web_crawler():
    return WebCrawler()


class WebCrawler:
    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize the WebCrawler with an optional User-Agent.
        """
        self.user_agent = user_agent or "Mozilla/5.0 (compatible; WebCrawler/1.0)"

    async def fetch(self, url: str) -> str:
        """
        Fetch the content of the webpage asynchronously.
        """
        headers = {"User-Agent": self.user_agent}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text

    def sanitize_content(self, html_content: str) -> str:
        """
        Sanitize the HTML content by removing all tags and returning plain text.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove scripts and style elements (if needed)
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Extract and return the text
        raw = soup.get_text(separator=" ").strip()
        lines_and_tabs_removed = raw.replace("\n", "").replace("\t", "")
        extra_space_removed = re.sub(" +", " ", lines_and_tabs_removed)
        return extra_space_removed

    async def crawl(self, url: str) -> str:
        """
        Crawl the provided URL and return sanitized content (plain text).
        """
        try:
            html_content = await self.fetch(url)
            sanitized_content = self.sanitize_content(html_content)
            return sanitized_content
        except Exception as e:
            return f"Error occurred while crawling {url}: {str(e)}"
