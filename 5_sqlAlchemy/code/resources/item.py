import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


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
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred finding the item."}, 500  # Internal Server Error

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

        #either matching item and 200 OK, or None and 404 
           
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # 400 - Bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500    # Internal Server Error

        return item.json(), 201    # 201 CREATED
   
    def delete(self,name):
        if ItemModel.find_by_name(name) is None:
            return {'message': "An item with name '{}' doesn't exists.".format(name)}, 400  # 400 - Bad request
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        """Insert an item or update existing item"""   
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()
    

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}