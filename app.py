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

import httpx

from fastapi import FastAPI, HTTPException

app = FastAPI()


async def fetch_random_quote():
    '''Fetches a random quote from the Quotable API, an open-source API (https://github.com/lukePeavey/quotable).
    '''
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.quotable.io/random')
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Unable to fetch quote")


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.get("/quote")
async def read_random_quote():
    quote_data = await fetch_random_quote()
    return quote_data


