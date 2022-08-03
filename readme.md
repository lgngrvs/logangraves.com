# logangraves.com: now with a backend and a frontend!
This is the development branch for my personal website, what will eventually be located on my domain [logangraves.com](https://logangraves.com). I don't have a 'stable' branch right now because it's running on a Heroku box; I just upload my code whenever it's stable and then keep it like that till the next version.

## About
I have built a back- and front-end from scratch (mostly), using [Flask](https://flask.palletsprojects.com/) and a SQLite database. Yes, I am aware that there will be issues with security if I build my own backend; I've done my best to escape user input in the url and in the search bars to prevent XSS, but I'm not experienced in web security so I'm not really sure what else I can do. Let's just say it's free incident response training if I get pwned.

## Usage
To run the site, install the venv or whatever + the requirements in requirements.txt, and run `py setup.py`. `setup.py` invokes the other necessary scripts; just go to `127.0.0.1:5000/` to see the results assuming that port isn't already used.