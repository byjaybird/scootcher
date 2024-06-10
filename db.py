#Python code that manages the connection with the database

import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, pass) VALUES (?, ?)",
            ('jake', 'jake')
            )

cur.execute("INSERT INTO users (username, pass) VALUES (?, ?)",
            ('tuna', 'tuna')
            )

connection.commit()
connection.close()
