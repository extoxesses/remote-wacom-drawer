This project is a python-based application that allows to use old tablets (possibily with dedicated pen) as a drawing tablet for your computer.
The application is composed by a server and two clients:
- a remote viewer via browser
- a desktop client to move the mouse and simulate the pen input

The application uses WebSockets to communicate the input events and exposes a simple webserver to reach pages.

## Components

1. **Server** and **web viewer** ([server.py](server.py))
   - Server Flask/SocketIO that handles WebSocket connections and event routing
   - Uses Redis for session management and MongoDB for data persistence
   - Handles rooms for drawer/viewer connections
   - Implemented in Python using Flask and Flask-SocketIO

2. **Drawing Client** ([app.py](app.py))
   - Python client that captures tablet/stylus input
   - Uses pyautogui to simulate mouse movements
   - Connects to the server via WebSocket
   - Handles screen calibration between different display sizes
