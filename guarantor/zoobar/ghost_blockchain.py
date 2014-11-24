#!/usr/bin/python3

import blockchain.createwallet
import blockchain.pushtx

def create_wallet():
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
	wallet = blockchain.createwallet.create_wallet(password, api_code, priv=private_key, label=label, email=email)
	return wallet

def push_to_blockchain(hex_transaction):
	blockchain.pushtx.pushtx(hex_transaction)