from typing import Any, Dict
from app.services.report_service import report_service
from app.core.errors import ValidationError

async def generate_report(
    title: str,
    data: Dict[str, Any],
    format: str
) -> Dict[str, Any]:
    """Generate report in specified format."""
    try:
        if format == "html":
            content = report_service.generate_html(title, data)
            file_extension = "html"
        elif format == "markdown":
            content = report_service.generate_markdown(title, data)
            file_extension = "md"
        elif format == "json":
            content = report_service.generate_json(title, data)
            file_extension = "json"
        else:
            raise ValidationError(f"Unsupported report format: {format}")
        
        return {
            "report_title": title,
            "format": format,
            "file_extension": file_extension,
            "report_content": content,
            "status": "generated"
        }
    
    except Exception as e:
        raise ValidationError(f"Report generation failed: {str(e)}")