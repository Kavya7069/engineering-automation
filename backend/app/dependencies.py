import httpx
from app.config import get_settings

settings = get_settings()

async def get_http_client():
    """Provide HTTP client for external API calls."""
    async with httpx.AsyncClient(
        timeout=settings.external_api_timeout,
        limits=httpx.Limits(max_connections=100)
    ) as client:
        yield client        