import markdown
from markdown.extensions.toc import TocExtension
from slugify import slugify
from flask import Markup
import sqlite3
import os
from no_underscores_italics import NoUnderscoresItalics # imports markdown italics disabler

list_of_file_names = os.listdir("posts")
parent_directory = "posts/"

list_of_file_names = [f'{parent_directory}{file}' for file in list_of_file_names]

print(list_of_file_names)

for filename in list_of_file_names: 
    if filename[6] == ".": 
        pass
    else: 
        # print("Preparing to add post \"" + str(filename) + "\"")
        # print(list_of_file_names)
        whole_post_list = []

        with open(filename) as file:
            for linenumber, line in enumerate(file): 
                if linenumber < 6: 
                    whole_post_list.append(line)
                else: 
                    whole_post_list[5] += line
                linenumber += 1

        title = Markup.escape(whole_post_list[0][2:]).strip("\n")
        date = Markup.escape(whole_post_list[1][6:]).strip("\n")
        tags = Markup.escape(whole_post_list[2][6:]).strip("\n")
        content_type = Markup.escape(whole_post_list[3][6:]).strip("\n")
        description = Markup.escape(markdown.markdown(whole_post_list[4][6:], extensions=["tables"]))
        descriptionplain = Markup.escape(whole_post_list[4][6:]).strip("\n")
        content = Markup.escape(markdown.markdown(whole_post_list[5], extensions=[NoUnderscoresItalics(), "tables", "footnotes", "fenced_code", "sane_lists", "codehilite", TocExtension(title="Table of Contents", toc_depth="2-6")]))
        slug = slugify(filename)[6:][:-3]
        wordcount = len(whole_post_list[5].split(" "))

        # print(title, slug, date, tags, content_type, content, wordcount, sep=" || ")
        print("Added " + title)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        test = connection.execute(f"SELECT * FROM posts where slug LIKE '{slug}'").fetchone()
        if test == None:
            connection.execute(f"INSERT INTO posts (timestamp, type, title, slug, tags, content, description, descriptionplain, wordcount) VALUES ('{date}', '{content_type}', '{title}', '{slug}', '{tags}', '{content}', '{description}', '{descriptionplain}', '{wordcount}')")
            connection.commit()
            connection.close()
        else: 
            pass