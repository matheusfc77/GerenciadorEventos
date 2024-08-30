import pymongo
from ModelDAO.Persist.IPersistt import IPersist

class MongoDBPersist(IPersist):

    def __init__(self, name_database, client, collection):
        self.name_database = name_database
        self.client = client
        self.collection = collection

    def getConnection(self):
        myclient = pymongo.MongoClient(self.client)
        mydb = myclient[self.name_database]
        mycol = mydb[self.collection]
        return mycol
    