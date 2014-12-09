#!/usr/bin/python

from checkbits import *
import random

#Need to change transaction id for every test
#merchant needs to check for the same transaction_id
transaction_id = 123456789101112131415161718192021222324252627282930 

#1 Satoshi
amount = .00000001

#Ada's Coinbase Account for Receiving
merchant_address = "17tezGZcySJeDWsKYBsDubCEQZWM8YgnKT"
bulletin = "54.68.222.230"

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


#Guarantor address
guarantor_address = "54.69.86.196"


print check
print "Encrypting check"
encrypted_check = make_check(check, signing_key, encrypting_key)
print encrypted_check

print "TEST decryption"


#TODO send encrypted_check to guarantor_address


