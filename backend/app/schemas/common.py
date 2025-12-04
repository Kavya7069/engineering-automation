from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class WorkflowRequest(BaseModel):
    """Base workflow request."""
    workflow_type: str
    timestamp: Optional[datetime] = None

class WorkflowResponse(BaseModel):
    """Base workflow response."""
    status: str
    message: str
    data: Any
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseModel):
    """Error response."""
    status: str = "error"
    detail: str
    timestamp: datetime = datetime.now()

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str