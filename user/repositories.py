from django.conf import settings
import pymongo
from weather.exception import WeatherException
from pymongo.errors import ConnectionFailure
from bson import ObjectId

class UserRepository:

    collection = ''

    def __init__(self, collectionName) -> None:
        self.collection = collectionName

    def getConnection(self):
        try:
            client = pymongo.MongoClient(
                getattr(settings, "MONGO_CONNECTION_STRING"))
        except ConnectionFailure as e:
            raise WeatherException(f"Error when connecting to database.(e)")
        connection = client[
            getattr(settings, "MONGO_DATABASE_NAME")]
        return connection

    def getColletion(self):
        conn = self.getConnection()
        collection = conn[self.collection]
        return collection
    
    def getAll(self):
        document = []
        for doc in self.getColletion().find({}):
            id = doc.pop('_id')
            doc['id'] = str(id)
            print(doc)
            document.append(doc)
        return document
    
    def getByID(self, id):
        document = self.getColletion().find_one({"_id": ObjectId(id)})
        id = document.pop('_id')
        document['id'] = str(id)
        return document
    
    def insert(self, document):
        self.getColletion().insert_one(document)

    def update(self, document, id):
        self.getColletion().update_one({"_id": ObjectId(id)}, {"$set":document})
    
    def deleteAll(self):
        self.getColletion().delete_many({})

    def deleteById(self, id) -> None:
       ret = self.getColletion().delete_one({"_id": ObjectId(id)})
       return ret.deleted_count
    


    

