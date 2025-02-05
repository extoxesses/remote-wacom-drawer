from server import app, socketio, PORT, DEBUG

if __name__ == '__main__':
    debug = DEBUG.lower() == 'true'
    socketio.run(app, host='0.0.0.0', port=PORT, debug=debug)
