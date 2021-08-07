#!/bin/bash

set -e

PROGNAME=$0

function usage {
   echo "Usage: $PROGNAME /path/to/chainstate" >/dev/stderr
   if [ -n "$1" ]; then 
      echo "$1" > /dev/stderr
   fi
   exit 1
}

function blockpath {
   local HASH=$1
   local PART1="${HASH:0:4}"
   local PART2="${HASH:4:4}"
   echo "$PART1/$PART2/$HASH"
   return 0
}

test -f "./blockstack-core" || usage "Missing ./blockstack-core.  Hint: run from the rust ./target/{debug|release} directory." 

CHAIN_DIR="$1"
if [ -z "$CHAIN_DIR" ]; then
   usage
fi

STAGING_DB="$CHAIN_DIR/blocks/staging.db"
BLOCKS_DIR="$CHAIN_DIR/blocks/"
HEADERS_DB="$CHAIN_DIR/vm/headers.db"
CLI="./blockstack-core"

NUM_BLOCKS="$(sqlite3 "$STAGING_DB" 'select max(height) from staging_blocks')"
if [ $? -ne 0 ] || [ -z "$NUM_BLOCKS" ]; then 
   echo "Failed to query number of blocks" >/dev/stderr
   exit 1
fi

for BLOCK in $(seq 1 $NUM_BLOCKS); do
   for ROW in $(sqlite3 "$STAGING_DB" "select index_block_hash,anchored_block_hash from staging_blocks where height = $BLOCK"); do
      INDEX_HASH="$(echo $ROW | cut -d '|' -f 1)"
      BLOCK_HASH="$(echo $ROW | cut -d '|' -f 2)"
      BLOCK_PATH="$(blockpath "$INDEX_HASH")"
      SIGNER="$($CLI decode-block "$BLOCKS_DIR"/"$BLOCK_PATH" | grep 'signer' | head -n 1 | sed -r 's/ //g' | cut -d ':' -f 2)"
      PARENT="$($CLI decode-block "$BLOCKS_DIR"/"$BLOCK_PATH" | grep 'parent_block' | head -n 1 | sed -r 's/ //g' | cut -d ':' -f 2)"

      echo "$BLOCK: $BLOCK_HASH: mined by $SIGNER child of $PARENT"
   done
   echo ""
done

