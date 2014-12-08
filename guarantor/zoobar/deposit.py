import time

from zoodb import *
# import ghost_bitcoin as bitcoin
import fake_bitcoin as bitcoin

def check_for_deposits():
    # TODO: make sure that deposit service has bank access for updating user balances
    bank_db = bank_setup()

    while True:
        users = bank_db.query(Bank).all()
        for user in users:
            # should assume that each of these one-time deposit addresses only has a single transaction
            # may need to specify minConf to something greater than 1 later for more insurance
            amount = bitcoin.getreceivedbyaddress(user.deposit_address)

            # note: we could use listreceivedbyaddress to get all transactions for all addresses to further
            # ensure that each address is used only once (or only one transaction is processed per address)
            
            if amount > 0:
                user.bitcoin_balance += amount
                new_address = proxy.getnew()
                user.deposit_address = new_address
                bank_db.commit()
 
        # current pause is 5 minutes
        time.sleep(300)
