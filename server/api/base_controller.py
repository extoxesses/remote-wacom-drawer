from server import app, HOST_IP, HOST_PORT, BUTTON

from flask import render_template

@app.route('/api/v1/draw', methods=['GET'])
def draw():
    # TODO: sistemare bene sta parte
    return render_template('drawer.html', ip=HOST_IP, port=HOST_PORT, drawer_button=BUTTON)

@app.route('/api/v1/view', methods=['GET'])
def display():
    # TODO: sistemare bene sta parte
    return render_template('viewer.html', ip=HOST_IP, port=HOST_PORT, drawer_button=BUTTON)
