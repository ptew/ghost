from flask import g, request
from login import requirelogin
from debug import *

import bank_client as bank
@catch_err
@requirelogin
def transaction():
    if request.args.get('check'):   
        status = bank.process_check(request.args.get('check'))
        return status
    return False
