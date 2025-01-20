from app import sio, logging, point_queue
from app import websocketService
from commons.topic import TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION
from commons.events import DrawerEvent, CalibrationEvent

logger = logging.getLogger(__name__)

# Define event handlers
@sio.event
async def connect():
    await websocketService.on_connect()

@sio.event
async def disconnect():
    await websocketService.on_disconnect()

@sio.on(TOPIC_POSITION)
async def position(event):
    # await websocketService.on_position(DrawerEvent.from_dict(event))
    point_queue.put_nowait(DrawerEvent.from_dict(event))

@sio.on(TOPIC_SCREEN_CALIBRATION)
async def screen_calibration(event):
    await websocketService.on_screen_calibration(CalibrationEvent.from_dict(event))
