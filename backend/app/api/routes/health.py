from fastapi import APIRouter
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }