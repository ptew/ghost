#!/usr/bin/python

from checkbits import *
import random
import httplib

from setup_test_keys import *

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

signing_key = M2Crypto.RSA.load_pub_key ('Customer-private.pem')
encrypting_key = M2Crypto.RSA.load_pub_key ('Guarantor-public.pem')

print check
print "Encrypting check"
encrypted_check = make_check(check, signing_key, encrypting_key)
print encrypted_check

versigning_key = M2Crypto.RSA.load_pub_key ('Customer-public.pem')
decrypting_key = M2Crypto.RSA.load_pub_key ('Guarantor-private.pem')

print "TEST decryption"
decrypted_check = decrypt_check(encrypted_check, decrypting_key, versigning_key)
print decrypted_check

#Send check to Guarantor
conn = httplib.HTTPConnection(guarantor)
conn.request("GET", "/transaction?check=encrypted_check")
r1 = conn.getresponse()
if r1.read() != 'success!':
    raise ValueError('post did not return success')
conn.close()


#Check for receipt on Bulletin
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


