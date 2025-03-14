function drawOnCanvas(context, pressedButton, drawerFunction, drawerButton, eraserButton) {
    
    // TODO:
    // - add color palette to change pen color for "blackboard mode"
    //   In this scenario, the color should be send with move mouse event

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
        x: x * (canvas.width / rect.width),
        y: y * (canvas.height / rect.height)
    };
}
