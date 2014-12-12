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

    encrypted_check = encrypt_check(plaintext_check, encrypting_public_key)
    signature = sign_check(encrypted_check, customer)

    #TODO also encrypt signature
    return (encrypted_check, signature)

def encrypt_check(check, guarantor_public_key):
    CipherText = guarantor_public_key.public_encrypt (check, M2Crypto.RSA.pkcs1_oaep_padding)
    print "\nCustomer's encrypted message to Guarantor:"
    print CipherText.encode ('base64')

    return CipherText

def sign_check(check, customer):
    MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
    MsgDigest.update(check)

    signature = customer.sign_rsassa_pss(MsgDigest.digest())
    print "Customer's signature for this message:"
    return signature

def decrypt_check(check, decrypting_key):
    try:
        PlainText = decrypting_key.private_decrypt(check, M2Crypto.RSA.pkcs1_oaep_padding)
    except:
        print "Error: wrong key?"
	PlainText = ""
    
    return json.loads(PlainText)

    
def verify_check(check, signature, ver_signing_key):
    print "Signature verificaton:"
    MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
    MsgDigest.update(check)

    if ver_signing_key.verify_rsassa_pss (MsgDigest.digest(), signature) == 1:
        return True
    else:
        return False


