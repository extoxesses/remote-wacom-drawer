function startViewer(drawerButton = 'primary', eraserButton = 'secondary') {

    let socket;
    const canvas = document.getElementById('drawingCanvas');

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

        socket.on('mouse/move', (position) => {
            console.log(position)
            drawCanvas(canvas, position, drawerButton, eraserButton);
        });
    });

}

// function configViewer(socket, drawerButton = 1, eraserButton = 2) {
    
//     document.addEventListener('DOMContentLoaded', () => {
//         canvas = document.getElementById('displayCanvas');
//         configViewerSocket(socket, canvas, drawerButton, eraserButton)
//     });

// }


// -- "Private" functions

// function configViewerSocket(socket, canvas, drawerButton, eraserButton) {

//     socket.on('position', (position) => {
//         drawCanvas(canvas, position, drawerButton, eraserButton);
//     });

// }

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
