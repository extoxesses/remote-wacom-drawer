from flask_socketio import send, emit

from server import logging, socketio
from server.service import websocketService
from commons.events import DrawerEvent, CalibrationEvent
from commons.topic import TOPIC_CONNECT, TOPIC_DISCONNECT, TOPIC_CLIENT_DISCONNECTING, TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION

logger = logging.getLogger(__name__)


###########################
# Base events handlers    #
###########################

@socketio.on(TOPIC_CONNECT)
def connect_handler(auth) -> None :
    websocketService.on_connect(auth)
    
@socketio.on(TOPIC_DISCONNECT)
def disconnect_handler(reason) -> None :
    websocketService.on_disconnect(reason)



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
    websocketService.on_client_disconnect(data)

@socketio.on('display')
def handle_message(msg) -> None :
    print('Message: ' + msg)
    send(msg, broadcast=True)


@socketio.on(TOPIC_POSITION)
def handle_position(event : DrawerEvent) -> None :
    logger.debug(f'[Event: position] Incoming message {event}')
    websocketService.broadcast_on_room(TOPIC_POSITION, event)

@socketio.on(TOPIC_SCREEN_CALIBRATION)
def handle_calibration(event : CalibrationEvent) -> None :
    logger.debug(f'[Event: screen/calibration] Incoming message {event}')
    websocketService.broadcast_on_room(TOPIC_SCREEN_CALIBRATION, event)

@socketio.on('mouseclick') # TODO sistemare
def handle_calibration(event) -> None :
    logger.debug(f'[Event: mouseclick] Incoming message {event}')
    websocketService.broadcast_on_room('mouseclick', event)