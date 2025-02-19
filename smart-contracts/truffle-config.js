const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const { infuraKey, mnemonic } = require('./secrets.json');

const provider = new HDWalletProvider(mnemonic, `https://rinkeby.infura.io/v3/${infuraKey}`);
const web3 = new Web3(provider);

module.exports = {
    networks: {
        rinkeby: {
            provider: () => provider,
            network_id: 4,
        },
    },
    compilers: {
        solc: {
            version: "0.8.0",
        },
    },
};
