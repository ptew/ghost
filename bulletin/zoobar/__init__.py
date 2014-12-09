#!/usr/bin/env python

from flask import Flask, g

import view
import zoodb
from debug import catch_err

app = Flask(__name__)

app.add_url_rule("/post", "post", view.post, methods=['GET', 'POST'])
app.add_url_rule("/lookup", "lookup", view.lookup, methods=['GET', 'POST'])

@app.after_request
@catch_err
def disable_xss_protection(response):
    response.headers.add("X-XSS-Protection", "0")
    return response

if __name__ == "__main__":
    app.run()
