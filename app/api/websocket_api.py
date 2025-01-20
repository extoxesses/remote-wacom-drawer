from app import sio, logging
from app.service import websocketService
from commons.topic import TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION
from commons.events import DrawerEvent, CalibrationEvent

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
    websocketService.on_position(DrawerEvent.from_dict(event))

@sio.on(TOPIC_SCREEN_CALIBRATION)
def screen_calibration(event):
    websocketService.on_screen_calibration(CalibrationEvent.from_dict(event))
