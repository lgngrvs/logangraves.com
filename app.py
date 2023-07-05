# this is what runs.

import init_db
import post_parser_script
from flask import Flask, render_template, Markup, request
import sqlite3 
from markupsafe import escape
from dotenv import load_dotenv
from feedgen.feed import FeedGenerator
from flask import make_response
from datetime import datetime
from dateutil.tz import tzoffset
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
    # print(len(posts))

    x = 0
    print("Posts include: " + str(posts))
    for temp_post in posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        # print("temp post is currently")
        # print(temp_post)
        posts[x] = temp_post
        x += 1
    # print("posts in current state")
    # print(posts)
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
    # print("------------- Tag query: " + tag)
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    relevant_posts = connection.execute(f"SELECT * FROM posts WHERE tags MATCH '[{tag}]'").fetchall()
    # find all posts with the tag
    relevant_posts = list(relevant_posts)
    # turn results into a list
    #try: 
    x = 0
    # print(relevant_posts)
    for temp_post in relevant_posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        # print("temp post is currently")
        print(temp_post)
        relevant_posts[x] = temp_post
        x += 1
    # print("posts in current state")
    # print(relevant_posts)
    if not(relevant_posts): 
        return f""" <h5>Displaying tag "{tag}"</h5> <p> No posts found with tag "{tag}." </p>"""
    else:
        return render_template('tag.html', posts=relevant_posts, tag=tag)

# Old POST search method. Switched to GET because it looks nicer. 
'''
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
'''

@app.route("/search", methods=["GET"])
def search(): 
    search_query = escape(request.args.get("q")).replace("(", " ").replace(")", " ")
    print(search_query)
    try: 
        if search_query == "": 
            print("search is none")
            return render_template("no_search.html")
        else:
            connection = get_db_connection()
            connection.row_factory = sqlite3.Row
            # print(search_query)
            relevant_posts = connection.execute(f"SELECT * FROM posts WHERE posts MATCH '{search_query}'").fetchall()
            relevant_posts = list(relevant_posts)
            x = 0
            # print(relevant_posts)
            for temp_post in relevant_posts: 
                temp_post = dict(temp_post)
                for key, value in temp_post.items(): 
                    new_value = Markup(value).unescape()
                    temp_post[key] = new_value
                relevant_posts[x] = temp_post
                x += 1
            # print(relevant_posts)
            return render_template('search.html', search=search_query, posts=relevant_posts)
    except TypeError:
        render_template("no_search.html")

"""
posts = get_posts()
    #some sort of object
    posts = list(posts)
    #posts is a tuple containing objects? 
    x = 0
    #print(posts)
    for temp_post in posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        #print("temp post is currently")
        #print(temp_post)
        posts[x] = temp_post
        x += 1
    # print("posts in current state")
    # print(posts)
"""

@app.route("/rss.xml")
def rss():
    feed = FeedGenerator()
    feed.title("All Posts - logangraves.com")
    feed.description("Feed containing all posts and pages (e.g. the about page) from logangraves.com.")
    feed.language("en")
    feed.link(href="https://logangraves.com/rss.xml", rel="self")
    feed.logo("https://logangraves.com/static/favicon.png")

    # Duplicated code from /index app route because it already works and I don't want to make an entire new function that may break something
    posts = get_posts()
    posts = list(posts)
    x = 0
    for temp_post in posts: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        posts[x] = temp_post
        x += 1

    for post in posts: # get_news() returns a list of articles from somewhere
        fe = feed.add_entry()
        fe.title(post["title"])
        fe.link(href="https://logangraves.com/" + post["slug"])
        fe.description(post["content"])
        fe.author(name="Logan Graves", email="me@logangraves.com")
        postDatetime = datetime.strptime(post["timestamp"], '%Y-%m-%d')
        postDatetime = postDatetime.replace(tzinfo=tzoffset("UTC+0",0))
        fe.pubDate(postDatetime)

    response = make_response(feed.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')
    return response


@app.errorhandler(404)
def not_found(error): 
    return render_template("404.html")

# @app.errorhandler


if __name__ == '__main__':
    app.run(debug=True)