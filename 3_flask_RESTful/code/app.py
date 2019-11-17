from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# Every resource has to be a class
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item                # flask-restful does jsonify by itself
        return {'item': None}, 404     # in order to get JSON, instead of null and 404

    def post(self,name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item, 201    # 201 CREATED


api.add_resource(Item,'/item/<string:name>')  

app.run(port=5000,debug=True)