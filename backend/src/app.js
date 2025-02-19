const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const routes = require('./routes');
const logger = require('./utils/logger');

dotenv.config();

const app = express();
app.use(express.json());
app.use('/api', routes);

const PORT = process.env.PORT || 5000;

// Database connection
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        app.listen(PORT, () => {
            logger.info(`Server is running on port ${PORT}`);
        });
    })
    .catch(err => logger.error(err));
