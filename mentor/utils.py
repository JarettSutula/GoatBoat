import os
import pymongo
from dotenv import load_dotenv
import certifi

# This starts the connection to the mongo server.
def start_db():
    ca = certifi.where()

    # load the .env file in local directories for DB access.
    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(connection_string, tlsCAfile = ca)
    db_handle = client.get_database('gbmDB')
    db_collection = db_handle.users

    return db_handle, db_collection
