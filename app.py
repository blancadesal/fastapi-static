import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def fetch_random_quote():
    """Fetch a random quote from the Quotable API, an open-source API (https://github.com/lukePeavey/quotable)."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.quotable.io/random")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Unable to fetch quote"
            )


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/quote")
async def get_quote():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.quotable.io/random")
        quote_data = response.json()

    # Check if the author has a Wikipedia page
    author = quote_data["author"]
    wikipedia_url = await get_wikipedia_url(author)

    return {
        "content": quote_data["content"],
        "author": author,
        "wikipedia_url": wikipedia_url,
    }


async def get_wikipedia_url(author):
    # Attempt to find a Wikipedia page for the author
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={author}"
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)
        data = response.json()

    if data["query"]["search"]:
        # If a page is found, return the URL
        page_title = data["query"]["search"][0]["title"].replace(" ", "_")
        return f"https://en.wikipedia.org/wiki/{page_title}"
    else:
        # If no page is found, return None
        return None


@app.get("/")
async def read_root(request: Request):
    button_color = os.getenv("BUTTON_COLOR", "blue")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "button_color": "#28a745" if button_color == "green" else "#007bff",
        },
    )
