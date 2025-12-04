import json
import xml.etree.ElementTree as ET
import csv
import io
from typing import Any, Dict
from app.core.errors import ValidationError

async def convert_format(
    source_format: str,
    target_format: str,
    data: str
) -> Dict[str, Any]:
    """Convert data between formats."""
    try:
        # Parse source format
        if source_format == "json":
            parsed_data = json.loads(data)
        elif source_format == "csv":
            parsed_data = _parse_csv(data)
        elif source_format == "xml":
            parsed_data = _parse_xml(data)
        else:
            raise ValidationError(f"Unsupported source format: {source_format}")
        
        # Convert to target format
        if target_format == "json":
            converted = json.dumps(parsed_data, indent=2)
        elif target_format == "csv":
            converted = _to_csv(parsed_data)
        elif target_format == "xml":
            converted = _to_xml(parsed_data)
        else:
            raise ValidationError(f"Unsupported target format: {target_format}")
        
        return {
            "source_format": source_format,
            "target_format": target_format,
            "converted_data": converted,
            "conversion_status": "success"
        }
    
    except Exception as e:
        raise ValidationError(f"Format conversion failed: {str(e)}")

def _parse_csv(data: str) -> Dict[str, Any]:
    """Parse CSV string to dict."""
    reader = csv.DictReader(io.StringIO(data))
    return {"rows": list(reader)}

def _parse_xml(data: str) -> Dict[str, Any]:
    """Parse XML string to dict."""
    root = ET.fromstring(data)
    return {"root": _xml_to_dict(root)}

def _xml_to_dict(elem):
    """Convert XML element to dict."""
    result = {elem.tag: {} if elem.attrib else None}
    children = list(elem)
    if children:
        dd = {}
        for child in children:
            cd = _xml_to_dict(child)
            for k, v in cd.items():
                dd[k] = v
        result = {elem.tag: dd}
    elif elem.text:
        result[elem.tag] = elem.text
    return result

def _to_csv(data: Dict[str, Any]) -> str:
    """Convert dict to CSV."""
    if "rows" in data:
        rows = data["rows"]
        if not rows:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()
    
    return json.dumps(data)

def _to_xml(data: Dict[str, Any]) -> str:
    """Convert dict to XML."""
    def build_xml(tag, value):
        elem = ET.Element(tag)
        if isinstance(value, dict):
            for k, v in value.items():
                elem.append(build_xml(k, v))
        else:
            elem.text = str(value)
        return elem
    
    root = build_xml("root", data)
    return ET.tostring(root, encoding='unicode')