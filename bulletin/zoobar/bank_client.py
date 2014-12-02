from debug import *
from zoodb import *
import rpclib

def transfer(sender, recipient, zoobars, token):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {"sender":sender, "recipient":recipient, "zoobars":zoobars, "token": token}
        return rpc_client.call('transfer', **keyword_args)

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('balance', **keyword_args)

def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('get_log', **keyword_args)

def register(username):
    with rpclib.client_connect('/banksvc/sock') as rpc_client:
        keyword_args = {'username':username}
        return rpc_client.call('register', **keyword_args)
