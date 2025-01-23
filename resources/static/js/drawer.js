function startDrawer(socket, drawerButton = 1, eraserButton = 2) {
    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');

    // TODO: questo sarà generato dal server
    //       > Su chrome sul tablet non esiste la libreriea "crypto"
    const client = "pippo" // crypto.randomUUID();

    // First, send "drawing area" size to calibrare the client receiver
    console.log("Sending screen calibration event");
    socket.emit(CALIBRATION_TOPIC, screenCalibrationEvent(client, canvas));

    canvas.addEventListener('mousedown', (event) => {
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawOnCanvas(context, event.buttons, () => drawStartPoint(context, relativePos.offsetX, relativePos.offsetY),
                        drawerButton, eraserButton);
        // emitPositionEvent(socket, event, user, true);
        // console.log(event);

        button = event.button === 0 ? 'PRIMARY' : 'SECONDARY' 
        socket.emit('mouseclick', { event: 'mousedown', button });

        // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/button
        // 0: Main button pressed, usually the left button or the un-initialized state
        // 1: Auxiliary button pressed, usually the wheel button or the middle button (if present)
        // 2: Secondary button pressed, usually the right button
        // 3: Fourth button, typically the Browser Back button
        // 4: Fifth button, typically the Browser Forward button

    });

    canvas.addEventListener('mouseup', (event) => {
        console.log(event);
        button = event.button === 0 ? 'PRIMARY' : 'SECONDARY' 
        socket.emit('mouseclick', { event: 'mouseup', button });
    });

    canvas.addEventListener('mousemove', (event) => {
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawOnCanvas(context, event.buttons, () => drawLine(context, relativePos.offsetX, relativePos.offsetY),
                        drawerButton, eraserButton);
        //console.log(event);
        emitPositionEvent(socket, event, client);
    });

    canvas.addEventListener('contextmenu', (event) => {
        event.preventDefault();
    });

    document.getElementById('clearButton').addEventListener('click', () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit('clear', client);
    });

}

function configDrawerSocket(socket) {

    window.onbeforeunload = () => {
        // TODO: to be defined
        let payload = {
            'username':localStorage.getItem('username')
        }
        socket.emit(CLIENT_DISCONNECTING_TOPIC, payload);
    }

}
