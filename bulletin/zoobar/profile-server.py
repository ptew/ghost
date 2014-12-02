#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import hashlib
import socket
import bank_client as bank
import zoodb

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor
        
        db = zoodb.cred_setup()
        self.user_token = db.query(zoodb.Cred).get(user).token
        
        uid = 60015
        os.setegid(uid)
        os.setgid(uid)
        os.setresuid(uid, uid, uid)
        
    
    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        return bank.get_log(username)

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': p.profile,
                 'zoobars': bank.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank.transfer(self.user, target, zoobars, self.user_token)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        uid = 60015

        userdir = '/tmp'+hashlib.sha512(user).hexdigest()

        try:
            os.mkdir(userdir)
            os.chmod(userdir, 0o1363)
            os.chown(userdir, uid, -1)
        except:
            pass


        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/prflsvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
