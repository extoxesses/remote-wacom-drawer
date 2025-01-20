function configViewer(socket, drawerButton = 1, eraserButton = 2) {
    
    document.addEventListener('DOMContentLoaded', () => {
        canvas = document.getElementById('displayCanvas');
        configViewerSocket(socket, canvas, drawerButton, eraserButton)
    });

}


// -- "Private" functions

function configViewerSocket(socket, canvas, drawerButton, eraserButton) {

    socket.on('position', (position) => {
        drawCanvas(canvas, position, drawerButton, eraserButton);
    });

}

function drawCanvas(canvas, event, drawerButton, eraserButton) {
    let context = canvas.getContext('2d');
    let relativePosition = getRelativeMousePosition(event.position.x, event.position.y, canvas)
    let pressedButton = event.position.button;

    if (event.isStart) {
        drawOnCanvas(context, pressedButton, () => drawStartPoint(context, relativePosition.offsetX, relativePosition.offsetY),
                        drawerButton, eraserButton);
    } else {
        drawOnCanvas(context, pressedButton, () => drawLine(context, relativePosition.offsetX, relativePosition.offsetY),
                        drawerButton, eraserButton);
    }
}
