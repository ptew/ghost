#!/usr/bin/python

import rpclib
import sys
import bulletin
from debug import *

class BulletinRpcServer(rpclib.RpcServer):
    def rpc_post(self, transaction_id, signed_receipt):
        return bulletin.transfer(transaction, signed_receipt)
    def rpc_lookup(self, transaction_id):
        return bank.balance(username)
(_, dummy_zookld_fd, sockpath) = sys.argv

s = BulletinRpcServer()
s.run_sockpath_fork(sockpath)

