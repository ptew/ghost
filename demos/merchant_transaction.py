#!/usr/bin/python

import sys
import httplib

#Need to change transaction id for every test
#merchant needs to check for the same transaction_id
transaction_id = ""

#1 Satoshi
amount = .00000001

#Ada's Coinbase Account for Receiving
merchant_address = "17tezGZcySJeDWsKYBsDubCEQZWM8YgnKT"


bulletin = "172.16.148.129"

#Test 1
conn = httplib.HTTPConnection(bulletin)
conn.request("GET", "/post?transaction_id=test1&signed_receipt=test2")
r1 = conn.getresponse()
if r1.read() != 'success!':
    raise ValueError('post did not return success')

conn.request("GET", "/lookup?transaction_id=test1")
r2 = conn.getresponse()
print r2.read()

conn.close()
