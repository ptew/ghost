from djutils.decorators import async
# import may not work...check https://en.bitcoin.it/wiki/API_reference_(JSON-RPC)
# python documentation seems outdated, maybe switch to the python_bitcoinrpc?
from jsonrpc import ServiceProxy
import time

# use os.urandom? prob doesn't matter for this...
import random

@async
def process_deposits(transactions):
    for t in transactions:
        if t["category"] == "receive":
            # extract user, deposit id, amount
            ### have block and account, what to do? where is deposit id?
            ### how to map deposit id to user?
            # verify deposit id
            # increase user balance by amount
            # generate new deposit id
            break

@async
def check_for_deposits():
    # username:password@address
    access = ServiceProxy('guarantor bitcoin wallet/block?')
    acct = 'specific bitcoin account?'
    current = 0
    while True:
        # will get up to count = 25 (by default) of the most recent transactions
        new_transactions = access.listtransactions(account = acct, offset = current)["transactions"]
        process_deposits(new_transactions)

        # update offset
        current += len(new_transactions)
        
        # current pause is 5 minutes
        time.sleep(300)
