import logging
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from redis import Redis
from server.config.settings import server_config

# load_dotenv()

# Configure Redis connection and active session
redis_connection = Redis(
    host=server_config.redis.host,
    port=server_config.redis.port
)
SESSION_TYPE = 'redis'
SESSION_REDIS = redis_connection
SESSION_PERMANENT = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE=None # TODO: Questo non funziona

# Start application
app = Flask(
    __name__,
    template_folder=server_config.webserver.templates_path,
    static_folder=server_config.webserver.statics_path
)
app.config.from_object(__name__)

# Logging settings
logging.basicConfig(
    level=server_config.logging.level,
    format=server_config.logging.pattern,
    datefmt=server_config.logging.date_format
)
logger = logging.getLogger(__name__)

# Session and CORS settings
CORS(app)
if (server_config.webserver.cors_allowed_origins == '*'):
    logger.warning("CORS_ALLOWED_ORIGINS is set to 'all'")
Session(app)

# SocketIO settings
socketio = SocketIO(app, cors_allowed_origins=server_config.webserver.cors_allowed_origins)

with app.app_context():
    from .api import ui_controller
    from .api import websocket_api
