# a quick script so that I don't have to do the same 3 commands over and over. 
import init_db
import post_parser_script
from flask import Flask, render_template, Markup, request
import sqlite3 
from markupsafe import escape
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
def home(): 
    return render_template("home.html")

@app.route("/index")
def index():
    posts = get_posts()
    #some sort of object
    posts = list(posts)
    #posts is a tuple containing objects? 
    x = 0
    print(posts)
    for temp_post in posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        print("temp post is currently")
        print(temp_post)
        posts[x] = temp_post
        x += 1
    print("posts in current state")
    print(posts)
    return render_template('index.html', posts=posts)

"""
@app.route("/posts/<i>")
def show_post_number(i):
    i = escape(i)
    try: 
        i = int(i)
        posts = get_posts()
        # print(posts)
        post = dict(posts[i])
        for key, value in post.items(): 
            new_value = Markup(value).unescape()
            post[key] = new_value
        return render_template("page.html", post = post)
    except ValueError: 
        return render_template("404.html")
"""

@app.route("/<slug>")
def show_post_slug(slug):
    slug = escape(slug)
    connection = get_db_connection()
    found_post = connection.execute(f"SELECT * FROM posts WHERE slug='{slug}';").fetchone()
    try: 
        post = dict(found_post)
        # print(post)
        for key, value in post.items(): 
            new_value = Markup(value).unescape()
            post[key] = new_value
        # print(post)
        if post['type'] == "post": 
            return render_template("post.html", post=post)
        elif post['type'] == "page":
            return render_template("page.html", post=post)
    except TypeError: 
        return render_template("404.html")


@app.route("/tag/<tag>")
def show_tag(tag):
    tag = escape(tag)
    print("------------- Tag query: " + tag)
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    relevant_posts = connection.execute(f"SELECT * FROM posts WHERE tags MATCH '{tag},'").fetchall()
    # find all posts with the tag
    relevant_posts = list(relevant_posts)
    # turn results into a list
    #try: 
    x = 0
    print(relevant_posts)
    for temp_post in relevant_posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        print("temp post is currently")
        print(temp_post)
        relevant_posts[x] = temp_post
        x += 1
    print("posts in current state")
    print(relevant_posts)
    if not(relevant_posts): 
        return f""" <h5>Displaying tag "{tag}"</h5> <p> No posts found with tag "{tag}." </p>"""
    else:
        return render_template('tag.html', posts=relevant_posts, tag=tag)

@app.route("/search", methods=["POST"])
def search(): 
    search_query = request.form.get("search")
    search_query = escape(search_query)
    if search_query == "":
        render_template("no_search.html")
    else:    
        connection = get_db_connection()
        connection.row_factory = sqlite3.Row
        print(search_query)
        relevant_posts = connection.execute(f"SELECT * FROM posts WHERE posts MATCH '{search_query}'").fetchall()
        relevant_posts = list(relevant_posts)
        x = 0
        print(relevant_posts)
        for temp_post in relevant_posts: 
            temp_post = dict(temp_post)
            for key, value in temp_post.items(): 
                new_value = Markup(value).unescape()
                temp_post[key] = new_value
            relevant_posts[x] = temp_post
            x += 1
        print(relevant_posts)
        return render_template('search.html', search=search_query, posts=relevant_posts)

if __name__ == '__main__':
    app.run(debug=True)