import ollama
import requests
import json
import os
from dotenv import load_dotenv
from exa_py import Exa
from src.rainbow_print import *

def search_internet(query: str) -> str:
    load_dotenv() # For API Keys etc
    try:
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            raise Exception("EXA_API_KEY not set")
        
        exa = Exa(api_key)

        response = exa.search(
        query,
        num_results = 1,
        type = "auto",
        contents = {
            "text": {
            "verbosity": "compact"
            }
        }
        )

        return response.results[0].text


    except Exception as e:
        return f"Search error: {e}"

search_internet_tool = {
    "type": "function",
    "function": {
        "name": "search_internet",
        "description": "Search the internet for up-to-date information on a topic using the Exa search engine.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up."
                }
            },
            "required": ["query"]
        }
    }
}

available_tools = {
    'search_internet': search_internet
}

if __name__ == '__main__':
    rainbow_print(search_internet('react custom hook docs'))
