from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
import uvicorn
import asyncio
from bot import Chat
import re
import json
import urllib.parse


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


@app.post("/get_result", response_class=JSONResponse)
async def get_result(request: Request):
    data = await request.json()
    query = data.get("query")
    print(f"Received query: {query}")
    print("Processing query...")
    
    result = Chat().chat(f"Find me the car parts for {query}")
    
    # Use regex to find the JSON-like parts
    json_pattern = re.compile(r'{(.*?)}', re.DOTALL)
    matches = json_pattern.findall(result)

    parsed_json_list = []  # Initialize an empty list to hold parsed JSON objects

    # Process the matches to make them valid JSON
    for match in matches:
        # Replace double curly braces with single ones
        json_str = match.replace('{{', '{').replace('}}', '}')
        # Add the enclosing braces
        json_str = '{' + json_str + '}'
        
        try:
            # Parse the JSON string
            parsed_json = json.loads(json_str)
            parsed_json_list.append(parsed_json)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")

    if not parsed_json_list:
        return JSONResponse(content={"message": "No products found.", "data": []})
    else:
        return JSONResponse(content={"message": "Here are the found products.", "data": parsed_json_list})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
