from pymongo import MongoClient

# The MongoDBConnection class is a context manager that allows you to connect to a MongoDB database and perform
# operations on it.
class MongoDBConnection:
    def __init__(self, database):
        self.host = 'localhost'
        self.port = 27017
        self.database = database
        self.client = None

    def __enter__(self):
        self.client = MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.database]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()