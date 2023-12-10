from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from db_migration import Migration
from dynamo_client import DynamoClient, TableClient
from url_service import UrlService

app = FastAPI()
BASE_URL: str = "http://locahost:8080"

client = DynamoClient()
migration = Migration(client)
migration.migrate()

table = TableClient()
url_service = UrlService(table)


class ShortenRequest(BaseModel):
    url: str = Form(...)


@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.
    """
    short_url = url_service.shorten_url(request.url)
    return {"short_url": f"{BASE_URL}/r/{short_url}"}


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    original_url = url_service.lengthen_url(short_url)
    if original_url == '':
        raise HTTPException(status_code=404, detail="Url not found")

    return RedirectResponse(original_url)


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
