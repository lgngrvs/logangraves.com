# Notes on "A Mathematical Framework for Transformer Circuits"
Date: 2025-06-14
Tags: interpretability notes
Type: post
Desc: Close-reading a classic interpretability paper and trying to make sense of it

This paper, "A Mathematical Framework for Transformer Circuits" establishes some of the vocabulary and mental model for circuit-finding in attention heads. I started writing notes to process the material actively because it's interesting and seems important. These notes ended up turning into basically me just summarizing the paper for future reference; cool, I guess. This blog post is likely best read *alongside* the original paper. It's relatively complete and, after the first section, tied chronologically to the paper's structure.

[TOC]

## 1. The Tensor Product

I've studied applied linear algebra, but never seen this notation before. The tensor product is essential for understanding this blog post, though, and it's one of the core pieces of notation they use. Thus, let's first understand the tensor product (kind of). There are many ways to talk about the tensor product. I'm going to try and explain it in the simplest way that I understand it; you shouldn't require an immense amount of understanding in order to grasp it for the purposes of this paper. I'm aiming to give just enough intuition here to be able to work with the notation in the paper. 

We write the tensor product, $\otimes$, with $A \otimes W$ and when applying it to vectors we use $(A \otimes W)x$. The tensor product has some nice properties, particularly the **mixed-product property** $$(A \otimes B) \cdot (C \otimes D) = (AC)\otimes(BD).$$ We will use this property a lot later.

Normal linear algebra specifies matrix composition sequentially: $ABx$ means "apply $B$ to $x$, then apply $A$ to the result." In theory, this should capture a lot of linear operations that we care about. However, some operations we want to specify are not nicely decomposed into sequential matrix multiplications. The tensor product is one such operation.

One way to think about it is, for some matrix $X$, "the tensor product expresses operations on the columns and the rows of $X$." Formally, we can think of this as left-right multiplication: 
$$(A \otimes W)X = AXW^T$$
You can use this to see more obviously why we have the mixed-product property described above; in particular,  $$ACXD^TB^T = (AC)X(BD)^T = (AC)\otimes (BD) \cdot X.$$
In the "Additional Intuition and Observations" section, there are additional descriptions of the tensor product. Also, Axler has a treatment of it in *Linear Algebra Done Right* that describes it as a way to multiply vectors in different vector spaces. For now I'm going to just work with this 'right-left multiplication' version, since I think it's the most intuitive.

From the paper: 
> In transformers specifically, our activations are often 2D arrays representing vectors at different context indices, and we often want to multiply "per position" or "across positions." Frequently, we want to do both!

In other words, activations for a given sequence are matrices of shape `[sequence_length, embedding_dimension]`. We can describe these matrices vectors as vectors of size `embedding_dimension` concatenated together, giving each a position in the context (i.e. the first column is position 1, the second column is position 2 in the context, etc). Oftentimes we want to apply transformations *per position* (meaning differently to each vector) or *across positions* (meaning the same across vectors). We will see why we want this in the next section. 

The tensor product packages this together. In order to write it as a single composition of right or left-multiplications, instead of right-left multiplications, you'd need something like the identity $vec(AXW^T) = (W \otimes A) vec(X)$ where $vec(V)$ is the vectorization of the matrix $V$ in which you stack the columns of the matrix together to make a single vector (see [Vectorization - Wikipedia](https://en.wikipedia.org/wiki/Vectorization_(mathematics))) . This sucks and takes away our intuition.

But $AXW^T$ is still a linear transformation! It is just annoying to talk about independent of $X$, since you need to have something to stick in between to indicate that it's not just $AW^T$, a very different operation. Thus, in order to represent the operation compactly, we denote it with  $A\otimes W$ and move on.

(There was more writing here trying to reconcile this version with the linear algebra you get from Axler's *Linear Algebra Done Right* but I removed it because it's incomplete.)

## 2. Using the Tensor product to describe attention layers alone

An attention head is usually described by first computing $Q = XW_Q$, $K= XW_K$, $V = XW_V$ with $X$ of shape `[num_batches, seq_len, embed_dim]` and those W projection matrices of shape `[embed_dim, head_dim]`, $W_V$ of shape ==something else ==
$$\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$$
Then you concatenate these heads together and project them out using $W_O$. 

This gives you some vague intuition about keys and queries, but it terns out there's a much cleaner way to think about this, which is the whole point of the paper. Here's the formalism. The output of a single attention head for the transformer $h(X)$, with $X$ the residual stream, is given as
$$ h(x) = (A \otimes W_OW_V)X $$
Where $A$ is the matrix describing the attention pattern, written in one step as $A = \text{softmax}(X^TW_Q^TW_KX)$ and the rest is the same as above. You can see these derivations in more detail in the original paper, but I'm not going to cover them here since they're intuitive once I stare at them a bit. I will make one note, though, which is the unconventional use of the $W_O$ matrix. In the original formulation of the transformer that I learned, the $W_O$ matrix was supposed to combine all the information together from the different heads after you concatenate them together. Instead, this paper wants you to just think of that project out vector as just another linear transformation within the head, so that the output of any given head is just summed with those of the other heads.

This is why we spent all the time defining the tensor product. We will use this in a bunch of ways. 

First, let's take a step back and note what we're doing here: we're packaging together the attention mechanism into a 4d tensor that maps a matrix (the residual stream) onto a new matrix (the attention head). 

Second, let's note what is actually happening when we expand this. First, note that $X$ is shape `[seq_len, embed_dim]`, meaning it has `seq_len` rows (tokens or token residuals) and `embed_dim`  columns in the embed space.

- $A$ is multiplied on the left. We can think of this as $A$ being applied to each *column* of $X$, which corresponds to our intuition that *attention should be mixing information across rows*.
- $W_OW_V$ is multiplied on the right. We can think of this as $W_OW_V$ being applied to each *column* of $X$, thus *the value projection and the projection out are operating on each column of $X$ independently.* Since these always operate together, we'll refer to them going forward as $W_{OV}$ following the notation in the paper.

## 3. Describing a one-layer, attention-only transformer.

Now we want to describe the entire transformer. A one-layer, attention-only transformer looks like:

1. List of tokens becomes a token embedding: $X_0 = W_E T_{\text{in}}$ 
2. Run the embedding matrix through attention, and add the result to the identity transformation: $X_F = X_0 + (\sum_{\text{heads}} A\otimes W_{OV})X$ (with $A$ defined as above)
3. Unembed the residual stream to get logits: $T_\text{out} = W_UX_F$ 

Let's combine these into one transformation $\mathbf{T}$ that we can apply to $T_\text{in}$ to get $T_\text{out}$. We can write this in one line by plugging 1 into 2, and then 2 into 3, yielding
$$\mathbf{T} = W_E(Id  +\sum_{\text{heads}} A\otimes W_{OV})(W_E)$$and simplifying to 
$$\mathbf{T} = (Id\otimes W_E) \cdot (Id + \sum_{\text{heads}} A\otimes W_{OV}) \cdot (Id \otimes W_Et)$$which allows us to use our properties to simplify as 
$$\mathbf{T} = Id \otimes W_UW_E + \sum_{\text{heads } h}A^h\otimes W_UW^h_{OV}W_E.$$The paper wants you to think of these as two 'routes' along which the processing goes. The first term is the "direct path": it can't take any information from other tokens,  so it's approximating "most frequent next token given this token in any context" across the dataset. In other words, it's just approximating the dataset's *bigram statistics*.

The second path is more interesting. The paper claims that it's approximating a *skip-trigram* method. Expanding it a bit more, we have two 'circuits': 

- The model computes the attention weights for token $n$ (the destination), taking into account tokens $1, ..., n-1$ (the source tokens). This is a function depending both on token $n$ and on those previous tokens. 
- The model computes the $W_{VO}$ values, which are weighted by the attention pattern. This operation influences the logits of the direct path, i.e. it changes from the default bigram statistics. Note that this is a function depending *only on those previous tokens, not at all on token $n$*.

This offers us a "skip-trigram" structure: 
- Destination token attends some amount to the source tokens
- The source tokens alter the logits some amount to change the output token

You can therefore think of each attention head's output as being a weighted combination of "trigram" structures, with each source-destination pairing (e.g. token $n$ and token $n-2$, or token $n$ and token $1$) influencing the output logits (the prediction weights for token $n +1$) in some way. It's a skip-trigram because, since the source tokens can be in any position in the input sequence — they don't have to just be in position $n-1$ for the model to be able to attend to them — the model can "skip" some amount of tokens between source and destination, i.e. `[src], ..., [destination], [logits for output]`.

### 3.1 Skip-trigram examples

The paper gives a number of examples of the skip-trigram structure. Here are some examples. 

| src       | dest                | out             | trigram                                              |
| --------- | ------------------- | --------------- | ---------------------------------------------------- |
| "perfect" | "looks"             | "perfect"       | "perfect ... looks perfect"                          |
| "large"   | "using", "contains" | "large", small" | "large... using large"<br>"large ... contains small" |
| " Ralph"  | "R"                 | "alph"          | " Ralph, ... Ralph"                                  |

*Note that a trigram is not confined to a single destination token. Trigrams are not unique for 3-word pairs, but are rather pairs of 2 words, e.g. (perfect, looks), (perfect, super) — the first one is from the $QK$ circuit, and then the second one is from the $WO$ circuit. I should have added more destination tokens when I copied this table, but it would be a lot of copying and I don't feel like it. Read the "Skip-Trigram Bugs" section of the paper to understand what I mean by this more precisely*

More concretely, at the risk of inaccuracy: the model is at token $n$, "looks," and wants to predict the next token. A common trigram structure is, when an author of text in the training distribution writes that something is "perfect", often when they use the word "looks" later they're describing the same object. Therefore, the "perfect" object is likely to "look perfect." Similarly, if the text previously talked about something being large, often when that "large" thing "contains" something or some amount of stuff, it is a "small" amount, or when someone is using something later it is often that large thing. (This is )

Lastly, the Ralph example shows a common pattern with names: in some situations a person's name will get split by the tokenizer when it doesn't have a leading space, but will not get split when it does have a leading space. Thus, when there's a single capitalized letter R, the model might look back for names that start with R like " Ralph" that *had* been kept as one token (though since the letters are tokenized, this is a purely statistical relationship, not an actual letter-based pattern) and use that to predict that what follows the single R was the continuation of a tokenizer-split name.

That's how I interpret these examples, at least. Reference the Anthropic paper for more examples, I doubt that I would be totally confident on what's going on here just by reading these examples. It's good for you to feel confident with these examples, though, because they form the basis of what we're headed towards next. 

A couple more:

- Predicting that an `else` keyword is more likely when indentation reduces by 1: `\n\t\t\t` ... `\n\t\t` → `else`. (note that these newline tab sequences are tokenized since they occur frequently enough)
- Predicting that `\right` in latex is more likely to be a command in LaTeX after a `\left`:  `\right` ... `\` → `\left`
- Common turns of phrase: `keep`... `in` → `mind`

Some attention heads are a little less trigrammy, and more positional. For example, a head that causes a token to attend to itself allows `corresponding`  to consistently be followed by `to` because it's allowing `corresponding` to influence the logits of the word after it. Also, if "coinciding" or "coincides" is tokenized as `coinc` and `iding` or `ides` you can see a "previous token" head that will allow `coinc` `iding` `with`, a common pattern. Again, see the original paper for more examples, they're cool. 

One fun detail: since the $OV$ circuit only depends on the source tokens, you can have bugs. I mentioned this briefly earlier. **A more accurate but more complicated model than 'skip-trigram' might be 'linked pairs of pairs':** For example, you often see "keep... at bay" as well as "keep... in mind." The $QK$ circuit tells the $OV$ circuit to increase logits of tokens that are related to the source token `keep`, but can't give information about what that source token is paired with in the destination, so when the $OV$ circuit fires on `keep`, the logits for both `bay` and `mind` increase, because it doesn't get told whether it's "keep... at bay" or "keep... in mind." 


*Fun thing: using eigenvalues to try to summarize OV/QK matrices and in particular determine whether they are copying or not.* Looks interesting but is something for future exploration — the results were not perfect.

## 4. Two-Layer Transformers

**Note:** *The team issued a correction on this section. The section acts as if there is less attention head composition going on than there actually is. In particular, there's much more $Q$-composition and $K$-composition than indicated.*

Let's do two-layer transformers now. Consider the fact that the second layer is undertaking a similar operation to the first layer, but now it's operating on the modified residual stream. What then makes this layer more interesting? The answer is *composition of heads*: because the second layer gets to use modified embeddings from the first layer the model can engage in much more powerful processing, "something much more like a computer program running an algorithm, rather than look-up tables of skip-trigrams we saw in one-layer models." This is what the paper wants you to use as intuition for why deep networks become more powerful than shallow ones, at least in this case.

Think of it this way: much of the information from the original embedding is preserved in the residual stream after the first layer; the previous layer is "writing" to specific subspaces in the residual stream. If the second layer operated only on the parts of the residual stream that first-layer heads had not written to (i.e. the original embedding information) and had no interaction with the previous layer's computations, our two-layer model could be collapsed into a one-layer model, just with extra heads. 

Thus in this section we focus on composition, where the second layer's computations are drawing on the results of the first's. There are three ways this can happen: 

1. **Q-composition:** The second layer's $W_Q$ matrix reads in a part of the residual stream affected by a first-layer head when creating the $Q$ matrix.
2. **K-composition:** Same but for $W_K$
3. **V-composition:** Same but for $W_V$. 

V-composition is different in an important way from Q-composition and K-composition. It's not affecting which tokens are getting attended to; it's only affecting what information gets moved by the head. If the model does V-composition alone, we can therefore collapse it into a 'virtual attention head' given our simplified model: when you compose the heads, intuitively you are just moving information twice. You could collapse this into a single move.

You can't do the same for $Q$ and $K$ composition. It's not stated explicitly in the paper so it might be more complicated, but I think this is just because there's a nonlinearity in the attention layer: if you compose *before* the softmax, then your composition can't collapse into simply a new attention head, whereas if you compose *after* the softmax it's two independent nonlinear functions and then you're composing the linear parts; linearity composes nicely.


Ok, let's do what we did above and compute the $\mathbf{T}$ operation for a two-layer transformer: 
$$\mathbf{T} = Id \otimes W_U \cdot (\text{Layer 2}) \cdot (\text{Layer 1}) \cdot Id \otimes W_E$$
expanding to
$$\mathbf{T} = Id \otimes W_U \cdot (Id + \sum_{h \in H_2} A^h\otimes W_{OV}^h) \cdot (Id + \sum_{h \in H_1} A^h\otimes W_{OV}^h) \cdot Id \otimes W_E$$
Expanding this as usual by multiplying out, we get
$$\mathbf{T} = Id \otimes W_UW_E + \sum_{h \in H_1\cup H_2} A^h\otimes (W_UW_{OV}^hW_E)$$$$+ \sum_{h_2 \in H_2} \sum_{h1 \in H_1} (A^{h_2}A^{h_1}) \otimes (W_U W_{OV}^{h_2} W_{OV}^{h_1} W_E)$$
 This is nicely intuitive: we have the direct path (bigram stats), then skip-trigrams by independent heads, then this third route is the 'virtual attention head' created by $V$-composition. Where is our $Q$- or $K$-composition, though? It's hidden in the $A$ matrices in the middle term where $h \in H_2$. 

Let's expand out the attention computation into $A^h = \text{softmax}(X_1^T C^h_{QK} X_1)$ with $X_1$ the first layer's residual stream output and $C^h_{QK}$ the matmuls involved in computing attention scores.  However, we want this in terms of our $T_{in}$ (input embeddings), not in terms of another layer's residual stream, since $\mathbf{T}$ is supposed to be working with $T_{in}$ as the input. This is where things get vaguely evil. We want to express this as a 6-dimensional tensor using an additional tensor product. 

...I've spent some time staring at these equations and decided to skip them for now because they are not sparking joy. It ends up all being big tensor products. Basically when you get to the end you end up expressing the $C^h_{QK}$ i.e. the attention pattern as
$$= \text{Id} \otimes \text{Id} \otimes \left(W_E^T W_{QK}^h W_E\right) 
+ \sum_{h_q \in H_1} A^{h_q} \otimes \text{Id} \otimes \left(W_E^T W_{OV}^{h_q\, T} W_{QK}^h W_E\right)$$
$$+ \sum_{h_k \in H_1} \text{Id} \otimes A^{h_k} \otimes \left(W_E^T W_{QK}^h W_{OV}^{h_k} W_E\right) $$$$+ \sum_{h_q \in H_1} \sum_{h_k \in H_1} A^{h_q} \otimes A^{h_k} \otimes \left(W_E^T W_{OV}^{h_q\, T} W_{QK}^h W_{OV}^{h_k} W_E\right)$$

Which is evil, but basically the first term corresponds to direct path (i.e. no composition), second corresponds to $Q$-composition, third term corresponds to $K$-composition, and the last corresponds to both at the same time.

### 4.1 Induction Heads as K-composition

An induction head works with two layers: 

1.  A prev-token head in the first layer extracts information about the previous token (and sometimes a little bit of the present token) and then adds it to the next token
2. "induction heads" use this information to perform an advanced form of copying.

The best illustration is with examples: `Potter` is tokenized as `Pot` and `ter`. The first-layer prev-token head has embedded the information that `Pot` precedes `ter` into the `ter` token, for all the previous `ter` tokens. Then when the attention head sees `Pot` again, it attends ~exclusively to previous instances of `ter`, and then predicts `ter`. In other words, it is querying for "what token usually follows `Pot`?" and the `ter` tokens reply "me!" as the keys. A similar dynamic occurs with `Dursley`, tokenized as `D`+`urs`+`ley`. When `urs` pops up, it attends back to `ley` and predicts it correctly. (Refer to the original paper "analyzing a two-layer model" section and play with the visualization if this is unclear.) We see this result for not just Harry Potter text but for uniformly random sampling of tokens, affirming this as a general principle of how this head functions.

If you think about it a bit, it should become clear why this is K-composition. At least, writing this example out did this for me: A previous layer has embedded information in the `ter` tokens, so that when the `Pot` token solicits keys for its query, the key behavior is different. In other words, **the prev-token head in the previous layer has embedded information that is used by the key, but not the query**. That's why we go through all the effort to express the $Q$ and $K$ operations as separate — induction heads don't make sense without that distinction. 

The Anthropic team describes this as "The query searches for 'similar' key vectors, but because keys are shifted" by the prev-token head, the query "finds the next token" instead. (See "How induction heads work.") It turns out that the eigenvalues of the $OV$ and $QK$ circuits are extremely positive, validating the idea that they are probably doing a kind of copying behavior. We can summarize the induction head in one more way: 

1. $QK$ circuit captures the relationship described above, attending heavily to the 'next token' in previous examples (e.g. `ter`).
2. $OV$ circuit acts as a 'copying' circuit, increasing logits for the tokens that are attended to.

## 5. Ablation studies to determine $V$-composition importance

We now turn away from $Q$- and $K$-composition and start thinking about $V$-composition. When the paper authors looked at the model, they decided that there wasn't much $V$-composition going on and so the virtual attention heads were probably not that important. Now we want to check this experimentally.

This is slightly difficult, because $V$-composition is explicitly present in the equation we gave above, but not in the actual activations: it's unclear which part of the activations was contributed to by this term in the equation, because the model isn't actually running the equation we used, but a different, more efficient formulation of it. if we tried to run the math version, it would get very bad very quickly as we scaled. ~~(I think this is because you would get terms with double sums, then triple sums, then quadruple sums, etc., producing an $\mathcal{O}(n^2)$ computation increase as you increased layers? Unsure? Also I think there's a component of it which is that we have merged many smaller matrices into low-rank larger matrices e.g. $W_{QK}$ which also would hurt computation speed a lot.)~~ (Actually I think this is wrong: the problem is that you get an exponential blowup in the number of terms) In any case, we want a scalable approach. 

There's a way we can empirically determine the effect of ablating specific paths. As a brief review, we'll talk about terms using 'order' terminology: order 0 is the direct path (no attention head movement of information), order 1 is a single head, order 2 is 2 heads composed, order 3 is 3 heads composed, etc. 

Now, here's my reformulation of the algorithm the paper gives us:

> **Step 0:** Run the model normally and save the attention patterns.
> 
> **Step 1:** Run the model again using the attention patterns you saved from step 1. Instead of adding attention head outputs to the residual stream, add a 0 tensor to the residual stream, and save the attention head outputs separately. Record the loss. (To summarize: model attends normally, but layers cannot use residual stream modifications from previous layers. We therefore record the attention outputs for up to $1$st-order terms, i.e. individual heads never composed, along with the loss for $0$th-order layers.)
> 
> **Step 2:** Run the model a third time, again forcing the model to use the 'normal' attention pattern, and then instead of adding those head outputs to the residual stream,  add the attention outputs you recorded in step 1. (Model attends normally, and layers can now use residual stream modifications from exactly 1 layer back. Thus we are recording attention outputs for up to $2$nd-order terms, i.e. heads composed with 1 or fewer other heads, and recording the loss for $1$st order layers) 
> 
> Run this for $k+1$ steps to get the $k$th-order total loss, from which you can take the change in the difference with the original model loss to see the marginal loss. (i.e. look at difference between original loss and loss at order $k-1$, and see how much that difference decreases when you look at order $k$.)

This algorithm is a bit unwieldy to describe, because each step is doing two things. It's first recording attention outputs for order $n+1$, but then computing the loss for order $n$. You kind of just need to stare at it for a while, and maybe write it out. I think the way I've described it above should clear things up slightly by describing the $n+1$, $n$ pattern (the original paper does not talk about this) but it is likely that this version will not immediately make sense either. 

The nice thing is that it scales nicely! It turns out that on this specific model with up to order 2 terms, the marginal loss reductions are: 

- Order 0 terms ($W_UW_E$) reduce by 1.8 nats relative to uniform predictions
- Order 1 terms of the form $A^h \otimes (W_UW_{OV}^hW_E)$ reduce loss by 5.2 nats relative to order 0
	- Layer 1 Order 1 terms only reduce by 0.05 nats relative to direct path combined with layer 2, but against direct path alone contribute to 1.3 nats
	- Layer 2 Order 1 terms reduce by 4.0 nats relative to direct path combined with Layer 1, and 5.2 nats relative to direct path alone
- Order 2 terms of the form $(A^{h_2}A^{h_1}) \otimes (W_UW_{OV}^{h_2}W_{OV}^{h_1}W_E)$ reduce loss by 0.3 nats relative to order 1

(Nats are units you employ when using $\ln$; they're base $e$ in the way a bit is base 2.)

So we can conclude that the order 1 and order 0 terms are what really matter in this smaller network, helping us to conclude that $V$-composition doesn't really matter, as supposed previously. ($Q$- and $K$-composition might matter a lot.) At the end of the section, the authors provide some interesting thoughts on virtual attention heads in the context of transformers more generally, as opposed to just this small two-layer one: for example, they're elegant, there's a lot of them, and they may be able to account for various other useful functions that are harder to describe in other ways. You might find that section interesting.

## 6. Conclusions/Going Forward/Later Work

What does this paper give us?

- "Some circuits appear to be *primarily attentional*." This work might be useful for figuring out those circuits.
- Large models empirically *do* form induction heads(!), and these heads tend to use $K$-composition in the way described above
- However, MLP makes up two thirds of the parameters in a transformer. Since attention heads probably interact with those MLP layers, the proportion of the model's parameters we can understand without understanding MLP layers is probably less than 1/3. 

We see these sentences at the end of the paper:

> More complete understanding will require progress on MLP layers. At a mechanistic level, their circuits actually have a very nice mathematical structure... However, the clearst path forward would require individually interpretable neurons, which we've had limited success finding.

Writing in 2025 and looking back on 2021, this is really interesting. *I* know that Sparse Autoencoders are a big thing now (though they [may be on their way out](https://deepmindsafetyresearch.medium.com/negative-results-for-sparse-autoencoders-on-downstream-tasks-and-deprioritising-sae-research-6cadcfc125b9)?) — in fact, I've trained SAEs myself. I'm excited to see how this plays out as I learn about research closer to today's.

There's conveniently a section "Summary of Follow-up Research"! Here are some notes from that: 

- MLP neurons are polysemantic (Black et al) and hard to interpret
- Lots of research undoing superposition in MLP neurons 
	- Another perspective, alternative to superposition: "Polytope lens"; can you use SVD to find interpretable feature directions?
- There's a follow-up paper specifically on induction heads
	- "causal scrubbing" is used to "rigorously" characterize induction heads (?)
	- Paper by Von Oswald — "a repeated induction head-like mechanism could learn a linear model in-context by simulating gradient descent" (?!??)
- There's more work on circuits


**General takeaways from the paper:**

- Circuits are cool! This approach is cool! I think circuit-finding feels more holistically interesting than SAEs, though they are obviously complementary research styles.  
- Math can probably be quite useful for structuring research questions on toy models; it may not scale well, but the intuitions you get from it might?
- It's not always correct to think about the model's mechanisms in the way that they are officially presented. There are lots of ways of thinking about language models, and reformulating the network might reveal useful insight.
- Attention heads can compose together; induction heads show examples of how multiple attention heads composed together can create a much more powerful circuit.
- It's interesting to think about the residual stream as 'memory' or 'communication channel' that the attention heads are writing into, and that everything is modifying or adding onto bigram statistics.
- Some things I want to look further into: 
	- More modern research combining MLP interp with attention circuits
	- Interested to get a better grasp of statistical methods in general (possibly learn about linear regressions to understand some basic statistical intuitions)
	- Understand applied linear algebra techniques, like matrix decompositions
	- Generally better intuitions for matrices and tensors as mathematical objects; have a better sense for "what they are doing," particularly re: the unity of left- and right-hand matrix multiplications.
	- Better intuition for multilinear algebra, though probably not a *ton* of time spent on it. Wondering what the Kronecker and Tensor products are in more depth, because it seems like there's some very cool math involved.
- Random research questions it made me wonder about: 
	- I've seen research training SAEs for vision models. I wonder if you can do circuit tracing on vision models? 
	- Google wants to do omnimodal models. Multimodal interpretability seems pretty interesting. What if I did toy experiments on ViTs like Anthropic did with those small language models? What if I tried messing with CLIP to see if I could understand some feature alignment or something?
	- Can you do multimodal, not just vision-only or language-only interpretability? What would you even look for?


Extra random notes: 

- They open-sourced PySvelte, a library for interactive visualizations that they used for this
- They have a companion problem set of problems they found helpful in building intuition for attention heads (maybe worth it?)
- "Attention is a generalization of convolution" (!!) (See Virtual Weights and convolution-like structure)
	- This is fascinating, and they just stuck it into a footnote in the paper??
- **Privileged basis:** if some part of a model has a privileged basis, that means that some architectural component (e.g. an activation function) causes the model to be more likely to align features with the explicit basis (i.e. $e_1, ... e_n$  or whatever or the generalization of that if you need one). If you have a privileged basis, that's nice because you can come up with hypotheses about what those features are, without having to wonder whether or not they are features at all. Without a privileged basis, you lose some interpretability. The residual stream here does not have a privileged basis. (It's "**basis-free**.")
- There are some typos in the paper (mainly using "it's" instead of "its") lol



<!-- **Extra: tensor products map matrices to matrices**
Another thing you may think about when considering tensor product is that we want to define a linear transformation from residual stream to residual stream, i.e. `[seq_len, embed_dim]` to `[seq_len, embed_dim]`. But we can't use our basic tools from linear algebra; those map vectors to vectors. We need something that maps matrices to matrices. You could think of this as a mapping of linear transformations onto linear transformations, but that might not be useful intuitively. 
Instead, we can turn to the formal derivations of the tensor product. in *Linear Algebra Done Right* Axler starts the section on the tensor product with

> The motivation for our next topic comes from wanting to form the product of a vector $v \in V$ and a vector $w \in W$. This product will be denoted by $v \otimes w$, pronounced “$v$ tensor $w$”, and will be an element of some new vector space called $V \otimes W$ (also pronounced “$V$ tensor $W$”).

Note that here $V$ and $W$ are vector spaces, not matrices. Here Axler wants you to think about the tensor product as a way to define the product of two vectors from two different vector spaces. How does this connect?

Axler wants you to be able to connect vectors to vectors from different vector spaces. It turns out that the natural way to do this is to package the two vectors together into a matrix using the outer product, meaning that you create a matrix where the value at position $(i, j)$ is $v_i \cdot w_j$. Thus, $v_i \otimes w_j$ yields a matrix that can take vectors to vectors. -->