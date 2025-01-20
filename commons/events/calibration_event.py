import datetime
from dataclasses import dataclass

@dataclass
class ScreenSize :
    width : int
    height : int
        
    @classmethod
    def from_dict(cls, data : dict) -> 'ScreenSize':
        return cls(**data)

@dataclass
class CalibrationEvent :
    screen_size : ScreenSize
    client : str
    timestamp : datetime
        
    @classmethod
    def from_dict(cls, data : dict) -> 'CalibrationEvent':
        return cls(ScreenSize.from_dict(data['screen_size']), data['client'], data['timestamp'])