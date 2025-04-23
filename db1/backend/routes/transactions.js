const express = require('express');
const router = express.Router();
const db = require('../db');

// Get all transactions
router.get('/', async (req, res) => {
  const result = await db.query('SELECT * FROM TransactionHistory');
  res.json(result.rows);
});

module.exports = router;