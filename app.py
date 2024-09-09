import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from quote_utils import get_quote, initialize_cache

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    await initialize_cache()


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/quote")
async def get_quote_route():
    return await get_quote()


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
