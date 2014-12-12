#!/usr/bin/python

from checkbits import *
import random
import requests

#Need to change transaction id for every test
#merchant needs to check for the same transaction_id
transaction_id = 123456789101112131415161718192021222324252627282930 

#1 Satoshi
amount = .00000001

#Ada's Coinbase Account for Receiving
merchant_address = "17tezGZcySJeDWsKYBsDubCEQZWM8YgnKT"

#Guarantor address
guarantor = "172.16.148.129"
bulletin = "172.16.148.129"


check = {}
check['transaction_id'] = transaction_id
check['amount'] = amount
check['merchant_address'] = merchant_address
check['bulletin'] = bulletin
check['randomness'] = random.getrandbits(40)
#TODO padding?

#TODO set up working signing and decrypting keys
signing_key = customer_private_key()
encrypting_key = guarantor_public_key()

print "SIGNING KEY"
print signing_key

print "ENCRYPTING KEY"
print encrypting_key

print check
print "Encrypting check"
encrypted_check = make_check(check, signing_key, encrypting_key)
print encrypted_check

print "TEST decryption"

#Test Guarantor
guarantor_url = "http://" + guarantor + ":8080/zoobar/index.cgi"
transaction_url = guarantor_url + "/transaction?"
check_params = {'check': encrypted_check}
r1 = request.get(transaction_url, params=check_params)
if r1.text != True:
  print r1.text
  raise ValueError('Transaction failed.')

conn = httplib.HTTPConnection(guarantor)
conn.request("GET", "/post?transaction_id=transaction_id&signed_receipt=signed_receipt")
r1 = conn.getresponse()
if r1.read() != 'success!':
    raise ValueError('post did not return success')

conn.request("GET", "/lookup?transaction_id=transaction_id")
r2 = conn.getresponse()
print r2.read()

conn.close()


#Test Bulletin
conn = httplib.HTTPConnection(bulletin)
conn.request("GET", "/post?transaction_id=transaction_id&signed_receipt=signed_receipt")
r1 = conn.getresponse()
if r1.read() != 'success!':
    raise ValueError('post did not return success')

conn.request("GET", "/lookup?transaction_id=test1")
r2 = conn.getresponse()
print r2.read()

conn.close()



#TODO send encrypted_check to guarantor_address


