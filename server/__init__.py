import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='../resources/templates', static_folder='../resources/static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

load_dotenv()

# Server config
HOST_IP = os.getenv('HOST_IP')
HOST_PORT = os.getenv('HOST_PORT')
DEBUG = os.getenv('DEBUG', 'False')

# App config
BUTTON = os.getenv('BUTTON')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


with app.app_context():
    from .api import base_controller
    from .api import websocket_api
