from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

import json

# Default fields:
# transaction_id
# amount
# merchant_address
# bulletin


def make_check(check, signing_private_key, encrypting_public_key):

    plaintext_check = json.dumps(check)
    print "JSON CHECK"
    print plaintext_check

    if('merchant_address' not in check):
        raise ValueError("Merchant address not provided")
    elif ('amount' not in check):
	raise ValueError("Amount not found")

    signed_check = sign_check(plaintext_check, signing_private_key)

    encrypted_check = encrypt_check(signed_check, encrypting_public_key)

    return encrypted_check
    
def sign_check(check, key):
    rng = Random.new().read
    hash = MD5.new(check).digest()
    signature = key.sign(hash, rng)

    print "SIGNATURE"
    print signature[0]
    return str(signature[0])

def encrypt_check(check, key):
    rng = Random.new().read
    key = PKCS1_OAEP.new(key)
    encrypted = key.encrypt(check)
    print "ENCRYPTED CHECK"
    print encrypted
    return encrypted
   
def verify_check():
    pass 



def guarantor_public_key():
    return RSA.importKey("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAns+4VqXtvOeS/agGr70h
n6vjdaWrTL9k4jlHxw0eTbTBn4HgU+KOosmExnNtLZQoEhX+g1fZ0LnfRr/w925X
5HC3MvbEtTVHZs37YivNAERJMzZtcgFuDBcSKbQd9hPgZIgbmy/uy3jiIApuynzW
jokN8qBFQCJGw479SMfeWSvazje7Uk6YE+Jjpc/vSyrFVaJO/xO9uVOlKqtRLwIz
Lxa/10FVXQvXEhKRFwzsDr+DNMyATzl/nLF/+3ewZr0ofE0Vg/eHPiVLsmyKbC5H
2P8UuXEiGbgER6KR8rD5AiJzvti9jRtnhGwSkv2IqqK2MsVbLANRNnW4ZZl6jrJo
kwIDAQAB
-----END PUBLIC KEY-----""")

def guarantor_private_key():
    return RSA.importKey("""-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAns+4VqXtvOeS/agGr70hn6vjdaWrTL9k4jlHxw0eTbTBn4Hg
U+KOosmExnNtLZQoEhX+g1fZ0LnfRr/w925X5HC3MvbEtTVHZs37YivNAERJMzZt
cgFuDBcSKbQd9hPgZIgbmy/uy3jiIApuynzWjokN8qBFQCJGw479SMfeWSvazje7
Uk6YE+Jjpc/vSyrFVaJO/xO9uVOlKqtRLwIzLxa/10FVXQvXEhKRFwzsDr+DNMyA
Tzl/nLF/+3ewZr0ofE0Vg/eHPiVLsmyKbC5H2P8UuXEiGbgER6KR8rD5AiJzvti9
jRtnhGwSkv2IqqK2MsVbLANRNnW4ZZl6jrJokwIDAQABAoIBAQCHziPZ3PznHLSj
O0u0fqzBKTFSysAo2ka/+bG6syol0xv8dgjKUyQcau2i8tP7NQXrKWnDEZ4PEtOv
YbYDMRXyIL1Y1JM0ToJnlF+S/NfKkZpzM+j1o+liZ1w902wHocmyzn2lAKFY2F+u
fJ1vhL/JlcQaphlyFZ2j36QS1+/5Gdm75Rf37dyfMdB0Jc+GZo6D8bhKrPRb/HKK
YHWGxOrEX6r95aet5pS8jIcp3hNXD6gMhaK2buaY1lQ0vvtrxO2HoUaTGkFysVpz
KNJgmRyUNOph6EU3x71XaBWFcCNH3f6dCtgCE4jYAmXlLJnj4DNVJH3GKpFaxLRS
NUsGJQXpAoGBAPml8qr7XoD7417zVpAAwj8iJ6VG0pSbKh0LQqdvdgVDPBDFAmvZ
T4CSq1SMkNxBJnmpTIp9FVasSXhN4rpBcJXdTHdjzL+zLmCkQD7/3MqNDLAIbul8
wK/QOPq5K2yK/3Ih1CnuqhMiXEO3sgtlyRuWnnsDdyBD1gajTcG0dnWnAoGBAKLa
HjWv02fdC48T88xvg12fOLzW2W6ed4WiTE0h8XFzvkrmFIPAok/AEMff26PUnmPw
TmEC6ipbORSo5PMZm7OTe6YtWwAgOzxAnFti1nAfD2kfhaA+zsoB7ZvJISkoo+yu
1v49N3H+kRb7QkjglW+XoDffiEwFMS/TKY2Pbys1AoGBAJtG/7Af14EMqzi0zCOX
hTp1iQlBCtvJwyD7jwLLzjGpxyN7Fm10ZgHHuG9HWxbUIxVLG0OMV4hocu40K5DE
AT4FvnkIByM5VOBhaWCGDpOhtcGMDUiHAuaX8cjpAbxqnEYmCmvmebybA55PFJwI
PFU/kuVam27jIq1QR53zHDdDAoGAVzq+M8OaWWftaRYm4LpagytmGMB8duQq4Umt
1SL5UOvOYhAbrPbh+hXG50jhPUAGF0IAubX19/ok+Qv+lriAzg+Ri9F/jPG2yO9S
0SB//E6m0ogv60W5PjsKKwfw2zsJkx2Ty1q++DCDRuwO9TpW0Q9Goqb5Or8NObDB
8TGDOoECgYEAwW5gk2mSVSo9uQzixu91nUvKAl5IgjHMFKh1nczzQ9JudOs8fji0
jfZACky6fcOWJd3N9ng9TtS4uzLbN67RzuxJewqw1WgNNbZWEjx7Q4HaIyB+DZFt
8j2PjwOPdEn2KrOqBH5QfEZ1+lxVwW6d70FveEc61PmGF1c9AUeAi6A=
-----END RSA PRIVATE KEY-----""")

def customer_private_key():
    return RSA.importKey("""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmP7P8OzVNjKUJTGx/nwge2f77c9kdAuq2N/zoYBqIq8UxsMU
+vjuZN90oW/9AiRH3wptbPR+KCw0Xt7wp1teSDHusYdp5t1xzJcL0gXCQ3fe5Rdu
mnUUIyowZFBqJIsW9pgyxeJpAptlWXkqvSKguOdFcW45PCOjmfU6nvB4WMl4x30k
3d+0TB2MbUpiwIjFRfMNoQ2Od05oamYSytX6SloFgPWl2ukuigg/9GuLoDmkGzLO
ciOzJF1XPZDBRJa+HcRhVAV/pKELZEx+U8zh+608FEMEXP64TNHF5xNbR5L6cxyu
NjX14FlYsoohPhEhR3jklXn+EO3wcHU1/UafiQIDAQABAoIBAC8rsRUJEBursH1f
Ow/JWYJy5vvFS6Vzy3MeaVFL9G1JKdC2aQuQIIA9XQpBKvK0GOytnFtRbmwYZPUz
K2OOCh2cN4nIxGAHuoRntZ9FY0XF+ZUMim9Y1aKZ6V2kZXVq5OOWvWDBk7rYCoFx
mDnEKWWY+JImd8MRAen/79j9Lz3ANU+/M6vSkwrgqcVaY4pc77HWGek8PJfquwHI
lcZEgtPzLN8GtBwLy4k+rRSYtSEk1NLdGn3/BDWNxRLTiwMkuCMz8+BUbp8DtR+z
RaS1o4Fss5V1hLpMTVpwDeAciHs80hLx+pRPjZeRo/GpMoM8Sb67xjA3EcRVqPnW
SbQuzAECgYEA4QPgTfaLJlKyNMJ6jlpvkKCM5PsH0/gZYTA0kaowuEPbAL8ri6up
iO9VERtcMo+7YwZJ5dZ/TFoUz/UjcVZ3dD0egTF6z9F7h86AOlspZNONiUNnJoXC
+QoIbNnKrEGb7Vmc9Js+8Lk5njKfmZ7KFHnHl+KhskoaB9mNSP8yJkkCgYEArhAh
RLw5vCYe/OCawiupIWdsJFlrseEzn3UjF5RqdSDZRAakFFJepEyARdbvJT9/XpsB
N4ZqEYriqF48b3F1K+2E3tbMrtF4UfQazKZsMkq1fWyuBqON2ZQoVv9RI6/fN0RF
P6UfyrT0wn2FEfe50sOjmtggxAsMMfpFAHJnr0ECgYA3/DDo9Pi2Nkkkm2bG2HV9
tJSZvGO8N7SI2+eYfpHUpv1seCQrgjCSY4n00avk4KItBzmHuBDAPIGFJGcHIg5i
m3plhpwZ7PMhXR3GZzwrW/+RMXYOvaU/NWHXQ3EL3t8e9Pb6XU4RsuRFGi9fl4SM
B6jDf53fsFQ9s8FVcjlWEQKBgGXl73PrtOjecDmdyztsj+CMSRSmfJNvwObSji6Z
phDXoBlgweFbrygD2PwJrYpit8/MclPtDl8irTnfoQWkp/GFZMmHed/FpOhlPOMd
ci2m6sR4QRCF4t7DCzKS2Q9JQCV8hAWURx5F/Rt2m9Y+7bvi5/4YFGZwCT2gw5BV
aTmBAoGBAMrFVp5gI9oqrhXcjLbswGuvJO7yVAvSyk6IGeSmEiYQ1NMOg/wDkvyp
dP51BF6t+QfKCBk0Fiqfmmo8qYzxxESqNx9Et6/zVYvxL2LIEjAU4XJkFL6tBDCE
AyLwLe9hx74LKdFB4Dr+WxoMB4CVbgJUNAgmzNClJc9zM0mX+bNb
-----END RSA PRIVATE KEY-----""")

def customer_public_key():
    return RSA.importKey("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmP7P8OzVNjKUJTGx/nwg
e2f77c9kdAuq2N/zoYBqIq8UxsMU+vjuZN90oW/9AiRH3wptbPR+KCw0Xt7wp1te
SDHusYdp5t1xzJcL0gXCQ3fe5RdumnUUIyowZFBqJIsW9pgyxeJpAptlWXkqvSKg
uOdFcW45PCOjmfU6nvB4WMl4x30k3d+0TB2MbUpiwIjFRfMNoQ2Od05oamYSytX6
SloFgPWl2ukuigg/9GuLoDmkGzLOciOzJF1XPZDBRJa+HcRhVAV/pKELZEx+U8zh
+608FEMEXP64TNHF5xNbR5L6cxyuNjX14FlYsoohPhEhR3jklXn+EO3wcHU1/Uaf
iQIDAQAB
-----END PUBLIC KEY-----""")


