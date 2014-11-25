from zoodb import *
from debug import *
from flask import g

import time
import auth_client as auth

def transfer(sender, recipient, zoobars, token):

    if auth.check_token(sender, token) == False:
        return False

    db = bank_setup()
    sender_bank = db.query(Bank).get(sender)
    recipient_bank = db.query(Bank).get(recipient)

    sender_balance = sender_bank.zoobars - zoobars
    recipient_balance = recipient_bank.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    sender_bank.zoobars = sender_balance
    recipient_bank.zoobars = recipient_balance
    db.commit()
    
    transfer = Transfer()
    transfer.sender = sender

    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    account = db.query(Bank).get(username)
    return account.zoobars

def register(username):
    db = bank_setup()
    newaccount = Bank()
    newaccount.username = username
    db.add(newaccount)
    db.commit()

def get_log(username):
    db = transfer_setup()
    entries = db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))
    def formatter(transfer):
        return {"time":transfer.time,"sender":transfer.sender, "recipient":transfer.recipient, "amount": transfer.amount}

    return [formatter(entry) for entry in entries]
        







