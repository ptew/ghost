#!/usr/bin/python

import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_register(self, username):
      return bank.register(username)
    def rpc_balance(self, username):
      return bank.balance(username)
    def rpc_update_client_key(self, username, key):
      return bank.update_client_key(username, key)
    def rpc_current_address(self, username):
      return bank.current_address(username)
    def rpc_process_check(self, check):
      return bank.process_check(check)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)