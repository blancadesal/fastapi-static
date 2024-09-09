import json
from typing import Any, List, Optional

import httpx
from fastapi import HTTPException


async def get_wikipedia_url(author: str) -> Optional[str]:
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={author}&srlimit=5"
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)
        data = response.json()

    if data["query"]["search"]:
        for result in data["query"]["search"]:
            if result["title"].lower() == author.lower():
                page_title = result["title"].replace(" ", "_")
                return f"https://en.wikipedia.org/wiki/{page_title}"
    return None


async def fetch_quote_from_api() -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.quotable.io/random")
        if response.status_code == 200:
            quote_data = response.json()
            wikipedia_url = await get_wikipedia_url(quote_data["author"])
            return {**quote_data, "wikipedia_url": wikipedia_url}
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Unable to fetch quote"
            )


def load_cached_quotes(filename: str = "quote_cache.json") -> List[dict[str, Any]]:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


quote_cache: List[dict[str, Any]] = load_cached_quotes()
