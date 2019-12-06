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
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

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

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500    # Internal Server Error

        return item.json(), 201    # 201 CREATED

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        """Insert an item or update existing item"""   
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # data['price'], data['store_id']
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()
    

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}