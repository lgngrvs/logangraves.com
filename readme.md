# logangraves.com: now with a backend and a frontend!
This is the current stable version of my personal website, located on my (apex) domain [logangraves.com](https://logangraves.com). It's running on a [Heroku](https://heroku.com) box. 

## About
Back- and front-ends written 'from scratch' using [Flask](https://flask.palletsprojects.com/) and a SQLite database, and no CSS/HTML frameworks. Site doesn't use JS (see `# JavaScript`), does not contain any trackers, does not measure traffic and avoids collecting data wherever possible (all of this as of Jun 27 2023, since its inception a long time ago). 

## Security 
I did my best to prevent most common injection attacks and tested extensively. All user inputs are escaped. Let me know if you find a vulnerability (feel free to open an issue) and I will fix it; let's just say it's free incident response training if I get pwned!

*(well not really, i can just turn the site off in heroku dashboard lol)*

## JavaScript
JS can do cool things. My site can do cool things without JS. I believe in a lightweight internet free of tracking, advertising, data-mining, and most of all, popups and the various annoyances I need to install entire browser extensions to prevent. On principle, therefore, I avoid using JS whenever that is possible. (All animations on this site are done with CSS only.)

*I reserve the right to use JS for fun programming projects on here in the future though. If I do that, the JS part will be isolated from the main site and will only load when specifically visited.*

## Usage
To run the site locally:

1. Clone the repo
2. Open a `venv` in the directory (optional but recommended)
3. `pip install -r requirements.txt` to install dependencies in the venv
4. Make sure your port 5000 is open
5. Run `app.py`
6. View test site in browser (127.0.0.1:5000)