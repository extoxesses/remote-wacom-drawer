from server import logging, socketio
from server.service import websocket_service
from commons.events import DrawerEvent, MouseClickEvent, CalibrationEvent
from commons.topic import *

from server.models import EnrollRequest

logger = logging.getLogger(__name__)

###########################
# Base events handlers    #
###########################

@socketio.on(TOPIC_CONNECT)
def connect_handler(auth : EnrollRequest) -> None :
    websocket_service.on_connect(EnrollRequest.from_dict(auth))
    
@socketio.on(TOPIC_DISCONNECT)
def disconnect_handler(reason) -> None :
    websocket_service.on_disconnect(reason)

###########################
# Service events handlers #
###########################

@socketio.on(TOPIC_CLIENT_DISCONNECTING)
def client_disconnect_handler(data) -> None :
    websocket_service.on_client_disconnect(data)

@socketio.on(TOPIC_SCREEN_CALIBRATION)
def handle_calibration(event: CalibrationEvent) -> None:
    logger.debug(f'[Event: {TOPIC_SCREEN_CALIBRATION}] Incoming message {event}')
    websocket_service.update_drawer_screen_size(CalibrationEvent.from_dict(event))
    websocket_service.broadcast_on_room(TOPIC_SCREEN_CALIBRATION, event)

@socketio.on(TOPIC_MOUSE_MOVE)
def handle_position(event : DrawerEvent) -> None :
    logger.debug(f'[Event: {TOPIC_MOUSE_MOVE}] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_MOUSE_MOVE, event)

@socketio.on(TOPIC_MOUSE_CLICK)
def handle_mouse_click(event: MouseClickEvent) -> None:
    logger.debug(f'[Event: {TOPIC_MOUSE_CLICK}] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_MOUSE_CLICK, event)


@socketio.on(TOPIC_ACTION_CLEAN)
def handle_clean_action(event : str) -> None :
    logger.debug(f'[Event: {TOPIC_ACTION_CLEAN}] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_ACTION_CLEAN, event)
