function startDrawer(drawerButton = 1, eraserButton = 2) {
    // Per documentazione: https://socket.io/docs/v4/client-api/

    let serviceUrl = window.location.host;
    fetch(`http://${serviceUrl}/api/v1/login`)
        .then(response => response.json())
        .then(response => {
            let client = response.session_id;
            let authorizationRequest = {
                'api-key': client,
                'api-secret': 'pippo' // Usare HTTPS per sfruttare: crypto.randomUUID()
            };
            localStorage.setItem(RANDOM_USER_KEY, JSON.stringify(authorizationRequest));
            let socket = setSharedConfigurations();

            configDrawerSocket(socket)
            configDrawer(socket, drawerButton, eraserButton);
        }).catch(err => {
            console.log(err);
            alert('Fetch Error :-S', err); // TODO: gestire errore
        });
}

function configDrawer(socket, drawerButton, eraserButton) {
    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');

    // First, send "drawing area" size to calibrare the client receiver
    console.log("Sending screen calibration event");
    socket.emit(CALIBRATION_TOPIC, screenCalibrationEvent(canvas));

    canvas.addEventListener('contextmenu', (event) => {
        event.preventDefault();
    });

    canvas.addEventListener('mousedown', (event) => { // serve anche il touchetdon per il dito
        event.preventDefault(); 
        console.log('mousedown');
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawerFunction = () => drawStartPoint(context, relativePos.offsetX, relativePos.offsetY);
        drawOnCanvas(context, event.buttons, drawerFunction, drawerButton, eraserButton);
        emitMouseClickEvent(socket, event, 'pippo');
    });

    canvas.addEventListener('mouseup', (event) => {  // serve anche il touchend per il dito
        event.preventDefault(); 
        console.log('mouseup');
        emitMouseClickEvent(socket, event, 'pippo');
    });

    canvas.addEventListener('touchstart', (event) => {
        event.preventDefault(); 
        console.log('touchstart');
        let relativePos = getRelativeMousePosition(event.offsetX, event.offsetY, canvas);
        drawerFunction = () => drawStartPoint(context, relativePos.offsetX, relativePos.offsetY);
        drawOnCanvas(context, event.buttons, drawerFunction, drawerButton, eraserButton);
        emitMouseClickEvent(socket, event, 'pippo');
    });

    canvas.addEventListener('touchend', (event) => {
        event.preventDefault(); 
        console.log('touchend');
        emitMouseClickEvent(socket, event, 'pippo');
    });

    canvas.addEventListener('mousemove', (event) => {
        mouseMoveCallback(socket, canvas, remapMouseEvent(canvas, event), drawerButton, eraserButton);
    });

    canvas.addEventListener('touchmove', (event) => {
        mouseMoveCallback(socket, canvas, remapTouchEvent(canvas, event), drawerButton, eraserButton);
    });

    // document.getElementById('cleanButton').addEventListener('click', () => {
    //     context.clearRect(0, 0, canvas.width, canvas.height);
    //     socket.emit('clear', client); // TODO: rinominare il topic
    // });

}

function configDrawerSocket(client, socket) {

    window.onbeforeunload = () => {
        // TODO: questa potrebbe essere una banale api rest: non ho bisogno di comunicazione bidirezionale tra client e server
        //    ma forse ha senso tenere il ws per notificare i "viewer" che il server è stato disconnesso
        socket.emit(CLIENT_DISCONNECTING_TOPIC, {
            'client': localStorage.getItem(RANDOM_USER_KEY)['api-key'],
        });
        localStorage.clear();
    }

}

function mouseMoveCallback(socket, canvas, event, drawerButton, eraserButton) {
    const context = canvas.getContext('2d');
    let relativePos = getRelativeMousePosition(event.position.x, event.position.y, canvas);

    drawerFunction = () => drawLine(context, relativePos.x, relativePos.y)
    drawOnCanvas(context, event.button, drawerFunction, drawerButton, eraserButton);
    emitMouseMoveEvent(socket, event);
}