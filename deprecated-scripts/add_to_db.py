from slugify import slugify
from flask import Markup
import sqlite3

"""
----- THIS FILE IS NO LONGER USED; USE post_parser.py INSTEAD ------
"""

def add_to_db(title, tags, content):
    slug = slugify(title)
    title = Markup.escape(title)
    content = Markup.escape(content)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    print(slug)
    connection.execute(f"INSERT INTO posts (title, slug, tags, content) VALUES ('{title}', '{slug}', '{tags}', '{content}')")
    connection.commit()
    connection.close()

post1_title = """Minimalism's sad results"""

post1_tags = "minimalism,sadness,quotes"

post1_content = """My boring computer theme and phone setup make my devices feel less friendly. It's sad. I'm sad. You know, a wise man once said, "too much minimalism is literally nothing lmao" and I'll remember that forever. YOu & me both know." """ # how do I deal with post ending in a quote?

post2_title = """How fast should I read books?"""

post2_tags = """reading,productivity,quotes"""

post2_content = """People seem to say that I should be reading books for learning, and that I should "alter my speed depending on the difficulty of the content." However, I need to find a balance between actually getting through books and getting the most out of them."""

add_to_db(post1_title, post1_tags, post1_content)
add_to_db(post2_title, post2_tags, post2_content)