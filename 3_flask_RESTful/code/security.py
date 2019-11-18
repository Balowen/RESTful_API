from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', '1234')
]

# Set comprehension // u.username is u, for u in users
username_mapping = { u.username: u for u in users}
userid_mapping = { u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None) # None is a default value
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    # payload is the contents of the JWT token
    # this function extracts the user ID
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)