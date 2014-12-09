from debug import *
from zoodb import *
import rpclib

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('balance', **keyword_args)

def register(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('register', **keyword_args)

def process_check(check):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'check': check}
        return rpc_client.call('process_check', **keyword_args)
