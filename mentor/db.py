import os
import pymongo
from dotenv import load_dotenv
import certifi
ca = certifi.where()

# load the .env file in local directories for DB access.
load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
client = pymongo.MongoClient("mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority", tlsCAfile = ca)

#
db = client.get_database('gbmDB')
users = db.users

# change this locally to your name to add a test user!
new_user = {
    'firstName': 'Jarett',
    'lastName': 'Sutula'
}
users.insert_one(new_user)
