from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import workflows, health
from app.core.errors import WorkflowException
from app.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Engineering Workflow Automation",
    description="Automate common engineering workflows",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(WorkflowException)
async def workflow_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status": "error"}
    )

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(workflows.router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Engineering Workflow Automation API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
