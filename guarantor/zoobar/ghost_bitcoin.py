#!/usr/bin/python

import hashlib
from bitcoin import rpc, SelectParams

# SelectParams('mainnet')
SelectParams('testnet')

def get_new_address():
    proxy = rpc.Proxy()
    newaddress = str(proxy.getnewaddress())
    return newaddress

def getreceivedbyaddress(address):
    proxy = rpc.Proxy()
    amount = proxy.getreceivedbyaddress(address)
    print(amount)
    return amount

def send_bitcoins(address,amount):
    proxy = rpc.Proxy()
    transaction = proxy.sendtoaddress(address, amount)
    print(transaction)
    return transaction

def get_balance():
    proxy = rpc.Proxy()
    balance = proxy.getbalance()
    print("balance: " + str(balance))
    return float(balance)

# print get_new_address()

# send_bitcoins('mmHExc9mUChgAsqBVNZ1WVpFa2Do2r9gnR', get_balance()/4)
