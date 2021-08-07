#!/bin/sh

sqlite3 ~/debian-testing/home/debian/.blockstack-server/blockstack-server.db 'select * from history where op = "$" and vtxindex > 0 order by block_id,vtxindex' > /tmp/token-txs.list
(echo -n '['; cat /tmp/token-txs.list | sed -r -e 's/\|+/\|/g' -e 's/^[0-9a-f]{64}\|/\|/g' -e 's/[^\|]+\|//g' -e 's/^\|//g' -e 's/(.+)/\1/g' | tr '\n' ',' | sed -r 's/},$/}/g'; echo ']') > /tmp/token-txs.json

for addr in $(cat /tmp/token-txs.json | jq -r '.[].address' | sort | uniq); do 
   c32addr=$(blockstack-cli convert_address $addr | jq -r '.mainnet.STACKS')
   echo -n "$addr $c32addr "
   found_c32="$(fgrep -r $c32addr ~/genesis-block/genesis-data/genesis-block/data/ | egrep -v -i 'muneeb|ali')"

   if [ -n "$found_c32" ]; then
      qry=".[] | select(.address == \"$addr\") | .token_fee"
      cat /tmp/token-txs.json | jq -r "$qry" | add
   else
      echo ""
   fi
done

