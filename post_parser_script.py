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