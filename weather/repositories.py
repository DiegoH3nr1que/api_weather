# repositories.py

from django.conf import settings
import pymongo

class WeatherRepository:

    collection = ''
    
    def __init__(self, collectionName) -> None:
        self.collection = collectionName
        
    def getConnection(self):
        stringConnection = getattr(settings, "MONGO_CONNECTION_STRING")
        database = getattr(settings, "MONGO_DATABASE_NAME")
        client = pymongo.MongoClient(stringConnection)
        connection = client[database]
        return connection
        
    def getCollection(self):
        connection = self.getConnection()
        collection = connection[self.collection]
        return collection


#CRUD
    
    def GetById(self):
        pass

    def GetAll(self):
        document = self.getCollection().find({})
        
    def GetByAttribute(self, attribute, value):
        pass

    def insert(self, document)-> None:
        self.getCollection().insert_one(document)

    def delete(self, document) -> None:
        pass

    def deleteAll(self, document) -> None:
        pass