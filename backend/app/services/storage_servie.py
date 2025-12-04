import os
import aiofiles
from pathlib import Path
from app.core.errors import StorageError
from app.config import get_settings

settings = get_settings()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class StorageService:
    """Handle file storage operations."""
    
    @staticmethod
    async def save_file(content: bytes, filename: str) -> str:
        """Save uploaded file."""
        try:
            # Security: sanitize filename
            filename = Path(filename).name
            filepath = UPLOAD_DIR / filename
            
            # Check file size
            if len(content) > settings.max_upload_size:
                raise StorageError(f"File size exceeds limit: {settings.max_upload_size} bytes")
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(content)
            
            return str(filepath)
        except Exception as e:
            raise StorageError(f"Failed to save file: {str(e)}")
    
    @staticmethod
    async def read_file(filepath: str) -> bytes:
        """Read file content."""
        try:
            async with aiofiles.open(filepath, 'rb') as f:
                return await f.read()
        except Exception as e:
            raise StorageError(f"Failed to read file: {str(e)}")
    
    @staticmethod
    async def delete_file(filepath: str) -> None:
        """Delete file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            raise StorageError(f"Failed to delete file: {str(e)}")

storage_service = StorageService()