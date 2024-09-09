#!/usr/bin/env python
import asyncio
import json
from typing import Any

import aioboto3

from quote_utils import BUCKET_NAME, OBJECT_KEY, S3_ENDPOINT_URL, fetch_quote_from_api

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
            print(f"Successfully saved quotes to S3-compatible storage: {BUCKET_NAME}")
        except Exception as e:
            print(f"Error saving quotes to S3-compatible storage: {e}")


async def load_quotes_from_s3() -> list[dict[str, Any]]:
    async with session.client("s3", endpoint_url=S3_ENDPOINT_URL) as s3_client:
        try:
            response = await s3_client.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
            async with response["Body"] as stream:
                data = await stream.read()
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            if "NoSuchKey" in str(e):
                print(
                    "No existing quote cache found in S3-compatible storage. Creating a new one."
                )
                return []
            else:
                print(f"Error loading quotes from S3-compatible storage: {e}")
                return []


async def main() -> None:
    print("Prefetching quotes...")
    quotes = await prefetch_quotes()
    await save_quotes_to_s3(quotes)
    print(
        f"Successfully prefetched and saved {len(quotes)} quotes to S3-compatible storage."
    )


if __name__ == "__main__":
    asyncio.run(main())
