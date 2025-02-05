from server import logging, socketio
from server.service import websocket_service
from commons.events import DrawerEvent, MouseClickEvent, CalibrationEvent
from commons.topic import TOPIC_CONNECT, TOPIC_DISCONNECT, TOPIC_CLIENT_DISCONNECTING, TOPIC_MOUSE_CLICK, TOPIC_MOUSE_MOVE, TOPIC_SCREEN_CALIBRATION


from server.models import EnrollRequest, EnrollRole

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
# Room events management  #
###########################

# @socketio.on('room/join')
# def on_join(join_request : dict) -> None :
#     # TODO: rivedere le logiche on cui mettere in sicurezza la rejoin sulle room.
#     # Potrebbe essere figo generare un basic a partire da due dati generati dinamicamente
#     print(data)
#     # username = session['username']
#     # room = data['room']
#     # join_room(room)
#     # send(username + ' has entered the room.', to=room)
# 
# @socketio.on('room/leave')
# def on_leave(data) -> None :
#     print(data)
# #    username = data['username']
# #    room = data['room']
# #    leave_room(room)
# #    clients[request.sid] = {'username': None, 'room': None}
# #    socketio.emit('message', f'{username} has left the room.', room=room)



###########################
# Service events handlers #
###########################

@socketio.on(TOPIC_CLIENT_DISCONNECTING)
def client_disconnect_handler(data) -> None :
    websocket_service.on_client_disconnect(data)

@socketio.on(TOPIC_SCREEN_CALIBRATION)
def handle_calibration(event : CalibrationEvent) -> None :
    logger.debug(f'[Event: screen/calibration] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_SCREEN_CALIBRATION, event)

@socketio.on(TOPIC_MOUSE_MOVE)
def handle_position(event : DrawerEvent) -> None :
    logger.debug(f'[Event: mouse/move] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_MOUSE_MOVE, event)

@socketio.on(TOPIC_MOUSE_CLICK)
def handle_calibration(event : MouseClickEvent) -> None :
    logger.debug(f'[Event: mouse/click] Incoming message {event}')
    websocket_service.broadcast_on_room(TOPIC_MOUSE_CLICK, event)
