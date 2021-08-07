#!/usr/bin/python

import sqlite3
import sys
import blockstack
import blockstack.lib.nameset.db as db
import blockstack.lib.scripts as scripts

DB_PATH = sys.argv[1]
BLOCK_HEIGHT = int(sys.argv[2])

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

addrs = db.namedb_get_all_account_addresses(con)
vesting_addrs = get_all_accounts_vesting(con)

all_addrs = list(set(addrs + vesting_addrs))
all_addrs.sort()

account_balances = {}
for addr in all_addrs:
    account = db.namedb_get_account(con, addr, 'STACKS')
    balance = 0
    if account is not None:
        balance = db.namedb_get_account_balance(account)

    vesting = get_amount_to_vest(con, addr, BLOCK_HEIGHT)

    account_balances[addr] = balance + vesting

for addr in all_addrs:
    if account_balances[addr] > 100000 * 10**6:
        print "{},{}".format(addr, account_balances[addr])
