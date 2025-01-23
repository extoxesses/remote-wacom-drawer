from pyautogui import mouseDown, mouseUp, moveTo, size

from app import logging, SERVER
from commons.events import CalibrationEvent, DrawerEvent, PointEvent


class WebsocketService :
    _instance = None
    _logger = logging.getLogger(__name__)
    _buttons_map = { 0 : None, 1 : 'left', 2 : 'right' }

    _scale_factor_x = 1.0
    _scale_factor_y = 1.0

    def __init__(self) :
        if WebsocketService._instance is not None:
            raise Exception("This class is a singleton!")
        self._logger.debug('WebsocketService initialized')
        WebsocketService._instance = self

    @classmethod
    def instance(cls) -> 'WebsocketService' :
        if cls._instance is None :
            cls._instance = WebsocketService()
        return cls._instance
    
    def on_connect(self) -> None :
        self._logger.info(f'Client connected to server {SERVER}')

    def on_disconnect(self) -> None :
        self._logger.info(f'Client disconnected from server {SERVER}')

    def on_position(self, event : DrawerEvent) -> None :
        x, y = self.rescale_points(event.point)
        moveTo(x, y)

    def on_screen_calibration(self, event : CalibrationEvent) -> None :
        screen_size = size()
        self._scale_factor_x = screen_size.width / event.screen_size.width
        self._scale_factor_y = screen_size.height / event.screen_size.height

    def on_click(self, event : DrawerEvent) -> None :
        button = self._buttons_map[event.button]
        if button is not None :
            mouseDown()
        else :
            mouseUp()

    def rescale_points(self, point : PointEvent) -> int :
        return round(point.x * self._scale_factor_x), round(point.y * self._scale_factor_y)
