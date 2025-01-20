import logging
import os
# from queue import Queue
import socketio

from dotenv import load_dotenv
from threading import Thread

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# App global state
load_dotenv()
SERVER = f"ws://{os.getenv('HOST_IP', 'localhost')}:{os.getenv('HOST_PORT', '5000')}"
logger.info(f"Connecting to server {SERVER}")
DEBUG = os.getenv('DEBUG', 'False')

sio = socketio.AsyncClient()
# point_queue = Queue()
import asyncio
point_queue = asyncio.Queue()

from app.service.mouse_mover_service import MouseMoverService
mouseMoverService = MouseMoverService.instance()

from app.service.websocket_service import WebsocketService
websocketService = WebsocketService.instance(point_queue)

async def test() :
    while True:
        await websocketService.on_position()
        point_queue.task_done()

asyncio.create_task(test()) 

# from app.service.worker_service import WorkerService
# workerService = WorkerService.instance(point_queue)
# worker = Thread(target=workerService.process_events, daemon=True)

from .api import websocket_api
