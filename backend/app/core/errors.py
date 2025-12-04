from fastapi import HTTPException, status

class WorkflowException(HTTPException):
    """Base workflow exception."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class ValidationError(WorkflowException):
    """Validation error."""
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)

class IntegrationError(WorkflowException):
    """External API integration error."""
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_502_BAD_GATEWAY)

class StorageError(WorkflowException):
    """File storage error."""
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)