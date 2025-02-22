// autoConnect.js

const axios = require('axios');
require('dotenv').config(); // Load environment variables from .env file

// Load environment variables
const PI_NETWORK_API_URL = process.env.PI_NETWORK_API_URL || 'https://minepi.com/api';
const PI_API_KEY = process.env.PI_API_KEY; // Your API key for the Pi Network
const ENABLE_PI_NETWORK_CONNECTIVITY = process.env.ENABLE_PI_NETWORK_CONNECTIVITY === 'true';
const PEER_DISCOVERY_INTERVAL = parseInt(process.env.PEER_DISCOVERY_INTERVAL, 10) || 60;
const MAX_PEERS = parseInt(process.env.MAX_PEERS, 10) || 100;

// Function to connect to the Pi Network
async function connectToPiNetwork() {
    if (ENABLE_PI_NETWORK_CONNECTIVITY) {
        try {
            const response = await axios.get(PI_NETWORK_API_URL, {
                headers: {
                    'Authorization': `Bearer ${PI_API_KEY}`, // Include the API key in the request headers
                },
            });

            if (response.status === 200) {
                console.log("Successfully connected to the Pi Network.");
                // Handle successful connection logic here
                console.log(response.data); // Log the response data for debugging
            } else {
                console.error(`Failed to connect to Pi Network: ${response.status}`);
            }
        } catch (error) {
            console.error(`An error occurred while connecting to Pi Network: ${error.message}`);
        }
    } else {
        console.log("Pi Network connectivity is disabled.");
    }
}

// Automatically connect to the Pi Network
connectToPiNetwork();

// Optional: Set up a periodic check for connection
setInterval(connectToPiNetwork, PEER_DISCOVERY_INTERVAL * 1000); // Check every PEER_DISCOVERY_INTERVAL seconds
