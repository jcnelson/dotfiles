#!/usr/bin/env python2
import time
import socket
import os
import sys
import threading
import virtualchain

def bitcoin_regtest_connect( opts, reset=False ):
    """
    Create a connection to bitcoind -regtest
    """
    bitcoind = virtualchain.default_connect_bitcoind(opts)
    return bitcoind


def bitcoin_regtest_opts(working_dir):
    """
    Get connection options for bitcoind in regtest mode
    """
    return {
        "bitcoind_server": "localhost",
        "bitcoind_port": 18443,
        # "bitcoind_p2p_port": 18444,
        "bitcoind_p2p_port": 18445,
        "bitcoind_user": "blockstack",
        "bitcoind_passwd": "blockstacksystem",
        "bitcoind_use_https": False,
        "bitcoind_timeout": 60,
        "bitcoind_spv_path": os.path.join(working_dir, "spv_headers.dat")
    }


def pinger(working_dir):
    bitcoind = bitcoin_regtest_connect( bitcoin_regtest_opts(working_dir) )
    print dir(bitcoind)
    while True:
        try:
            bitcoind.ping()
            time.sleep(0.25)
        except socket.error:
            bitcoind = bitcoin_regtest_connect( bitcoin_regtest_opts(working_dir) )

if __name__ == "__main__":
    pinger(sys.argv[1])
