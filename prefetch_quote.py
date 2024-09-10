#!/usr/bin/env python
import asyncio
import json
import logging
from typing import Any

import aioboto3

from quote_utils import BUCKET_NAME, OBJECT_KEY, S3_ENDPOINT_URL, fetch_quote_from_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = aioboto3.Session()


async def prefetch_quotes(num_quotes: int = 100) -> list[dict[str, Any]]:
    tasks = [fetch_quote_from_api() for _ in range(num_quotes)]
    results = await asyncio.gather(*tasks)
    return [quote for quote in results if quote is not None]


async def save_quotes_to_s3(quotes: list[dict[str, Any]]) -> None:
    async with session.client("s3", endpoint_url=S3_ENDPOINT_URL) as s3_client:
        try:
            await s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=OBJECT_KEY,
                Body=json.dumps(quotes),
                ContentType="application/json",
            )
        except Exception as e:
            logger.error(f"Error saving quotes to S3-compatible storage: {e}")


async def main() -> None:
    logger.info("Starting quote prefetch process")
    quotes = await prefetch_quotes()
    await save_quotes_to_s3(quotes)
    logger.info(f"Prefetched and saved {len(quotes)} quotes")


if __name__ == "__main__":
    asyncio.run(main())
