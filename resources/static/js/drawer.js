function startDrawer(drawerButton = 'primary', eraserButton = 'secondary') {
    // Per documentazione: https://socket.io/docs/v4/client-api/

    // Look for 'x-api-key' in the cookies
    const authToken = document.cookie.split(';')
            .find(str => str.includes('x-api-key'))
            ?.split('=')[1]
    if (!authToken) {
        alert('Unexpected error during drawer creation: try to refresh the page');
        return;
    }
    
    // Now generate 'auth' object using:
    // - 'api-key' from the cookie
    // - 'api-secret' from the localStorage (if present) or generate a random value
    // Update the localStorage with the new 'api-secret'
    const apis = atob(authToken).split(':')
    const storage = JSON.parse(localStorage.getItem(SESSION_USER_KEY));
    const secret = (storage && apis[0] === storage['api-key']) ? storage['api-secret'] : (Math.random()*1e32).toString(36).substring(0,8);
    const auth = {
        'api-key': apis[0],
        'api-secret': secret,
        role: 'drawer'
    }
    localStorage.setItem(SESSION_USER_KEY, JSON.stringify(auth));
    
    // Configure drawer page (A)
    configDrawer(auth, drawerButton, eraserButton);
}

function configDrawer(auth, drawerButton, eraserButton) {
    const socket = connectToServer(auth)
    //setSharedConfigurations(configDrawer(auth, drawerButton, eraserButton));
    setSharedConfigurations();

    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');

    // First, send "drawing area" size to calibrare the client receiver
    canvasCalibration(socket, canvas)

    const sessionData = JSON.parse(localStorage.getItem(SESSION_USER_KEY));
    document.getElementById('drawerId').textContent = sessionData['api-key'];
    document.getElementById('drawerSecret').textContent = sessionData['api-secret'];

    window.onbeforeunload = () => {
        socket.emit(CLIENT_DISCONNECTING_TOPIC, {
            'client': localStorage.getItem(SESSION_USER_KEY)['api-key'],
        });
        localStorage.clear();
    }

    canvas.addEventListener('contextmenu', event => {
        event.preventDefault();
    });

    // Sidebar button events management
    
    document.getElementById('calibrateButton').addEventListener('click', () => canvasCalibration(socket, canvas));

    document.getElementById('cleanButton').addEventListener('click', () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit(CLEAN_BOARD_TOPIC, sessionData['api-key']);
    });

    document.getElementById('blackboardModeSwitch').addEventListener('change', () => {
        // TODO: Send event to server to manager status for drawer
        context.clearRect(0, 0, canvas.width, canvas.height);
    }); 

    // Canvas drawing events management

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

}


// --- Listener functions ---

function canvasCalibration(socket, canvas) {
    // First, send "drawing area" size to calibrare the client receiver
    console.log("Sending screen calibration event");
    socket.emit(CALIBRATION_TOPIC, screenCalibrationEvent(canvas));
}

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
