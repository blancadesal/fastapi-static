import json
from typing import Any, Optional

import aioboto3
import httpx
from botocore.exceptions import ClientError
from fastapi import HTTPException

S3_ENDPOINT_URL = "https://object.eqiad1.wikimediacloud.org"
BUCKET_NAME = "slavina-test"
OBJECT_KEY = "quote_cache.json"

session = aioboto3.Session()


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


async def load_cached_quotes() -> list[dict[str, Any]]:
    async with session.client("s3", endpoint_url=S3_ENDPOINT_URL) as s3_client:
        try:
            response = await s3_client.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
            async with response["Body"] as stream:
                data = await stream.read()
            return json.loads(data.decode("utf-8"))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                print("No existing quote cache found in S3-compatible storage.")
                return []
            else:
                print(f"Error loading quotes from S3-compatible storage: {e}")
                return []


quote_cache: list[dict[str, Any]] = []


async def initialize_cache():
    global quote_cache
    quote_cache = await load_cached_quotes()


async def get_quote():
    global quote_cache
    if not quote_cache:
        await initialize_cache()
    if quote_cache:
        return quote_cache.pop(0)
    else:
        return await fetch_quote_from_api()
