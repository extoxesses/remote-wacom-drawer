import datetime
from pydantic import BaseModel

class ScreenSize(BaseModel):
    width: int
    height: int

class CalibrationEvent(BaseModel):
    screen_size: ScreenSize
    client: str
    timestamp: datetime.datetime