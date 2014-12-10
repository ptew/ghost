from debug import *
from zoodb import *
import rpclib

def register(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('register', **keyword_args)

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('balance', **keyword_args)

def new_address(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('new_address', **keyword_args)

def update_client_key(username, key):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username, 'key': key}
        return rpc_client.call('update_client_key', **keyword_args)

def display(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('display', **keyword_args)

def process_check(check):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'check': check}
        return rpc_client.call('process_check', **keyword_args)

def key(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('key', **keyword_args)
