import bcrypt
from utils import start_db, collection_link
# import argparse
# import sys
import logging

# This is a TEMPORARY test file that shows how to do logins for GoatBoat.
# We can encode and hash plaintext passwords using bcrypt,
# then we can safely store those hashed passwords in the DB without worrying
# about anything safety/privacy related.

# start the DB connection and save the collections as vars.
db_name = start_db()
logins = collection_link(db_name, 'logins')
users = collection_link(db_name, 'users')

# makeshift account creation in the collection "logins" to test this.
logging.Logger.info("account creation\n")
username = input("username: ")
password = input("password: ")

# bcrypt requires passwords to be encoded before they are hashed.
byte_pswd = password.encode('UTF-8')

# hash the plaintext password.
new_pswd = bcrypt.hashpw(byte_pswd, bcrypt.gensalt())

# make a test user for 'logins' and create it here with hashed password.
test_user = {
    'username': username,
    'password': new_pswd
}

logins.insert_one(test_user)

# now that the basic test user is in the database, let's 'log in' to the account.
logging.Logger.info('\nlogin time woohoo')
done = False

# simple loop to keep asking for login if it is wrong.
# ask for username/password, check collection for object with that name, compare passwords.
while(not done):
    logging.Logger.debug("what is your username")
    login_user = input("what is your username? ")
    logging.Logger.debug("what is your password")
    login_pswd = input("what is your password? ")

    # encode - needs to be encoded to compare to Hashed password in DB.
    attempted_pswd = login_pswd.encode('UTF-8')
    
    # grab the user's object from the database by username.
    attempted_find = logins.find_one({'username': login_user})
    logging.Logger.debug("get user object from DB by username")
    
    # pymongo returns none if there is no object in DB with said username.
    if attempted_find == None:
        logging.Logger.warning("wrong username, try again.")

    # check the encoded plaintext pswd with hashed pswd in the object from DB.
    elif bcrypt.checkpw(attempted_pswd, attempted_find['password']):
        # if they match, we are good and can finish. in real time, this would likely
        # bring the user to their profile now that they have logged in.
        logging.Logger.info("it matches! yay!")
        done = True

    # this means the user has correct username but wrong password. Probably not best practice.
    # not really important in the scope - later, just do 'invalid username or password' so 
    # security is better.
    else:
        logging.Logger.warning("incorrect password, try again.")
  

# example hashed binary passwords.
# b'$2b$12$VCCAWilr3Fueq6wmoaeZcu2iSqHNJTASNRJZwqUK2jh4VxSKQIrwK'
# b'$2b$12$OBMGNV4n2sAAAVm9PB.IG.jjB.p0/Of8Ky12zmgqRqLDl0fu0e4wO'
