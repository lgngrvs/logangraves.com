# logangraves.com: now with a backend and a frontend!
This is the development branch for my personal website, what will eventually be located on my domain [logangraves.com](https://logangraves.com).

## About
I am building a back- and front-end from scratch (mostly), using [Flask](https://flask.palletsprojects.com/) and SQLite. I may use a frontend framework -- tbd. Yes, I am aware that there will be issues with security if I build my own backend, let's just say it's free incident response training. 

## Usage
To run the server, (I haven't added a requirements.txt, sorry) locally you (I) build the database (`py init_db.py`) and then run the app (`flask run` since it automatically uses app.py). Results will appear on `127.0.0.1:5000/` assuming that port isn't already used.