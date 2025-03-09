from urllib.request import OpenerDirector, BaseHandler
from urllib.error import URLError
import http.client
import logging
import json
from functools import wraps

# Setup logging
logging.basicConfig(level=logging.WARNING, format='📦 anyprompt: %(message)s')
logger = logging.getLogger('anyprompt')

# Load existing prompts from prompts.json if it exists
prompts_list = []
try:
    with open('prompts/prompts.json', 'r') as f: prompts_list = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    prompts_list = []

def print_http_request(method, url, headers=None, body=None):
    full_url = url
    logger.debug(f"HTTP request to {full_url}")
    should_allow = True  # Default to allowing the request

    # Create a record of this request
    request_record = {
        'method': method,
        'url': full_url,
        'headers': dict(headers) if headers else None,  # Convert CaseInsensitiveDict to regular dict
        'body': body.decode('utf-8') if isinstance(body, bytes) else body
    }
    
    if headers:
        logger.debug(f"Headers: {headers}")
    if body:
        try:
            body_content = json.loads(body.decode('utf-8')) if isinstance(body, bytes) else body
            logger.critical(f"Body: {json.dumps(body_content, indent=3) if isinstance(body_content, dict) else f'   {body_content}'}")
        except:
            logger.debug(f"Body: {body}")
    
    # Add this request to the list and save
    prompts_list.append(request_record)
    try:
        with open('prompts/prompts.json', 'w') as f:
            json.dump(prompts_list, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save prompts/prompts.json: {e}")
    
    logger.debug("\n")
    return should_allow  # Return whether the request should be allowed

# Patch urllib.request
original_open = OpenerDirector._open
@wraps(original_open)
def patched_open(self, req, *args, **kwargs):
    if hasattr(req, 'get_method') and hasattr(req, 'full_url'):
        body = None
        if hasattr(req, 'data') and req.data:
            body = req.data
        should_allow = print_http_request(req.get_method(), req.full_url, headers=req.headers, body=body)
        if not should_allow:
            raise URLError("Request cancelled by anyprompt.")
    return original_open(self, req, *args, **kwargs)
OpenerDirector._open = patched_open

# Patch http.client
original_request = http.client.HTTPConnection.request
@wraps(original_request)
def patched_request(self, method, url, body=None, headers=None, **kwargs):
    host = self.host
    if self.port != 80 and self.port is not None:
        host = f"{host}:{self.port}"
    full_url = f"{self.scheme}://{host}{url}"
    should_allow = print_http_request(method, full_url, headers=headers, body=body)
    if not should_allow:
        class RequestCancelledError(Exception):
            pass
        raise RequestCancelledError("Request cancelled by anyprompt.")
    return original_request(self, method, url, body=body, headers=headers, **kwargs)
http.client.HTTPConnection.request = patched_request

# Patch for aiohttp if it's used
try:
    import aiohttp
    original_request_aiohttp = aiohttp.ClientSession._request
    @wraps(original_request_aiohttp)
    async def patched_aiohttp_request(self, method, url, **kwargs):
        body = kwargs.get('data') or kwargs.get('json')
        should_allow = print_http_request(method, url, headers=kwargs.get('headers'), body=body)
        if not should_allow:
            raise aiohttp.ClientError("Request cancelled by anyprompt.")
        return await original_request_aiohttp(self, method, url, **kwargs)
    aiohttp.ClientSession._request = patched_aiohttp_request
except ImportError:
    pass

# Patch for httpx if it's used
try:
    import httpx
    original_httpx_send = httpx.Client.send
    @wraps(original_httpx_send)
    def patched_httpx_send(self, request, **kwargs):
        body = None
        if request.content:
            body = request.content
        should_allow = print_http_request(request.method, str(request.url), headers=request.headers, body=body)
        if not should_allow:
            raise httpx.RequestError("Request cancelled by anyprompt.")
        return original_httpx_send(self, request, **kwargs)
    httpx.Client.send = patched_httpx_send
    
    # Patch async httpx
    original_httpx_async_send = httpx.AsyncClient.send
    @wraps(original_httpx_async_send)
    async def patched_httpx_async_send(self, request, **kwargs):
        body = None
        if request.content:
            body = request.content
        should_allow = print_http_request(request.method, str(request.url), headers=request.headers, body=body)
        if not should_allow:
            raise httpx.RequestError("Request cancelled by anyprompt.")
        return await original_httpx_async_send(self, request, **kwargs)
    httpx.AsyncClient.send = patched_httpx_async_send
except ImportError:
    pass

# Patch for requests if it's used
try:
    import requests
    original_requests_send = requests.Session.send
    @wraps(original_requests_send)
    def patched_requests_send(self, request, **kwargs):
        body = None
        if request.body:
            body = request.body
        should_allow = print_http_request(request.method, request.url, headers=request.headers, body=body)
        if not should_allow:
            raise requests.exceptions.RequestException("Request cancelled by anyprompt.")
        return original_requests_send(self, request, **kwargs)
    requests.Session.send = patched_requests_send
except ImportError:
    pass