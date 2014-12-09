from debug import *
import rpclib

def post(transaction_id, signed_receipt):
    with rpclib.client_connect('/bulletinsvc/sock') as rpc_client:
        keyword_args = {'transaction_id':transaction_id, 'signed_receipt':signed_receipt}
        return rpc_client.call('post', **keyword_args)

def lookup(transaction_id, signed_receipt):
    with rpclib.client_connect('/bulletinsvc/sock') as rpc_client:
        keyword_args = {'transaction_id':transaction_id, 'signed_receipt':signed_receipt}
        return rpc_client.call('lookup', **keyword_args)
