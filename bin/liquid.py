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

addrs = db.namedb_get_all_account_addresses(con)
accounts = {}
for addr in addrs:
    account = db.namedb_get_account(con, addr, 'STACKS')
    accounts[addr] = {
        'account': account,
    }

unlocked_total = 0
for addr in addrs:
    account = accounts[addr]['account']
    if account is None:
        continue
  
    if not scripts.check_address(str(addr)):
        continue

    if account['lock_transfer_block_id'] > BLOCK_HEIGHT:
        continue

    balance = db.namedb_get_account_balance(account)
    if balance == 0:
        continue

    c32addr = blockstack.lib.c32.b58ToC32(str(addr))
    print '{},{}'.format(c32addr, balance)
    unlocked_total += balance

print unlocked_total
