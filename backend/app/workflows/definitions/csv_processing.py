import csv
import io
from typing import Any, Dict
from app.core.errors import ValidationError

async def process_csv(file_content: bytes, operation: str) -> Dict[str, Any]:
    """Process CSV file."""
    try:
        # Decode CSV
        text_content = file_content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text_content))
        rows = list(reader)
        
        if not rows:
            raise ValidationError("CSV file is empty")
        
        if operation == "validate":
            return await _validate_csv(rows)
        elif operation == "summary":
            return await _generate_summary(rows)
        elif operation == "transform":
            return await _transform_csv(rows)
        else:
            raise ValidationError(f"Unknown operation: {operation}")
    
    except Exception as e:
        raise ValidationError(f"CSV processing failed: {str(e)}")

async def _validate_csv(rows: list) -> Dict[str, Any]:
    """Validate CSV structure."""
    return {
        "validation_status": "passed",
        "total_rows": len(rows),
        "columns": list(rows[0].keys()) if rows else [],
        "has_empty_cells": any('' in row.values() for row in rows),
        "message": "CSV validation completed"
    }

async def _generate_summary(rows: list) -> Dict[str, Any]:
    """Generate CSV summary."""
    return {
        "summary": {
            "total_records": len(rows),
            "columns": list(rows[0].keys()) if rows else [],
            "first_row": rows[0] if rows else {},
            "sample_rows": rows[:5] if len(rows) > 5 else rows
        }
    }

async def _transform_csv(rows: list) -> Dict[str, Any]:
    """Transform CSV data."""
    # Simple transformation: add row numbers and compute row size
    transformed = []
    for idx, row in enumerate(rows, 1):
        transformed.append({
            "row_number": idx,
            "data": row,
            "field_count": len(row)
        })
    
    return {
        "transformed_rows": transformed[:10],  # Return first 10
        "total_transformed": len(transformed),
        "message": "CSV transformation completed"
    }
