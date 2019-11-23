import sqlite3

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))     # parameters has to be iterable, that's why the single value tuple 
        row = result.fetchone()
        if row:
            user = cls(*row)                            # cls(row[0], row[1], row[2]) // *row is a set of parameters (the same thing)
        else:
            user = None

        connection.close()
        return user
 
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))     
        row = result.fetchone()
        if row:
            user = cls(*row)                            
        else:
            user = None

        connection.close()
        return user