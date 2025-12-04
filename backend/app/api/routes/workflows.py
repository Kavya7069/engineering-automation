from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.common import WorkflowResponse
from app.workflows.engine import workflow_engine
from app.workflows.definitions import csv_processing, file_conversion, api_integration, report_generation
from app.workflows.models import (
    FileConversionRequest,
    APIIntegrationRequest,
    ReportGenerationRequest
)

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.post("/csv-processing", response_model=WorkflowResponse)
async def csv_processing_workflow(
    file: UploadFile = File(...),
    operation: str = Form(...)
):
    """CSV processing workflow."""
    try:
        content = await file.read()
        result = await workflow_engine.execute(
            "csv-processing",
            csv_processing.process_csv,
            file_content=content,
            operation=operation
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/file-conversion", response_model=WorkflowResponse)
async def file_conversion_workflow(request: FileConversionRequest):
    """File conversion workflow."""
    try:
        result = await workflow_engine.execute(
            "file-conversion",
            file_conversion.convert_format,
            source_format=request.source_format,
            target_format=request.target_format,
            data=request.data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api-integration", response_model=WorkflowResponse)
async def api_integration_workflow(request: APIIntegrationRequest):
    """API integration workflow."""
    try:
        result = await workflow_engine.execute(
            "api-integration",
            api_integration.call_external_api,
            endpoint=request.endpoint,
            method=request.method,
            params=request.params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/report-generation", response_model=WorkflowResponse)
async def report_generation_workflow(request: ReportGenerationRequest):
    """Report generation workflow."""
    try:
        result = await workflow_engine.execute(
            "report-generation",
            report_generation.generate_report,
            title=request.title,
            data=request.data,
            format=request.format
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
async def get_execution_history():
    """Get workflow execution history."""
    return {
        "history": workflow_engine.get_history(),
        "total_executions": len(workflow_engine.get_history())
    }