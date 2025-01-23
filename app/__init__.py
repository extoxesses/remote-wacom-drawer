import logging
import os
import socketio

from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# App global state
load_dotenv()
SERVER = f"ws://{os.getenv('HOST_IP', 'localhost')}:{os.getenv('HOST_PORT', '5000')}"
DEBUG = os.getenv('DEBUG', 'False')

sio = socketio.Client()

from app.service.websocket_service import WebsocketService
websocketService = WebsocketService.instance()

from .api import websocket_api
