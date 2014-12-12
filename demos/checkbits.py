import json

# Default fields:
# transaction_id
# amount
# merchant_address
# bulletin

import os
import M2Crypto

#Test keys for Customer and Guarantor set up here
from setup_test_keys import *

def make_check(check, signing_private_key, encrypting_public_key):

    plaintext_check = json.dumps(check)
    print "JSON CHECK"
    print plaintext_check

    if('merchant_address' not in check):
        raise ValueError("Merchant address not provided")
    elif ('amount' not in check):
	raise ValueError("Amount not found")

    #signed_check = sign_check(plaintext_check, signing_private_key)

    encrypted_check = encrypt_check(plaintext_check, encrypting_public_key)

    return encrypted_check
    
def sign_check(check, key):
    rng = Random.new().read
    hash = MD5.new(check).digest()
    signature = key.sign(hash, rng)

    print "SIGNATURE"
    print signature[0]
    return str(signature[0])

def encrypt_check(check, key):

    WriteRSA = M2Crypto.RSA.load_pub_key('Guarantor-public.pem')
    CipherText = WriteRSA.public_encrypt (check, M2Crypto.RSA.pkcs1_oaep_padding)
    print "\nAlice's encrypted message to Bob:"
    print CipherText.encode ('base64')
    
    MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
    MsgDigest.update(CipherText)

    Signature = Customer.sign_rsassa_pss(MsgDigest.digest())
    # 2) Print the result
    print "Alice's signature for this message:"
    print Signature.encode ('base64')

def decrypt_check(check, decrypting_key):
    pass


def verify_check():
    pass 



