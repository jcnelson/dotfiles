#!/usr/bin/python

import sqlite3
import sys
import blockstack
import blockstack.lib.nameset.db as db
import blockstack.lib.scripts as scripts

DB_PATH = sys.argv[1]
BLOCK_HEIGHT = int(sys.argv[2])
ADDRESS = "1AtPvrrMiuBdoA6R6atZpgfLsRM7V9ep1W" # this is "SP1P72Z3704VMT3DMHPP2CB8TGQWGDBHD3RPR9GZS"
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

def get_addresses_sent_to(con, dest_addr):
    sql = "SELECT DISTINCT history.history_id FROM history JOIN accounts ON history.txid = accounts.txid WHERE accounts.type = 'STACKS' AND accounts.address = ?1 AND history.vtxindex > 0 ORDER BY history.block_id,history.vtxindex"
    args = (dest_addr,)
    addrs = []
    rows = db.namedb_query_execute(con, sql, args)
    for row in rows:
        addrs.append(row['history_id'])

    return addrs

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

con = sqlite3.connect(DB_PATH)
con.row_factory = row_factory

all_addrs = get_addresses_sent_to(con, ADDRESS)
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
        'locked': vesting
    }

print 'address,balance_microSTX,locked_microSTX'
for addr in all_addrs:
    print "{},{},{}".format(addr, account_balances[addr]['balance'], account_balances[addr]['locked'])
