import json
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path

# Create directories if they don't exist
os.makedirs("prompts", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app = FastAPI(title="Prompts Viewer")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Function to read prompts data
def get_prompts_data():
    try:
        with open('prompts/prompts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty list if file doesn't exist or is invalid
        return []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/prompts")
async def get_prompts():
    """API endpoint to get prompts data"""
    prompts = get_prompts_data()
    return {"prompts": prompts}

if __name__ == "__main__":
    # Ensure the prompts.json file exists
    if not Path("prompts.json").exists():
        with open("prompts/prompts.json", "w") as f:
            json.dump([], f)
    
    # Run the server
    print("💫 Starting Prompts Viewer on http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=3000) 