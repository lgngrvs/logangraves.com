# Your model of the world changes the world
Date: 2025-08-24
Tags: snippets
Type: page
Desc: Known by many other names: goodharting, overfitting, legibility bias, "the map alters the territory"

[The map is not the territory](https://en.wikipedia.org/wiki/Map%E2%80%93territory_relation) (said everyone ever) but the map can alter the territory. The famous (?) example of this is [Agloe, NY](https://en.wikipedia.org/wiki/Agloe%2C_New_York), a fake town put on the map by mapmakers from General Drafting in the early 1900s to catch plagiarism of their maps. However,

> in 1930, a business named Agloe Lodge Farms was incorporated, which acquired a fishing lodge in the area and renamed it Agloe Lodge.

The purchaser of the land was suspected to be a front for another company, so that

> When General Drafting approached Rand McNally about the violation of their copyright, Rand McNally representatives said that the information about the town had come from [Delaware County](https://en.wikipedia.org/wiki/Delaware_County,_New_York "Delaware County, New York") records *\[citation needed\]* which showed that a business with the name Agloe existed there.

This is a funny anecdote but it doesn't illustrate the point as well as it would if some random people saw Agloe on the map and decided to found a town there. Luckily I can do whatever I want on my website, so I'll say that what actually happened was that

> in 1930, a small religious community in Delaware County, New York that had formed during the Second Great Awakening looked for a place with some infrastructure but minimal population to settle their newly independent sect. Since it was nearby, they chose to move to Agloe; they were surprised to find on arrival that the town did not exist. Since they had already filled out paperwork and spread the word that they were moving to Agloe, they chose to settle down anyway; a business named Agloe Lodge Farms was incorporated, which acquired a fishing lodge in the area and renamed it Agloe Lodge, the first building in the newly-formed town of Agloe.

I don't claim that this is my novel insight, it's everywhere, but I'm stitching all these concepts together into a blog post because it keeps popping up.

I was listening to a Machine Learning Street Talk [episode with Dan Hendrycks](https://podcasts.apple.com/us/podcast/superintelligence-strategy-dan-hendrycks/id1510472996?i=1000721878387) on my way home, when Dan and the host, Tim Scarfe, had a brief disagreement about intelligence. 

Dan does a lot of benchmarks research. He said that he thinks about intelligence roughly along 10 axes:

- Fluid intelligence (ARC-AGI, Raven's progressive matrices)
- Crystallized knowledge/Acquired knowledge (MMLU, image classification)
- Reading/writing ability
- Visual processing (counting things in images, discerning latent patterns, precise image modifications, determining properties)
- audio processing ability
- Short-term memory
- Long-term memory
- Input processing speed
- Output processing speed
- (does not give a 10th afaict but i'm sure he says it somewhere)

Benchmarks tend to measure only one, maybe a couple of these aspects. Making good integrated benchmarks seems useful; Tim objected to the idea that one can factorize intelligence, and wanted to think of things more generally along the lines of "doing more with less."

It popped into my head that this was an instance of a more general pattern in... let's say, human civilizations, where the models that we make of the world change the world itself. Making better benchmarks for what we call 'aspects of intelligence' (if such things exist; I tend to buy the idea that Dan's factorization is [useful, if not true](wrong-but-useful)) allows us to measure those aspects better, of course, but it also causes us to more directly target those benchmarks. Even if companies are not directly targeting those benchmarks narrowly, the benchmarks that are available and prominent will dictate what's considered progress — though, of course, the ultimate benchmark is "how useful is this thing *actually*?" For Dan, the point at which people actually want to use the AI for some purpose is the point at which the capability "emerges," if I understand him right.

That's the whole idea of [Goodharting](https://en.wikipedia.org/wiki/Goodhart%27s_law): you use quantitative metrics as proxies for things you care about (e.g. standardized test scores to measure education), and as soon as you start maximizing that metric (e.g. teaching to the test) that metric is no longer a good measurement of what you actually care about (e.g. actually educating people). The choice of that metric to model the world has changed the way you behaved, and thus changed the world — the map you make has eventually changed the territory itself. Benchmarkmaxxing is Goodharting. Overfitting is Goodharting. Training on test is Goodharting.

The book [Seeing like a State](https://en.wikipedia.org/wiki/Seeing_Like_a_State) (well-known among rationalists) is about this idea: for example, in order to collect taxes, the government arbitrarily separates communities into well-defined households, with a 'head of household.' By doing so, they turn the household into an *actual* institution, and make the head of household *an actual real thing* that did not exist prior to the State's tax collection system. This book calls it "legibility" being forced on the world where it wasn't before.

> Examples include the introduction of family names, censuses, uniform languages, and standard units of measurement. While such innovations aim to facilitate state control and economies of scale, Scott argues that the eradication of local differences and silencing of local expertise can have adverse effects.
