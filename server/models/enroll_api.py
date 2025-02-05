from enum import Enum
from dataclasses import dataclass
from commons import BaseModel

class EnrollRole(Enum):
    DRAWER = 'drawer'
    VIEWER = 'viewer'
    EMULATOR = 'emulator'

@dataclass
class EnrollRequest :
    api_key: str
    api_secret: str
    role: EnrollRole

    @classmethod
    def from_dict(cls, data : dict) -> 'EnrollRequest':
        return cls(data['api-key'], data['api-secret'], data['role'])

@dataclass
class EnrollResponse(BaseModel):
    session_id: str

    @classmethod
    def from_dict(cls, data : dict) -> 'EnrollResponse':
        return cls(**data)
