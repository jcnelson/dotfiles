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
    sql = "SELECT block_id FROM account_vesting WHERE address = ?1 AND type = 'STACKS' ORDER BY block_id"
    args = (addr,)
    rows = db.namedb_query_execute(con, sql, args)
    
    values = []
    for row in rows:
        if row['block_id'] is not None:
            values.append(int(row['block_id']))

    if len(values) == 0:
        return 0

    return min(values)


def get_vesting_end(con, addr):
    sql = "SELECT block_id FROM account_vesting WHERE address = ?1 AND type = 'STACKS' ORDER BY block_id"
    args = (addr,)
    rows = db.namedb_query_execute(con, sql, args)
    
    values = []
    for row in rows:
        if row['block_id'] is not None:
            values.append(int(row['block_id']))

    if len(values) == 0:
        return 0

    return max(values)


con = sqlite3.connect(DB_PATH)
con.row_factory = row_factory

all_addrs = db.namedb_get_all_account_addresses(con)
all_addrs.sort()

print >> sys.stderr, '{} addresses'.format(len(all_addrs))

account_balances = {}
for (i, addr) in enumerate(all_addrs):
    if i % 100 == 0:
        print >> sys.stderr, '{} queried....'.format(i)

    account = db.namedb_get_account(con, addr, 'STACKS')
    balance = 0
    unlock_height = 0
    if account is not None:
        balance = db.namedb_get_account_balance(account)
        unlock_height = account['lock_transfer_block_id']

    vesting = get_amount_to_vest(con, addr, BLOCK_HEIGHT)

    account_balances[addr] = {
        'balance': balance,
        'locked': vesting,
        'unlock_height': unlock_height,
        'first_unlock': get_vesting_start(con, addr),
        'last_unlock': get_vesting_end(con, addr)
    }

    hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, account_balances[addr]['unlock_height'], allow_none=True)
    if hdr is None:
        now_hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, BLOCK_HEIGHT)
        account_balances[addr]['unlock_height_timestamp'] = now_hdr['timestamp'] + (account_balances[addr]['unlock_height'] - BLOCK_HEIGHT) * 600
        account_balances[addr]['unlock_height_extrapolated'] = True
    else:
        account_balances[addr]['unlock_height_timestamp'] = hdr['timestamp']
        account_balances[addr]['unlock_height_extrapolated'] = False

    hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, account_balances[addr]['first_unlock'], allow_none=True)
    if hdr is None:
        now_hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, BLOCK_HEIGHT)
        account_balances[addr]['first_unlock_timestamp'] = now_hdr['timestamp'] + (account_balances[addr]['first_unlock'] - BLOCK_HEIGHT) * 600
        account_balances[addr]['first_unlock_extrapolated'] = True
    else:
        account_balances[addr]['first_unlock_timestamp'] = hdr['timestamp']
        account_balances[addr]['first_unlock_extrapolated'] = False
    
    hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, account_balances[addr]['last_unlock'], allow_none=True)
    if hdr is None:
        now_hdr = virtualchain.SPVClient.read_header(BLOCK_HEADERS, BLOCK_HEIGHT)
        account_balances[addr]['last_unlock_timestamp'] = now_hdr['timestamp'] + (account_balances[addr]['last_unlock'] - BLOCK_HEIGHT) * 600
        account_balances[addr]['last_unlock_extrapolated'] = True
        
    else:
        account_balances[addr]['last_unlock_timestamp'] = hdr['timestamp']
        account_balances[addr]['last_unlock_extrapolated'] = False


    assert account_balances[addr]['last_unlock'] == 0 or account_balances[addr]['first_unlock'] < account_balances[addr]['last_unlock']

print "address,microSTX,microSTX_locked,spend_unlock_height,spend_unlock_timestamp,spend_unlock_timestamp_extrapolated,first_unlock,first_unlock_timestamp,first_unlock_timestamp_extrapolated,last_unlock,last_unlock_timestamp,last_unlock_timestamp_extrapolated"
for addr in all_addrs:
    c32addr = None
    try:
        c32addr = blockstack.lib.c32.b58ToC32(str(addr))
    except:
        continue

    print "{},{},{},{},{},{},{},{},{},{},{},{}".format(
            c32addr, account_balances[addr]['balance'], account_balances[addr]['locked'], 
            account_balances[addr]['unlock_height'], account_balances[addr]['unlock_height_timestamp'], account_balances[addr]['unlock_height_extrapolated'],
            account_balances[addr]['first_unlock'], account_balances[addr]['first_unlock_timestamp'], account_balances[addr]['first_unlock_extrapolated'],
            account_balances[addr]['last_unlock'], account_balances[addr]['last_unlock_timestamp'], account_balances[addr]['last_unlock_extrapolated'])
