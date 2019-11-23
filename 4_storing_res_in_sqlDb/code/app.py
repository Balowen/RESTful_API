from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'bart'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth endpoint


api.add_resource(Item,'/item/<string:name>')  
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # if it's not __main__, it means we have imported this file (don't run the app then)
    app.run(port=5000,debug=True)