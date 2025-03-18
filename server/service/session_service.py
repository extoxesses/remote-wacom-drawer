import base64, random, string
from flask import session
from server import logging

class SessionService :
    logger = logging.getLogger(__name__)
    
    def __init__(self) :
        pass

    def create_api_key(self) -> str:
        self.logger.info('Creating new random keys for drawer...')
        drawer_id = ''.join(random.choices(string.digits, k=12))
        if 'api-key' in session.keys() is not None:
            self.logger.info('Refreshing drawer keys...')
            drawer_id = session['api-key']
        else:
            session['api-key'] = drawer_id
        
        # "decode()" statement is required to convert the byte-array to string (and remove the `b'...'` wrapper)
        return base64.b64encode(bytes(drawer_id, 'utf-8')).decode('utf-8')
