from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import bank_client as bank

def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password, cred.salt).hexread(32):
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    print "auth register"
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred:
        return None
    newcred = Cred()
    newcred.username = username
    salt = os.urandom(16).encode('base_64')
    newcred.password = pbkdf2.PBKDF2(password, salt).hexread(32)
    newcred.salt = salt
    db.add(newcred)
    db.commit()

    # TODO: register bank account to user
    bank.register(username)

    newperson = Person()
    newperson.username = username
    ndb = person_setup()
    ndb.add(newperson)
    ndb.commit()    

    return newtoken(db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False


