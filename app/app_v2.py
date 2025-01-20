import logging
import math
import os
import socketio
import sys

from dotenv import load_dotenv
from pyautogui import click, moveTo, size
from typing import Tuple, List

from queue import Queue
from threading import Thread, Event
import time

from commons.topic import TOPIC_POSITION, TOPIC_SCREEN_CALIBRATION
from commons.events import DrawerEvent, CalibrationEvent

# Add to global section
event_queue = Queue()
processing_done = Event()
processing_done.set()  # Initially set to True

# App configurations
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# App global state
load_dotenv()
sio = socketio.Client()
scale_factor = { 'x': 1.0, 'y': 1.0 }

def interpolate_points(start_x: int, start_y: int, end_x: int, end_y: int, steps: int) -> List[Tuple[int, int]]:
    """Generate intermediate points between two coordinates"""
    points = []
    
    for i in range(steps + 1):
        t = i / steps
        x = round(start_x + (end_x - start_x) * t)
        y = round(start_y + (end_y - start_y) * t)
        points.append((x, y))
    
    return points


def process_events():
    """Worker thread to process events sequentially"""
    while True:
        event = event_queue.get()
        if event is None:  # Poison pill to stop the worker
            break
            
        processing_done.clear()
        try:
            event_type, event_data = event
            if event_type == TOPIC_POSITION:
                handle_position_event(event_data)
            elif event_type == TOPIC_SCREEN_CALIBRATION:
                handle_screen_calibration(event_data)
        finally:
            processing_done.set()
            event_queue.task_done()

def handle_position_event(event):
    """Process position event"""
    point_event = DrawerEvent.from_dict(event).point
    xa = round(point_event.x * scale_factor['x'])
    ya = round(point_event.y * scale_factor['y'])

    points = interpolate_points (
        last_position['x'],
        last_position['y'],
        xa,
        ya,
            round(math.sqrt(scale_factor['x']**2 + scale_factor['y']**2))
    )

    for x, y in points:
        moveTo(x, y)
        time.sleep(0.001)  # Small delay between movements

    if point_event.button == 1:
        click(button='left')
    elif point_event.button == 2:
        click(button='right')

    last_position['x'] = xa
    last_position['y'] = ya

def handle_screen_calibration(event):
    """Process calibration event"""
    drawer_size = CalibrationEvent.from_dict(event).screen_size
    screen_size = size()
    scale_factor['x'] = screen_size.width / drawer_size.width
    scale_factor['y'] = screen_size.height / drawer_size.height

# Modify socket handlers to use queue
@sio.on(TOPIC_POSITION)
def position(event):
    event_queue.put((TOPIC_POSITION, event))

@sio.on(TOPIC_SCREEN_CALIBRATION)
def screen_calibration(event):
    event_queue.put((TOPIC_SCREEN_CALIBRATION, event))

# Start worker thread in main
try:
    host = os.getenv('HOST')
    logger.info(f'Connecting to server at {host}')
    
    # Start worker thread
    worker = Thread(target=process_events, daemon=True)
    worker.start()
    
    sio.connect(host)
    while True:
        time.sleep(0.1)  # Prevent CPU hogging
except KeyboardInterrupt:
    event_queue.put(None)  # Stop worker thread
    worker.join()
    sio.disconnect()