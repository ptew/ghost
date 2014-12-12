from zoodb import *
from debug import *

import time

#TODO Make sure that there is a little less trust of the fact that these fields will be correct

def post(transaction_id, signed_receipt):
    bulletin = Bulletin()
    bulletin.transaction_id = transaction_id
    bulletin.signed_receipt = signed_receipt
    bulletin.time = time.asctime()

    bulletindb = bulletin_setup()
    bulletindb.add(bulletin)
    bulletindb.commit()
    return True

def lookup(transaction_id):
    db = bulletin_setup()
    # results = db.query(Bulletin).filter(Bulletin.transaction_id==transaction_id)
    return 'signed_receipt'
