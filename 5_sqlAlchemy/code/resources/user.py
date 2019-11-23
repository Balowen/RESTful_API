import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    # parse through json and make sure username&password are there
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type = str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with username '{}' already exists".format(data['username'])}, 400 # Bad request   

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()           
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201   # 201-Created