# import may not work...check https://en.bitcoin.it/wiki/API_reference_(JSON-RPC)
# python documentation seems outdated, maybe switch to the python_bitcoinrpc?
from jsonrpc import ServiceProxy
import time

from zoodb import *
import ghost_blockchain

def check_for_deposits():
    # username:password@address
    access = ServiceProxy('guarantor bitcoin wallet/block?')
    acct = 'specific bitcoin account?'
    wallet_db = wallet_setup()
    
    # TODO: make sure that deposit service has bank access for updating user balances
    bank_db = bank_setup()

    while True:
        wallets = wallet_db.query(Wallet).all()
        for wallet in wallets:
            # TODO: find some way to get transactions for the wallet
            
            # should assume that each of these one-time use wallets only has a single transaction
            if (len(wallet.transactions) > 0):
                transaction = wallet.transactions[0]
                
                # send bitcoins from temp wallet to guarantor wallet
                # TODO: replace arguments with correct method calls or values
                ghost_blockchain.send_bitcoins(wallet.identifier, wallet.wallet_creds, guarantor.address, transaction.amount) 

                # find user and update user balance
                # wallet address should be one-to-one mapping for user
                user = bank_db.query(Bank).filter(Bank.bank_id == wallet.bank_id)[0]
                user.balance += transaction.amount

                # commit changes to user
                bank_db.commit()

                # get new wallet and update wallet_db
                # TODO: update with correct password and api code
                new_wallet_info = ghost_blockchain.create_wallet(some_password, some_api_code)
                new_wallet = Wallet()
                new_wallet.wallet_address = new_wallet_info.address
                new_wallet.wallet_creds = some_password
                new_wallet.bank_id = wallet.bank_id
                wallet_db.add(new_wallet)

                # doesn't the user need to know what one-time-use wallet to deposit to?

                # remove current wallet from wallet_db
                # TODO: not sure if this is the right command, since remove only works on a query
                wallet.remove(False)
        
        # commit all changes after all wallets have been processed
        wallet_db.commit()
 
        # current pause is 5 minutes
        time.sleep(300)
