from db import db, getValues
import json, requests, decimal
import nanolib
from nano.models import Nano
from handles import Convert
from nanolib import *

import threading

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): 
                while not stopped.wait(interval): 
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True 
            t.start()
            return stopped
        return wrapper
    return decorator


def pending(account):
	data = '{"action":"pending","account":"' + account + '"}'
	response = requests.post('https://api.nanex.cc/',data=data)
	return response.json()

def process(block):
	data = {"action": "process", "json_block": "false", "block":json.dumps(block)}
	response = requests.post('https://api.nanex.cc/', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
	return response.json()

def account_balance(account):
	data = '{"action":"account_balance","account":"' + account + '"}'
	response = requests.post('https://api.nanex.cc/', data=data)
	return response.json()

def history(account, count):
	data = '{"action":"account_history","account":"' + account + '", "count": "' + count + '"}'
	response = requests.post('https://api.nanex.cc/',data=data)
	return response.json()

def blocks_info(hashes):
	List = str(hashes).replace("'", "\"")
	data = '{"action":"blocks_info","json_block":"true","hashes":' + List + '}'
	response = requests.post('https://api.nanex.cc/',data=data)
	return response.json()

def receive(address, amount, link, private_key):
	try:
		previous = str(history(address, '1')['history'][0]['hash'])
	except:
		previous = '0'*64
	balancenow = account_balance(address)
	actual_balance = int(balancenow['balance'])
	block = Block(block_type="state",account=address,representative=address,previous=previous,link=link,balance=actual_balance+amount)
	block.sign(private_key)
	print("doing")
	block.solve_work()
	print("made")
	print(block.block_hash)
	hash = process(block.to_dict())
	print(hash)
	return hash    

def receive_pendings(address, private_key):
	pendings = pending(address)['blocks']
	if pendings != '':
		blocks = blocks_info(pendings)
		for x in pendings:
			nanos = int(blocks['blocks'][x]['amount'])
			if nanos >= 10**27:
				receive(address, nanos, x, private_key)
		return pendings
	else:
		return False

def makewithdraw():
	for x in db.pendings.find():
		previous = str(history(x['account'], '1')['history'][0]['hash'])
		balancenow = account_balance(x['account'])
		actual_balance = int(balancenow['balance'])
		amount = int(nanolib.convert(decimal.Decimal(str(x['amount'])), nanolib.NanoDenomination.MEGANANO, nanolib.NanoDenomination.RAW))
		if int(actual_balance) >= int(amount):
			block = Block(block_type="state",account=x['account'],representative=x['account'],previous=previous,link_as_account=x['link_as_account'],balance=int(actual_balance)-int(amount))
			block.sign(x['private_key'])
			print("doing")
			block.solve_work()
			print("made")
			hash = process(block.to_dict())
			print(hash)
			db.pendings.delete_one({'_id': x['_id']})
			Nano().withdraws(x['link_as_account'], x['amount'], x['user_id'], hash)
	getValues().updateprocessing(False)


def makedeposits():
	while True:
		for x in db.users.find({},{ "nano_address": 1, "sequencial_id": 1 }):
			receives = receive_pendings(x['nano_address'], generate_account_private_key(Nano().seed, x['sequencial_id']))
			if receives != False:
				user = db.users.find_one({'sequencial_id': x['sequencial_id']})
				Nano().pendings(account = x['nano_address'], amount = nanolib.convert(decimal.Decimal(str(account_balance(user['nano_address'])['balance'])), nanolib.NanoDenomination.RAW, nanolib.NanoDenomination.MEGANANO), user_id = x['sequencial_id'])
				db.users.update_one({'sequencial_id': user['sequencial_id']}, {"$set": {'balance': user['balance'] + Convert().Nano(nanolib.convert(decimal.Decimal(str(account_balance(user['nano_address'])['balance'])), nanolib.NanoDenomination.RAW, nanolib.NanoDenomination.MEGANANO))}})
		receives = receive_pendings(Nano().CassinoWallet['address'], generate_account_private_key(Nano().seed, 0))
		if receives != False:
			if getValues().processing() == False:
				getValues().updateprocessing(True)
				makewithdraw()

