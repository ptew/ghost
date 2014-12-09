from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os
from debug import *

BulletinBase = declarative_base()

#TODO Should we have store the subfields for easy access?
# ex, field for transaction id, status, etc

class Bulletin(BulletinBase):
    __tablename__ = "bulletin"
    # id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(128), primary_key=True)
    signed_receipt = Column(String(5000), default="")
    time = Column(String)

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

def bulletin_setup():
    return dbsetup("bulletin", BulletinBase)

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [init-bulletin]" % sys.argv[0]
        exit(1)

    cmd = sys.argv[1]
    if cmd == 'init-bulletin':
        bulletin_setup()
    else:
        raise Exception("unknown command %s" % cmd)
