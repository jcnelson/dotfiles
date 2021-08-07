#!/bin/bash

host=52.0.54.100:20443
body='\
{ \
   "sender": "SP31DA6FTSJX2WGTZ69SFY11BH51NZMB0ZW97B5P0.get-info", \
   "arguments": [ \
        "0x0100000000000000000000000000000002" \
   ] \
}'

body_len=${#body}

echo "$body" | curl -D - -X POST -H "content-type: application/json" -H "content-length: $body_len" --data-binary @- "http://$host/v2/contracts/call-read/SP000000000000000000002Q6VF78/pox/get-total-ustx-stacked"

