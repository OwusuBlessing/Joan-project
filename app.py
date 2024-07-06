from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import uvicorn
import asyncio


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/next_search", response_class=HTMLResponse)
async def next_search(request: Request):
    return templates.TemplateResponse("next_search.html", {"request": request})


@app.post("/get_result")
async def get_result(request: Request):
    data = await request.json()
    query = data.get("query")
    print(f"Received query: {query}")
    print("Processing query...")
    # Simulate a delay
    await asyncio.sleep(10)
    # Process the query and return a response
    return JSONResponse(content={"result": f"Received query: {query}"})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
