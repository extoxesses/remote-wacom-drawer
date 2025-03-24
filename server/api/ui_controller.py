from flask import make_response, render_template

from server import app, server_config
from server.models.enroll_api import EnrollRole
from server.service import sessionService

drawer_button = server_config.app.drawer_button
eraser_button = server_config.app.eraser_button

@app.route('/', methods=['GET'])
def index():
    return make_response(render_template('index.html'))

@app.route('/api/v1/drawer', methods=['GET'])
def drawer():
    api_key = sessionService.create_api_key()
    response = make_response(render_template('drawer.html', drawer_button=drawer_button, eraser_button=eraser_button))
    response.set_cookie('x-api-key', str(api_key))
    return response

@app.route('/api/v1/viewer', methods=['GET'])
def display():
    return render_template('viewer.html', drawer_button=drawer_button, eraser_button=eraser_button)
