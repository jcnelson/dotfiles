#!/usr/bin/python

import sqlite3
import sys
import blockstack
import blockstack.lib.nameset.db as db
import blockstack.lib.scripts as scripts
import virtualchain

DB_PATH = sys.argv[1]
BLOCK_HEIGHT = int(sys.argv[2])
BLOCK_HEADERS = "/home/jude/debian-testing/home/debian/.virtualchain-spv-headers.dat"
ADDRESS = "1AtPvrrMiuBdoA6R6atZpgfLsRM7V9ep1W" # this is "SP1P72Z3704VMT3DMHPP2CB8TGQWGDBHD3RPR9GZS" -- Binance's hot wallet
if len(sys.argv) > 3:
    ADDRESS = sys.argv[3]

def row_factory( cursor, row ):
    """
    Row factor to enforce some additional types:
    * force 'revoked' to be a bool
    """
    d = {}
    for idx, col in enumerate( cursor.description ):
        if col[0] in ['revoked', 'locked', 'receive_whitelisted']:
            if row[idx] == 0:
                d[col[0]] = False
            elif row[idx] == 1:
                d[col[0]] = True
            elif row[idx] is None:
                d[col[0]] = None
            else:
                raise Exception("Invalid value for 'revoked': %s" % row[idx])

        elif col[0] in ['credit_value', 'debit_value', 'vesting_value', 'token_fee']:
            # convert back to int.
            # this is safe in Python, since Python ints don't overflow
            try:
                d[col[0]] = int(row[idx]) if row[idx] is not None else None
            except ValueError as ve:
                log.exception(ve)
                log.fatal("Caught exception while converting '{}' to an int".format(row[idx]))
                os.abort()

        else:
            d[col[0]] = row[idx]

    return d

def get_addresses_sent_or_received(con, addr):
    sql = "SELECT DISTINCT txid FROM accounts WHERE type = 'STACKS' AND address = ?1 AND vtxindex > 0 ORDER BY block_id,vtxindex"
    args = (addr,)
    txids = []
    rows = db.namedb_query_execute(con, sql, args)
    for row in rows:
        txids.append(row['txid'])

    addrs = set([])
    for txid in txids:
        sql = "SELECT history_id FROM history WHERE txid = ?1 AND vtxindex > 0 ORDER BY block_id,vtxindex"
        args = (txid,)
        rows = db.namedb_query_execute(con, sql, args)
        for row in rows:
            addrs.add(row['history_id'])

    return list(addrs)

def get_all_accounts_vesting(con):
    sql = "SELECT DISTINCT address FROM account_vesting WHERE type = 'STACKS'"
    args = ()
    addrs = []
    rows = db.namedb_query_execute(con, sql, args)
    for row in rows:
        addrs.append(row['address'])

    return addrs

def get_amount_to_vest(con, addr, block_height):
    sql = "SELECT SUM(vesting_value) FROM account_vesting WHERE address = ?1 AND type = 'STACKS' AND block_id >= ?2"
    args = (addr, block_height)
    rows = db.namedb_query_execute(con, sql, args)
    values = []
    for row in rows:
        if row['SUM(vesting_value)'] is not None:
            values.append(int(row['SUM(vesting_value)']))
        else:
            values.append(0)

    assert len(values) == 1
    return values[0]


def get_vesting_start(con, addr):
    sql = "SELECT block_id FROM account_vesting WHERE address = ?1 AND type = 'STACKS' ORDER BY block_id ASC LIMIT 1"
    args = (addr,)
    rows = db.namedb_query_execute(con, sql, args)
    
    values = []
    for row in rows:
        if row['block_id'] is not None:
            values.append(int(row['block_id']))

    if len(values) == 0:
        return 0

    return values[0]


con = sqlite3.connect(DB_PATH)
con.row_factory = row_factory

all_addrs = get_addresses_sent_or_received(con, ADDRESS)
all_addrs.sort()

account_balances = {}
for addr in all_addrs:
    account = db.namedb_get_account(con, addr, 'STACKS')
    balance = 0
    if account is not None:
        balance = db.namedb_get_account_balance(account)

    vesting = get_amount_to_vest(con, addr, BLOCK_HEIGHT)

    account_balances[addr] = {
        'balance': balance,
        'locked': vesting,
        'unlock_height': account['lock_transfer_block_id'],
        'first_unlock': get_vesting_start(con, addr)
    }

    hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, account_balances[addr]['unlock_height'])
    account_balances[addr]['unlock_height_timestamp'] = hdr['timestamp']

    hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, account_balances[addr]['first_unlock'])
    account_balances[addr]['first_unlock_timestamp'] = hdr['timestamp']


print 'address,balance_microSTX,locked_microSTX,unlock_block_height,unlock_timestamp,first_unlock_block_height,first_unlock_timestamp'
for addr in all_addrs:
    print "{},{},{},{},{},{},{}".format(blockstack.c32.b58ToC32(str(addr)), account_balances[addr]['balance'], account_balances[addr]['locked'], account_balances[addr]['unlock_height'], account_balances[addr]['unlock_height_timestamp'], account_balances[addr]['first_unlock'],account_balances[addr]['first_unlock_timestamp'])
