const RANDOM_USER_KEY = 'authorization';

function connectToServer() {
    let serviceUrl = window.location.host;
    return io(`ws://${serviceUrl}`, {
        reconnectionDelayMax: 5000,
        auth: localStorage.getItem(RANDOM_USER_KEY)
    });
}

/**
 * This method is shared between the drawer and the viewer, and allows to set the common environment
 * of the two applications.
 *  
 * @param {*} socket WebSocket client
 */
function setSharedConfigurations() {

    let socket = connectToServer();
    resizeCanvas();

    socket.on('connect', () => {
        alert('Connected to server')
    });

    socket.on('disconnect', () => {
        alert('Disconnected from server')
    });

    window.addEventListener('resize', resizeCanvas);

    // window.addEventListener('resize', () => {
    //     const container = document.getElementById('drawingCanvasContainer');
    //     canvas.width = container.clientWidth;
    //     canvas.height = container.clientHeight;
    // });

    // Add event listeners for buttons
    document.getElementById('connectButton').addEventListener('click', () => {
        socket = connectToServer();
    });

    // document.getElementById('calibrateButton').addEventListener('click', calibrationCallback);

    return socket;

}

function drawOnCanvas(context, pressedButton, drawerFunction, drawerButton, eraserButton) {
    // TODO: qua potrebbe essere interessante dare la possibilità di dare una palete di colori per la penna in modalità "lavagna"
    if (pressedButton > 0) {
        if (pressedButton === drawerButton) {
            context.strokeStyle = 'black';
        } else if (pressedButton === eraserButton) {
            context.strokeStyle = 'white';
        }
        drawerFunction();
    }
}

function drawLine(context, x, y) {
    context.lineTo(x, y);
    context.stroke();
}

function drawStartPoint(context, x, y) {
    context.beginPath();
    context.moveTo(x, y);
}

function getRelativeMousePosition(x, y, canvas) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: x * (canvas.width / rect.width),
        y: y * (canvas.height / rect.height)
    };
}

// -- Topics ---

const CALIBRATION_TOPIC = 'screen/calibration';
const CLIENT_DISCONNECTING_TOPIC = 'client_disconnectisng';
const MOUSE_CLICK_TOPIC = 'mouse/click';
const MOUSE_MOVE_TOPIC = 'mouse/move';

// https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/button
MOUSE_BUTTON = ['primary', 'middle', 'secondary'];

function emitMouseMoveEvent(socket, event) {
    socket.emit(MOUSE_MOVE_TOPIC, mouseMoveEvent(event));
}

function emitMouseClickEvent(socket, event, client) {
    socket.emit(MOUSE_CLICK_TOPIC, mouseClickEvent(client, event));
}

// --- Models ---

function baseEvent() {
    return {
        client: JSON.parse(localStorage.getItem(RANDOM_USER_KEY))['api-key'],
        timestamp: Date.now()
    };
}

function mouseMoveEvent(event) {
    return {
        ...baseEvent(),
        point: {
            x: event.position.x,
            y: event.position.y
        }
    };
}

function mouseClickEvent(client, event) {
    return {
        ...baseEvent(client),
        event: event.type,
        button: MOUSE_BUTTON[event.button] || 'primary'
    };
}

function screenCalibrationEvent(canvas) {
    return {
        ...baseEvent(),
        screen_size: {
            width: canvas.width,
            height: canvas.height
        }
    };
}

// --- Mappers ---
// TODO: QUESTI VANNO ASSOLUTAMENTE SISTEMATI! NON FUNZIONA PIù NA CEPPA

function remapMouseEvent(canvas, event) {
    // This controll is necessary due to a know bug in canvas events position after canvas rescaling
    // issue: https://github.com/CreateJS/EaselJS/issues/772
    return {
        position: {
            x: Math.max(0, Math.min(canvas.width, event.offsetX)),
            y: Math.max(0, Math.min(canvas.height, event.offsetY))
        },
        button: event.buttons,
        keyboardState: {
            altKey: event.altKey,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey
        }
    };
}

function remapTouchEvent(canvas, event) {
    const rect = event.target.getBoundingClientRect();
    let rescaled_x = Math.floor(event.targetTouches[0].pageX - rect.left);
    let rescaled_y = Math.floor(event.targetTouches[0].pageY - rect.top);

    // This controll is necessary due to a know bug in canvas events position after canvas rescaling
    // issue: https://github.com/CreateJS/EaselJS/issues/772
    return {
        position: {
            x: Math.max(0, Math.min(canvas.width, rescaled_x)),
            y: Math.max(0, Math.min(canvas.height, rescaled_y))
        },
        button: 1,
        keyboardState: {
            altKey: event.altKey,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey
        }
    };
}

// TODO: da sistemare
function resizeCanvas() {
    const canvas = document.getElementById('drawingCanvas');
    const container = document.getElementById('drawingCanvasContainer');
    
    // Added padding management to avoid canvas overflow
    let padding = window.getComputedStyle(container).getPropertyValue('padding').replace('px', '');

    canvas.width = container.clientWidth - 2 * padding;
    canvas.height = container.clientHeight - 2 * padding;
}