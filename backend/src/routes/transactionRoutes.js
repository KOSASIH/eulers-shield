const express = require('express');
const { createTransaction, getTransactions } = require('../controllers/transactionController');
const authMiddleware = require('../middleware/authMiddleware');
const router = express.Router();

router.post('/', authMiddleware, createTransaction);
router.get('/', authMiddleware, getTransactions);

module.exports = router;
