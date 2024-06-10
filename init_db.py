#Python code that manages the connection with the database

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, pass, email) VALUES (?, ?, ?)",
            ('jake', 'jake', 'jake@byjaybird.com')
            )
cur.execute("INSERT INTO points (userid, tokens, points) VALUES (?, ?, ?)",
            ('1', '10000', '0')
            )

cur.execute("INSERT INTO users (username, pass, email) VALUES (?, ?, ?)",
            ('tuna', 'tuna', 'tuna@byjaybird.com')
            )
cur.execute("INSERT INTO points (userid, tokens, points) VALUES (?, ?, ?)",
            ('2', '10000', '0')
            )

connection.commit()
connection.close()
