#!/usr/bin/env node

const BigNum = require('bn.js');
const process = require('process');

// node.js is a garbage fire.
// It remains the *only* widely-used language whose REPL has been *intentionally
// lobotomized* into not knowing how to load modules.
const transactions = require('/usr/lib/node_modules/stacks.js/packages/transactions');
const network = require('/usr/lib/node_modules/stacks.js/packages/network');
const makeSTXTokenTransfer = transactions.makeSTXTokenTransfer;
const broadcastTransaction = transactions.broadcastTransaction;
const StacksMainnet = network.StacksMainnet;

privk = process.argv[2];
addr = process.argv[3];
amount = process.argv[4];
nonce = process.argv[5];
fee = process.argv[6];

if (privk === undefined || addr === undefined || amount === undefined || fee === undefined) {
  console.error(`Usage: ${process.argv[1]} PRIVKEY ADDR AMOUNT NONCE FEE`);
  process.exit(1);
}

const mainnet = new StacksMainnet();

const txOptions = {
  recipient: addr,
  amount: new BigNum(amount),
  senderKey: privk,
  network: mainnet,
  memo: '',
  nonce: new BigNum(nonce), // set a nonce manually if you don't want builder to fetch from a Stacks node
  fee: new BigNum(fee), // set a tx fee if you don't want the builder to estimate
};

makeSTXTokenTransfer(txOptions)
.then((transaction) => {
  const serializedTx = transaction.serialize().toString('hex');
  console.log(serializedTx)
  process.exit(0)
})

