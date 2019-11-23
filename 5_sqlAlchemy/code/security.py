from werkzeug.security import safe_str_cmp
from resources.user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    # payload is the contents of the JWT token
    # this function extracts the user ID
    user_id = payload['identity']
    return User.find_by_id(user_id)