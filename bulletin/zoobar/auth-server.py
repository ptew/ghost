#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    def rpc_post(self, transaction_id, signed_receipt):
        return auth.post(transaction_id, signed_receipt)
    def rpc_lookup(self, transaction_id):
        return auth.lookup(transaction_id)
(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)

