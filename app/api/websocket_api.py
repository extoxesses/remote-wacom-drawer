from app import sio, logging
from app import websocketService
from commons.topic import TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION
from commons.events import DrawerEvent, CalibrationEvent

from pyautogui import mouseDown, mouseUp

logger = logging.getLogger(__name__)

# Define event handlers
@sio.event
def connect():
    websocketService.on_connect()

@sio.event
def disconnect():
    websocketService.on_disconnect()

@sio.on(TOPIC_POSITION)
def position(event):
    # print(event)
    drawerEvent = DrawerEvent.from_dict(event)
    websocketService.on_position(drawerEvent)

@sio.on(TOPIC_SCREEN_CALIBRATION)
def screen_calibration(event):
    calibrationEvent = CalibrationEvent.from_dict(event)
    websocketService.on_screen_calibration(calibrationEvent)

@sio.on('mouseclick')
def mouseclick(event):
    print(event)
    action = event['event']
    button = event['button']

    if (action == 'mousedown') :
        mouseDown(button=button)
    else :
        mouseUp(button=button)