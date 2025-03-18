from flask import request
from flask_socketio import emit, join_room

from server import logging, redis_connection
from server.models import EnrollRequest, EnrollRole
from commons.utils import get_room_from_cookie

logger = logging.getLogger(__name__)

def on_connect(connection_request : EnrollRequest) -> None :
    logger.info(f'Client \'{connection_request.api_key}\' requires to connect to websocket channel')
    room_id = connection_request.api_key

    if connection_request.role == EnrollRole.DRAWER.value:
        # In case of drawer connection, redis entry must be updated and drawer must be added to the room.
        # In reconnection scenario, the 'leave_room' is called during disconnection phase.
        redis_connection.hset(room_id, mapping={
            'drawer': request.sid
        })
        redis_connection.pexpire(room_id, 3600000) # TODO: da rendere configurabile
        
    elif connection_request.role == EnrollRole.VIEWER.value:
        room_id = connection_request.api_key
        # TODO: implementare "autenticazione" con il drawer
        #self.add_viewer_to_room(room_id, session_id)

    else:
        #self.logger.error(f'Invalid role {request.role} for enrolling client')
        raise ValueError(f'Invalid role {connection_request.role} for enrolling client')
    
    join_room(room_id)
    logger.info(f'Client \'{connection_request.api_key}\' connected')

def on_disconnect(reason: str) -> None :
    logger.info('Client disconnected due reason:', reason)

def on_client_disconnect(data: str) -> None :
    logger.info(f'User disconnected: {data['username']}')
    emit('room/leave', data, broadcast=False)

def broadcast_on_room(topic : str, event, include_self=False) -> None :
    # Qua portarsi dentro la logica di gestione delle room
    room = get_room_from_cookie(request)
    emit(topic, event, to=room, broadcast=True, include_self=include_self)

def create_room(room_id : str) -> None :
    join_room(room_id, sid=room_id, namespace='remote-drawer')
