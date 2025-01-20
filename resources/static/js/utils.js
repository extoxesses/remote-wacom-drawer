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
