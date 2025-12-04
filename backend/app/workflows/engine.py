import logging
from typing import Any, Dict
from datetime import datetime
from app.core.errors import WorkflowException

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Orchestrate workflow execution."""
    
    def __init__(self):
        self.execution_history = []
    
    async def execute(
        self, 
        workflow_type: str, 
        handler_func, 
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a workflow."""
        try:
            logger.info(f"Starting workflow: {workflow_type}")
            
            # Execute the workflow handler
            result = await handler_func(**kwargs)
            
            # Log execution
            self._log_execution(workflow_type, "completed", result)
            
            return {
                "status": "success",
                "message": f"Workflow '{workflow_type}' completed successfully",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        
        except WorkflowException as e:
            logger.error(f"Workflow error: {e.detail}")
            self._log_execution(workflow_type, "failed", {"error": e.detail})
            raise
        
        except Exception as e:
            error_msg = f"Unexpected error in {workflow_type}: {str(e)}"
            logger.error(error_msg)
            self._log_execution(workflow_type, "error", {"error": str(e)})
            raise WorkflowException(error_msg)
    
    def _log_execution(self, workflow_type: str, status: str, result: Any) -> None:
        """Log workflow execution."""
        execution_record = {
            "workflow": workflow_type,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "result_summary": str(result)[:200]  # Truncate for storage
        }
        self.execution_history.append(execution_record)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_history(self) -> list:
        """Get execution history."""
        return self.execution_history

workflow_engine = WorkflowEngine()