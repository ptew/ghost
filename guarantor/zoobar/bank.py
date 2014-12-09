from zoodb import *
from debug import *
from flask import g

import auth_client as auth
import ghost_bitcoin as bitcoin
import time
import urllib
import urllib2 as url

# VARIABLES
SUCCESS_CODE = 200

def balance(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    return account.bitcoin_balance

def check_balance(amount, user):
  return amount <= balance(user)

def withdraw(amount, username):
  db = bank_setup()
  account = db.query(Bank).get(username)
  account.balance -= amount
  db.commit()

def register(username):
    db = bank_setup()
    newaccount = Bank()
    newaccount.username = username
    address = bitcoin.getnew()
    newaccount.deposit_address = address
    db.add(newaccount)
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
    else: 
      raise ValueError('Not enough credit. Transaction failed.')

    # Make transaction from guarantor to merchant.
    bitcoin.send_bitcoins(decrypted['merchant_addr'], amount)

    # Post to bulletin via HTTP request
    bulletin_url = decrypted['bulletin']
    params = {'transaction_id': decrypted['transaction_id'], 'signed_receipt': '129ud'}
    req = url.Request(bulletin_url, urllib.urlencode(params))
    handler = url.urlopen(req)

    # Check to see if bulletin posting was successful.
    if handler.getcode() == SUCCESS_CODE:
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
            'bulletin': 'https://bulletin.com',
            'timestamp': 123124}
  return False

# Stubbed out verification.
def verify_signature(check):
  return True
