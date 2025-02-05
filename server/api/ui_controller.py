from flask import make_response, render_template

from server import app, DRAWER_BTN, ERASER_BTN
from server.models.enroll_api import EnrollRole
from server.service import sessionService

# This endpoint exposes the drawer UI to the user.
# [GET] /api/v1/drawer
# Returns: HTML page with the drawer UI.
@app.route('/api/v1/drawer', methods=['GET'])
def drawer():
    api_key = sessionService.create_api_key()
    response = make_response(render_template('drawer.html', drawer_button=DRAWER_BTN, eraser_button=ERASER_BTN))
    response.set_cookie('x-api-key', str(api_key))
    return response

@app.route('/api/v1/view', methods=['GET'])
def display():
    # TODO: sistemare bene sta parte
    return render_template('viewer.html', drawer_button=DRAWER_BTN, eraser_button=ERASER_BTN)
