import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# INTEGER PRIMARY KEY -- auto increments itself unlike int
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real - number with a decimal point 
create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

connection.commit()

connection.close()