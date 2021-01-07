import jwt
from flask import json
import os
import requests

class defHandles:
    def __init__(self):
        self.JWTKEY = os.getenv("JWTKEY")

    def encodeapi(self, argument):
        return jwt.encode(argument, self.JWTKEY, algorithm='HS256')

    def decodeapi(self, argument):
        return jwt.decode(argument, self.JWTKEY, algorithms=['HS256'])
    


class Convert:
    def __init__(self):
        pass

    def Bitcoin(self, deposited_amount):
        crypto_price = requests.get('https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD').json()['quotes']['USD']['price']
        coins = (crypto_price * 100) * deposited_amount
        return "%.0f" % coins

    def Ethereum(self, deposited_amount):
        crypto_price = requests.get('https://api.coinpaprika.com/v1/tickers/eth-ethereum?quotes=USD').json()['quotes']['USD']['price']
        coins = (crypto_price * 100) * deposited_amount
        return "%.0f" % coins

    def Nano(self, deposited_amount):
        crypto_price = requests.get('https://api.coinpaprika.com/v1/tickers/nano-nano?quotes=USD').json()['quotes']['USD']['price']
        coins = (int(crypto_price) * 100) * int(deposited_amount)
        return "%.0f" % coins

        

