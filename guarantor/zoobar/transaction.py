from flask import g, redirect, request, url_for
from login import requirelogin
from debug import *

import bank_client as bank
@catch_err
@requirelogin
def transaction():
    if request.args.get('check'):   
        bank.process_check(request.args.get('check'))
    return redirect(url_for('index'))
