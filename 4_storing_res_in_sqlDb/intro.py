import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"  # query
cursor.execute(create_table)

user = (1,'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'bart', 'asdf'),
    (3, 'kal', 'aswds')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)
# whenewer we insert, we have to say the connection to save db
connection.commit()

connection.close()