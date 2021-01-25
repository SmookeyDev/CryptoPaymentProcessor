from flask import Blueprint
import electrum
import os

bitcoinpay = Blueprint('bitcoinpay', __name__)

@bitcoinpay.route('/api/payments/bitcoin/create_wallet')
def bitcoin_create_wallet():
    return electrum