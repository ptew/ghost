from flask import g, render_template, request
from login import requirelogin
from debug import *
from zoodb import *

import bank_client as bank

@catch_err
@requirelogin
def index():
    username = g.user.person.username
    address = bank.current_address(g.user.person.username)

    if 'client_key' in request.form:
        bank.update_client_key(username, request.form['client_key'])

    return render_template('index.html', address=address)
