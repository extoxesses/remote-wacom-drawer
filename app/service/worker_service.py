from queue import Queue

from app import logging, mouseMoverService

class WorkerService :
    _instance = None
    _logger = logging.getLogger(__name__)
    _point_queue = None

    def __init__(self, point_queue : Queue) :
        if WorkerService._instance is not None:
            raise Exception("This class is a singleton!")
        self._logger.debug('WebsocketService initialized')
        WorkerService._instance = self
        self._point_queue = point_queue

    @classmethod
    def instance(cls, point_queue : Queue) -> 'WorkerService' :
        if cls._instance is None :
            cls._instance = WorkerService(point_queue)
        return cls._instance

    def process_events(self):
        while True:
            event = self._point_queue.get()
            if event is None:
                break
                
            # self._point_queue.clear()
            try:
                x, y, button = event
                mouseMoverService.move_mouse(x, y, button)
            finally:
                self._point_queue.task_done()