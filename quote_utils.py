import json
import logging
from typing import Any

import aioboto3
import httpx
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_ENDPOINT_URL = "https://object.eqiad1.wikimediacloud.org"
BUCKET_NAME = "slavina-test"
OBJECT_KEY = "quote_cache.json"

session = aioboto3.Session()


async def get_wikipedia_url(author: str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={author}&format=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if (
                "query" in data
                and "search" in data["query"]
                and data["query"]["search"]
            ):
                page_id = data["query"]["search"][0]["pageid"]
                return f"https://en.wikipedia.org/?curid={page_id}"
            return ""
        except Exception as e:
            logger.error(f"Error fetching Wikipedia URL for {author}: {e}")
            return ""


async def fetch_quote_from_api() -> dict[str, Any] | None:
    url = "https://api.quotable.io/random"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            quote_data = response.json()
            quote_data["wikipedia_url"] = await get_wikipedia_url(quote_data["author"])
            return quote_data
        except Exception as e:
            logger.error(f"Error fetching quote: {e}")
            return None


async def load_cached_quotes() -> list[dict[str, Any]]:
    async with session.client("s3", endpoint_url=S3_ENDPOINT_URL) as s3_client:
        try:
            response = await s3_client.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
            async with response["Body"] as stream:
                data = await stream.read()
            quotes = json.loads(data.decode("utf-8"))
            logger.info(f"Loaded {len(quotes)} quotes from cache")
            return quotes
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.info("No existing quote cache found")
                return []
            else:
                logger.error(f"Error loading quotes from S3-compatible storage: {e}")
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
        logger.info("Cache empty, fetching new quote from API")
        return await fetch_quote_from_api()
