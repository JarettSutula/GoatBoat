import os
import pymongo
from dotenv import load_dotenv
import certifi

def start_db():
    """This starts the connection to the mongo server.
    If a file wants to access the 'users' collection, call 
    my_db = start_db(), then call collection_link(my_db, 'users').
    """
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

def collection_link(db_handle, collection_name):
    """Connect to a specific collection given a specified database and
    collection. Reduces need to call start_db() multiple times for
    multiple collections.
    """
    db = db_handle
    return db.get_collection(collection_name)

def create_day_array(start, end):
    """Create an array of one-hour blocks from given start time and 
    end time. Returns an empty array if the start/end time was filled
    as "----", otherwise splits the time given into one-hour objects
    and returns the array of block objects.
    """
    day = []
    # Validation: if either is -1, return empty array.
    if(start == -1 or end == -1):
        return day

    # loop through each hour block between start and end.
    for x in range(start, end):
        block = {'starttime':x, 'endtime':x +1}
        day.append(block)
    
    # When done, return the array of block objects.
    return day