from pyautogui import mouseUp, mouseDown, moveTo, size
from queue import Queue

from app import logging, mouseMoverService, SERVER
from commons.events import DrawerEvent, CalibrationEvent


class WebsocketService :
    _instance = None
    _last_button = 0
    _last_button_name = None
    _logger = logging.getLogger(__name__)
    _point_queue = None
    _scale_factor = { 'x': 1.0, 'y': 1.0 }

    def __init__(self, point_queue) :
        if WebsocketService._instance is not None:
            raise Exception("This class is a singleton!")
        self._logger.debug('WebsocketService initialized')
        WebsocketService._instance = self
        self._point_queue = point_queue

    @classmethod
    def instance(cls, point_queue) -> 'WebsocketService' :
        if cls._instance is None :
            cls._instance = WebsocketService(point_queue)
        return cls._instance
    
    async def on_connect(self) -> None :
        self._logger.info(f'Connected to server {SERVER}')

    async def on_disconnect(self) -> None :
        self._logger.info(f'Disconnected from server {SERVER}')

    # async def on_position(self, event : DrawerEvent) -> None :
    async def on_position(self) -> None :
        event = await self._point_queue.get
        x = self.rescale_point(event.point.x, 'x')
        y = self.rescale_point(event.point.y, 'y')
        await mouseMoverService.move_mouse(x, y, event.point.button)
        #self._point_queue.put((x, y, event.point.button))

    async def on_screen_calibration(self, event : CalibrationEvent) -> None :
        screen_size = size()
        self._scale_factor['x'] = screen_size.width / event.screen_size.width
        self._scale_factor['y'] = screen_size.height / event.screen_size.height

    def rescale_point(self, point : int, coordinate : str) -> int :
        return round(point * self._scale_factor[coordinate])