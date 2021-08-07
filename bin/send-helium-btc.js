#!/usr/bin/env node

bsk = require('blockstack')
process = require('process')
bitcoinjs = require('bitcoinjs-lib')

cmd = process.argv[2]
privk = process.argv[3]
addr = process.argv[4]
amount = process.argv[5]

if (cmd === undefined || privk === undefined || addr === undefined) {
  console.error(`Usage: ${process.argv[1]} [send|tx] PRIVKEY ADDR [AMOUNT]`);
  process.exit(1)
}

if (cmd !== 'send' && cmd !== 'tx') {
  console.error(`Usage: ${process.argv[1]} [send|tx] PRIVKEY ADDR [AMOUNT]`);
  process.exit(1)
}

if (amount === undefined) {
  amount = 10000000000000
}

const network = new bsk.network.BlockstackNetwork(
  bsk.network.blockstackAPIUrl, bsk.network.broadcastServiceUrl,
  new bsk.network.BitcoindAPI("http://localhost:28443", { username: "blockstack", password: "blockstacksystem" }),
  bitcoinjs.networks.testnet)

bsk.config.network = network

bsk.transactions.makeBitcoinSpend(addr, privk, parseInt(amount))
.then((tx) => {
  if (cmd === 'tx') {
    console.log(tx)
    process.exit(0)
  }
  else {
    return bsk.network.defaults.MAINNET_DEFAULT.broadcastTransaction(tx)
  }
})
.then((res) => {
  console.log(res)
  process.exit(0)
})
.catch((e) => {
  console.log(e)
  process.exit(1)
})
