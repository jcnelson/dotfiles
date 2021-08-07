#!/usr/bin/env python2

import virtualchain
import os
import sys
import json
import sqlite3

headers_path = sys.argv[1]

if os.path.exists("/tmp/bitcoin-headers.db"):
    os.unlink("/tmp/bitcoin-headers.db")

conn = sqlite3.connect("/tmp/bitcoin-headers.db")
conn.execute("""
    CREATE TABLE headers(
        version INTEGER NOT NULL,
        prev_blockhash TEXT NOT NULL,
        merkle_root TEXT NOT NULL,
        time INTEGER NOT NULL,
        bits INTEGER NOT NULL,
        nonce INTEGER NOT NULL,
        height INTEGER PRIMARY KEY NOT NULL     -- not part of BlockHeader, but used by us internally
    );""")

sz = os.stat(headers_path).st_size / 81
f = open(headers_path, "r")
hdrs = []
for i in range(0,sz):
    if i % 100 == 0:
        print "Read headers {}-{}".format(i, i+100)

    f.seek(81 * i)
    hdr = virtualchain.SPVClient.read_header_at(f)

    row = (hdr['version'], hdr['prev_block_hash'], hdr['merkle_root'], hdr['timestamp'], hdr['bits'], hdr['nonce'], i)
    hdrs.append(row)
    
conn.executemany("INSERT INTO HEADERS (version, prev_blockhash, merkle_root, time, bits, nonce, height) VALUES (?,?,?,?,?,?,?)", hdrs)
conn.commit()
