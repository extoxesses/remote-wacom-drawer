from enum import Enum
import datetime
from dataclasses import dataclass

@dataclass
class PointEvent :
    x : int
    y : int

    @classmethod
    def from_dict(cls, data : dict) -> 'PointEvent':
        return cls(**data)

@dataclass
class DrawerEvent :    
    client : str
    point : PointEvent
    timestamp : datetime

    @classmethod
    def from_dict(cls, data : dict) -> 'DrawerEvent':
        return cls(data['client'], PointEvent.from_dict(data['point']), data['timestamp'])

class MouseClickEventType(Enum):
    MOUSE_DOWN = 'mousedown'
    MOUSE_UP = 'mouseup'
    TOUCH_START = 'touchstart'
    TOUCH_END = 'touchend'

class MouseClickButtonType(Enum):
    PRIMARY = 'primary'
    AUXILIARY = 'middle'
    SECONDARY = 'secondary'

@dataclass
class MouseClickEvent :
    event: MouseClickEventType
    button: MouseClickButtonType
    client: str
    timestamp: datetime

    @classmethod
    def from_dict(cls, data : dict) -> 'MouseClickEvent':
        return cls(**data)