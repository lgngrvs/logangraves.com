# "Flask Run" to start development server locally. 

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_posts():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return posts

@app.route("/")
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route("/posts/<i>")
def show_post(i):
    i = int(i)
    posts = get_posts()
    print(posts)
    post = posts[i]
    return render_template("page.html", post = post)