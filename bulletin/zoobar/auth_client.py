from debug import *
from zoodb import *
import rpclib

def login(username, password):
    with rpclib.client_connect('/authsvc/sock') as rpc_client:
        keyword_args = {"username":username, "password":password}
        return rpc_client.call('login', **keyword_args)

def register(username, password):
    with rpclib.client_connect('/authsvc/sock') as rpc_client:
        keyword_args = {"username":username, "password":password}
        return rpc_client.call('register', **keyword_args)

def check_token(username, token):
    with rpclib.client_connect('/authsvc/sock') as rpc_client:
        keyword_args = {"username":username, "token":token}
        return rpc_client.call('check_token', **keyword_args)
