#!/usr/bin/python

import rpclib
import sys
import guarantor
from debug import *

class GuarantorRpcServer(rpclib.RpcServer):
    def rpc_receive_check(self, check):
        return guarantor.receive_check(check)
(_, dummy_zookld_fd, sockpath) = sys.argv

s = GuarantorRpcServer()
s.run_sockpath_fork(sockpath)

