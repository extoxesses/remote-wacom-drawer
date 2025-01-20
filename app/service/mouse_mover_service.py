from pyautogui import mouseUp, mouseDown, moveTo, size

from app import logging

class MouseMoverService :
    _instance = None
    _logger = logging.getLogger(__name__)
    _last_button = { 'value': 0, 'name': None }

    def __init__(self) :
        if MouseMoverService._instance is not None:
            raise Exception("This class is a singleton!")
        self._logger.debug('WebsocketService initialized')
        MouseMoverService._instance = self

    @classmethod
    def instance(cls) -> 'MouseMoverService' :
        if cls._instance is None :
            cls._instance = MouseMoverService()
        return cls._instance

    async def move_mouse(self, x : int, y : int, button : int) -> None :
        moveTo(x, y)
        self.click(button)

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

    def click(self, button : str) -> None :
        #self._logger.debug(f'===================')
        #self._logger.debug(f'Button: {button} with last_button: {self._last_button}/{self._last_button['name']}')
        if button != self._last_button['value'] :
            self._logger.debug(f'Button changed from {self._last_button['value']} to {button}')
            match button :
                case 0:
                    mouseUp(button=self._last_button['name'])
                    self._last_button['name'] = None
                case 1:
                    mouseDown(button='left')
                    self._last_button['name'] = 'left'
                case 2:
                    mouseDown(button='right')
                    self._last_button['name'] = 'right'
                case _:
                    self.logger.warning(f'Unknown button {button}')

            self._last_button['value'] = button
        #self._logger.debug(f'-------------------')

            # if button == 0 :
            #     self._logger.debug(f'mouseUp {self._last_button_name}')
            #     mouseUp(button=self._last_button_name)
            #     self._last_button = 0
            #     self._last_button_name = None
            # if button == 1 :
            #     mouseDown(button='left')
            #     self._last_button = 1
            #     self._last_button_name = 'left'
            #     self._logger.debug('mouseDown left')
            # elif button == 2 :
            #     mouseDown(button='right')
            #     self._last_button = 2
            #     self._last_button_name = 'right'
            #     self._logger.debug('mouseDown right')