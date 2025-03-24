import json
from flask import request
from flask_socketio import emit, join_room

from server import logging, redis_connection, server_config, socketio
from server.config.redis_fields import *
from server.models import EnrollRequest, EnrollRole
from commons.events import CalibrationEvent
from commons.utils import get_room_from_cookie
from commons.topic import TOPIC_SCREEN_CALIBRATION, TOPIC_ROOM_AUTH

logger = logging.getLogger(__name__)

def broadcast_on_room(topic : str, event, include_self=False) -> None :
    # Qua portarsi dentro la logica di gestione delle room
    room = get_room_from_cookie(request)
    emit(topic, event, to=room, broadcast=True, include_self=include_self)

def on_connect(connection_request: EnrollRequest) -> None:
    logger.info(f'Client \'{connection_request.api_key}\' requires to connect to websocket channel')
    room_id = connection_request.api_key

    if connection_request.role == EnrollRole.DRAWER:
        enroll_drawer(room_id)
        
    elif connection_request.role == EnrollRole.VIEWER:
        enroll_viewer(connection_request)

    else:
        raise ValueError(f'Invalid role {connection_request.role} for enrolling client')
    
    join_room(room_id)
    logger.info(f'Client \'{connection_request.api_key}\' connected')

def on_disconnect(reason: str) -> None :
    logger.info(f'Client disconnected due reason: {reason}')

def on_client_disconnect(data: dict) -> None:
    logger.info(f"User disconnected: {data.get('username', 'unknown')}")
    emit('room/leave', data, broadcast=False)

def update_drawer_screen_size(event: CalibrationEvent) -> None:
    room_id = get_room_from_cookie(request)
    redis_connection.hset(room_id, mapping={
        REDIS_DRAWER_SCREEN_SIZE: event.screen_size.model_dump_json()
    })


def enroll_drawer(room_id: str) -> None :
    # In case of drawer connection, redis entry must be updated and drawer must be added to the room.
    # In reconnection scenario, the 'leave_room' is called during disconnection phase.
    redis_connection.hset(room_id, mapping={
        REDIS_DRAWER_SID: request.sid,
        REDIS_VIEWERS_SIDS: '[]',
        REDIS_DRAWER_SCREEN_SIZE: '{}'
    })
    redis_connection.pexpire(room_id, server_config.redis.expiration_time)
        
def enroll_viewer(connection_request: EnrollRequest) -> None:
    # Verify drawer exists
    room_id = connection_request.api_key
    drawer_sid = redis_connection.hget(room_id, REDIS_DRAWER_SID)
    if not drawer_sid:
        raise ValueError(f'No active drawer found for room {room_id}')
    drawer_sid = drawer_sid.decode("utf-8")
    
    try:
        # Send authentication request and wait for response
        auth_response = socketio.call(TOPIC_ROOM_AUTH,
            {'request': 'authenticate'},
            room=drawer_sid,
            timeout=5.0
        )
        if not auth_response or auth_response.get('apiSecret', None) is None:
            raise ValueError('Viewer authentication rejected by drawer')
        elif auth_response.get('apiSecret', None) != connection_request.api_secret:
            raise ValueError('Invalid api-secret provided!')

        # Get current screen size and viewer list
        screen_size_data = redis_connection.hget(room_id, REDIS_DRAWER_SCREEN_SIZE)
        screen_size = json.loads(screen_size_data) if screen_size_data else {}
        
        viewers_data = redis_connection.hget(room_id, REDIS_VIEWERS_SIDS)
        viewers = json.loads(viewers_data.decode("utf-8")) if viewers_data else []
        
        # Add new viewer
        viewers.append(request.sid)
        redis_connection.hset(room_id, mapping={REDIS_VIEWERS_SIDS: json.dumps(viewers)})
        
        # Send screen calibration if available
        if screen_size:
            emit(TOPIC_SCREEN_CALIBRATION, {'screen_size': screen_size}, to=request.sid)
            
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f'Error processing room data: {e}')
        raise ValueError('Invalid room data format')
    except TimeoutError:
        logger.error('Authentication request timed out')
        raise ValueError('Authentication request timed out')
    except Exception as e:
        logger.error(f'Errore generico: {e}')


__all__ = [
    'broadcast_on_room',
    'on_connect',
    'on_disconnect',
    'on_client_disconnect',
    'update_drawer_screen_size'
]