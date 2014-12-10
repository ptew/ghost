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
    def rpc_new_address(self, username):
      return bank.new_address(username)
    def rpc_update_client_key(self, username, key):
      return bank.update_client_key(username, key)
    def rpc_display(self, username):
      return bank.display(username)
    def rpc_process_check(self, check):
      return bank.process_check(check)
    def rpc_key(self, username):
      return bank.key(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)