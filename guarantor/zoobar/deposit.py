# Using this library as suggested by Parker
from bitcoin import rpc
import time

from zoodb import *
import ghost_blockchain

def check_for_deposits():
    proxy = rpc.Proxy()
    
    # TODO: make sure that deposit service has bank access for updating user balances
    bank_db = bank_setup()
    address_db = address_setup()

    while True:
        addresses = address_db.query(Address).all()
        for addr in addresses:
            
            # should assume that each of these one-time deposit addresses only has a single transaction
            # may need to specify minConf to something greater than 1 later for more insurance
            amount = proxy.getreceivedbyaddress(addr.address)

            # note: we could use listreceivedbyaddress to get all transactions for all addresses to further
            # ensure that each address is used only once (or only one transaction is processed per address)
            
            if amount > 0:
                # get new address and update address_db
                new_address = proxy.getnewaddress()
                address = Address()
                address.address = new_address
                address.bank_id = addr.bank_id
                address_db.add(new_address)

                # mark current address for deletion
                # TODO: not sure if this is the right command, since delete only works on a query
                address_db.delete(addr)
                
                # find user and update user balance
                # deposit address should be one-to-one mapping for user
                user = bank_db.query(Bank).filter(Bank.bank_id == addr.bank_id)[0]
                user.bitcoin_balance += amount
                user.deposit_address = new_address

                # commit changes to user
                bank_db.commit()
        
        # commit all changes after all wallets have been processed
        address_db.commit()
 
        # current pause is 5 minutes
        time.sleep(300)
