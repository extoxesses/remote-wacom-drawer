import pyautogui
from pyautogui import click, moveTo, size

from app import logging, SERVER
from commons.events import DrawerEvent, CalibrationEvent

class WebsocketService :
    _instance = None
    logger = logging.getLogger(__name__)
    scale_factor = { 'x': 1.0, 'y': 1.0 }

    def __init__(self) :
        if WebsocketService._instance is not None:
            raise Exception("This class is a singleton!")
        self.logger.debug('WebsocketService initialized')
        WebsocketService._instance = self

    @classmethod
    def instance(cls):
        if cls._instance is None :
            cls._instance = WebsocketService()
        return cls._instance
    
    def on_connect(self) -> None :
        self.logger.info(f'Connected to server {SERVER}')

    def on_disconnect(self) -> None :
        self.logger.info(f'Disconnected from server {SERVER}')

    def on_position(self, event : DrawerEvent) -> None :
        rescaled_x = self.rescale_point(event.point.x, 'x')
        rescaled_y = self.rescale_point(event.point.y, 'y')
        moveTo(rescaled_x, rescaled_y)

        # Temo che per non fare casino, la cosa più bella sarebbe:
        #  - leggere i messaggi dal topic
        #  - metterli in una coda
        #  - processare la coda in un thread separato dal websocket
        #  - fare il moveTo() in quel thread
        # In questo modo dovrei riuscire ad essere più smooth nel movimento del mouse

        # Prima di fare sta cosa, però, provare a gestire il mouseup - mousedown per vedere
        # se il problema non sia solo del click, e se il software si gestisce tutto da solo
        # (cosa che dubito)

        # if last_position['x'] == 0 and last_position['y'] == 0:
        #     moveTo(xa, ya)
        #     last_position['x'] = xa
        #     last_position['y'] = ya
        # else :
        #     # Generate interpolated points
        #     points = interpolate_points(
        #         last_position['x'], 
        #         last_position['y'], 
        #         xa, 
        #         ya, 
        #         round(math.sqrt(scale_factor['x']**2 + scale_factor['y']**2))
        #     )

        #     for x, y in points:
        #         logger.debug(f'Moving to {x}, {y}')
        #         moveTo(x, y)

        #     last_position['x'] = xa
        #     last_position['y'] = ya

        # logger.debug(f'--- Last position: {last_position}') 

        # va gestita meglio la storia del mouseup - mousedown, altrimenti sono n-mila click invece che un "keep"
        # if point_event.button == 1:
        #     click(button='left')
        # elif point_event.button == 2:
        #     click(button='right')

    def on_screen_calibration(self, event : CalibrationEvent) -> None :
        screen_size = pyautogui.size()
        self.scale_factor['x'] = screen_size.width / event.screen_size.width
        self.scale_factor['y'] = screen_size.height / event.screen_size.height

    def rescale_point(self, point : int, coordinate : str) -> int :
        return round(point * self.scale_factor[coordinate])