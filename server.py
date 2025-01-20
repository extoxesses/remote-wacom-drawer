from server import app, socketio, HOST_PORT, DEBUG

if __name__ == '__main__':
    debug = DEBUG.lower() == 'true'
    socketio.run(app, host='0.0.0.0', port=HOST_PORT, debug=debug)
