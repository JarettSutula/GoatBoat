from django.test import TestCase
import os
import unittest
import pymongo
from dotenv import load_dotenv
import certifi



# Create your tests here.

class TestDatabaseMethods(unittest.TestCase):

    def test_dbconnect(self):
        ca = certifi.where()

        # load the .env file in local directories for DB access.
        load_dotenv()
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

        client = pymongo.MongoClient(connection_string, tlsCAfile = ca)
        db_handle = client.get_database('gbmDB')

        self.assertEqual(db_handle.list_collection_names()[0], 'users') 

    def test_dbcount(self):
        ca = certifi.where()

        # load the .env file in local directories for DB access.
        load_dotenv()
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

        client = pymongo.MongoClient(connection_string, tlsCAfile = ca)
        db_handle = client.get_database('gbmDB')
        db_collection = db_handle.users

        self.assertNotEqual(db_collection.estimated_document_count(), 0)
    

    def connect_db():
        ca = certifi.where()

        # load the .env file in local directories for DB access.
        load_dotenv()
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

        client = pymongo.MongoClient(connection_string, tlsCAfile = ca)
        db_handle = client.get_database('gbmDB')
        
        return db_handle        
        


if __name__ == '__main__':
    unittest.main()

