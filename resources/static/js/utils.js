function configSocket(socket) {

    socket.on('connect', () => {
        alert('Connected to server')
    });

    socket.on('disconnect', () => {
        alert('Disconnected from server')
    });

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
        offsetX: x * (canvas.width / rect.width),
        offsetY: y * (canvas.height / rect.height)
    };
}

// -- Topics ---

const CALIBRATION_TOPIC = 'screen/calibration';
const CLIENT_DISCONNECTING_TOPIC = 'client_disconnecting';
const POSITION_TOPIC = 'position';

function emitPositionEvent(socket, event, client, isStart = false) {
    socket.emit(POSITION_TOPIC, positionEvent(client, event));
}

// --- Models ---

function baseEvent(client) {
    return {
        client,
        timestamp: Date.now()
    };
}

function positionEvent(client, event) {
    return {
        ...baseEvent(client),
        point: {
            x: event.offsetX,
            y: event.offsetY
        }
    };
}

function screenCalibrationEvent(client, canvas) {
    return {
        ...baseEvent(client),
        screen_size: {
            width: canvas.width,
            height: canvas.height
        }
    };
}
