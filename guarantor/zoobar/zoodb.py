# TODO: remove Transfer and Bank databases

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os
from debug import *

PersonBase = declarative_base()
WalletBase = declarative_base()
CredBase = declarative_base()
BankBase = declarative_base()

class Person(PersonBase):
    __tablename__ = "person"
    username = Column(String(128), primary_key=True)
    profile = Column(String(5000), nullable=False, default="")

class Cred(CredBase):
    __tablename__ = "cred"
    username = Column(String(128), primary_key=True)
    password = Column(String(128))
    token = Column(String(128))
    salt = Column(String(128))

class Bank(BankBase):
    __tablename__ = "bank"
    username = Column(String(128), primary_key=True)
    bank_id = Column(String(128))
    bitcoin_balance = Column(Integer, nullable=False, default=10)

class Wallet(WalletBase):
    __tablename__ = "wallet"
    wallet_address = Column(String(128), primary_key=True)
    wallet_creds = Column(String(128))
    bank_id = Column(String(128))
    balance = Column(Integer, nullable=False, default=0)

def dbsetup(name, base):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    dbdir   = os.path.join(thisdir, "db", name)
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)

    dbfile  = os.path.join(dbdir, "%s.db" % name)
    engine  = create_engine('sqlite:///%s' % dbfile,
                            isolation_level='SERIALIZABLE')
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()

def person_setup():
    return dbsetup("person", PersonBase)

def wallet_setup():
    return dbsetup("wallet", WalletBase)

def cred_setup():
    return dbsetup("cred", CredBase)

def bank_setup():
    return dbsetup("bank", BankBase)

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [init-person|init-wallet|init-cred|init-bank]" % sys.argv[0]
        exit(1)

    cmd = sys.argv[1]
    if cmd == 'init-person':
        person_setup()
    elif cmd == 'init-wallet':
        wallet_setup()
    elif cmd == 'init-cred':
        cred_setup()
    elif cmd == 'init-bank':
        bank_setup()
    else:
        raise Exception("unknown command %s" % cmd)
