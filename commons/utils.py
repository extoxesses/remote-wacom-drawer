import base64
import logging
from typing import Optional

def get_room_from_cookie(request) -> Optional[str]:
    """
    Extract and decode room information from request cookie.
    
    Args:
        request: The incoming request object containing cookies
        
    Returns:
        str: Decoded room identifier in format 'room:{room_id}'
        None: If cookie is missing or invalid
    """
    try:
        # Get cookie value, return None if not present
        api_key = request.cookies.get("x-api-key")
        if not api_key:
            return None
            
        # Decode base64 and convert to string
        room_bytes = base64.b64decode(api_key)
        return room_bytes.decode('utf-8')

    except (KeyError, base64.binascii.Error, UnicodeDecodeError) as e:
        # Handle any decoding/encoding errors
        logging.error(f"Error extracting room from cookie: {str(e)}")
        return None

__all__ = [
    'get_room_from_cookie'
]