from flask import request
import bulletin_client

def post():
    transaction_id = request.args['transaction_id']
    signed_receipt = request.args['signed_receipt']
    bulletin_client.post(transaction_id, signed_receipt)
    return 'success!'

def lookup():
    transaction_id = request.args['transaction_id']
    return bulletin_client.lookup(transaction_id)
