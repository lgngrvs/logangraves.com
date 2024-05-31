# how do transformers actually work?
Date: 2024-05-09
Tags: notes ai
Type: post
Desc: describing how transformers work in a way that's intuitive to me

Transformers are a cutting-edge architecture for learning from data that can be processed sequentially, e.g. images, audio, and text. I'm learning how they work by writing a post about them. This will be a pretty messy post, following my thoughts as I try and grok it. I may write a cleaned-up version later.

*note: images won't work yet due to differences between local workspace and my website urls. check back once this post is finished and the images will work probably*

Ideally I will eventually be able to write my own textbook on this or something. maybe this is hubris but i feel like i could explain this way better than the existing resources do, save maybe for 3b1b. At least, from fundamentals.
## meta: how to learn this
basically i want to learn by explaining how transformers work. why they work... different question.

i've done this once before, and it didn't go very well. the main problem was that I didn't do a good job of conceptually organizing the content. 

i'm thinking about learning as follows: 
- **high-abstraction to low abstraction:** get a high level architecture to organize all the parts, then go down gradually through layers of abstraction and learn how the parts work gradually.
- **low abstraction to high abstraction:** get a good sense about how a really important thing works (in this case, probably dot-product attention) and then abstract it; build each component up afterwards until you have a high-abstraction model.
	- this is the direction taken by *Understanding Deep Learning* ([link](https://udlbook.github.io/udlbook/)) by Simon Prince, a textbook I've been considering working through

There are lots of resources that I could use. Probably I should prioritize doing things in a way that makes intuitive sense to me — high to low abstraction — using high-quality resources.

**Helpful Interlocutor:** you tried learning this before. why didn't it work out before?

**me:** my best guess is that I didn't produce enough stuff myself. i took notes, but didn't draw diagrams, or implement any code. mainly i didn't try hard enough.

**HI:** how are you going to do things differently this time? 

**me:** ugh, idk, try a little harder?

**hi:** ok, fine. what's the goal here? how will you know that you know these things?

**me:** i will know i know things when: 

1. I can draw out a diagram by hand on a whiteboard and explain the high-level concepts to a smart but not knowledgeable person in about an hour
2. I can implement a simple-ish transformer model in pytorch from scratch
3. I can explain why each part of the model is there and describe its operations mathematically

these are listed in order of importance. i want to hit the abstractions first.

plan: 
- [ ] get a grasp on how information flows through the transformer network, and the *purpose* of each component
	- [ ] start with inputs and outputs
	- [ ] draw my own diagrams, removing the important stuff
	- [ ] key question to answer: *what does each component do? explain it to me in one sentence.*

principles: 
- be highly reflexive. spend time effectively.

## resources & prerequisites
things I know going into this:
- Neel Nanda mech interp foundations
- some vague ideas about autoregression and stuff

resources
- *Understanding Deep Learning* ([link](https://udlbook.github.io/udlbook/)) by Simon Prince
- [3blue1brown videos](https://www.youtube.com/watch?v=wjZofJX0v4M&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=5)
- The original [Attention is All You Need](http://arxiv.org/abs/1706.03762) paper that introduced transformers
- [An Introduction to Transformers](http://arxiv.org/abs/2304.10557), a short paper by Richard Turner

## part 1: wtf is going on here

![[transformers-udl.png]]

![[transformers-aiayn.png]]

ok, so these images are basically the same actually. the diagram on the left for the second one is isomorphic to the first one. they consist of the following parts:

Input → (transformer layer) → output

**Transformer layer:**
1. Multi-head attention
2. LayerNorm
3. Parallel neural network ("feed forward")
4. LayerNorm

...plus some stuff going on with the residual stream.

(And then it gets wired in again later in the transformers diagram on the right. idrk what's going on there but we'll figure that out later I guess.)

(Also, regarding the inputs: there's the matter of input → embedding → positional encoding, but we'll get there later cause I already know this stuff and I'm getting impatient.)

Ok, what do i need to understand? Questions that come to mind?
1. Why is the residual stream wired back in, and not just a straight line through each layer? What even is the residual stream? (answering one will maybe answer the other)
2. What does attention do?
3. Why do we have two layerNorms? what do they do? Do we need them? (I mean, the paper is called "attention is all you need", but evidently we need more stuff.)
4. What does the feed forward/Parallel NN do? Do we need it?

Let me start with the first question. 

### 1.1 what is the residual stream?

"residual stream" doesn't have any results in the "attention is all you need" paper, but "residual" does. 

> We employ a residual connection around each of the two sub-layers, followed by layer normalization. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.


This tells me nothing about what it is. I know what a residual is from statistics — it's the difference between the *predicted value* by a model and the *actual datapoint*, used to measure how accurate a model is — but it doesn't seem to be serving that purpose here. It links to another paper from 2016 called "Deep residual learning for image recognition" which I doubt will be very helpful right now. Let's try a different resource.

> **Residual connections.** The use of residual connections is widespread across machine learning as they make initialisation simple, have a sensible inductive bias towards simple functions, and stabilise learning [Szegedy et al., 2017]. Instead of directly specifying a function $x^{(m)} = fθ(x^{(m−1)})$, the idea is to parameterise it in terms of an identity mapping and a residual term $$x^{(m)} = x^{(m−1)} + resθ(x^{(m−1)})$$.

Uh, wtf?
Things I don't understand here, and guesses for what they mean: 
- *initialisation* — the weights you have before training?
- *inductive bias towards simple functions* — uh, I guess they're more likely to learn simpler functions or something?
- *stabilise learning* — change in loss is more predictable? 

none of those things really tell me about the residual stream though.

- *parameterise*: not sure what this means in the context of ml
- *identity mapping*: mapping onto itself, the $x^{(m−1)}$ term
- *residual term*: the $resθ(x^{(m−1)})$ but idk what this does

The math indicates at least *something*: that is, rather than doing a simple function $f$, we do... something, and then also add in previous outputs? 

From the previous paragraph: 

> We can now stack MHSA and MLP layers to produce the transformer block. Rather than doing this directly, we make use of two ubiquitous transformations to produce a more stable model that trains more easily: residual connections and normalisation.

So it looks like the residual connection is a bonus to make the model work more nicely, as is the layerNorm. The Multi-head self attention and the multi-layer perceptron — the feed-forward part — is what matters. So we can get rid of the residual thing for now and just imagine a simpler architecture, where it's just input → MHSA → Feed forward → output. 

oh wait! LOL! I have ai that can explain this to me and reasonably reliably answer my *exact questions*! wtf am I doing? what am i paying $20/mo for?

Residual Stream: 

> In the context of transformers, particularly in deep learning, a "residual stream" typically refers to the use of residual connections, a key feature in architectures like the Transformer model used in natural language processing and other tasks. These connections are also known as "skip connections" and were first popularized by the ResNet model in computer vision tasks.
> 
> The residual stream or connection works by allowing the input to a particular layer to be added directly to its output, effectively skipping the layer (or series of layers) in between. This approach helps in addressing the vanishing gradient problem that can occur in very deep networks, where gradients (used in training the network through backpropagation) can become increasingly small, thus stalling the training process. By adding the input directly to the output, gradients can flow more directly through the network.
>
> (...) the output of the sub-block is added to its input (the residual), and then usually followed by layer normalization. This design encourages learning modifications to the identity mapping (input), rather than complete transformations, stabilizing the training of very deep models


oh ok so it's just — "we calculate attention and then add it to the input of the layer and then stick that into the next part of the layer."

great! so now we know it goes like

input → calculate attention → add attention to input to make attention-input combo →  feedforward network → add feedforward output to attention-input combo → output

### 1.2 input output? huh?

ok so i know: 

- input is a matrix of shape $N \times D$
	- N is the number of input tokens; this tells you that each column corresponds to a vector, which represents a token 
	- D is the size of the embeddings (how precise in meaning-space you get? how expensive computations are?)
- output is a probability distribution across vectors e.g. vector 1 has 90% probability of being the next token
	- this is also an $N \times D$ matrix? huh? where do you put the probabilities?

what happens to get from one to the other?? 
- prediction: MHSA processes the input
- feed-forward 

to figure out what the output actually is, I should probably figure out multi-head self-attention? maybe? and see what that gives as an output

let's look at mhsa i guess

### 1.3 attention?? (multi-head self-attention)

![[selfattention-udl.png]]

this diagram makes some sense — you do some sort of calculation using $K, Q, V$ to produce the attention matrix, and then you multiply it to the inputs to get outputs?

> A self-attention block $sa[•]$ takes $N$ inputs $x1, . . . , xN$ , each of dimension $D × 1$, and returns $N$ output vectors of the same size.

Ok so the outputs of self-attention are vectors. are they... tokens?

No! looking back at the residual stream thing above, these are *not* tokens. the attention matrix is added to the original input — this is the *add* in *add & norm.* 

Ok. So we have this idea, that the attention matrix is computed and then added to the inputs. What actually does the attention matrix represent — what's going on?

Let's take a look at the 3b1b [attention video](https://www.youtube.com/watch?v=eMlx5fFNoYc&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=6) to try and understand the diagram above at the beginning of section 1.3.

> The aim of a transformer is to progressively adjust these embeddings so that they don't merely encode an individual word, but they instead bake in some much, much richer contextual meaning.
>(Timestamp: 01:28-01:35)

This tells us something super useful! the attention mechanism computes the relations of a bunch of words to one another. 

What's happening here is that individual vectors represent the token *out of context.* (well, that along with the position of the word in the sentence, which I'll look more into later.) It's a very rough guess at meaning.

Attention is *adding context* to each embedding's meaning, based on their relationships with one another — it's adding to the vector in order to make the word represent its meaning *in the sentence that the transformer is seeing it,* not just the abstracted-away meaning of the word.

Continuing on with the 3b1b video this gets even more interesting. Since the transformer model is sequential (i.e. it works token-by-token, going forward through the sentence) the next token is predicted based *only on the last token.* 

We were wondering earlier what the outputs of the model are: the model spits out a highly-refined version of all the embeddings, a matrix where the attention mechanisms have now adjusted the values on the vectors. 

Adjusted *so much so* that now it somehow contains *all the information in the whole passage.* Then we predict the next token based *only on this final token.* Woah!

#### 1.3.1 How Does attention work: Query, Keys, Values

To understand how multi-head self-attention works, let's keep looking at the original diagram: 

![[Screenshot 2024-05-11 at 12.58.27 PM.png]]
We have a reasonable guess at what's happening overall. 

1. Input is turned into tokens with positional encodings
	- What's happening: The raw text input is turned into vectors, which roughly represent the abstract meaning of words. Positional encodings add position data on top of this
2. **Multi-head attention**: With those embeddings as input, we compute attention for each word relative to each other word.
	- we do scaled dot-product attention a couple times
	- this has that query, key, values thing going on idk what that means though

What I want to start doing is turning this into code, or at least pseudo-code, that reflects what I've talked about.

here's what we have so far: 

![[Screenshot 2024-05-11 at 1.24.48 PM.png]]
now i want to high-level cover the rest of the model.

![[Screenshot 2024-05-15 at 10.06.54 PM.png]]

#### attention head (ignore me for now)
> The ELI5 for attention head is really not easy.
> 
> We start with one representation for each word, and with an MLP we produce 3 new representations for each word. Then we mix these representations in a way that allows us to produce one final contextualized representation for each word.
> 
> The "not easy part" is how we mix it. In a way it doesn't really matter, we could say "we tried many things and this one is the best". We could also just show the maths. But that's not an explanation.
> 
> One representation is "how I interpret this main word with all other secondary words", another representation is "how this word as a secondary word should be interpreted when all other words are perceived as the main word", and a final representation is "what should I keep from this word to build a final representation". It's hard to explain it if you didn't see the maths. I'm not able to do a real ELI5 on this. If you implement it by yourself it's usually more clear.
> 
> The transformer is just a bunch of attention heads. If you get the attention head, the rest is easy.


## what does feed forward do

answer: https://www.reddit.com/r/LanguageTechnology/comments/gsyw10/comment/fs8veo8/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
(is this true? doubt)

> Before that layer, a given element is partitioned by heads. If you had a 32 dimensional vector with eight heads, then elements 0-3 are functions of other position's 0-3. Elements 4-7 are functions of other position's 4-7. One head can't talk to another. To mix them, you have a linear layer. To mix them expressively, follow that with a nonlinearity?



ok, so sorta maybe. basically, attention is a linear transformation. if you have 70 linear transformations, they can all be combined into one single transformation. having multiple linear layers is pointless, because they're equivalent to a single linear transformation. (why is this? matrix transformations can be composed into a single equivalent transformation)  


## Encoder Vs. Decoder

Part of the reason transformers are so hard is that there are lots of different ways they're used, and so different people try to teach them to you in different purpose-specific ways.

One of the core ways that I was confused when I was trying to figure this out was the concept of the encoder vs. the decoder.

In the original *attention is all you need* paper, they have both an encoder and a decoder. Initially I was like WTF? why is this here? And the complicated structure threw me off. I got sidetracked trying to figure out the difference, and when tutorials showed how to do both i was kinda crying. 

It turns out that was dumb. It's actually not that deep.

The encoder/decoder thing is specific for machine translation and similar tasks. Something like, "the encoder generates a nice representation of the input sentence" and then "the decoder goes word-by-word and generates the translation, using the generated representation from the encoder for context"

ChatGPT:

> Yes, there are several applications of transformers where only the encoder or the decoder component is utilized, instead of both:
> 
> 1. **Encoder-Only Applications:**
>    - **BERT (Bidirectional Encoder Representations from Transformers):** This model uses only the transformer encoder. It's designed to pre-train deep bidirectional representations by conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications.
>    - **Sentence Embeddings:** Transformers that use only the encoder can be employed to generate dense vector representations of sentences, which can then be used in various NLP tasks such as semantic search, clustering, and information retrieval.
>    - **Document Classification:** In this use case, the encoder processes the text of a document and outputs a representation that can be used for classification tasks, like determining the topic of a document or detecting the sentiment.
> 
> 2. **Decoder-Only Applications:**
>    - **GPT (Generative Pre-trained Transformer):** In contrast to BERT, GPT uses only the transformer decoder. It is trained on a language modeling objective and is used for generating text. GPT models are trained to predict the next word in a sentence and can generate coherent and contextually relevant text over extended passages.
>    - **Image Generation:** Models like DALL-E, which use a transformer-based architecture for generating images from textual descriptions, primarily employ a decoder-like architecture. These models interpret and convert textual descriptions into coherent visual representations without the need for an encoder processing textual inputs.
> 
> In each of these cases, the chosen architecture (encoder-only or decoder-only) aligns with the specific requirements of the task. Encoder-only models excel in applications where the entire input needs to be understood, while decoder-only models are fit for generative tasks where the output is sequentially produced based on some form of input (like a prompt for text generation or a conditioning image/text in multimodal tasks). These models demonstrate the flexibility and adaptability of the transformer architecture to a wide range of tasks beyond the encoder-decoder setups typically seen in machine translation.

GPTs are only decoders. *You don't need to stress about this lol!* Just think about one half of the diagram from attention is all you need.


![[CDC23534-7708-4BC3-A9A2-AD2B378D8BE6.png]]

[3b1b video!!](https://www.youtube.com/watch?v=LyGKycYT2v0&pp=ygULZG90IHByb2R1Y3Q%3D)



Ok now I'm skipping a bunch because I don't feel like logging the learning I did. 

Basically I learned how Key and Queries work — they're two different matrices and they correspond to each other but they're different so that attention doesn't have to be bidirectional.

Wow, positional encodings seem complicated but maybe they aren't. 

Now I'm interested in learning about parallelization and stuff. I wonder if there's a good textbook on the development of ML architectures. Wait, actually, there probably is. Wikipedia is pretty good for this.

[[Parallel computing]]

![[History of Language Models.png]]

