#!/bin/sh

CONSENSUS_HASH="$1"
BLOCK_HASH="$2"

if [ -z "$BLOCK_HASH" ] || [ -z "$CONSENSUS_HASH" ]; then
   echo >&2 "Usage: $0 CONSENSUS_HASH BLOCK_HASH"
   exit 1
fi

echo -n "${BLOCK_HASH}${CONSENSUS_HASH}" | xxd -r -p | openssl dgst -sha512-256 - | cut -f 2 -d ' '
