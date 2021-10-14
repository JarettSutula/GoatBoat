from utils import start_db
db_handle, users = start_db()

test_new = {
    'firstName': 'testing',
    'lastName': 'views'
}

users.insert_one(test_new)