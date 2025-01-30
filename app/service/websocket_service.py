from pyautogui import mouseDown, mouseUp, moveTo, size

from app import logging, SERVER
from commons.events import CalibrationEvent, DrawerEvent, PointEvent, MouseClickEvent, MouseClickEventType


class WebsocketService :
    _instance = None
    _logger = logging.getLogger(__name__)

    _screen_size = size()
    _scale_factor_x = 1.0
    _scale_factor_y = 1.0

    def __init__(self) :
        if WebsocketService._instance is not None:
            raise Exception('This class is a singleton!')
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

    def on_screen_calibration(self, event : CalibrationEvent) -> None :
        self._scale_factor_x = self._screen_size.width / event.screen_size.width
        self._scale_factor_y = self._screen_size.height / event.screen_size.height

    def on_mouse_click(self, event : MouseClickEvent) -> None :
        self._logger.debug(f'Mouse click event: {event}')
        match event.event:
            case MouseClickEventType.MOUSE_DOWN.value:
                mouseDown(button=event.button)
            case MouseClickEventType.MOUSE_UP.value:
                mouseUp(button=event.button)
            case MouseClickEventType.TOUCH_START.value:
                mouseDown(button=event.button)
            case MouseClickEventType.TOUCH_END.value:
                mouseUp(button=event.button)

    def on_mouse_move(self, event : DrawerEvent) -> None :
        x, y = self.rescale_points(event.point)
        moveTo(x, y)

    # Rescale the points to the screen size
    #
    # Rescaling uses (1) as minimum pixel value and screen size - 2 as maximum pixel value to avoid
    # to rise pyautogui.FailSafeException
    def rescale_points(self, point : PointEvent) -> int :
        x = max(1, min(round(point.x * self._scale_factor_x), self._screen_size.width - 2))
        y = max(1, min(round(point.y * self._scale_factor_y), self._screen_size.height - 2))
        return x, y
