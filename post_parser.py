import markdown
from slugify import slugify
from flask import Markup
import sqlite3


filename = input("file name (relative to this .py file): ")

# Line 1: title, Line 2: date, Line 3: tags, line 4+: content

whole_post_list = []

with open(filename) as file:
    for linenumber, line in enumerate(file): 
        if linenumber < 4: 
            whole_post_list.append(line)
        else: 
            whole_post_list[3] += line
        linenumber += 1

title = Markup.escape(whole_post_list[0][2:])
date = Markup.escape(whole_post_list[1][6:])
tags = Markup.escape(whole_post_list[2][6:])
content = Markup.escape(markdown.markdown(whole_post_list[3]))
slug = slugify(whole_post_list[0][2:])

print(title, slug, date, tags, content, sep=" || ")

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
connection.execute(f"INSERT INTO posts (timestamp, title, slug, tags, content) VALUES ('{date}', '{title}', '{slug}', '{tags}', '{content}')")
connection.commit()
connection.close()