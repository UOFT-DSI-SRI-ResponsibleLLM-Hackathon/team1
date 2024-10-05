const express = require('express');
const cors = require('cors');  // Import the CORS library

const app = express();
const port = 5000;

app.use(cors());  // Enable CORS for all routes
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello from the Node.js backend!');
});

app.post('/data', (req, res) => {
  const userData = req.body;
  console.log('Received data:', userData);
  res.send({ message: 'Data received successfully!' });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://localhost:${port}`);
});