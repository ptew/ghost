import os
import M2Crypto

def empty_callback ():
 return

M2Crypto.Rand.rand_seed (os.urandom (2048))

#If you don't like the default M2Crypto ASCII "progress" bar it makes when generating keys, you can use:
# Alice = M2Crypto.RSA.gen_key (1024, 65537, empty_callback)
#You should probably leave the public exponent at 65537 (http://en.wikipedia.org/wiki/Rsa#Key_generation_2)
Customer = M2Crypto.RSA.gen_key (2048, 65537)
Customer.save_key ('Customer-private.pem', None)
Customer.save_pub_key ('Customer-public.pem')

Guarantor = M2Crypto.RSA.gen_key (2048, 65537)
Guarantor.save_key ('Guarantor-private.pem', None)
Guarantor.save_pub_key ('Guarantor-public.pem')
