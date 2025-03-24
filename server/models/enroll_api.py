from enum import Enum
from pydantic import BaseModel

class EnrollRole(Enum):
    DRAWER = 'drawer'
    VIEWER = 'viewer'
    EMULATOR = 'emulator'

class EnrollRequest(BaseModel):
    api_key: str
    api_secret: str
    role: EnrollRole

    # If you need to maintain the same field names as in the original
    class Config:
        alias_generator = lambda x: x.replace('_', '-')
        allow_population_by_field_name = True

class EnrollResponse(BaseModel):
    session_id: str
