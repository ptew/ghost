from flask import render_template, redirect, request, url_for
from debug import *

import auth_client as bulletin

@catch_err
def index():
    return render_template('layout.html')

@catch_err
def post():
    transaction_id = request.args.get('transaction_id')
    signed_receipt = request.args.get('signed_receipt')
    resp = bulletin.post(transaction_id, signed_receipt)
    return redirect(url_for('index')) 

@catch_err
def lookup():
    transaction_id = request.args.get('transaction_id')
    args['receipt'] = bulletin.lookup(transaction_id)
    return render_template('index.html') 
