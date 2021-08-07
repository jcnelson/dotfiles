#!/usr/bin/env python2

import virtualchain
import os
import sys
import json

headers_path = sys.argv[1]
height = int(sys.argv[2])

f = open(headers_path, "r")
f.seek(81 * height)
hdr = virtualchain.SPVClient.read_header_at(f)

print "bits: {},".format(hdr['bits'])
print "merkle_root: Sha256dHash::from_hex(\"{}\").unwrap(),".format(hdr['merkle_root'])
print "nonce: {},".format(hdr['nonce'])
print "prev_blockhash: Sha256dHash::from_hex(\"{}\").unwrap(),".format(hdr['prev_block_hash'])
print "time: {},".format(hdr['timestamp'])
print "version: 0x{:08x},".format(hdr['version'])

