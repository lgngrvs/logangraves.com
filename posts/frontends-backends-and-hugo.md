# Frontends, Backends, and Setup with Hugo
Date: 2025-07-31
Tags: organic-web
Type: post
Desc: A brief tutorial on setting up Hugo for personal use on GitHub pages. Written for a workshop on building your own personal website at [PAIR](https://pair.camp) 2025. 

Ok so if you want to have a website here you go. You *can* build it using a commercial website builder (the ones you've heard of, like Wix or Squarespace or Wordpress or whatever) but imo that's boring (and the web is saturated with tutorials for them) so I won't say anything more about commercial site builders. 

This section is for you if you want to write some code and get some hands dirty with how stuff actually works :)

## Backend or no?

There are many ways you can set up a site, each of which abstracts different amount of the complicated stack of protocols on which the web works. Closest to the simplest thing is, 'write a raw html file, put it in a repo on github, click the github pages button, and boom you have a website.' 

What I have going on is slightly less abstract; I wrote web server code. Websites sit on computers, usually on datacenters, and the computers receive requests from other computers and send data out to them; that's what the internet is. GitHub Pages does all the web server stuff for you. Instead, I wrote code telling the computer that my website runs on how to handle requests and figure out what data to respond with (this is called a 'backend') as well as frontend code telling it how to e.g. structure the web page it sends back and style links. (A framework like [Flask](https://palletsprojects.com/p/flask/) abstracts away most of the complexity of web protocols, allowing you to focus on the details of how you want your site to be served.) 

So writing your own site breaks down into 2 parts, basically:
1. Frontend code/styling: HTML/CSS/JS code ('the web suite') — tells the browser how your page should look
2. Backend code: tells the server what information (which webpage, mainly) to send to the browser when someone visits your site in their browser. This might involve hosting a database which the server queries.

You really don't need to write #2. You *can* if you want to, but it's a lot of work. The upside is that you can exert, again, a lot more control over your website (in this case, you can write your own custom scripting for different styles and different pages and different directories that gets generated dynamically), and notably **you can have a native search bar on your site** (hacky ways exist to run search on the frontend but they're hacky). 

To be honest, though, I think that search bars are less useful than people make them out to be. (I ended up hiding the search bar on my site for a couple years just because it didn't seem to add much and I didn't want to bother figuring out how to make it look good.) And the downside of writing your own backend is that you need to set up a ton of basic stuff and make do with additional overhead. Note that you don't *have* to write your own backend -- I'm sure there's stuff out there that makes it easy to have a search function without needing to write your own web app -- but I'm a designer at heart, not a web engineer, and so this is the accouny you're getting from me.

If it's your first time building your own website, I think that it'll be a better experience if you start with the frontend and customize it, then build a backend later if you want. I say this because there's a reasonable amount of technical overhead involved in building the site: this method requires 

1. a little bit of python,
2. setting up DNS records
3. familiarity with markdown, 
4. usage of `git` and GitHub, and 
5. learning the organization of a new python package, `hugo`.

These may be things you already know, but when I was doing this the first time around they weren't. And if these aren't things you already know, it's a pretty big jump for someone totally new — I think it will be a solid dose of new stuff already, without having to deal with writing backend code or server config. If you want to build your own backend nonetheless, I can recommend the [flask](https://flask.palletsprojects.com/en/stable/) framework; that's what I use. See my website's [source](https://github.com/lgngrvs/logangraves.com) for inspiration if interested. (That code is what runs what you're reading right now!)

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
