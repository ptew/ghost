#!/usr/bin/python

from checkbits import *
import random
import requests

from setup_test_keys import *

import os
import M2Crypto

import json

#Need to change transaction id for every test
#merchant needs to check for the same transaction_id
transaction_id = 123456789101112131415161718192021222324252627282930 

#1 Satoshi
amount = .00000001

#Ada's Coinbase Account for Receiving
merchant_address = "17tezGZcySJeDWsKYBsDubCEQZWM8YgnKT"

#Guarantor address
guarantor = "172.16.148.129/zoobar/index.cgi"
bulletin = "172.16.148.129"


check = {}
check['transaction_id'] = transaction_id
check['amount'] = amount
check['merchant_address'] = merchant_address
check['bulletin'] = bulletin
check['randomness'] = random.getrandbits(40)

signing_key = M2Crypto.RSA.load_key ('Customer-private.pem')
encrypting_key = M2Crypto.RSA.load_pub_key ('Guarantor-public.pem')

check = json.dumps(check)
print check

print "\n\nTEST Encrypting check"
encrypted_check = encrypt_check(check, encrypting_key)
print encrypted_check

print "\n\nTEST Signing check"
signature = sign_check(check, signing_key)
print signature

ver_signing_key = M2Crypto.RSA.load_pub_key ('Customer-public.pem')
decrypting_key = M2Crypto.RSA.load_key ('Guarantor-private.pem')

print "\n\nTEST Decryption"
decrypted_check = decrypt_check(encrypted_check, decrypting_key)
print decrypted_check

print "\n\nTEST verification"
verification = verify_check(decrypted_check, signature, ver_signing_key)
print verification


#Send check to Guarantor
guarantor_url = "http://" + guarantor + ":8080/zoobar/index.cgi"
transaction_url = guarantor_url + "/transaction?"
check_params = {'check': encrypted_check}
r1 = request.get(transaction_url, params=check_params)
if r1.text != True:
  print r1.text
  raise ValueError('Transaction failed.')

#Check for receipt on Bulletin
conn = httplib.HTTPConnection(bulletin)
conn.request("GET", "/lookup?transaction_id=transaction_id")
r2 = conn.getresponse()
print r2.read()

conn.close()

