from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'bart'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth endpoint

items = []

# Every resource has to be a class
class Item(Resource):
    parser = reqparse.RequestParser()   # initializes object to parse requests
    parser.add_argument('price',        # only 'price' will go through the parser, the rest is erased
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()     #we have to authenticate before calling get()
    def get(self, name):
        # returns first matching item, parameter is a default value, in case if none is found
        item = next(filter(lambda x: x['name'] == name, items), None)
        # flask-restful does jsonify by itself

        #either matching item and 200 OK, or None and 404 
        return {'item': item}, 200 if item is not None else 404   

    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            # 400 - Bad request
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201    # 201 CREATED

    def delete(self,name):
        global items    # items variable in this block is the global items variable
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        """creates or updates existing item"""   
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')  
api.add_resource(ItemList, '/items')

app.run(port=5000,debug=True)