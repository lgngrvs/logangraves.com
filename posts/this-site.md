# This site
Date: 2023-12-08
Tags: #design #meta
Type: post
Desc: Notes on function, philosophy, and design.

Welcome to Logangraves.com!

This website serves a couple of purposes, and will continally evolve as I evolve myself. Here are some important functions: 

1. **Hosting thoughts.** A major function of this site is to host ideas that I'm developing or have encountered. Things I post here are things I'm interested in talking about — the hope is that someone who finds them equally interesting will be inspired to start a conversation. (Hint: My preferred contact methods are on my [about page](https://logangraves.com/about)!). Also, writing ideas down allows me to develop my thoughts; this site is a place I can post the products of that process.

2. **Verifying my identity.** This site also serves as a central link in my online identity web, hosting my PGP keys as well as a signed list of identites. In other words, this site hosts the cryptographic means to verify I am me, as well as every online presence I publicly claim to operate. Any accounts that are not listed on this website should be assumed to be another Logan Graves; if there's ever confusion over whether I own an online account or identity (or if someone with the name Logan Graves is me), this site will (hopefully) be able to resolve it. See [Identities](https://logangraves.com/identities) for more info.

3. **Broadcasting important things.** There are some beliefs/attitudes I have that I want to broadcast to the world — for example, "I appreciate it when people speak honestly about their feelings about me and give me constructive criticism when I make mistakes" — that would be inappropriate to insert into, say, a social media bio or a conversation. This site is a place that I can indicate those things.

## Disclaimer

I hope to have this site be a *public representation* of me — meaning it will ideally be one that is honest and useful for starting conversations and developing ideas publicly, yet one that is attentive to the fact that what I write here will probably be preserved on the internet forever. (Hosting this site under my real name helps me somewhat to keep this in mind.) This means that I may leave out important details or nuance, for long-term personal purposes or simply doing so unintentionally. No site can be a full representation of a person, and this site is no exception.

Hence, please avoid taking things published on this website or associated subdomains as indications of (a) my full, nuanced positions or system of belief or (b) my future beliefs. They are explorations, not full explanations; language itself can even get in the way, since words can carry different connotations to different people. 

## Design choices

I wrote this website "from scratch" in HTML/CSS and a Python/SQLite backend, using the [Flask framework](https://palletsprojects.com/p/flask/). Coding this site was an excuse to teach myself the relevant programming skills; I wanted to have an intimate knowledge of CSS and HTML before I began using frameworks, so that I wouldn't be missing important intuitions and run into problems later. You can see the source code on my [GitHub](https://github.com/lgngrvs/logangraves.com). 

Notably, this site does not use JavaScript. All animations are CSS-based, and any input processing is done on the backend. 

JS can do cool things. My site can do cool things without JS. I believe in a lightweight internet free of tracking, advertising, data-mining, popups and other miscellaneous annoyances. (We shouldn't need to install entire browser extensions to avoid these things.) On principle, therefore, I avoid using JS whenever that is possible. I don't use any analytics services, though note that my server does log requests for debug purposes. I do not check these logs unless I'm using them for that purposes, and they are regularly purged — but obviously, please do not put any personal information into any input boxes on this site. 

*I do, however, reserve the right to use JS for fun programming projects on here in the future though. If I do that, the JS part will be isolated from the main site and will only load when specifically visited.*

Regarding security, I did my best to prevent most common injection attacks and tested extensively. All user inputs are escaped. Let me know if you find a vulnerability (feel free to open an issue on the repo linked above) and I will fix it; let's just say it's free incident response training if I get pwned! (well not really, I can just turn the site off in heroku dashboard lol)

The site's design is intentionally minimalist and as lightweight as possible. It has a dynamic CSS-based light/dark mode, and typography using fonts that are free and open. (Licenses are contained in the `static/fonts` directory; you can read those licenses on the GitHub.)