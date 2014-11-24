#!/usr/bin/python3

import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import hashlib

import bitcoin
import ghost_blockchain
import bitcoin.rpc
from bitcoin.core import *
from bitcoin.core.script import *
from bitcoin import SelectParams
# from bitcoin.core import b2x, b2lx, lx, CTxIn, COIN, MAX_MONEY, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
# from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_RETURN, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

SelectParams('testnet')
# SelectParams('regtest')

BLOCKCHAIN_ADDRESS = '183uPVwF3V9JHy86hXen9FkkLvXU164BmQ'

def send_bitcoins():
	proxy = bitcoin.rpc.Proxy()

	unspent = sorted(proxy.listunspent(0), key=lambda x: hash(x['amount']))

	txins = [CTxIn(unspent[-1]['outpoint'])]
	value_in = unspent[-1]['amount']
	change_addr = proxy.getnewaddress()
	print(change_addr)
	change_pubkey = proxy.validateaddress(change_addr)['pubkey']
	change_out = CMutableTxOut(MAX_MONEY, CScript([change_pubkey, OP_CHECKSIG]))

	digest_outs = [CMutableTxOut(0, CScript([OP_RETURN, digest]))]

	txouts = [change_out] + digest_outs

	tx = CMutableTransaction(txins, txouts)

	print(tx)

	FEE_PER_BYTE = 0.00025*COIN/1000
	while True:
		tx.vout[0].nValue = int(value_in - max(len(tx.serialize()) * FEE_PER_BYTE, 0.00011*COIN))

		r = proxy.signrawtransaction(tx)
		assert r['complete']
		tx = r['tx']

		if value_in - tx.vout[0].nValue >= len(tx.serialize()) * FEE_PER_BYTE:
			print(b2x(tx.serialize()))
			print(len(tx.serialize()), 'bytes')
			print(b2lx(proxy.sendrawtransaction(tx)))
			break

def transfer(address):
	# Create the (in)famous correct brainwallet secret key.
	h = hashlib.sha256(b'correct horse battery staple').digest()
	seckey = CBitcoinSecret.from_secret_bytes(h)

	# Same as the txid:vout the createrawtransaction RPC call requires
	# lx() takes *little-endian* hex and converts it to bytes; in Bitcoin
	# transaction hashes are shown little-endian rather than the usual big-endian.
	# There's also a corresponding x() convenience function that takes big-endian
	# hex and converts it to bytes.
	txid = lx('8e4734d1349cea9c9c4e2a9e201c7dfd833dea89f13d26535e3052d35ad5974a')
	vout = 0

	# Create the txin structure, which includes the outpoint. The scriptSig
	# defaults to being empty.
	txin = CMutableTxIn(COutPoint(txid, vout))

	# We also need the scriptPubKey of the output we're spending because
	# SignatureHash() replaces the transaction scriptSig's with it.
	#
	# Here we'll create that scriptPubKey from scratch using the pubkey that
	# corresponds to the secret key we generated above.
	txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

	# Create the txout. This time we create the scriptPubKey from a Bitcoin
	# address.
	txout = CMutableTxOut(0.001*COIN, CBitcoinAddress(address).to_scriptPubKey())

	# Create the unsigned transaction.
	tx = CMutableTransaction([txin], [txout])

	print(tx)

	# Calculate the signature hash for that transaction.
	sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

	# Now sign it. We have to append the type of signature we want to the end, in
	# this case the usual SIGHASH_ALL.
	sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

	# Set the scriptSig of our transaction input appropriately.
	txin.scriptSig = CScript([sig, seckey.pub])

	# Verify the signature worked. This calls EvalScript() and actually executes
	# the opcodes in the scripts to see if everything worked out. If it doesn't an
	# exception will be raised.
	VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
	print(tx)

	# Done! Print the transaction to standard output with the bytes-to-hex
	# function.
	# print(ghost_blockchain.push_to_blockchain(b2x(tx.serialize())))
	proxy = bitcoin.rpc.Proxy()
	print(b2lx(proxy.sendrawtransaction(tx)))
			

def unspent():
	proxy = bitcoin.rpc.Proxy()

	unspent = proxy.listunspent()
	print(unspent)

# transfer('msj42CCGruhRsFrGATiUuh25dtxYtnpbTx')
# print(unspent())
# transfer('mrSTZyMJrX3KokBpH7FM2ircXiiosDXH2W')



send_bitcoins()

# import hashlib