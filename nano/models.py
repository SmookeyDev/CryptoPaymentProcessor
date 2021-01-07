from flask import jsonify, request
from db import db, getValues
import uuid, decimal, os
from nanolib import *

class Nano:

    def __init__(self):
        self.seed = getValues().nano_seed()

        self.CassinoWallet = {'address': get_account_id(private_key = generate_account_private_key(self.seed, 0), prefix = AccountIDPrefix.NANO), 'private_key': generate_account_private_key(self.seed, 0)}

    def pendings(self, **kwargs):

        if not kwargs:
            account = self.CassinoWallet['address']
            amount = float(decimal.Decimal(request.args.get('amount')))
            link_as_account = request.args.get('address')
            private_key = self.CassinoWallet['private_key']
            user_id = request.args.get('id')
        else:
            account = kwargs['account']
            amount = kwargs['amount']
            private_key = generate_account_private_key(self.seed, int(kwargs['user_id']))
            link_as_account = self.CassinoWallet['address']
            user_id = kwargs['user_id']

        pendings = {
            "_id": uuid.uuid4().hex,
            "account": account,
            "amount": float(decimal.Decimal(amount)),
            "link_as_account": link_as_account,
            "private_key": private_key,
            "user_id": user_id,
            }

        db.pendings.insert_one(pendings)
        return True
        
    def withdraws(self, link_as_account, amount, user_id, hash):

        withdraws = {
            "_id": uuid.uuid4().hex,
            "link_as_account": link_as_account,
            "amount": amount,
            "user_id": user_id,
            "hash": hash['hash']
        }

        db.withdraws.insert_one(withdraws)