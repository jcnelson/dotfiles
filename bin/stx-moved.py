#!/usr/bin/env python

import requests
import sys

CORE_URL = "http://localhost:6270"
DEBUG = True

def debug(msg):
    if DEBUG:
        print >> sys.stderr, msg

def find_transfers(block_height):
    ret = []
    ops = requests.get(CORE_URL + "/v1/blockchains/bitcoin/operations/{}".format(block_height)).json()
    for op in ops:
        if op['opcode'] == 'TOKEN_TRANSFER' and op['token_units'] == 'STACKS':
            ret.append(op)

    debug("Block {}: {} token ops".format(block_height, len(ret)))
    return ret

start_block_height = int(sys.argv[1])
end_block_height = int(sys.argv[2])

all_ops = []
for i in range(start_block_height, end_block_height):
    block_ops = find_transfers(i)
    all_ops += block_ops

total_debited = sum(int(op['token_fee']) for op in all_ops)
print "Total spent: {}".format(total_debited)
