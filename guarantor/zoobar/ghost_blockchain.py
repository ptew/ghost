#!/usr/bin/python3

from blockchain import pushtx, createwallet
from blockchain.wallet import *

API_CODE='a44bf714-158d-4374-95db-0b7b3d5f5194'
GHOST_BLOCKCHAIN_ADDRESS = '183uPVwF3V9JHy86hXen9FkkLvXU164BmQ'


def create_wallet(password,api_code,private_key=None,label=None,email=None):
	# 	  URL: https://blockchain.info/api/v2/create_wallet
	#     Method: POST or GET

	#     $password The password for the new wallet. Must be at least 10 characters in length.
	#     $api_code An API code with create wallets permission.
	#     $priv A private key to add to the wallet (Wallet import format preferred). (Optional)
	#     $label A label to set for the first address in the wallet. Alphanumeric only. (Optional)
	#     $email An email to associate with the new wallet i.e. the email address of the user you are creating this wallet on behalf of. (Optional)

	# 	Response = {
	#     "guid": "4b8cd8e9-9480-44cc-b7f2-527e98ee3287",
	#     "address": "12AaMuRnzw6vW6s2KPRAGeX53meTf8JbZS",
	#     "link": "https://blockchain.info/wallet/4b8cd8e9-9480-44cc-b7f2-527e98ee3287"
	# }
	wallet_info = blockchain.createwallet.create_wallet(password, api_code, priv=private_key, label=label, email=email)
	print("Wallet Identifier: " + str(wallet_info.identifier))
	print("Wallet Address: " + str(wallet_info.address))
	print("Wallet Link: " + str(wallet_info.link))

	return wallet_info

def push_to_blockchain(hex_transaction):
	blockchain.pushtx.pushtx(hex_transaction)


def send_bitcoins(wallet_obj,recipient, amount, from_address=None, fee=None, note=None):
	# 	"""Send bitcoin from your wallet to a single address.
	# 	:param str to: recipient bitcoin address
	# 	:param int amount: amount to send (in satoshi)
	# 	:param str from_address: specific address to send from (optional)
	# 	:param int fee: transaction fee in satoshi. Must be greater than the default
	# 	fee (optional).
	# 	:param str note: public note to include with the transaction (optional)
	# 	:return: an instance of :class:`PaymentResponse` class
	# 	"""
	return wallet_obj.send(recipient,amount,from_address,fee,note)



# create_wallet("iShJS1kf9o7RwkHjTAzh",API_CODE)