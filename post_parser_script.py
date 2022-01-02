import markdown
from slugify import slugify
from flask import Markup
import sqlite3
import os

list_of_file_names = os.listdir("posts")
parent_directory = "posts/"

list_of_file_names = [f'{parent_directory}{file}' for file in list_of_file_names]

print(list_of_file_names)

for filename in list_of_file_names: 
    print("running for loop")
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
    test = connection.execute(f"SELECT * FROM posts where content LIKE '{content}'").fetchone()
    if test == None:
        connection.execute(f"INSERT INTO posts (timestamp, type, title, slug, tags, content) VALUES ('{date}', '{content_type}', '{title}', '{slug}', '{tags}', '{content}')")
        connection.commit()
        connection.close()
    else: 
        pass