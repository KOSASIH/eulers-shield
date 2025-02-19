const Transaction = require('../models/Transaction');

exports.createTransaction = async (req, res) => {
    const { amount } = req.body;
    const transaction = new Transaction({ userId: req.user.id, amount });
    await transaction.save();
    res.status(201).send(transaction);
};

exports.getTransactions = async (req, res) => {
    const transactions = await Transaction.find({ userId: req.user.id });
    res.send(transactions);
};
