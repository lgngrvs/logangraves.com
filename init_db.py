import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

with open("schema.sql") as file:
    cursor.executescript(file.read())

#for i in range(4):
#    ins = i
#    connection.executescript(f"INSERT INTO posts (title, content) VALUES ('Title for Post {ins}', 'Content for Post {ins}')")

connection.commit()
connection.close()