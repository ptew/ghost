from zoodb import *
from debug import *

import time
import urllib
import urllib2 as url
import ghost_blockchain as ghost

from djutils.decorators import async
# import may not work...check https://en.bitcoin.it/wiki/API_reference_(JSON-RPC)
# python documentation seems outdated, maybe switch to the python_bitcoinrpc?
from jsonrpc import ServiceProxy

# use os.urandom? prob doesn't matter for this...
import random

def balance(username):
  db = bank_setup()
  account = db.query(Bank).get(username)
  return account.balance

def check_balance(amount, user):
  return amount <= balance(user)

def withdraw(amount, username):
  db = bank_setup()
  account = db.query(Bank).get(username)
  account.balance -= amount
  db.commit()

# Verifies that check is from valid user. Sends bitcoin transaction to merchant.
def receive_check(check):
  decrypted = decrypt_check(check)
  if decrypted:
    amount = decrypted['amount']
    user = decrypted['username']

    # Update client's balance
    if check_balance(amount, user):
      withdraw(amount, user)
    else
      raise ValueError('Not enough credit. Transaction failed.')

    # Make transaction from guarantor to merchant.
    ghost.make_transaction(decrypted['merchant_addr'], amount)

    # Post to bulletin via HTTP request
    bulletin_url = 'https://bulletin.com'
    params = {'bulletin_id': decrypted['bulletin_id'], 'transaction_id': decrypted['transaction_id']}
    req = url.Request(bulletin_url, urllib.urlencode(params))
    handler = url.urlopen(req)

    # Check to see if bulletin posting was successful.
    if handler.getcode() == 200:
      return True
  return False

# Calls library fn to check signature.
# Decrypts check and returns original message in a dictionary.
def decrypt_check(check):
  isVerified = verify_signature(check)
  if isVerified:
    return {'username': 'ghost'
            'transaction_id': 123,
            'amount': 1,
            'merchant_addr': '12jdb9F',
            'bulletin_id': '124JDKL',
            'timestamp': 123124}
  return False

# Stubbed out verification.
def verify_signature(check):
  return True

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

