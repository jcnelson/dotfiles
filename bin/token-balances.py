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

con = sqlite3.connect(DB_PATH)
con.row_factory = row_factory

all_addrs = db.namedb_get_all_account_addresses(con)
all_addrs.sort()

account_balances = {}
for addr in all_addrs:
    account = db.namedb_get_account(con, addr, 'STACKS')
    balance = 0
    if account is not None:
        balance = db.namedb_get_account_balance(account)

    account_balances[addr] = balance

print "address,microSTX"
for addr in all_addrs:
    if account_balances[addr] > 0:
        print "{},{}".format(addr, account_balances[addr])
