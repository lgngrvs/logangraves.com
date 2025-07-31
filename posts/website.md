# Personal Websites: An Introduction
Date: 2025-07-31
Tags:
Type: post
Desc: A brief tutorial on building a personal website. Written for a workshop on building your own personal website at [PAIR](https://pair.camp) 2025. 

## Who should create a personal website?

The internet of the 2000s, as I am told, was a landscape of individuality — creative, hand-crafted websites, blogrolls, and forums; hypertextual and organic. The internet of the 2020s, so it seems, is an algorithmic hellscape destroyed by Big Internet, a slop-filled rotting husk dotted by tiny oases struggling for breath among the waste. (I wrote this line as joking hyperbole at first but the more I think about it the less humorous it feels.) It's designed for the opposite of thoughtful engagement; designed not to connect, but to addict, to distract.

The internet is for everyone, though! You can at any moment wade out of the slop onto the land, and construct a little house. Then you can found or join a village and connect your little human places with little hypertext roads. 

The first step is the house! A little home on the internet. That's a personal website. To build one, you can There are a couple reasons you might consider building your own site:
- It's fun! 
	- You get to learn things about how the web works
	- You get the satisfaction of having built everything yourself
- You have total creative control!
	- You have total control over what it looks like, what is on there, how it runs. 

Note that there are a couple downsides though: 
- *You have total control*; you have to set it up and learn how to write the code to make it run if you don't know how already
	- There's no doubt some technical overhead
- You have to pay a little bit for it
	- On the order of $10/year
- You have to maintain it

## Building your infrastructure

Ok so if you want to build your infrastructure here you go.

There are a couple ways you can do it. What I have going on is that I literally just wrote the entire site myself: I wrote server code telling it how to handle requests, as well as frontend code telling it how to nest pages and style links. This breaks down into 3 parts, basically:
1. Frontend code/styling: HTML/CSS/JS code ('the web suite') — tells the browser how your page should look
2. Backend code: tells the server what information (which webpage, mainly) to send to the browser when someone visits your site in their browser

You really don't need to write #2. You *can* if you want to, but it's a lot of work. The upside is that you can exert, again, a lot more control over your website (in this case, you can write your own custom scripting for different styles and different pages and different directories that gets generated dynamically), but the downside is that you need to write a ton of basic stuff and make do with additional overhead. 

If it's your first time building your own website, I think that it'll be a better experience if you start with building the frontend and then build a backend later if you want. I say this because there's a reasonable amount of technical overhead involved in building the site: this method requires (1) a little bit of python (2) setting up DNS records (3) familiarity with markdown (4) usage of `git` and GitHub (5) learning the organization of a new python package, `hugo`. That's a pretty big jump for someone totally new — I think it's a good dose, without having to deal with writing backend code or server config. If you want to build your own backend nonetheless, I can recommend the [flask](https://flask.palletsprojects.com/en/stable/) framework. See my website's [source](https://github.com/lgngrvs/logangraves.com) for inspiration if interested. (That code is what runs what you're reading right now!)

For now, I'll tell you the most basic way to get "something" that looks professional/nice and won't be unpleasant to maintain and add to. A good place to start is using [Hugo](https://gohugo.io/installation/). Hugo is a program that runs on your computer, which takes in `.md` files and generates a website on your laptop, which you then upload to the internet. Markdown (`.md`) files are pure text files with some extra syntax that tells the program how to format them visually. For example, you surround text with `**` e.g. `**bold**` to get **bold** text, and surround text with a single `*` (as in `*italics*`) to get *italicized* text. Markdown is a common standard for formatting text, so it'll likely be nice for you to understand in the future, if you haven't already encountered it.

The nice part of Hugo is that it abstracts away most of the annoying difficulty of structuring a site. You can just write the text that you want your site to show (and insert images, and links, etc.) and run it through Hugo, and Hugo uses a predefined template to give you back a nice looking, ready-to-go site. You can pick from [a huge library of Hugo templates](https://themes.gohugo.io/) that other people have designed, optionally tweak one of those designs to make it your own, or even start from scratch and design your own Hugo template. If it's your first time, I'd recommend starting with a Hugo template and then tweaking it to learn how it works.

Now, here's the flowchart. I don't want to go through and explain the whole process, myself; that would be duplicating work anyway, since there are a bunch of high-quality tutorials, usually from the sources themselves, on how to use the various tools. For now I'm just going to include links to those tutorials.

1. Get your GitHub repo set up
	1. [Create a repo](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-a-repository-for-your-site)
	2. Clone the repo locally (there should be instructions once you're done creating the repo)
2. Download [Hugo](https://gohugo.io/installation/) and pick a theme that you like from [https://themes.gohugo.io/](https://themes.gohugo.io/).
3. Follow [this tutorial](https://gohugo.io/getting-started/quick-start/) to generate your site's files
4. Push the site files to your GitHub 
5. Buy a domain name
	1. Go to [Namecheap](https://namecheap.com) or any other domain website
	2. Pick a domain name and buy it with a credit or debit card or PayPal or something
6. Point the GitHub pages to your domain and add the DNS record for GitHub pages
7. Check that it's been deployed!
# What in the world do I put on the website?

So you now have a website — what do you put on it? My thought on this has been structured by a blog post by Henrik Karlsson, "[A blog post is a very long and complex search query to find fascinating people and make them route interesting stuff to your inbox](https://www.henrikkarlsson.xyz/p/search-query)". The title tells you essentially what you need to know — I think you should generalize that to the site as a whole. 

There are lots of things that people use their sites for — sometimes a placeholder for their email address, sometimes a resume hosting site, sometimes a portfolio, if they're a designer; you *can* do all of that. But I think the personal site can be something deeper, if you'll let it. I'll quote from my current (as of July 2025) homepage:

> This site is about me — my thoughts, my contact info, my own little simulacrum — but it's made for the both of us. The explicit overarching goal of this site is for it to signal various interests and preoccupations to you, in hopes that you'll reach out and we can talk about them.

My site is a place where I put things that I love, things that I want to talk about. I hope that people who love similar things and want to talk about similar things will see them, and they'll scroll down to the bottom of the homepage and use the contact info I leave there. Over time, the site becomes a representation of myself.

Now, here's a list of things that might stimulate you: 

- Lists
	- blogs you like
	- quotes/selected passages from books you read
	- math problems you've enjoyed
	- books you like in general
	- playlists of music
	- book
	- starter pack
	- questions/problems you have
	- lists of people you like
- Personal
	- life updates
	- about page
	- starter pack
	- your resume
	- write-ups about your projects
	- discussions about places you've been
- Writing
	- book reviews
	- blog posts, to flesh out things that you're thinking about
	- technical posts; notes about things you have learned
- FAQs
	- things you wish you'd been asked

