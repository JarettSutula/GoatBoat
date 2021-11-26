import os
import pymongo
from dotenv import load_dotenv
import certifi
import re

def start_db():
    """This starts the connection to the mongo server.
    If a file wants to access the 'users' collection, call 
    my_db = start_db(), then call collection_link(my_db, 'users').
    """

    # load the .env file in local directories for DB access.
    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    connection_string = "mongodb+srv://"+DB_USERNAME+":"+DB_PASSWORD+"@gb-mentoring-cluster.jhwgr.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(connection_string, tlsCAfile = certifi.where())
    db_handle = client.get_database('gbmDB')
    
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
    # Ensure input is valid!
    if type(start) != int or type(end) != int:
        raise TypeError('Start and End times must be a valid integer.')

    if (start < 8 and start != -1) or (start > 22):
        raise ValueError('Start value must be in appropriate range.')

    if (end < 8 and end != -1) or (end > 22):
        raise ValueError('End value must be in appropriate range.')
        
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

def get_profile_snapshot(username, full_profile):
    """Returns a user's profile, given the username.
    If we want to get the full profile for matching, return all values.
    If we want to get generic search profile, it will just return the
    values that anyone should be able to see - username, first/last name,
    profession and major.
    """
    profile = {}
   
    # connect to database
    db = start_db()
    users = collection_link(db, 'users')
    attempted_find = users.find_one({'username': username})

    if attempted_find == None:
        # couldn't find username, return something that tells html it doesn't exist.
        profile = {'failed':True}

    else:
        if full_profile:
            # this is for matching.
            profile = {
                'username': attempted_find['username'],
                'firstname': attempted_find['firstname'],
                'lastname': attempted_find['lastname'],
                'email': attempted_find['email'],
                'profession': attempted_find['profession'],
                'major': attempted_find['major'],
                'mentorclasschoice': attempted_find['mentorclasschoice'],
                'menteeclasschoice': attempted_find['menteeclasschoice']
            }

        elif not full_profile:
            # this is for our 'snapshot' for generic profile searching.
            profile = {
                'firstname': attempted_find['firstname'],
                'lastname': attempted_find['lastname'],
                'profession': attempted_find['profession'],
                'major': attempted_find['major']
        }

        # if not passed in somehow, default to empty.
        else:
            profile = {}

    return profile

def restructure_day_array(day):
    """Restructures day array into start times and end times.
    Will be used to fill the editable profile form with correct
    values.
    """
    # day is received as a list [{starttime, endtime}, {startime, endtime}]
    # all are in 1-hour blocks. Only need first and last.
    # if the day we are given is empty, it will be 'false'.
    if not day:
        # return the 'none' values for both start and end times.
        return -1, -1
    else:
        # return the starting value of the first 1-hour block
        starttime = day[0]['starttime']
        # return the ending value of the last 1-hour block
        endtime = day[-1]['endtime']
        return starttime, endtime

def dynamic_class_dropdown(username, role):
    """Restructures class choices to fit in dynamic drop down form."""
    db = start_db()
    users = collection_link(db, 'users')
    our_user = users.find_one({'username': username})

    # fill classes with appropriate user object values
    if role == 'mentor':
        classes = our_user['mentorclasschoice']
    else:
        classes = our_user['menteeclasschoice']

    class_object = []

    # for each course, change it into a key-value pair ('class101') -> ('class101', 'class 101')
    # for django's form dropdown
    for course in classes:
        course_value = re.split('(\d+)', course)
        course_tuple = (course, course_value[0]+" "+course_value[1])
        class_object.append(course_tuple)

    return class_object


