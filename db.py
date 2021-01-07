import pymongo
from handles import Convert

client = pymongo.MongoClient('mongodb://rocketbetprj:xrocket2691bet@cluster0-shard-00-00.xydaa.mongodb.net:27017,cluster0-shard-00-01.xydaa.mongodb.net:27017,cluster0-shard-00-02.xydaa.mongodb.net:27017/rocketbet?ssl=true&replicaSet=atlas-11ufus-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.rocketbet

class getValues:
    def nano_seed(self):
        x = db.sudo.find_one({'_id': '5fed4d2eb83663d8b96bd566'})
        return x['nano_seed']

    def processing(self):
        x = db.sudo.find_one({'_id': '5fed4d2eb83663d8b96bd566'})
        return x['processing']

    def updateprocessing(self, value):
        db.sudo.update_one({'_id': '5fed4d2eb83663d8b96bd566'}, {"$set":{'processing': value}})

