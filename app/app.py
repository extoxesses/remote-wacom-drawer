import logging
import math
import os
import socketio
import sys

from dotenv import load_dotenv
from pyautogui import click, moveTo, size
from typing import Tuple, List

from commons.events import DrawerEvent, CalibrationEvent
from commons.topic import TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION

# App configurations
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# App global state
load_dotenv()
sio = socketio.Client()
scale_factor = { 'x': 1.0, 'y': 1.0 }

# Add these variables after existing globals
last_position = {'x': 0, 'y': 0, 'button': 0}
INTERPOLATION_STEPS = 10  # Adjust based on needed smoothness

def interpolate_points(start_x: int, start_y: int, end_x: int, end_y: int, steps: int) -> List[Tuple[int, int]]:
    """Generate intermediate points between two coordinates"""
    points = []
    
    for i in range(steps + 1):
        t = i / steps
        x = round(start_x + (end_x - start_x) * t)
        y = round(start_y + (end_y - start_y) * t)
        points.append((x, y))
    
    return points







# Define event handlers
@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on(TOPIC_POSITION)
def position(event):
    point_event = DrawerEvent.from_dict(event).point
    xa = round(point_event.x * scale_factor['x'])
    ya = round(point_event.y * scale_factor['y'])

    logger.debug('Position event received:')
    logger.debug(f'--- Position data from server: {point_event}')
    logger.debug(f'--- Scale factors: {scale_factor}')
    logger.debug(f'--- Rebalanced data: {xa}, {ya}')

    # moveTo(xa, ya)

    # Temo che per non fare casino, la cosa più bella sarebbe:
    #  - leggere i messaggi dal topic
    #  - metterli in una coda
    #  - processare la coda in un thread separato dal websocket
    #  - fare il moveTo() in quel thread
    # In questo modo dovrei riuscire ad essere più smooth nel movimento del mouse

    # Prima di fare sta cosa, però, provare a gestire il mouseup - mousedown per vedere
    # se il problema non sia solo del click, e se il software si gestisce tutto da solo
    # (cosa che dubito)

    if last_position['x'] == 0 and last_position['y'] == 0:
        moveTo(xa, ya)
        last_position['x'] = xa
        last_position['y'] = ya
    else :
        # Generate interpolated points
        points = interpolate_points(
            last_position['x'], 
            last_position['y'], 
            xa, 
            ya, 
            round(math.sqrt(scale_factor['x']**2 + scale_factor['y']**2))
        )

        for x, y in points:
            logger.debug(f'Moving to {x}, {y}')
            moveTo(x, y)

        last_position['x'] = xa
        last_position['y'] = ya

    logger.debug(f'--- Last position: {last_position}') 

    # va gestita meglio la storia del mouseup - mousedown, altrimenti sono n-mila click invece che un "keep"
    if point_event.button == 1:
        click(button='left')
    elif point_event.button == 2:
        click(button='right')

@sio.on(TOPIC_SCREEN_CALIBRATION)
def screen_calibration(event):
    drawer_size = CalibrationEvent.from_dict(event).screen_size
    screen_size = size()
    scale_factor['x'] = screen_size.width / drawer_size.width
    scale_factor['y'] = screen_size.height / drawer_size.height

    logger.debug('Screen calibration event received:')
    logger.debug(f'--- Drawer size: {drawer_size}')
    logger.debug(f'--- Screen size: {screen_size}')
    logger.debug(f'--- Scale factor: {scale_factor}')

# Start application
try:
    host = os.getenv('HOST')
    logger.info(f'Connecting to server at {host}')
    sio.connect(host)
    while True:
        try:
            sio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received Ctrl+C, shutting down...")
            sio.disconnect()
            sys.exit(0)
except Exception as e:
    logger.error(f"Connection error: {e}")
    sys.exit(1)