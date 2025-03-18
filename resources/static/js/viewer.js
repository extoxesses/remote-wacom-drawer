function startViewer(drawerButton = 'primary', eraserButton = 'secondary') {

    const canvas = document.getElementById('drawingCanvas');
    const context = canvas.getContext('2d');
    let buttonStatus = {
        button: 0,
        isStart: false
    };
    let drawerCanvasSize = {
        width: canvas.width,
        height: canvas.height
    };
    let socket;
    
    document.getElementById('connectButton').addEventListener('click', () => {
        const drawerId = document.getElementById('drawerId').value;
        const drawerSecret = document.getElementById('drawerSecret').value;
        
        if (!drawerId || !drawerSecret) {
            alert('Please enter both Drawer ID and Secret');
            return;
        }
        
        // Store in localStorage for persistence
        localStorage.setItem('authorization', JSON.stringify({
            'api-key': drawerId,
            'api-secret': drawerSecret
        }));
        
        // Connect to server
        socket = connectToServer({
            'api-key': drawerId,
            'api-secret': drawerSecret,
            role: 'viewer'
        });
        
        setSharedConfigurations();

        socket.on(MOUSE_MOVE_TOPIC, (event) => {
            const relativePosition = getRelativeMousePosition(event.point.x, event.point.y, canvas, drawerCanvasSize);

            if (buttonStatus.button === 0) {
                return;
            
            } else if (buttonStatus.isStart) {
                console.log(`Drawing event to canvas. Button: ${buttonStatus.button}, Status: ${buttonStatus.isStart}, Point: ${JSON.stringify(relativePosition)}`)
                drawOnCanvas(context, buttonStatus.button, () => drawStartPoint(context, relativePosition.x, relativePosition.y),
                                drawerButton, eraserButton);
                buttonStatus.isStart = false;
            
            } else {
                console.log(`Drawing event to canvas. Button: ${buttonStatus.button}, Status: ${buttonStatus.isStart}, Point: ${JSON.stringify(relativePosition)}`)
                drawOnCanvas(context, buttonStatus.button, () => drawLine(context, relativePosition.x, relativePosition.y),
                                drawerButton, eraserButton);
            }
        });

        socket.on(MOUSE_CLICK_TOPIC, (event) => {
            let ops = event.event
            switch (ops) {
                case 'mousedown':
                case 'touchstart':
                    buttonStatus = { button: labelToButton(event.button), isStart: true }
                    break;
                case 'mouseup':
                case 'touchend':
                    buttonStatus = { button: 0, isStart: false };
                    break;
                default:
                    console.log(`Event ${ops} not recognized. Skipped`)
                    break;
            }
        })

        socket.on(CALIBRATION_TOPIC, (event) => {
            console.log(`Drawer resing: update source drawing panel size to ${JSON.stringify(event.screen_size)}`);
            drawerCanvasSize = {
                width: event.screen_size.width,
                height: event.screen_size.height
            }
        })

        socket.on(CLEAN_BOARD_TOPIC, (event) => {
            console.log('clean')
            context.clearRect(0, 0, canvas.width, canvas.height);
        })

        // TODO: Add drawer disconnection management on both side (py amd js)

    });

}

function labelToButton(button) {
    switch (button) {
        case 'primary':
            return 1;
        case 'secondary':
            return 2;
        case 'middle':
            return 3;
        default:
            return undefined;
    }
}
