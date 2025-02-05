function startDrawer(drawerButton = 1, eraserButton = 2) {
    // Per documentazione: https://socket.io/docs/v4/client-api/

    const authToken = document.cookie.split(';')
            .find(str => str.includes('x-api-key'))
            ?.split('=')[1]
            .substring(2).replace('\'','');
    if (!authToken) {
        alert('Unexpected error during drawer creation: try to refresh the page');
        return;
    }
    
    const apis = atob(authToken).split(':')
    const storage = JSON.parse(localStorage.getItem(SESSION_USER_KEY));
    const secret = (storage && apis[0] === storage['api-key']) ? storage['api-secret'] : (Math.random()*1e32).toString(36).substring(0,8);
    localStorage.setItem(SESSION_USER_KEY, JSON.stringify({
        'api-key': apis[0],
        'api-secret': secret,
        role: 'drawer'
    }));
    
    const socket = setSharedConfigurations();
    configDrawerSocket(socket)
    configDrawer(socket, drawerButton, eraserButton);
}

function configDrawer(socket, drawerButton, eraserButton) {
    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');

    // First, send "drawing area" size to calibrare the client receiver
    console.log("Sending screen calibration event");
    socket.emit(CALIBRATION_TOPIC, screenCalibrationEvent(canvas));

    const sessionData = JSON.parse(localStorage.getItem(SESSION_USER_KEY));
    document.getElementById('drawerId').textContent = sessionData['api-key'];
    document.getElementById('drawerSecret').textContent = sessionData['api-secret'];

    canvas.addEventListener('contextmenu', event => {
        event.preventDefault();
    });

    canvas.addEventListener('mousedown', event => {
        mouseDownListener(event, context, socket, drawerButton, eraserButton);
    });

    canvas.addEventListener('mouseup', event => {
        mouseUpListener(event, socket)
    });

    canvas.addEventListener('touchstart', event => {
        mouseDownListener(event, context, socket, drawerButton, eraserButton);
    });

    canvas.addEventListener('touchend', event => {
        mouseUpListener(event, socket)
    });

    canvas.addEventListener('mousemove', event => {
        mouseMoveListener(socket, canvas, context, remapMouseEvent(canvas, event), drawerButton, eraserButton);
    });

    canvas.addEventListener('touchmove', event => {
        mouseMoveListener(socket, canvas, context, remapTouchEvent(canvas, event), drawerButton, eraserButton);
    });

    document.getElementById('cleanButton').addEventListener('click', () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit('clear', sessionData['api-key']);
    });

    document.getElementById('blackboardModeSwitch').addEventListener('change', () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }); 

}

function configDrawerSocket(socket) {

    window.onbeforeunload = () => {
        // TODO: questa potrebbe essere una banale api rest: non ho bisogno di comunicazione bidirezionale tra client e server
        //    ma forse ha senso tenere il ws per notificare i "viewer" che il server è stato disconnesso
        socket.emit(CLIENT_DISCONNECTING_TOPIC, {
            'client': localStorage.getItem(SESSION_USER_KEY)['api-key'],
        });
        localStorage.clear();
    }

}


// --- Listener functions ---

/**
 * Implementation to manage the "mouse move" event, both for mouse and touch events.
 * 
 * @param {*} socket 
 * @param {*} canvas 
 * @param {*} event 
 * @param {*} drawerButton 
 * @param {*} eraserButton 
 */
function mouseMoveListener(socket, canvas, context, event, drawerButton, eraserButton) {
    let relativePos = getRelativeMousePosition(event.position.x, event.position.y, canvas);
    emitMouseMoveEvent(socket, event);
    
    if (blackboardModeSwitch.checked) {
        drawerFunction = () => drawLine(context, relativePos.x, relativePos.y)
        drawOnCanvas(context, event.button, drawerFunction, drawerButton, eraserButton);

    } else{
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Draw a shadow at the cursor position
        context.beginPath();
        context.arc(relativePos.x, relativePos.y, 7, 0, 2 * Math.PI); // TODO 7 deve essere configurabile
        context.fillStyle = 'rgba(50, 50, 50, 0.1)'; // Semi-transparent black
        context.fill();
    }
}

/**
 * Implementation to manage the "mouse down" event, both for mouse and touch events.
 * 
 * @param {*} event 
 * @param {*} context 
 * @param {*} socket 
 * @param {*} drawerButton 
 * @param {*} eraserButton 
 */
function mouseDownListener(event, context, socket, drawerButton, eraserButton) {
    // console.log(`Touch event ${event.type}`);
    event.preventDefault();
    drawerFunction = () => drawStartPoint(context, event.offsetX, event.offsetY);
    drawOnCanvas(context, event.buttons, drawerFunction, drawerButton, eraserButton);
    emitMouseClickEvent(socket, event);
}

/**
 * Implementation to manage the "mouse up" event, both for mouse and touch events.
 * 
 * @param {*} event 
 * @param {*} socket 
 */
function mouseUpListener(event, socket) {
    // console.log(`Touch event ${event.type}`);
    event.preventDefault();
    emitMouseClickEvent(socket, event);
}
