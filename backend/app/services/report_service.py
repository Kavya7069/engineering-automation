import json
from typing import Any, Dict
from datetime import datetime

class ReportService:
    """Generate formatted reports."""
    
    @staticmethod
    def generate_html(title: str, data: Dict[str, Any]) -> str:
        """Generate HTML report."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #208d8d; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #208d8d; color: white; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
        </html>
        """
        return html_content
    
    @staticmethod
    def generate_markdown(title: str, data: Dict[str, Any]) -> str:
        """Generate Markdown report."""
        md_content = f"""# {title}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data

{json.dumps(data, indent=2)}
"""
        return md_content
    
    @staticmethod
    def generate_json(title: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON report."""
        return {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "data": data
        }

report_service = ReportService()