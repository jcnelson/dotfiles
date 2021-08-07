#!/bin/bash

host=52.0.54.100:20443

set -ueo pipefail

body='{
   "sender": "SP31DA6FTSJX2WGTZ69SFY11BH51NZMB0ZW97B5P0.get-info",
   "arguments": [
        "0x0100000000000000000000000000000002"
   ] 
}'

body_len=${#body}

ustx_hex="$(echo "$body" | curl -sf -X POST -H "content-type: application/json" -H "content-length: $body_len" --data-binary @- "http://$host/v2/contracts/call-read/SP000000000000000000002Q6VF78/pox/get-total-ustx-stacked" | \
        jq -r '.result' | \
        sed -r 's/0x010*//g')"

ustx="$(printf "%d" $((16#$ustx_hex)))"

echo "scale=6; $ustx/1000000" | bc
