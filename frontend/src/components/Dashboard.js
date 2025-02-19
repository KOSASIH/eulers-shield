import React, { useEffect, useState } from 'react';
import api from '../api';

const Dashboard = () => {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
const fetchTransactions = async () => {
            const response = await api.get('/transactions');
            setTransactions(response.data);
        };
        fetchTransactions();
    }, []);

    return (
        <div>
            <h1>Transaction Dashboard</h1>
            <ul>
                {transactions.map(transaction => (
                    <li key={transaction._id}>
                        Amount: {transaction.amount} | Date: {new Date(transaction.timestamp).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Dashboard;
