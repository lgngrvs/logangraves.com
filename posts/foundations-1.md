# Foundations of Math, Part 1 - Euclid and Cantor
Date: 2024-02-01
Tags: #mathematics #notes
Type: post
Desc: Introduction to basic set theory, ordinals, and cardinals.

These are my markdown notes for an in-progress project; see below sections for details. I've found that I learn best by grouping information into small sequential chunks, and writing it as if it's an explainer (except the goal is for me to understand by writing it and the audience is an afterthought, so I might skip some stuff I don't feel like writing out) published directly from my Obsidian vault. 

I found that, when learning about philosophy, anchoring myself in time and tracing the development of ideas over its course helped me conceptually organize the material and avoid getting stressed over the sheer volume of information I wanted to consume.

### Euclid and the parallel postulate

- Begins with Euclid, geometry -- the notion of *proof*. 
- Euclid has 5 postulates.
- Parallel postulate: An essential part of geometry as we think of it conventionally -- but if we don't accept it, we get Non-euclidean geometry, geometric systems that are formally consistent despite not representing physical space in the conventional way we might perceive it.

---
### Intuition and formality
- A parallel current going on: the need for formalization
- Before Cantor, math mostly deals with concrete, mathematical objects, and intuitions. Distinct disciplines.
	- Take a look at, e.g. islamic mathematicians, Euclid, etc. — proofs are like paragraphs, no symbolic notation
	- Newton and Leibniz developed calculus, but didn't really formalize it — e.g. used the notion of the infinitesimal. It worked, but wasn't formal. Hence, mathematicians wanted a formal notion of it.
- There's a need to *formalize infinity.* Ideas about infinite series, functions, limits, etc. could have paradoxes. 
- Also, how do we unify math? 

--- 

### Cantor|Georg Cantor introduces Set theory

- In a single paper — "On a Property of the Collection of All Real Algebraic Numbers" — Cantor introduced set theory.
	- *To be studied later: set theory as the formalization — the giving of notation — to notions of… idk, concepts? Categories?
- Sets can contain any kind of object — sets, numbers, etc. 
	- Potential to unify all the different branches of mathematics
- Can deal with *infinity* — different notions of infinity, etc.
- Why is this cool? 

--- 
### 🗝️ Key ideas in Set theory: Set and Subset
- **Set**: A collection of distinct objects. 
    - E.g. $A = \\{1, 2, 3\\}$
- **Subset**: Set B is a subset of A if every element contained in B is also in A. 
	- $B = \\{2, 3\\}$, therefore $B \subset A$
	- $B = \\{4, 5\\}$, therefore $B \not\subset A$
	- *Not* like a folder/hierarchy kind of thing. It's not that Set A contains   *only* Set B, and set B contains the elements; There's no hierarchy to sets. You're just selecting pieces of them.
- **The empty set:** written as $\varnothing$ or just $\\{\\}$, the empty set just doesn't have anything in it. (It's actually insanely useful and important.)

--- 
### 🗝️ Key ideas in Set Theory: Power Sets

- The **Power set** of set $A$, written as  $\mathcal{P}(A)$ , is the set of all possible subsets of $A$, including $A$ itself and the empty set (the set containing no elements, often denoted as $\varnothing$ ). 
	- For example, given that $$A = \\{0, 1, 2\\},$$ we can say that $$\mathcal{P}(A) = \\{\varnothing, \\{0\\}, \\{1\\}, \\{2\\}, \\{0, 1\\}, \\{1, 2\\}, \\{0, 2\\}, \\{0, 1, 2\\}\\}$$
- Think of this as *all possible ways to group the elements in set A*: to make each subset you're allowed to take any number of items from A, however you choose. (You can't add extra elements, though.)

--- 
### 🗝️ Key ideas in Set Theory: Cardinality
- **Cardinality**: How many elements are in a set
	- $A = \\{1, 2, 3\\}$, therefore $|A| = 3$
- Cardinality will be an integer if the set is finite. 
- If the set is infinite, it gets more complicated.
- Cardinality is also related to the notion of Isomorphism, correspondence, etc. I'll get there in a sec. For now we need to talk a little about how set theory let us deal with infinity.
--- 
### Cool sidebar: Cardinality of the Power Set

- A cool thing to note: the cardinality of $\mathcal{P}(A)$ will always be equal to $2^{|A|}$. This is Cantor's theorem, which we'll see in a moment.
	- This seems unintuitive at first, but if you think about it, it makes sense; there are $|A|$ elements, and for each subset, each element in $A$ can either be included or not included. (It's a binary choice.) 
	- *If you imagine it as a binary tree, the $2^{|A|}$ number makes a lot of sense intuitively.*

--- 
### Interlude: Number systems
- One of the cool things that set theory lets us do is talk about different kinds of infinity. 
- First, a quick review of important sets: 
	- The natural numbers, $\mathbb{N}$, are the numbers that we count with "naturally" — they're basically the most basic idea of numbers. 
		- You can list them out in order: $\mathbb{N} = \\{1, 2, 3, 4, 5 ...\\}$
	- The integers, $\mathbb{Z}$ (just by convention I guess), are all the whole numbers. They stretch out on both sides of 0: $\mathbb{z} = \\{... -3, -2,  -1,  0,  1,  2,  3, ...\\}$
	- The real numbers, $\mathbb{R}$, are all the numbers that we might normally talk about. This contains all the natural numbers, 0, fractions, infinite decimals, etc. 
		- Any normal "number" you might operate with in reality is a real number. 
		- You can't list out the real numbers in order — where do you start? 0? then what? 0.1, or 0.001, or 0.0000000001? or 1? 
	- (see more at [Varsity Tutors](https://www.varsitytutors.com/hotmath/hotmath_help/topics/number-systems))
- ==Important note for future Logan: explain how these are formalized==

--- 

### 🗝️ Key ideas in Set Theory: Ordering a set
- Sets don't have an order, necessarily. If you put apple, orange, and banana into a set, that concept doesn't make sense.
- However, order *can* be a property of some sets. 
- One formal concept is that of a Well-ordered set. 
	- Formally, a set is well-ordered if every possible subset of it has a *smallest element*. 
	- The natural numbers are well-ordered, because there's no way to define a subset of them that isn't well-ordered.
	- The real numbers $\mathbb{R}$ are not well-ordered, because we can define a subset that does not have a least element, for example $(0,1)$. 
- Well-ordered sets use the relation $<$, less than. There are other orderings of sets, which allow for flexibility, though. 
- They get pretty complicated, but for example lexicographic ordering for letters turns $\\{b,g,f,a\\}$ into $\\{a,b,f,g\\}$ (since "less than" doesn't make sense for letters).

--- 
### Interlude: Bijections 
- We need one more key idea to start talking about infinite cardinality: *relationships between elements in sets* — a special kind of correspondence called a Bijection, also known as a "one-to-one correspondence."
	- Set $A$ has a bijection with Set $B$ if each element in $A$ has a corresponding element in set $B$. 
	- Imagine we take a random element in set $A$.  Now let's take a random element in $B$, and draw a line between the two. 
	- Keep drawing lines until we can't draw any more lines. If there are no elements left un-connected in either set, there's a bijection between them; if there are elements left over that don't have a pair, they're not bijective.
- If you're curious about the formal way we talk about bijection, we have to define it as a function that *maps* one set onto another: We define a function $f$ that maps  (mapping is just the formal way to talk about drawing lines) set $A$ onto set $B$ as follows: $$f : A \rightarrow B$$ The function $f$ is bijective if $$\forall b \in B$$ — "for all elements (labeled $b$) in the set B" — $$\exists ! a \in A$$ — "there exists exactly one element in A" — such that $$f(a) = b$$  ("if you put $a$ into $f$, you get an element $b$ as an output").
- How this relates to cardinality: **if two sets are bijective, they must have the same cardinality. If they have the same cardinality, they must be bijective.**
	- Why? Think about it — same number of elements in each guarantees that you'll be able to draw an arrow between the two.
- There are more kinds of -jections (injection, surjection) which we'll get to later. For now, we'll leave this idea of Bijection cause it's intuitive.
- To add a little bit of vocabulary, just on the side, *Equinumerosity* is what we call it when there's a bijection between two sets, or alternatively $|A|=|B|$ . (I *think* these are the same thing.)
- (You might also see the term Isomorphism being thrown around; I avoid that term here even though it's technically maybe usable because the same two sets can be labeled isomorphic or not isomorphic depending on what characteristics you're looking at. Isomorphic might imply some sort of ordering relation. e.g. [this video](https://www.youtube.com/watch?v=efTeurdX__A0))
--- 
### 🗝️ Key ideas in set theory: Infinite cardinality
- There are lots of different kinds of infinity. 
- One easy distinction between kinds of infinity is where we talk about *countable* and *uncountable* infinity. 
	- We talked about this earlier with the naturals and the reals ($\mathbb{N}$ and $\mathbb{R}$) — you can *count out* the naturals. Start at 1, just keep going. 
	- Versus with $\mathbb{R}$, we don't know where to go next — there's no sense of *order.*
- Formally, we actually use $\mathbb{N}$ in some of our definitions. 
- The simplest kind of infinite cardinality is *countable* infinity: there's no limit to the amount of elements in the set, but you can list them out in some meaningful order.
	- A set is countably infinite if we can draw a bijection between it and the natural numbers: $$ A  \newcommand{\twoheadrightarrowtail}\mathrel{\mathrlap{\rightarrowtail}}\mathrel{\mkern2mu\twoheadrightarrow} \mathbb{N}$$
	- We denote the cardinality of $\mathbb{N}$ as $\aleph_0$ ("aleph null", a hebrew letter — don't ask me why, maybe they just used it cause it looks like N lol). I.e. $|\mathbb{N}| = \aleph_0$ A nicer way to say that there's a bijection between $A$ and $\mathbb{N}$ is to talk about it in terms of cardinality of N: $$|A| = \aleph_0$$
	- You can think about this also as "numbering" all the elements in $A$. If they have a bijective relationship, that means you could give a number to each element in $A$; e.g. you could select an element in $A$ and number it 1, then choose a different element in a and call it number 2, and continue on in this fashion infinitely.
	- The key idea here is that there must be a *systematic* way, some sort of algorithm to do this — you can't just select random elements, otherwise $\mathbb{R}$ would have cardinality $\aleph_0$, which would make the concept useless and defeat the point of distinguishing countable and uncountable infinity. 
		- For example, we can prove that $\mathbb{Z}$ (the integers, if you remember) is countably infinite because there's an algorithm that maps every element in $\mathbb{Z}$ onto another element in $\mathbb{N}$. 
		- One way to do this is using odd and even: zero maps onto zero, then each negative number in $\mathbb{Z}$ maps onto each odd number in $\mathbb{N}$ (e.g. $-1 \rightarrow 1$, then -$2 \rightarrow 3$, then $-3 \rightarrow 5$, and $-4 \rightarrow 7$, etc.) and each positive number maps onto each even number ($1 \rightarrow 2$, then $2 \rightarrow 4$, then $4 \rightarrow 6$, etc.)
	- Hopefully this idea of map $A$ onto $\mathbb{N}$ makes sense, but if not I don't think it's essential. 
- It seems intuitive that $|\mathbb{R}| > \aleph_0$  — there's some idea of, like, "bigger-ness" in the real numbers. There's just more of them, they don't really make sense, you can't map them onto $\mathbb{N}$. But how do we prove this?

### 🗝️ Key results in early set theory: Cantor's diagonalization proof
- Cantor came up with a cool method in order to prove that $|\mathbb{R}| \not = \aleph_0$, called Diagonalization. Diagonalization Generalization|generalizes in all sorts of cool ways, but for now I'm going to give you just this one argument. 
- Let's assume for a moment that $|\mathbb{R}| = \aleph_0$ . This means that we can write out all the elements in $\mathbb{R}$ in an ordered list.
- For simplicity, we'll look at just a subset of $\mathbb{R}$: we'll use the numbers between 0 and 1 — if these numbers aren't countable, then since they're a subset of $\mathbb{R}$, $\mathbb{R}$ isn't countable either. 
- *(For finite decimals we'll just add add 0s on the end to make them the same length as our infinite decimals.)*
- I'm going to use just some random numbers for illustration: 


 Index   | Number |   .  |  .   |  .   |   .  |   .  |   .
 ------- | ------ | ----- | ----- | ----- | ----- | ----- | ----- 
 ***1*** | 0.     | 1   | 0   | 0   | 0   | 0   | ... 
 ***2*** | 0.     | 7   | 7   | 7   | 7   | 7   | ... 
 ***3*** | 0.     | 7   | 1   | 8   | 2   | 8   | ... 
 ***4*** | 0.     | 1   | 0   | 2   | 0   | 1   | ... 
 ***5*** | 0.     | 9   | 9   | 0   | 0   | 0   | ... 
 ***6*** | 0.     | 3   | 9   | 8   | 4   | 6   | ... 
 ...     | ...    | ... | ... | ... | ... | ... |  ..   

(Using a markdown table is hard for this visually, sorry, so feel free to watch this [video version](https://youtu.be/0HF39OWyl54?feature=shared&t=72) created by Trefor Bazett or just search "diagonalization argument demonstration" or something like that online. I'm sure that there are plenty of other representations out there, this is just one that works well enough and which I found within like 5 minutes of searching.) 

- Let's assume that we have *every single possible number* in this list. 
- If we can come up with a new number that isn't in our list somehow, we prove that there would be a logical contradiction created if $\mathbb{R}$ were countable, and therefore that it cannot be countable.
- Turns out, there is a way. Let's do something clever. Let's select the digits going diagonally down the list, i.e. the 1st digit of the 1st number, 2nd digit of the 2nd number, etc. going down the whole list (so that there is a digit selected from every single number in the list)

| Index   | Number |     |     |     |     |     |     |
| ------- | ------ | --- | --- | --- | --- | --- | --- |
| ***1*** | 0.     | [1] | 0   | 0   | 0   | 0   | ... |
| ***2*** | 0.     | 7   | [7] | 7   | 7   | 7   | ... |
| ***3*** | 0.     | 7   | 1   | [8] | 2   | 8   | ... |
| ***4*** | 0.     | 1   | 0   | 2   | [0] | 1   | ... |
| ***5*** | 0.     | 9   | 9   | 0   | 0   | [0] | ... |
| ***6*** | 0.     | 3   | 9   | 8   | 4   | 6   | ... |
| ...     | ...    | ... | ... | ... | ... | ... |     |

- And let's add 1 to each value, turning 1 into 2, 5 into 6, and 9 into 0 (just rolling over instead of turning into 10). 

| Index   | Number |     |     |     |     |     |     |
| ------- | ------ | --- | --- | --- | --- | --- | --- |
| ***1*** | 0.     | [2] | 0   | 0   | 0   | 0   | ... |
| ***2*** | 0.     | 7   | [8] | 7   | 7   | 7   | ... |
| ***3*** | 0.     | 7   | 1   | [9] | 2   | 8   | ... |
| ***4*** | 0.     | 1   | 0   | 2   | [1] | 1   | ... |
| ***5*** | 0.     | 9   | 9   | 0   | 0   | [1] | ... |
| ***6*** | 0.     | 3   | 9   | 8   | 4   | 6   | ... |
| ...     | ...    | ... | ... | ... | ... | ... |     |

- There's our new number, 0.28911...
- And guess what? It *can't* be in the list already. Why? Because it is guaranteed to have at least 1 place value different from every single number in the list, since we generated it by taking a digit from every number from the list and adding 1 to the digit.
- Its 1st digit is different from the first number on the list, 2nd digit different from the 2nd, 3rd different from the 3rd, et cetera. 
- Hence, we've created a contradiction. We said we had all the real numbers between 0 and 1 in our countable list, but then turned out that no matter how we list the numbers, we can always come up with a number that's not in our list. Turns out our list isn't countable after all.
- Since our premise that $|\mathbb{R}| = \aleph_0$  led to a contradiction, our premise must be false; therefore $|\mathbb{R}| \not= \aleph_0$  $\blacksquare$ 
- This will reappear in all sorts of ways down the line, in everything from Russell's paradox to Godel's Incompleteness Theorems to Alan Turing's Halting problem. Diagonalization gets really abstract, though, so I think the best way to get to that abstraction is through seeing a bunch of examples, and then coming back and figuring out what they all have in common. So for now, we'll leave diagonalization. :)

--- 
### 🗝️ Key results in early set theory: Cantor's theorem
- Actually I don't have this in me right now, but I'll cover it when we talk about diagonalization more later. 
- [This video](https://www.youtube.com/watch?v=dwNxVpbEVcc) looks pretty interesting. #to-consume

--- 
### 🗝️ Key ideas in early set theory: Transfinite Numbers

^44ec4a

- Ok, so finite sets are pretty easy to deal with; cardinality makes sense because you can just count the objects in the set.
- But when we start getting infinite sets, how do we compare their sizes formally? How do we deal with precise positions within those sets — say, if we define a set as $\mathbb{N} \cup \\{0\\}$, i.e. $\\{1,2,3,4,...,0\\}$? What position is 0 in? %% Need to define order for this to make sense though%% 
- We need notation and concepts to deal with different kinds of infinity. 
- One of Cantor's most important contributions to math was his ideas about *transfinite numbers,* numbers that were meaningfully different in size but all bigger than the natural numbers — so infinite, but in different ways. Let's see what that means.

## 🗝️ Key ideas in Early Set Theory: Cardinals
- Let's start with Cardinal numbers. Every set has a cardinality — but when we have, say, uncountably infinite sets and countably infinite sets, we need to be able to express that. The *size* of those infinities is different.
- We've already seen $\aleph_0$: the size of $\mathbb{N}$. $\aleph_0$ is the smallest *countable* cardinal; in other words, it's the smallest infinity.
- $\aleph_1$ is the smallest *uncountable cardinal.* In other words, it's the smallest *uncountable* infinity.
	- The Continuum Hypothesis posits that $|\mathbb{R}| = |\mathbb{C}|$ = $\aleph_1$  — but as of now it's unproven. We're not quite sure *which* $\aleph$ it is. (Understanding why this is will probably mean that you understand cardinals.)

### 🗝️ Cardinals pt. 2

- Let's go back to our example,  $\mathbb{N} \cup \\{0\\}$. The cardinality of $\mathbb{N}$ is $\aleph_0$. Adding one more number into that set will not change its already-infinite cardinality. 
	- We can prove this by defining a function $f$ that maps $\mathbb{N}$ onto $\mathbb{N} \cup \\{0\\}$; intuitively, $f$ is a bijection between the two sets. Their cardinality is the same, because we can draw a 1-1 correspondence between element $n$ in $\mathbb{N}$ and $n-1$ in $\mathbb{N} \cup \\{0\\}$.  ==Unsure about this tbh==
- But we still need to be able to talk about the individual indexes — because if we insert $0$ at the end of the set, what index would have? How do we talk about *where in the set it is?*
- For this we need *ordinal numbers*.

### 🗝️ Ordinals 

- Cantor defined $\omega$, the number after all the natural numbers have been counted. 
	- So you go, $1,2,3,4\ldots, \omega, \omega + 1$, etc.
	- If we define a set $\mathbb{N} \cup \\{0\\}$, $0$ would be at the $\omega$-th place in the set — after all the natural numbers have been counted. ==is this correct==
- It's important now to distinguish between *order* and size — *ordinals* and *cardinals.* $\omega + 1$ isn't *bigger* than $\omega$, it just comes *after* $\omega$. 
- Ok, now let's see how far we can go now that we have $\omega$. $\omega, \omega +1, \omega +2, ..., \omega + \omega$ ($\omega + \omega$ makes sense intuitively as the union between two sets with cardinality $\aleph_0$, say, "count all the even numbers, and then count all the odd numbers."). We can rewrite $\omega + \omega$ as $2\omega$ for shorthand. 
- Then we can keep going, past $3\omega, 4\omega, ... \omega * \omega$. ($\omega * \omega$ = $\omega^2$; we can imagine this intuitively as a countably infinite list of countable infinities.)
	- Visualize $\omega^2$ as a 2d list $\omega$ by $\omega$. *An infinite list of infinite lists.*
	- Visualize $\omega^3$ as a list of those 2d lists, now extending into 3 dimensions, $\omega$ by $\omega$ by $\omega$. *An infinite list of infinite lists of infinite lists.*
	- We can't really visualize $\omega^{\omega}$, but in theory this should sorta make sense; an  $\omega$ -dimensional grid of $\omega$ by $\omega$ by $\omega$ by $\omega$ by ... by $\omega$. *An infinite list of infinite lists of infinite lists of infinite lists... infinitely nested.*
	- It no longer really makes sense to visualize past this, but we can go to $\omega^{\omega^{\omega^\omega...}}$ , applying this operation infinitely.
	- Past that we hit $\epsilon_0$.  
	- What is $\epsilon_0$ 

### Operations on Ordinals
- Note here that addition and multiplication are *not commutative.* $1 + \omega$ is equal to $\omega$ *(prove this by proving $\mathbb{N}\cup \\{0\\} = \mathbb{N}$)* but not $\omega + 1$ . Similarly, $2 * \omega$  is not equal to $\omega * 2$. 
	- This is weird and tells you a lot more about the nature of ordinals. 

It was at this point that I decided to try out a textbook. [Math Stack Exchange](https://math.stackexchange.com/questions/251490/textbooks-on-set-theory) recommended this one, so I'm gonna try it.
I tried it, and it just has a bunch of stuff that I don't really care about. I find textbooks too boring, i.e. too methodical, too heavy on notation, too formal.  I don't want the guide through everything, I want enough knowledge to interact with stuff I find interesting; I want *mathematical intuitions* that I can develop over time, not comprehensive knowledge on subject A before I get anywhere on subject B. (perhaps attention span plays a role here as well.)

### Moving on

- At this point, I'm beginning to feel bogged down by ordinals. Cardinals make sense mostly; ordinals seem not particularly useful, and I have the basic sense for them without much depth at this point. 
- I looked at a set theory textbook recently, which had them as chapter 8 — it's possible that I tried going too deep into this, too early. I'm going to move on for now, and then come back to this if ordinals come back up and I need the knowledge.
- For future self: To come back to this, [this video](https://www.youtube.com/watch?v=5NSg_wJkEMc) seems like it might be good.
- [This video series](https://www.youtube.com/watch?v=kv5k56b3XNA) also looks really good.

# Feedback
> 
>  Notes:
>     
>    1. This is the beginning
>     2. Informal (bad pun) but ultimately correct)
>     3. Confusion here is good. We can't actually define a set or an object. Just things we think it should do. We have a universe. Do we know it? No. We impose law.
>     4. Subset Correct, add union/intersection. Or XOR if you want.
>     5. Made a shit joke at [...] about how the powerset of the people at camp is even in size. I think add that its 2^|size of set| (explain in finite case)
>     6. Introduce cardinality here, so ignore 5 (or swap them). Infinite is indeed more complicated.
>     7. Ahhh, Call me the predictor. Remove the tidbits for 5-6, you name it here and this is good.
>     8. "List them out in order" i think is a little vague. The intuition I carry is if I count for any element in the set I'll eventually reach it. Normal is a 'math word' technically but it is fine here.
>     9. WOP! Give an example maybe why WOP holds in N and why it doesn't hold in Z.
>     10. Good explanation of bijection intuitively, add "vice versa" (just because currently it might allow duplicates). Image notation is good. You only do surjectivity which isnt enough for bijectivity, I think add this. Eqnumeriousity is a v rare word imo but it is used correctly here.
>     11. R has an 'order' but you get the point across --> maybe clarify by "theres no _next_ real number". Maybe add Q is countable to break intuition (ie we hope its because of this thing that is also true in Q, but Q is countable...)
>     12. Great explanation!!!
>     
>     14. Good transition, very soft
>     15. I'm not actually sure thats the immedate statement of CH, since you have to say |R| = 2^{N}. I think the intuition behind this for me is (0, 1) = R so you can take binary strings and map them to subsets of N, but that seems too much. But once you have that its clear why this CH is correct.
>     16. Whats the unsure bit about, I think that should be correct, good lead in
>     17. Effectively yes, that's the intuition for omega. The buildup goes hard. Use tetration._
>     18. Yep, ordinal operations are weird. This and 19 to me show you have a basic intuition for stuff and r ready
>     
> for 10 add injectivity was my only real comment