from utils import start_db, collection_link
db_handle= start_db()
users = collection_link(db_handle, 'users')

test_new = {
    'firstName': 'testing',
    'lastName': 'views'
}

users.insert_one(test_new)