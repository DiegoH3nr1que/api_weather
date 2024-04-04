from django.conf import settings
import pymongo
from weather.exception import WeatherException
from pymongo.errors import ConnectionFailure

class WeatherRepository:

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
        document = self.getColletion().find({})
        return document
    
    def insert(self, document):
        self.getColletion().insert_one(document)

    def delete(self, document) -> None:
        self.getColletion().delete_one(document)

    def deleteAll(self):
        self.getColletion().delete_many({})
