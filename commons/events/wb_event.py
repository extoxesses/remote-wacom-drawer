import datetime
from dataclasses import dataclass

@dataclass
class PointEvent :
    x : int
    y : int
    button : int

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