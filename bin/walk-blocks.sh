#!/bin/sh

set -e

which jq || exit 1
which bitcoin-cli || exit 1

BITCOIN_CONF="/etc/bitcoin/bitcoin.conf"

TIP="$(bitcoin-cli -conf="$BITCOIN_CONF" getblockchaininfo | jq -r '.bestblockhash')"
COUNT="$(bitcoin-cli -conf="$BITCOIN_CONF" getblockchaininfo | jq -r '.blocks')"
for i in $(seq 1 $COUNT); do 
   echo "tip: $TIP"
   bitcoin-cli -conf="$BITCOIN_CONF" getblock "$TIP" | jq -r '.tx[]'
   echo ""

   TIP="$(bitcoin-cli -conf="$BITCOIN_CONF" getblock "$TIP" | jq -r '.previousblockhash')"
done

