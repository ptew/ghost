from zoodb import *
from debug import *

import auth_client as auth
# import ghost_bitcoin as bitcoin
import fake_bitcoin as bitcoin
import time
import requests

# VARIABLES
SUCCESS_CODE = 200

def balance(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    print account
    return account.bitcoin_balance

def new_address(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    account.deposit_address = bitcoin.get_new_address()
    db.commit()

def update_client_key(username, key):
    db = bank_setup()
    account = db.query(Bank).get(username)
    account.client_key = key
    db.commit()

def display(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    return {'address': account.deposit_address, 'key': account.client_key}

def check_balance(amount, user):
  return amount <= balance(user)

def withdraw(amount, username):
  db = bank_setup()
  account = db.query(Bank).get(username)
  account.bitcoin_balance -= amount
  db.commit()

def register(username):
    print "REGISTERING: " + username
    db = bank_setup()
    newaccount = Bank()
    newaccount.username = username
    newaccount.deposit_address = bitcoin.get_new_address()
    newaccount.balance = 0
    db.add(newaccount)
    db.commit()

# Verifies that check is from valid user. Sends bitcoin transaction to merchant.
def process_check(check):
  decrypted = decrypt_check(check)
  if decrypted:
    amount = decrypted['amount']
    user = decrypted['username']
    transaction_id = decrypted['transaction_id']

    # Update client's balance
    if check_balance(amount, user):
      withdraw(amount, user)
    else: 
      raise ValueError('Not enough credit. Transaction failed.')

    # Make transaction from guarantor to merchant.
    bitcoin.send_bitcoins(decrypted['merchant_addr'], amount)
    signed_receipt = make_receipt(transaction_id)

    # Post to bulletin via HTTP request
    bulletin_url = decrypted['bulletin']
    params = {'transaction_id': transaction_id, 'signed_receipt': signed_receipt}
    #r = requests.post(bulletin_url, data=params)

    # Check to see if bulletin posting was successful.
    # if r.status_code == SUCCESS_CODE:
      # return True
  return True

# TODO: actually sign receipt
def make_receipt(transaction_id):
    return 'encyrpted and signed!: ' + str(transaction_id) + str(time.time())

# Calls library fn to check signature.
# Decrypts check and returns original message in a dictionary.
def decrypt_check(check):
  isVerified = verify_signature(check)
  if isVerified:
    return {'username': 'ghost',
            'transaction_id': 123,
            'amount': 1,
            'merchant_addr': '12jdb9F',
            'bulletin': 'http://google.com',
            'timestamp': 123124}
  return False

def key(username):
  db = bank_setup()
  account = db.query(Bank).get(username)
  return account.client_key

# Stubbed out verification.
def verify_signature(check):
  return True
