import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from redis import Redis
from os import getenv

load_dotenv()

redis_connection = Redis(host=getenv('REDIS_URL','localhost'), port=getenv('REDIS_PORT',6379))

SESSION_TYPE = 'redis'
SESSION_REDIS = redis_connection
SESSION_PERMANENT = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE=None # Questo non funziona

# Create application
app = Flask(__name__, template_folder='../resources/templates', static_folder='../resources/static')
app.config.from_object(__name__)

# Logging settings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# CORS settings
CORS(app)
CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', '*')
if (CORS_ALLOWED_ORIGINS == '*'):
    logger.warning("CORS_ALLOWED_ORIGINS is set to 'all'")

# Session settings
Session(app)

# SocketIO settings
socketio = SocketIO(app, cors_allowed_origins=CORS_ALLOWED_ORIGINS)

# Environment variables
PORT = getenv('PORT')
DEBUG = getenv('DEBUG', 'False')
DRAWER_BTN = getenv('DRAWER_BTN')
ERASER_BTN = getenv('ERASER_BTN')

with app.app_context():
    from .api import ui_controller
    from .api import websocket_api
