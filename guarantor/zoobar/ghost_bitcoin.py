#!/usr/bin/python

import hashlib
from bitcoin import rpc, SelectParams

# SelectParams('mainnet')
SelectParams('testnet')

def getnew():
	proxy = rpc.Proxy()
	newaddress = proxy.getnewaddress()
	print(newaddress)
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
# get_balance()
# send_bitcoins('mmHExc9mUChgAsqBVNZ1WVpFa2Do2r9gnR', get_balance()/4)
