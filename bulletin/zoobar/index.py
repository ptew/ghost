from flask import render_template
from debug import *

@catch_err
def index():
    return render_template('layout.html')
