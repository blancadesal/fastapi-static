# -*- coding: utf-8 -*-
#
# This file is part of the Toolforge Python ASGI tutorial
#
# Copyright (C) 2023 Slavina Stefanova and contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import httpx

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def fetch_random_quote():
    '''Fetch a random quote from the Quotable API, an open-source API (https://github.com/lukePeavey/quotable).
    '''
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.quotable.io/random')
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Unable to fetch quote")


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
        "wikipedia_url": wikipedia_url
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    button_color = os.getenv('BUTTON_COLOR', 'blue')
    return templates.TemplateResponse("index.html", {
        "request": request,
        "button_color": '#28a745' if button_color == 'green' else '#007bff'
    })
