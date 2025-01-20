from flask_socketio import emit
from server import logging
from commons.events import DrawerEvent, CalibrationEvent

class WebsocketService :
    logger = logging.getLogger(__name__)
    _instance = None
    _rooms = {}
    
    def __init__(self) :
        if WebsocketService._instance is not None:
            raise Exception("This class is a singleton!")
        self.logger.debug('WebsocketService initialized')
        WebsocketService._instance = self

    @classmethod
    def instance(cls):
        if cls._instance is None :
            cls._instance = WebsocketService()
        return cls._instance

    def on_connect(self, auth : dict) -> None :
        self.logger.debug('Client connected')
    
    def on_disconnect(self, reason: str) -> None :
        self.logger.debug('Client disconnected due reason:', reason)

    def on_client_disconnect(self, data: str) -> None :
        self.logger.info(f'User disconnected: {data['username']}')
        emit('room/leave', data, broadcast=False)
    
    #def on_position(self, event : DrawerEvent) -> None :
    #    # room = self.rooms.get(event.user, None)
    #    # if (room == None) :
    #    #     self.logger.critical(f'No room found for user {event.user}. Event will be dropped.')
    #    #     return
    #    # 
    #    # self.logger.info("Resend points to all users in drawer room")
    #    # event.user = None
    #    # emit('position', event, broadcast=False, room=room)
    #    emit('position', event, broadcast=True, include_self=False)

    #def on_screen_calibration(self, event : CalibrationEvent) -> None :
    #    emit('screen/calibration', event, broadcast=True, include_self=False)

    def broadcast_on_room(self, topic : str, event, include_self=False) -> None :
        # Qua portarsi dentro la logica di gestione delle room
        emit(topic, event, broadcast=True, include_self=include_self)