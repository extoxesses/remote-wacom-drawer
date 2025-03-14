from server import app, socketio, server_config

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=server_config.webserver.port)
