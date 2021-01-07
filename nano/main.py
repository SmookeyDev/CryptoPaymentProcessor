from flask import Blueprint, jsonify, request
from nanolib import *
from handles import defHandles
from nano.models import Nano
from db import db, getValues
import threading
import requests
import os, uuid, binascii
from nano.processor import makewithdraw, makedeposits
from nano.defs import withdraws

SEED = getValues().nano_seed()
handles = defHandles()
nanopay = Blueprint('nanopay', __name__)

@nanopay.route('/api/payments/nano/create_wallet')
def create_wallet():
    try:
        USER_ID = int(request.args.get('id'))
        wallet_address = generate_account_id(SEED, USER_ID).replace("xrb", "nano")
        if USER_ID == 0:
            return(jsonify(response = handles.encodeapi({'wallet_address': '', 'message': 'dont have permission to get this address','success': False})))
        if db.users.find_one({'sequencial_id': USER_ID}) == None:
            return(jsonify(response = handles.encodeapi({'wallet_address': '', 'message': 'user not found','success': False})))
        db.users.update_one({'sequencial_id': USER_ID}, {"$set":{'nano_address': wallet_address}})
        return(jsonify(response = handles.encodeapi({'wallet_address': wallet_address, 'message': 'created', 'success': True})))
    except ValueError:
        return(jsonify(response = handles.encodeapi({'wallet_address': '', 'message': 'error','success': False})))

@nanopay.route('/api/payments/nano/get_balance/<address>')
def get_balance(address):
    balance = requests.get("https://api.nanex.cc", data='{"action":"account_balance","account":"' + address + '"}').json()
    return(jsonify(response = handles.encodeapi({'wallet_balance': balance['balance_decimal'][:8]})))

@nanopay.route('/api/payments/nano/withdraw', methods=['GET'])
def withdraw():
    USER_ID = int(request.args.get('id'))
    if db.users.find_one({'sequencial_id': USER_ID}) == None:
        return(jsonify(response = handles.encodeapi({'message': 'user not found','success': False})))
    if is_account_id_valid(request.args.get('address')) != True:
        return(jsonify(response = handles.encodeapi({'message': 'the wallet is invalid', 'success': False})))
    if Nano().pendings() == True:
        if getValues().processing() == False:
            getValues().updateprocessing(True)
            withdraws.start()
        return jsonify(response = handles.encodeapi({'message': 'your withdraw will be processed soon', 'success': True}))

@nanopay.route('/api/payments/nano/teste')
def teste():
    deposits.start()
    return 'ok'
