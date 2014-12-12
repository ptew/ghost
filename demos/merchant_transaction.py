#!/usr/bin/python

import requests

#Need to change transaction id for every test
#merchant needs to check for the same transaction_id
transaction_id = ""

#1 Satoshi
amount = .00000001

#Ada's Coinbase Account for Receiving
merchant_address = "17tezGZcySJeDWsKYBsDubCEQZWM8YgnKT"

# URLS
# Replace with your bulletin
bulletin = "172.16.148.129"
bulletin_url = "http://" + bulletin + ":8080/zoobar/index.cgi"
post_url = bulletin_url + "/post?"
lookup_url = bulletin_url + "/lookup?"

# Test Post
post_params = {'transaction_id': 'test1', 'signed_receipt': 'test2'}
r1 = requests.get(post_url, params=post_params)
if r1.text != 'success!':
  raise ValueError('post did not return success')

# Test Lookup
lookup_params = {'transaction_id': 'test1'}
r2 = requests.get(lookup_url, params=lookup_params)
if r2.text != 'test2':
  raise ValueError('incorrect lookup.')

print 'All merchant tests passed!'
