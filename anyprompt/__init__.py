import logging
import os
import json
import threading
import socket
from functools import wraps
from urllib.request import OpenerDirector
from urllib.error import URLError
import http.client
from pathlib import Path
import atexit
import uuid

__version__ = "0.4.0"

# Setup logging with a clean, colorful format
logging.basicConfig(level=logging.WARNING, format='📦 \033[1;36manyprompt:\033[0m %(message)s')
logger = logging.getLogger('anyprompt')

# Global variables
_server_thread = None
_server_port = 2400  # Default port
_prompts_list = []
_server_url = None
_request_ids = {}  # Dictionary to map request objects to their IDs

def _find_available_port(start_port=2400, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return start_port  # Fallback to the default port

def _ensure_dirs():
    """Ensure necessary directories exist."""
    # Create in the user's current working directory
    cwd = Path.cwd()
    prompts_dir = cwd / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    return prompts_dir

def _load_prompts():
    """Load existing prompts from the prompts.json file."""
    global _prompts_list
    prompts_dir = _ensure_dirs()
    prompts_file = prompts_dir / "prompts.json"
    
    try:
        if prompts_file.exists():
            with open(prompts_file, 'r') as f:
                _prompts_list = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to load prompts file: {e}")
        _prompts_list = []

def _save_prompts():
    """Save prompts to the prompts.json file."""
    global _prompts_list
    prompts_dir = _ensure_dirs()
    prompts_file = prompts_dir / "prompts.json"
    
    try:
        with open(prompts_file, 'w') as f:
            json.dump(_prompts_list, f, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save prompts file: {e}")

def _print_http_request(method, url, headers=None, body=None, request_obj=None):
    """Log and record HTTP requests that might contain prompts."""
    global _prompts_list, _request_ids
    
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    
    # Create a record of this request
    request_record = {
        'id': request_id,
        'method': method,
        'url': url,
        'headers': dict(headers) if headers else None,
        'body': body.decode('utf-8') if isinstance(body, bytes) else body,
        'timestamp': datetime.now().isoformat(),
        'has_response': False,
        'response': None
    }
    
    # Extract and log relevant prompt information
    if body:
        try:
            body_content = json.loads(body.decode('utf-8')) if isinstance(body, bytes) else body
            if isinstance(body_content, dict):
                # Check if this looks like an LLM API call (OpenAI, Anthropic, etc.)
                if 'messages' in body_content or 'prompt' in body_content:
                    logger.info(f"📝 Captured prompt to {url}")
        except:
            pass
    
    # Add this request to the list and save
    _prompts_list.append(request_record)
    _save_prompts()
    
    # If we have a request object, store its ID for later linking with response
    if request_obj is not None:
        _request_ids[id(request_obj)] = request_id
    
    return request_id

def _print_http_response(response_obj, status_code, headers=None, body=None, request_id=None):
    """Log and record HTTP responses."""
    global _prompts_list
    
    # Try to find the matching request
    if request_id is None and response_obj is not None:
        request_id = _request_ids.pop(id(response_obj), None)
    
    # If we found a matching request, update it with response data
    if request_id:
        for i, entry in enumerate(_prompts_list):
            if entry.get('id') == request_id:
                response_data = {
                    'status_code': status_code,
                    'headers': dict(headers) if headers else None,
                    'body': body.decode('utf-8') if isinstance(body, bytes) else body,
                    'timestamp': datetime.now().isoformat()
                }
                
                _prompts_list[i]['has_response'] = True
                _prompts_list[i]['response'] = response_data
                
                # Log a message for LLM API responses
                if body:
                    try:
                        body_content = json.loads(body.decode('utf-8')) if isinstance(body, bytes) else body
                        if isinstance(body_content, dict):
                            # Check for common LLM API response fields
                            if any(key in body_content for key in ['choices', 'completion', 'content']):
                                logger.info(f"🤖 Captured response from {_prompts_list[i]['url']}")
                    except:
                        pass
                
                _save_prompts()
                break
    else:
        # If we don't have a request_id, still log this as a standalone response
        response_record = {
            'type': 'standalone_response',
            'status_code': status_code,
            'headers': dict(headers) if headers else None,
            'body': body.decode('utf-8') if isinstance(body, bytes) else body,
            'timestamp': datetime.now().isoformat()
        }
        _prompts_list.append(response_record)
        _save_prompts()

def _start_server():
    """Start the FastAPI server in a background thread."""
    global _server_thread, _server_port, _server_url
    
    # Import here to avoid circular imports
    from anyprompt.server import start_server
    
    # Find an available port
    _server_port = _find_available_port()
    _server_url = f"http://localhost:{_server_port}"
    
    # Start the server in a background thread
    _server_thread = threading.Thread(
        target=start_server,
        args=(_server_port,),
        daemon=True  # Make thread a daemon so it exits when the main program exits
    )
    _server_thread.start()
    
    # Print a nice message with the URL
    print(f"📦 \033[1;36manyprompt\033[0m is active | view at \033[1;34m{_server_url}\033[0m\n")


def _patch_http_libraries():
    """Patch various HTTP libraries to capture prompts and responses."""
    # Patch urllib.request
    original_open = OpenerDirector._open
    @wraps(original_open)
    def patched_open(self, req, *args, **kwargs):
        body = None
        if hasattr(req, 'data') and req.data:
            body = req.data
        
        request_id = None
        if hasattr(req, 'get_method') and hasattr(req, 'full_url'):
            request_id = _print_http_request(req.get_method(), req.full_url, headers=req.headers, body=body, request_obj=req)
        
        response = original_open(self, req, *args, **kwargs)
        
        # Capture response data
        if request_id and hasattr(response, 'code') and hasattr(response, 'headers'):
            try:
                response_body = response.read()
                # Put the data back so the caller can use it
                if hasattr(response, 'fp'):
                    from io import BytesIO
                    response.fp = BytesIO(response_body)
                _print_http_response(response, response.code, headers=response.headers, body=response_body, request_id=request_id)
            except:
                # If we can't read the response, at least log the status
                _print_http_response(response, response.code, headers=response.headers, request_id=request_id)
        
        return response
    OpenerDirector._open = patched_open

    # Patch http.client
    original_request = http.client.HTTPConnection.request
    original_getresponse = http.client.HTTPConnection.getresponse
    
    @wraps(original_request)
    def patched_request(self, method, url, body=None, headers=None, **kwargs):
        host = self.host
        if self.port != 80 and self.port is not None:
            host = f"{host}:{self.port}"
        # Determine scheme (http vs https)
        scheme = "https" if self.__class__.__name__ == "HTTPSConnection" else "http"
        full_url = f"{scheme}://{host}{url}"
        
        request_id = _print_http_request(method, full_url, headers=headers, body=body, request_obj=self)
        self._anyprompt_request_id = request_id  # Store request_id on the connection object
        
        return original_request(self, method, url, body=body, headers=headers, **kwargs)
    
    @wraps(original_getresponse)
    def patched_getresponse(self, **kwargs):
        response = original_getresponse(self, **kwargs)
        
        # Get request_id if it was stored during the request
        request_id = getattr(self, '_anyprompt_request_id', None)
        
        if request_id and hasattr(response, 'status') and hasattr(response, 'headers'):
            try:
                # Read response data while preserving the original behavior
                response_data = response.read()
                
                # Create a new HTTPResponse with the same data
                from io import BytesIO
                sock = BytesIO(response_data)
                
                # Record the response
                _print_http_response(response, response.status, headers=response.headers, 
                                    body=response_data, request_id=request_id)
                
                # Build a new response object with our data
                new_resp = http.client.HTTPResponse(sock)
                new_resp.begin()
                
                # Copy attributes from the original response
                for attr in dir(response):
                    if attr.startswith('_') or attr in ('read', 'readinto', 'getheader', 'getheaders'):
                        continue
                    try:
                        setattr(new_resp, attr, getattr(response, attr))
                    except (AttributeError, TypeError):
                        pass
                
                return new_resp
            except:
                # If we can't read the response, at least log the status
                _print_http_response(response, response.status, headers=response.headers, request_id=request_id)
        
        return response
    
    http.client.HTTPConnection.request = patched_request
    http.client.HTTPConnection.getresponse = patched_getresponse

    # Patch for requests if available
    try:
        import requests
        original_requests_send = requests.Session.send
        @wraps(original_requests_send)
        def patched_requests_send(self, request, **kwargs):
            body = None
            if request.body:
                body = request.body
            request_id = _print_http_request(request.method, request.url, headers=request.headers, body=body, request_obj=request)
            
            response = original_requests_send(self, request, **kwargs)
            
            # Capture response data
            if hasattr(response, 'status_code') and hasattr(response, 'headers'):
                _print_http_response(response, response.status_code, headers=response.headers, 
                                   body=response.content, request_id=request_id)
            
            return response
        requests.Session.send = patched_requests_send
    except ImportError:
        pass

    # Patch for httpx if available
    try:
        import httpx
        original_httpx_send = httpx.Client.send
        @wraps(original_httpx_send)
        def patched_httpx_send(self, request, **kwargs):
            body = None
            if request.content:
                body = request.content
            request_id = _print_http_request(request.method, str(request.url), headers=request.headers, body=body, request_obj=request)
            
            response = original_httpx_send(self, request, **kwargs)
            
            # Capture response data
            if hasattr(response, 'status_code') and hasattr(response, 'headers'):
                _print_http_response(response, response.status_code, headers=response.headers, 
                                   body=response.content, request_id=request_id)
            
            return response
        httpx.Client.send = patched_httpx_send
        
        # Patch async httpx
        original_httpx_async_send = httpx.AsyncClient.send
        @wraps(original_httpx_async_send)
        async def patched_httpx_async_send(self, request, **kwargs):
            body = None
            if request.content:
                body = request.content
            request_id = _print_http_request(request.method, str(request.url), headers=request.headers, body=body, request_obj=request)
            
            response = await original_httpx_async_send(self, request, **kwargs)
            
            # Capture response data
            if hasattr(response, 'status_code') and hasattr(response, 'headers'):
                _print_http_response(response, response.status_code, headers=response.headers, 
                                   body=response.content, request_id=request_id)
            
            return response
        httpx.AsyncClient.send = patched_httpx_async_send
    except ImportError:
        pass

    # Patch for aiohttp if available
    try:
        import aiohttp
        original_request_aiohttp = aiohttp.ClientSession._request
        @wraps(original_request_aiohttp)
        async def patched_aiohttp_request(self, method, url, **kwargs):
            body = kwargs.get('data') or kwargs.get('json')
            request_id = _print_http_request(method, url, headers=kwargs.get('headers'), body=body)
            
            response = await original_request_aiohttp(self, method, url, **kwargs)
            
            # Capture response data
            if hasattr(response, 'status') and hasattr(response, 'headers'):
                try:
                    # For aiohttp, we need to clone the response to read it without consuming it
                    content = await response.read()
                    _print_http_response(response, response.status, headers=response.headers, 
                                       body=content, request_id=request_id)
                except:
                    # If we can't read the body, at least log the status
                    _print_http_response(response, response.status, headers=response.headers, 
                                       request_id=request_id)
            
            return response
        aiohttp.ClientSession._request = patched_aiohttp_request
    except ImportError:
        pass

def shutdown():
    """Cleanup function called when the Python process exits."""
    # Save any pending prompts
    _save_prompts()
    logger.info("anyprompt server stopped")

# Register the shutdown function
atexit.register(shutdown)

# Store import time for timestamping
from datetime import datetime
import_time_iso = datetime.now().isoformat()

# Initialize: load prompts, patch HTTP libraries, and start server
_load_prompts()
_patch_http_libraries()
_start_server() 