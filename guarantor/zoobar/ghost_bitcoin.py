#!/usr/bin/python3

import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import hashlib

import bitcoin
import ghost_blockchain
import bitcoin.rpc
from bitcoin import SelectParams


# SelectParams('mainnet')
SelectParams('testnet')

def getnew():
	proxy = bitcoin.rpc.Proxy()
	newaddress = proxy.getnewaddress()
	print(newaddress)

def send_bitcoins(address,amount):
	proxy = bitcoin.rpc.Proxy()
	transaction = proxy.sendtoaddress(address, amount)
	print(transaction)
	return transaction

def get_balance():
	proxy = bitcoin.rpc.Proxy()
	balance = proxy.getbalance()
	print("balance: " + str(balance))
	return float(balance)

# send_bitcoins('mmHExc9mUChgAsqBVNZ1WVpFa2Do2r9gnR', get_balance()/4)