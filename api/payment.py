import json

from urllib.parse import quote_plus, urlencode
from os import environ as env
from flask import redirect, render_template, session, url_for, Blueprint, request

auth_bp = Blueprint('payment', __name__)


import hashlib
import hmac
@auth_bp.route("/webhook")
def webhook():
    signature  = request.headers.get('X-Signature')
    secret = '0EnGHO7rc8bDsbyX2dnsZtyWmvkVpjVr'
    data = request.get_json()
    print(data)
    print(request.body)
    digest = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(digest, signature):
        raise Exception('Invalid signature.')
    token = session["user"]
    print(token)
    return render_template('result.html')





