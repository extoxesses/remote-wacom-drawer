from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class PointEvent(BaseModel):
    x: int
    y: int

class DrawerEvent(BaseModel):
    client: str
    point: PointEvent
    timestamp: datetime

class MouseClickEventType(Enum):
    MOUSE_DOWN = 'mousedown'
    MOUSE_UP = 'mouseup'
    TOUCH_START = 'touchstart'
    TOUCH_END = 'touchend'

class MouseClickButtonType(Enum):
    PRIMARY = 'primary'
    AUXILIARY = 'middle'
    SECONDARY = 'secondary'

class MouseClickEvent(BaseModel):
    event: MouseClickEventType
    button: MouseClickButtonType
    client: str
    timestamp: datetime
