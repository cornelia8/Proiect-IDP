
const express = require('express');
const http = require('http');
const { WebSocketServer } = require('ws');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

const PORT = process.env.PORT || 3000;

let clients = new Map();  // Map to hold clientId -> WebSocket connection

// Handle WebSocket connections
wss.on('connection', (ws) => {
  const clientId = uuidv4();
  clients.set(clientId, ws);

  console.log(`Client ${clientId} connected. Active clients: ${clients.size}`);
  ws.send(`Connected to server. Your ID: ${clientId}`);

  ws.on('message', (message) => {
    const msg = message.toString().trim().toLowerCase();
    console.log(`Received message from ${clientId}: ${msg}`);
    
    if (msg === 'ping') {
      ws.send('Heard you.');
    } else if (msg === 'exit') {
      ws.send('Goodbye!');
      ws.close();
    } else {
      ws.send(`Unknown command: "${msg}". Please type "ping" or "exit".`);
    }
  });

  ws.on('close', () => {
    clients.delete(clientId);
    console.log(`Client ${clientId} disconnected. Active clients: ${clients.size}`);
  });
});

// Simple HTTP GET route to show server is alive
app.get('/', (req, res) => {
  res.send('WebSocket server is running.');
});

// Start the HTTP + WebSocket server
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// Handle graceful shutdown when typing "exit" in the server terminal
const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function checkServerInput() {
  rl.question('', (input) => {
    if (input.trim().toLowerCase() === 'exit') {
      console.log('Shutting down server...');
      wss.clients.forEach(client => client.close());
      server.close(() => {
        console.log('Server closed.');
        process.exit(0);
      });
    } else {
      checkServerInput();  // Keep listening for server-side commands
    }
  });
}

checkServerInput();
