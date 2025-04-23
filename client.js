const WebSocket = require('ws');
const readline = require('readline');

// Create a readline interface for input/output
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Connect to the WebSocket server
const ws = new WebSocket('ws://localhost:3000');

// WebSocket 'open' event: connected to the server
ws.on('open', () => {
  console.log('Connected to server.');
  askForInput();  // Only ask for input when the WebSocket is open
});

// WebSocket 'message' event: received message from server
ws.on('message', (data) => {
  console.log(`Server: ${data}`);
  askForInput();  // Ask for input after receiving a message from the server
});

// WebSocket 'close' event: server connection closed
ws.on('close', () => {
  console.log('Disconnected from server.');
  rl.close();  // Close readline when the WebSocket connection is closed
  process.exit(0);  // Exit the process
});

// Handle error events
ws.on('error', (error) => {
  console.error(`WebSocket error: ${error}`);
  rl.close();  // Close readline if an error occurs
  process.exit(1);  // Exit the process with an error code
});

// Function to ask for input from the user
function askForInput() {
  // Prevent asking for input if the WebSocket is closed
  if (ws.readyState !== WebSocket.OPEN) {
    console.log("WebSocket is not open. Cannot accept input.");
    return;
  }

  rl.question('', (input) => {
    if (input.trim().toLowerCase() === 'exit') {
      console.log('Closing client connection...');
      ws.close();  // Close the WebSocket connection
    } else {
      ws.send(input.trim());  // Send user input to the server
    }
  });
}