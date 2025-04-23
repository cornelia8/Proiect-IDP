const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

const transactionRoutes = require('./routes/transactions');
app.use('/transactions', transactionRoutes);

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
