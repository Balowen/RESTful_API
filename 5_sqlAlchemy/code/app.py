import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.item import Item, ItemList   # in order to create tables
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)                               #   postgres     or     local
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off flask_sqlalchemy modification tracker
app.secret_key = 'bart'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth endpoint

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# if it's not __main__, it means we have imported this file (don't run the app then)
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)