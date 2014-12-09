from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto import Random

# Default fields:
# transaction_id
# amount
# merchant_address
# bulletin


def make_check(args, signing_private_key, encrypting_public_key):

    plaintext_check = **args
    if('merchant_address' not in plaintext_check):
        raise ValueError("Merchant address not provided")
    elif ('amount' not in plaintext_check):
	raise ValueError("Amount not found")

    signed_check = sign_check(plaintext_check, signing_private_key)

    encrypted_check = encrypt_check(signed_check, encrypting_public_key)

    return encrypted_check
    
def sign_check(check, key):
    rng = Random.new().read
    hash = MD5.new(plaintext).digest()
    signature = key.sign(hash, rng)

def encrypt_check(check, key):
    rng = Random.new().read
    encrypted = key.encrypt(check)
    return encrypted
   
def verify_check():
    pass 





