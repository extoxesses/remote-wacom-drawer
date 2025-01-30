from app import sio, logging
from app import websocketService
from commons.topic import TOPIC_MOUSE_CLICK, TOPIC_MOUSE_MOVE, TOPIC_SCREEN_CALIBRATION
from commons.events import DrawerEvent, CalibrationEvent, MouseClickEvent

logger = logging.getLogger(__name__)

# Define event handlers
@sio.event
def connect():
    websocketService.on_connect()

@sio.event
def disconnect():
    websocketService.on_disconnect()

@sio.on(TOPIC_MOUSE_MOVE)
def position(event):
    drawerEvent = DrawerEvent.from_dict(event)
    websocketService.on_mouse_move(drawerEvent)

@sio.on(TOPIC_SCREEN_CALIBRATION)
def screen_calibration(event):
    print(event)
    calibrationEvent = CalibrationEvent.from_dict(event)
    websocketService.on_screen_calibration(calibrationEvent)

@sio.on(TOPIC_MOUSE_CLICK)
def mouseclick(event):
    mouseClickEvent = MouseClickEvent.from_dict(event)
    websocketService.on_mouse_click(mouseClickEvent)
