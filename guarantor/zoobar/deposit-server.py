#!/usr/bin/python

import rpclib
import sys
import deposit
from debug import *

#TODO create method that will manually check a wallet for updates to balance
class DepositRpcServer(rpclib.RpcServer):
     def rpc_update(self, wallet_address):
        return deposit.update(wallet_address)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = DepositRpcServer()
s.run_sockpath_fork(sockpath)
