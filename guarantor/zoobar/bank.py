from zoodb import *
from debug import *
from flask import g

import time
import auth_client as auth

def balance(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    return account.bitcoin_balance

def register(username):
    db = bank_setup()
    newaccount = Bank()
    newaccount.username = username
    db.add(newaccount)
    db.commit()