 // Get the canvas element and its context
 const canvas = document.getElementById('myCanvas');
 const ctx = canvas.getContext('2d');

 // Variables for drawing
 let isDrawing = false;
 let lastX = 0;
 let lastY = 0;
 let cursorX = 0;
 let cursorY = 0;
 let shadowTimeout = null;

 // Function to resize the canvas to fit the available space
 function resizeCanvas() {
     const container = document.getElementById('canvasContainer');
     const containerWidth = container.clientWidth;
     const containerHeight = container.clientHeight;

     // Set canvas dimensions to fit the container
     canvas.width = containerWidth;
     canvas.height = containerHeight;

     // Redraw content after resizing
     drawInitialContent();
 }

 // Function to draw a shadow at the cursor position
 function drawShadow() {
     if (!blackboardModeSwitch.checked) {
         // Clear the canvas
         ctx.clearRect(0, 0, canvas.width, canvas.height);

         // Redraw the initial content
         drawInitialContent();

         // Draw a shadow at the cursor position
         ctx.beginPath();
         ctx.arc(cursorX, cursorY, 10, 0, 2 * Math.PI); // Draw a circle
         ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'; // Semi-transparent black
         ctx.fill();
     }
 }

 // Function to start drawing
 function startDrawing(e) {
     if (blackboardModeSwitch.checked) {
         isDrawing = true;
         [lastX, lastY] = [e.offsetX, e.offsetY];
     }
 }

 // Function to draw on the canvas
 function draw(e) {
     cursorX = e.offsetX;
     cursorY = e.offsetY;

     if (blackboardModeSwitch.checked && isDrawing) {
         // Draw a line from the last position to the current position
         ctx.strokeStyle = '#000'; // Black color for drawing
         ctx.lineWidth = 2; // Line thickness
         ctx.lineCap = 'round'; // Rounded line ends
         ctx.beginPath();
         ctx.moveTo(lastX, lastY);
         ctx.lineTo(e.offsetX, e.offsetY);
         ctx.stroke();

         // Update the last position
         [lastX, lastY] = [e.offsetX, e.offsetY];
     } else if (!blackboardModeSwitch.checked) {
         // Draw a shadow at the cursor position
         drawShadow();
     }
 }

 // Function to stop drawing
 function stopDrawing() {
     isDrawing = false;
 }

 // Function to clear the shadow after a delay
 function clearShadow() {
     if (!blackboardModeSwitch.checked) {
         ctx.clearRect(0, 0, canvas.width, canvas.height);
         drawInitialContent();
     }
 }

 // Initial resize and draw
 resizeCanvas();

 // // Add event listeners for canvas drawing
 // canvas.addEventListener('mousedown', startDrawing);
 // canvas.addEventListener('mousemove', draw);
 // canvas.addEventListener('mouseup', stopDrawing);
 // canvas.addEventListener('mouseout', () => {
 //     stopDrawing();
 //     clearShadow();
 // });

 // Add event listener for window resize
 window.addEventListener('resize', resizeCanvas);

 // TODO: valutare se serve
 // // Add event listeners for buttons
 // document.getElementById('connectButton').addEventListener('click', () => {
 //     alert('Connect button clicked!');
 // });

 // TODO: aggiungere invocazione a evento
 document.getElementById('calibrateButton').addEventListener('click', () => {
     alert('Calibrate button clicked!');
 });

 // TODO: usare il mio listener
 // document.getElementById('cleanButton').addEventListener('click', () => {
 //     // Clear the canvas and redraw the initial content
 //     ctx.clearRect(0, 0, canvas.width, canvas.height);
 //     drawInitialContent();
 // });

 // Da tenere

 const blackboardModeSwitch = document.getElementById('blackboardModeSwitch');
 blackboardModeSwitch.addEventListener('change', (event) => {
     if (event.target.checked) {
         alert('Blackboard Mode enabled!');
     } else {
         alert('Blackboard Mode disabled!');
         // Clear the shadow when switching modes
         clearShadow();
     }
 });