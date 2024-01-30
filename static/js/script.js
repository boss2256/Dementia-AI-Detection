// Get references to the canvas and context
const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');

// Set initial drawing state
let isDrawing = false;
let drawingData = [];

// Set up event listeners
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Function to start drawing
function startDrawing(event) {
    isDrawing = true;
    context.beginPath();
    const { clientX, clientY } = event;
    const canvasX = clientX - canvas.offsetLeft;
    const canvasY = clientY - canvas.offsetTop;
    context.moveTo(canvasX, canvasY);
}

// Function to draw
function draw(event) {
    if (!isDrawing) return;
    const { clientX, clientY } = event;
    const canvasX = clientX - canvas.offsetLeft;
    const canvasY = clientY - canvas.offsetTop;
    context.lineTo(canvasX, canvasY);
    context.stroke();
    drawingData.push({ startX: canvasX, startY: canvasY, endX: canvasX, endY: canvasY });
}

// Function to stop drawing
function stopDrawing() {
    isDrawing = false;
    context.closePath();
}

// Event listener for the Save button
document.getElementById('saveButton').addEventListener('click', function() {
    const selectedUsername = document.getElementById('userSelect').selectedOptions[0].text;
    const testName = document.getElementById('testName').value;
    const testDate = document.getElementById('testDate').value;

    // Create a JSON object with the drawing data
    const jsonData = {
        user: selectedUsername,
        test_name: testName,
        date: testDate,
        drawing_data: drawingData
    };

    // Send the JSON data to the server using fetch
    fetch('/save_cognitive_test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Cognitive test saved successfully') {
            $('#successModal').modal('show');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Event listener for the Reset button
document.getElementById('resetButton').addEventListener('click', function() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawingData = [];
});
