#!/usr/bin/env node

const BigNum = require('bn.js');
const process = require('process');
const bns = require("@stacks/bns");
const net = require('@stacks/network');

/*
const bufferCVFromString = transactions.bufferCVFromString;
const uintCV = transactions.uintCV;
const hash160 = transactions.hash160;
*/

privk = process.argv[2];
namespace = process.argv[3];
salt = process.argv[4];

if (privk === undefined || namespace === undefined || salt === undefined) {
  console.error(`Usage: ${process.argv[1]} PRIVKEY NAMESPACE SALT`);
  process.exit(1);
}

const main = async function() {
  const namespace = "atlastest04122021";
  const network = new net.StacksTestnet();
  const cost = await bns.getNamespacePrice({ namespace, network });
  console.log(`Cost: ${cost}`);
}

main();

/*
const namespace_salted_hash = hash160(namespace + salt);

const txOptions = {
  contractAddress: "ST000000000000000000002AMW42H",
  contractName: "bns",
  functionName: "namespace-preorder",
  functionArgs: [bufferCVFromString(namespace_salted_hash), uintCV(cost)],
  senderKey: privk,
  validateWithAbi: true,
  network: net,
  postConditions: []
};

makeContractCall(txOptions)
.then((transaction) => {
  const serializedTx = transaction.serialize().toString('hex');
  console.log(serializedTx)
  process.exit(0)
})
*/
