import json

# Default fields:
# transaction_id
# amount
# merchant_address
# bulletin

import os
import M2Crypto

def make_check(check, customer, encrypting_public_key):

    plaintext_check = json.dumps(check)
    print "JSON CHECK"
    print plaintext_check

    if('merchant_address' not in check):
        raise ValueError("Merchant address not provided")
    elif ('amount' not in check):
	raise ValueError("Amount not found")

    return encrypt_check(plaintext_check, customer, encrypting_public_key)
    
def encrypt_check(check, customer, guarantor_public_key):

    CipherText = guarantor_public_key.public_encrypt (check, M2Crypto.RSA.pkcs1_oaep_padding)
    print "\nCustomer's encrypted message to Guarantor:"
    print CipherText.encode ('base64')
    
    MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
    MsgDigest.update(CipherText)

    Signature = customer.sign_rsassa_pss(MsgDigest.digest())
    print "Customer's signature for this message:"
    print Signature.encode ('base64')

def decrypt_check(check, decrypting_key):
    pass


def verify_check():
    pass 



