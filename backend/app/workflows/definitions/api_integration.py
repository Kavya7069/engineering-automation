
from typing import Any, Dict, Optional
import httpx
from app.core.errors import IntegrationError
from app.config import get_settings

settings = get_settings()

async def call_external_api(
    endpoint: str,
    method: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Call external API and return response."""
    try:
        async with httpx.AsyncClient(timeout=settings.external_api_timeout) as client:
            if method == "GET":
                response = await client.get(endpoint, params=params)
            elif method == "POST":
                response = await client.post(endpoint, json=params)
            elif method == "PUT":
                response = await client.put(endpoint, json=params)
            else:
                raise IntegrationError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            try:
                data = response.json()
            except:
                data = {"content": response.text}
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "response_data": data,
                "headers": dict(response.headers)
            }
    
    except httpx.TimeoutException:
        raise IntegrationError(f"API call timeout: {endpoint}")
    except httpx.RequestError as e:
        raise IntegrationError(f"Failed to call API: {str(e)}")
    except Exception as e:
        raise IntegrationError(f"API integration error: {str(e)}")
