# Godel, Tarski, Hilbert, and the Foundations of Mathematics
Date: 2024-02-01
Tags: #mathematics #notes
Type: post
Desc: The beginning of my notes attempting an introduction to the foundations of mathematics.

### About

These are my markdown notes for an in-progress project (see below sections for details). I've found that I learn best by grouping information into small sequential chunks, and writing it as if it's an explainer (except the goal is for me to understand by writing it and the audience is an afterthought, so I might skip some stuff I don't feel like writing out) published directly from my Obsidian vault (hence the \[\[links\]\]; I'll replace any links to published notes with actual URLs if I can.) I found that, when learning about philosophy, anchoring myself in time and tracing the development of ideas over its course helped me [[Conceptual organization|conceptually organize]] the material and avoid getting stressed over the sheer volume of information I wanted to consume.

### TeX additions

I defined a bijection symbol using code from [stack overflow](https://math.stackexchange.com/questions/46678/what-are-usual-notations-for-surjective-injective-and-bijective-functions) as follows: 
`\newcommand{\twoheadrightarrowtail}\mathrel{\mathrlap{\rightarrowtail}}\mathrel{\mkern2mu\twoheadrightarrow}`

Looks like: 
$$\newcommand{\twoheadrightarrowtail}\mathrel{\mathrlap{\rightarrowtail}}\mathrel{\mkern2mu\twoheadrightarrow}$$

### My learning method

Textbooks are great. But they don't work for me — at least, not for where I'm at right now, and the subject that I'm working with. 

In theory they're great — everything you want to know packaged together in one book. But every time I've tried to just read and learn from math textbooks, I've found them boring. I'm learning math because it's deeply interesting to me; if something I'm trying to use makes it boring, I don't want to use it anymore. 

Part of it is how heavy they are on notation. Part of it is how formal and methodical they are with each subject; I prefer to rapidly develop intuitions, and then refine them into formal knowledge over time, rather than going slowly but surely through *everything.* I don't want the guide through everything, I want *enough knowledge to interact with stuff I find interesting*.

Maybe part of the joy for me is piecing the concepts together myself, even if I get things wrong sometimes. Part of it may also be long-term effects of growing up with internet, leaving me with a fragmented attention span or whatever. 

But in general, textbooks haven't worked for me. I find myself bogged down, and then I abandon the learning project because the friction in it is too high.

So instead of trying to force myself to learn through textbooks, here's how I learn: 

1. Get grounded in the subject with LLMs — role prompt them as, say, "a professor of math and philosophy at cambridge university" (and tell them to be clear, concise, acknowledge ambiguity, etc.)
2. Ask for more detail on the general domains I think are interesting and relevant.
3. Map out the things that I want to understand based on that detail
4. Use online lectures, video content, textbook *selections* (ones I find online), blog posts to deepen the knowledge.
5. Write up as I go along, clarifying and reordering and refining concepts.

This feels optimal for me right now. It keeps me engaged and excited about new stuff. 

### Learning Math as a story

I think one of the most effective things I've been able to do for myself learning-wise is going from abstract to historical. Don't get me wrong, I really enjoy the abstract — but I find when I learn math embedded in its history, everything feels so much more meaningful. 

Knowing *why* new theories were developed helps make math feel *alive,* exciting, dynamic. That's why this series is focused on the historical timeline, the development of the math, just as much (if not moreso) as it is focused on the math itself.

## Notes on difficulty

I've seen it [argued](https://www.astralcodexten.com/p/book-review-sadly-porn) that making things harder to understand makes them also much harder to misunderstand — by forcing someone to engage with the material and parse it with effort, instead of spoon-feeding them the content in simple-to-understand, bite-sized chunks, you make them understand the ideas better.

I am sort of convinced of that idea. These notes are my own attempt to parse and effortfully process the ideas. I don't think that my shortened explanations will be enough to give you the level of intuition that I've gotten — it's like a lossily-compressed version of the many different sources I digested to make it.

In order to understand these things, you probably need to figure them out yourself. I just hope this can act as maybe a framework from which other people can jump off.

## Notes on preexisting knowledge

I had some basic familiarity with many of the basic notation, concepts, etc. involved in the early parts of this guide. If you have questions that arise, just try and look them up — they are probably pretty basic. 

That said, I don't want to go from the ultra-simple intuitions of math because I would find that boring — you have to start somewhere, and for me that's *wherever my preexisting knowledge left me.* Sorry lol

## Godel, Tarski, and Hilbert

The foundations of mathematics

Goal of this presentation: get myself acquainted with the through line between Hilbert, Godel, Tarski, Church, Turing, and lots of other important people whose thoughts seem interesting. I think formalizing stuff is really cool.

The local/temporary goal is to figure out Godel's incompleteness theorems in detail. 

---
## Where do we start?

It's hard to get anchored in math
I'll go high-level and then go into more detail.

---

## Broad Strokes

High-level ideas, stuff I *sort of get* before starting

- Cantor introduces set theory
- Set theory is kinda cool
- Uh oh, Russell's paradox
- Zermelo: axiom of choice
- Russell and Whitehead try to formalize everything with *Principia Mathematica*
- Hilbert says we should formalize everything; 23 unsolved problems
- *Intuitionism vs. Formalism?* <— I don't understand this
- Godel publishes incompleteness theorems; lots of other cool stuff like tarski and Church/Turing
- Then we re-evaluate and we get ZFC

Other related concepts I'd like to think about: 
- Church-Turing thesis
- Lambda calculus
- This connects into Wittgenstein tractatus, cool
- Category theory
- Type theory (supposedly related to the principia)

---

## Part 1: Euclid and Cantor

[Foundations of Math, Part 1 - Euclid and Cantor](/foundations-1)

---

## Part 2

[Foundations of Math, Part 2](/foundations-2)


Idea: email professors of mathematics and ask them questions about these things.

Other things I want to cover
- [[Godel's Incompleteness Theorems]]
- [[Russell's paradox]]
- [[David Hilbert]]
- [[Tarski's indefinability theorems]]