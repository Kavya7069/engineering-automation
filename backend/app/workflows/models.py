from pydantic import BaseModel
from typing import Any, Optional, Dict

class CSVProcessingRequest(BaseModel):
    """CSV processing workflow request."""
    operation: str  # validate, summary, transform

class FileConversionRequest(BaseModel):
    """File conversion workflow request."""
    source_format: str
    target_format: str
    data: str

class APIIntegrationRequest(BaseModel):
    """API integration workflow request."""
    endpoint: str
    method: str
    params: Optional[Dict[str, Any]] = None

class ReportGenerationRequest(BaseModel):
    """Report generation workflow request."""
    title: str
    data: Dict[str, Any]
    format: str  # html, json, markdown