import json
import typing
from typing import Annotated

import google.generativeai as genai
from fastapi import Depends

from config import Settings, get_settings
from utils import async_wrap


def get_gen_ai(settings: Annotated[Settings, Depends(get_settings)]):
    return GenAi(settings.gemini_api_key)


class AnalyseOutput(typing.TypedDict):
    answer: str
    confidence: float


class GenAi:
    def __init__(self, gemini_api_key):
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        self.model = model

    def get_search_terms(self, query: str) -> list[str]:
        """
        Takes in the query from user input and calls google gemini API to return list of possible search terms
        for pooling in the content.

        :param query: Query string to be given to the GenAI model
        :type query: str
        :return: List of search terms based on the given query string
        :rtype: list[str]
        """
        result = self.model.generate_content(
            f"""
            You are a useful assistant who can generate google search terms as a list based on a given query.
            Max search terms: 1
            Query: {query}
            """,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[str]
            ),
        )
        return json.loads(result.text)

    @async_wrap
    def analyse(self, content: str, question: str) -> AnalyseOutput:
        print(content, question)
        result = self.model.generate_content(
            f"""
                    You are a text analyst capable of searching for answers given a piece of content and a question.
                    Return the answer to the given question from the given content if present. 
                    Also make sure to include the degree of confidence (floating point number between 0 and 1)
                    that the given answer is present and completely matches the question. 
                    Content: {content}
                    Question: {question}
                    """,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=AnalyseOutput
            ),
        )
        return json.loads(result.text)
