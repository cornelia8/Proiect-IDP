const express = require('express');
const router = express.Router();
const db = require('../db');

// Get all transactions
router.get('/', async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM TransactionHistory');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Add a transaction
router.post('/', async (req, res) => {
  const { buyer_id, seller_id, product_name, quantity, price } = req.body;
  try {
    const result = await db.query(
      'INSERT INTO TransactionHistory (buyer_id, seller_id, product_name, quantity, price) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [buyer_id, seller_id, product_name, quantity, price]
    );
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send('Failed to insert transaction');
  }
});

module.exports = router;