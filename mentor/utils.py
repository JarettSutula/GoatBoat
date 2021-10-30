import os
import pymongo
from dotenv import load_dotenv
import certifi

# This starts the connection to the mongo server.
# if a file wants to access the 'users' collection, call my_db = start_db(),
# then call collection_link(my_db, 'users').
def start_db():
    ca = certifi.where()

    # load the .env file in local directories for DB access.
    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(connection_string, tlsCAfile = ca)
    db_handle = client.get_database('gbmDB')
    # db_collection = db_handle.get_collection(collection)

    return db_handle

# This lets us decide which collection to enter. 
# Reduces need to call start_db() multiple times for multiple collections.
def collection_link(db_handle, collection_name):
    db = db_handle
    return db.get_collection(collection_name)

# generate a day in this format, if 8-10am:
# "day": [{'starttime': 8, 'endtime': 9}, {'starttime': 9, 'endtime': 10}]
def create_day_object(start, end, day_string):
    # validation: if either is -1, return empty array of objects.
    if(start == -1 or end == -1):
        return {day_string:[]}

    # if not, create day object to be returned.
    blocks = []
    # loop through each hour block between start and end.
    for x in range(start, end):
        block = {'starttime':x, 'endtime':x +1}
        blocks.append(block)
    
    # when done, return the array of block objects.
    day = {day_string:blocks}
    return day