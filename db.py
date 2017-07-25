import  pymongo
from  config import  *
class dlmongodb:
    def __init__(self):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)
    def initdb(self):
        self.db=self.client.haiguan