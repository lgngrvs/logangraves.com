# THIS FILE IS DEPRECATED
import markdown
from slugify import slugify
from flask import Markup
import sqlite3


filename = input("file name (relative to this .py file): ")

# Line 1: title, Line 2: date, Line 3: tags, line 4: type, line 5+ content

whole_post_list = []

with open(filename) as file:
    for linenumber, line in enumerate(file): 
        if linenumber < 5: 
            whole_post_list.append(line)
        else: 
            whole_post_list[4] += line
        linenumber += 1

title = Markup.escape(whole_post_list[0][2:]).strip("\n")
date = Markup.escape(whole_post_list[1][6:]).strip("\n")
tags = Markup.escape(whole_post_list[2][6:]).strip("\n")
content_type = Markup.escape(whole_post_list[3][6:]).strip("\n")
content = Markup.escape(markdown.markdown(whole_post_list[4]))
slug = slugify(whole_post_list[0][2:])

print(title, slug, date, tags, content_type, content, sep=" || ")

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
connection.execute(f"INSERT INTO posts (timestamp, type, title, slug, tags, content) VALUES ('{date}', '{content_type}', '{title}', '{slug}', '{tags}', '{content}')")
connection.commit()
connection.close()