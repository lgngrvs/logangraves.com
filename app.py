# this is what runs.
import init_db
import post_parser_script
from flask import Flask, render_template, Markup, request, redirect, make_response
import sqlite3 
from markupsafe import escape
from dotenv import load_dotenv
from feedgen.feed import FeedGenerator
from datetime import datetime
from dateutil.tz import tzoffset
import os
import flask_talisman 
from flask_talisman import Talisman

load_dotenv()

app = Flask(__name__)


CSP = { 
    # Just some additions to the basic CSP provided by Talisman at
    # https://github.com/wntrblm/flask-talisman/blob/main/flask_talisman/talisman.py

    # Fonts from fonts.google.com
    'font-src': '\'self\' themes.googleusercontent.com *.gstatic.com',
    # <iframe> based embedding for Maps and Youtube.
    'frame-src': '\'self\' www.google.com www.youtube.com',
    # Assorted Google-hosted Libraries/APIs.
    # Added jsdelivr.net to allow MathJax, but I'm worried
    # that jsdelivr.net is not a great host to be allowing.
    # Will give some thought.
    'script-src': '\'self\' ajax.googleapis.com *.googleanalytics.com '
                  '*.google-analytics.com cdn.jsdelivr.net',
    # Used by generated code from http://www.google.com/fonts
    'style-src': '\'self\' ajax.googleapis.com fonts.googleapis.com '
                 '*.gstatic.com cdn.jsdelivr.net \'sha256-Wi3+8jbn12vus9Oq4FOqEUCOpuRG3clBaVvLZZ2b9Fs=\' '
                 '\'sha256-JLEjeN9e5dGsz5475WyRaoA4eQOdNPxDIeUhclnJDCE=\' '
                 '\'sha256-mQyxHEuwZJqpxCw3SLmc4YOySNKXunyu2Oiz1r3/wAE=\' '
                 '\'sha256-OCf+kv5Asiwp++8PIevKBYSgnNLNUZvxAp4a7wMLuKA=\' '
                 '\'sha256-h5LOiLhk6wiJrGsG5ItM0KimwzWQH/yAcmoJDJL//bY=\' '
                 '\'unsafe-hashes\'',
    'object-src': '\'none\'',
    'default-src': '\'self\' *.gstatic.com',
}


Talisman(app, content_security_policy=CSP)


app.config["TEMPLATES_AUTO_RELOAD"] = False

@app.context_processor
def utility_processor():
    return dict(file_exists=file_exists)

def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_all():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts;').fetchall() # gets everything in the database, posts and pages.
    connection.close()
    return posts

def get_only_posts(): 
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    posts_only = connection.execute("SELECT * FROM posts WHERE type = 'post'").fetchall()
    connection.close()
    return posts_only

def get_only_pages(): 
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    pages_only = connection.execute("SELECT * FROM posts WHERE type = 'page'").fetchall()
    connection.close()
    return pages_only

def file_exists(path):
    return os.path.exists(path)


@app.route("/")
def home(): 
    return render_template("home.html")


# ======== The index Page ========
# 
#   Sets up the index page 
#   properly (supposedly) but
#   because of heroku stuff it
#   has weird behavior 
#   sometimes.
#  
"""
@app.route("/index")
def index():

    posts_only = sorted(list(get_only_posts()), key=lambda item: item["timestamp"], reverse=True) # sorts by timestamp
    pages_only = sorted(list(get_only_pages()), key=lambda item: item["title"]) # sorts by title
"""
"""
    Both posts_only and pages_only return a list containing dictionaries 
    (actually they're sqlite objects accessible like dictionaries)

    [
        {
            "id": ..., 
            "timestamp":  ...,
            "type": 
            "title"
            "slug"
            "tags"
            "description"
            "descriptionplain"
            "content": string
            "wordcount": int
        },
        { "id": ..., ...}, 
        ...
    ]
"""

"""
    x = 0
    for temp_post in posts_only: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        # print("temp post is currently")
        # print(temp_post)
        temp_post["date_formatted"] = str(datetime.strptime(temp_post["timestamp"], '%Y-%m-%d').strftime('%b %d, %Y'))
        posts_only[x] = temp_post
        x += 1

    y=0

    for temp_page in pages_only: 
        temp_page = dict(temp_page)
        for key, value in temp_page.items(): 
            new_value = Markup(value).unescape()
            temp_page[key] = new_value
        # print("temp post is currently")
        # print(temp_post)
        pages_only[y] = temp_page
        y += 1


    # initialize new set
    # loop through each item and add to set
    # if any item already exists we just don't add it
    def remove_duplicates(dictionary_list):
        seen_titles = set()
        unique_list = []
        for item in dictionary_list:
            if item['title'] not in seen_titles:
                unique_list.append(item)
                seen_titles.add(item['title'])
        return unique_list

    posts_only = remove_duplicates(posts_only)
    pages_only = remove_duplicates(pages_only)
    # this is to compensate for the heroku bug

    return render_template('index.html', posts=posts_only, pages=pages_only)

"""

@app.route("/index")
def index_chronological():

    all_items = sorted(list(get_all()), key=lambda item: item["timestamp"], reverse=True) # sorts by timestamp

    x = 0
    for temp_post in all_items: 
        temp_post = dict(temp_post)
        for key, value in temp_post.items(): 
            new_value = Markup(value).unescape()
            temp_post[key] = new_value
        temp_post["date_formatted"] = str(datetime.strptime(temp_post["timestamp"], '%Y-%m-%d').strftime('%b %d, %Y'))
        all_items[x] = temp_post
        x += 1

    def remove_duplicates(dictionary_list):
        seen_titles = set()
        unique_list = []
        for item in dictionary_list:
            if item['title'] not in seen_titles:
                unique_list.append(item)
                seen_titles.add(item['title'])
        return unique_list

    all_items = remove_duplicates(all_items)
    # this is to compensate for the heroku bug

    return render_template('index-chronological.html', posts=all_items)



# ======== does most of the regular processing ========
# 
#   Most stuff is a /<slug> thing so this does most of
#   the web server work.
# 

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
        
        post["tags_list"] = post['tags'].replace("#", "").split(" ")
        post["date_formatted"] = str(datetime.strptime(post["timestamp"], '%Y-%m-%d').strftime('%b %d, %Y'))

        # print(post)

        if post['type'] == "post": 
            return render_template("post.html", post=post)
        elif post['type'] == "page":
            return render_template("page.html", post=post)
        elif post['type'] == "barebones":
            return render_template("barebones.html", post=post)

    except TypeError: 
        return render_template("404.html")



# ======== TAGS ========

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



# ======== SEARCH ========

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

# ======== /contact redirect ========

@app.route('/contact')
def contact():
    return redirect("https://logangraves.com/about", code=302)



# ======== RSS FEED ========

@app.route("/rss.xml")
def rss():
    feed = FeedGenerator()
    feed.title("All Posts - logangraves.com")
    feed.description("Feed containing all posts and pages (e.g. the about page) from logangraves.com.")
    feed.language("en")
    feed.link(href="https://logangraves.com/rss.xml", rel="self")
    feed.logo("https://logangraves.com/static/favicon.png")

    # Duplicated code from /index app route because it already works and I don't want to make an entire new function that may break something
    posts = get_all()
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

# === HEHE ===
@app.route("/you")
def you():
    return render_template("you.html")

@app.errorhandler(404)
def not_found(error): 
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=False)