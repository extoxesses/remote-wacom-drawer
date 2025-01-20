function startDrawer(socket, drawerButton = 1, eraserButton = 2) {
    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');
    // const user = crypto.randomUUID(); // TODO: questo sarà generato dal server: su chrome non ha funzionato
    const user = 'pippo';

    // First, send "drawing area" size to calibrare the client receiver
    console.log(`Emit event for object calibration: ${canvas.width}x${canvas.height}`);
    socket.emit('screen/calibration', { ...getBaseEvent('pippo'), screen_size : { width: canvas.width, height: canvas.height } });

    canvas.addEventListener('mousedown', (event) => {
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawOnCanvas(context, event.buttons, () => drawStartPoint(context, relativePos.offsetX, relativePos.offsetY),
                        drawerButton, eraserButton);
        emitPositionEvent(socket, event, user, true);
    });

    canvas.addEventListener('mousemove', (event) => {
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawOnCanvas(context, event.buttons, () => drawLine(context, relativePos.offsetX, relativePos.offsetY),
                        drawerButton, eraserButton);
        console.log(event);
        emitPositionEvent(socket, event, user);
    });

    canvas.addEventListener('contextmenu', (event) => {
        event.preventDefault();
    });

    document.getElementById('clearButton').addEventListener('click', () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit('clear', user);
    });

}

function configDrawerSocket(socket) {

    window.onbeforeunload = () => {
        socket.emit('client_disconnecting', {'username':localStorage.getItem('username')});
    }

}

// -- "Private" functions

function emitPositionEvent(socket, event, client, isStart = false) {
    let payload = {
        ...getBaseEvent(client),
        point : {
            x: event.offsetX,
            y: event.offsetY,
            button: event.buttons,
        },
        isStart // TODO: da valutare se tenere la funzionalità o se rimuoverla
    }
    socket.emit('position', payload);
}

function getBaseEvent(client) {
    return {
        client,
        timestamp: Date.now()
    }
}
