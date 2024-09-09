#!/usr/bin/env python
import asyncio
import json
from typing import Any

from quote_utils import fetch_quote_from_api


async def prefetch_quotes(num_quotes: int = 100) -> list[dict[str, Any]]:
    tasks = [fetch_quote_from_api() for _ in range(num_quotes)]
    results = await asyncio.gather(*tasks)
    return [quote for quote in results if quote is not None]


def save_quotes_to_file(
    quotes: list[dict[str, Any]], filename: str = "quote_cache.json"
) -> None:
    with open(filename, "w") as f:
        json.dump(quotes, f)


async def main() -> None:
    print("Prefetching quotes...")
    quotes = await prefetch_quotes()
    save_quotes_to_file(quotes)
    print(f"Successfully prefetched and saved {len(quotes)} quotes.")


if __name__ == "__main__":
    asyncio.run(main())
