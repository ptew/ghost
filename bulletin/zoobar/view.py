# from flask import request
# import bulletin_client

# def post():
#     transaction_id = request.args['transaction_id']
#     signed_receipt = request.args['signed_receipt']
#     bulletin_client.post(transaction_id, signed_receipt)
#     return 'success!'

# def lookup():
#     transaction_id = request.args['transaction_id']
#     return bulletin_client.lookup(transaction_id)
from flask import render_template, redirect, request, url_for
from debug import *

import auth_client as bulletin

@catch_err
def post():
    transaction_id = request.args.get('transaction_id')
    signed_receipt = request.args.get('signed_receipt')
    resp = bulletin.post(transaction_id, signed_receipt)
    if resp:
      message = "Success!"
    else:
      message = "Failed."
    return render_template('index.html', message=message)

@catch_err
def lookup():
    transaction_id = request.args.get('transaction_id')
    args['message'] = bulletin.lookup(transaction_id)
    return render_template('index.html', **args) 