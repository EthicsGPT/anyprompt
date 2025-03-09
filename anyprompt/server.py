import json
import os
import pkg_resources
import logging
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Get logger from main module
logger = logging.getLogger('anyprompt')

# Create FastAPI app
app = FastAPI(title="anyprompt", docs_url=None, redoc_url=None)

# Define the templates directory - this will be included in the package
templates_path = pkg_resources.resource_filename('anyprompt', 'templates')
templates = Jinja2Templates(directory=templates_path)

# Define the static files directory - this will be included in the package
static_path = pkg_resources.resource_filename('anyprompt', 'static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

def get_prompts_data():
    """Load prompts data from the prompts.json file."""
    prompts_file = Path.cwd() / "prompts" / "prompts.json"
    try:
        if prompts_file.exists():
            with open(prompts_file, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, Exception):
        pass
    return []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main page with the UI for viewing prompts."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/prompts")
async def api_get_prompts():
    """API endpoint to get prompts data."""
    prompts = get_prompts_data()
    return {"prompts": prompts}

@app.delete("/api/prompts")
async def api_clear_prompts():
    """API endpoint to clear all prompts."""
    prompts_file = Path.cwd() / "prompts" / "prompts.json"
    try:
        with open(prompts_file, 'w') as f:
            json.dump([], f)
        return {"status": "success", "message": "All prompts cleared"}
    except Exception as e:
        logger.error(f"Error clearing prompts: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

def start_server(port=2400):
    """Start the FastAPI server with uvicorn."""
    # This will be called in a background thread from __init__.py
    try:
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")
    except Exception as e:
        logger.error(f"Failed to start anyprompt server: {e}") 