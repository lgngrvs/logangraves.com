# Miscellaneous messy notes dump on optimizers, activation functions, normalization, and sparse attention
Date: 2026-03-23
Tags:
Type: research
Desc: Messy notes for future reference


I recently had the opportunity to go back and review all the basics, and fill in some holes on stuff I didn't already know (e.g. GLU activation functions, sparse attention, muon optimizer). Posting these notes here (straight out of my obsidian) as a reminder of how much of a great time I had doing it.

[TOC]



### Transformer from scratch outline

- tokenizer (bpe)
- positional embedding (sinusoidal?)
- for i in range blocks:
	- attention block
		- input is batch, seq_len, hidden dim
		- project to key, query, value, using w_k, w_q, w_v (hidden, head_dim)
		- matmul key and query to get batch (seq_len by seq_len ) square
		- mask (- inf so that softmax ignores)
		- apply column-wise(?) softmax
			- softmax is the only nonlinearity here; keeps attention values bounded nicely between 0 and 1; allocates proportionally.
		- matmul by V
		- (do this $h$ times for $h$ heads)
		- concat heads and then project out with W_o
	- layernorm
		- compare layernorm with other norms
	- feedforward/MOE
		- activation functions
	- layernorm
	- residual connection
- output: project from `resid_size` to `vocab_size` and run a softmax
	- softmax creates probability distribution
- standard loss is cross-entropy loss against a one-hot vector -- $-log(p_\text{correct token})$. derivative ends up being 
	- train using adam optimizer -- what distinguishes adam from other stuff?

To batchify this, you just do $b$ of these at a time. 

Quick attention implementation for my einsum review: 

```python
# x: b, s, l
# W_K: n, l, h
# W_Q: n, l, h
# W_V: n, s, h
# W_O: l, l

K = torch.einsum('bsl, nlh -> bsnh', x, W_K)
Q = torch.einsum('bsl, nlh -> bsnh', x, W_Q)

QK = torch.einsum('bsnh, btnh -> bnst', Q, K) # this is taking the dot products of Q_i and K_j. einsum requires s and t to be different even though they're equal values
sq_d_k = torch.sqrt(K.shape[-1])

attn_pre_v = torch.softmax(QK)/sq_dk

attn = torch.einsum('bsns, nsh -> bsnh', attn_pre_v, v)

# ok now we concat all the n attention vectors
mix_in = attn.reshape(b, s, n * h)

attn_mixed = torch.einsum('bsl, ll -> bsl', mix_in, W_O)

# then we just layernorm

```
### Activation functions

**Standard** 

- ReLU: $max(0, x)$
	- Standard, most basic piecewise.
		- How do you differentiate ReLU?
			- the derivative of a scalar input with respect to the relu is 1 if >0, 0 otherwise. by convention you just say that its derivative is 0 at relu.
			- we lowkey don't actually care that it's not differentiable at 0. :) 
- $\text{Swish}_\beta$ is given as $x \cdot \sigma(\beta x)$ for some $\beta$ parameter -- a variant on sigmoid (keeps between 0 and 1 , 0 at $-\infty$, 1 at $\infty$.) (recall sigmoid = $\frac{1}{1+e^x}$)
- GELU is $x \Phi (x)$ where $\Phi(x)$ is the Gaussian CDF (0 at -infinity, 1 at infinity 1/2 at 0)
	- Sigmoid and Gaussian are similar, guassian just grows a little faster? yeah, $GELU(x) \approx x\sigma(1.1702x)$ 
	- GELU has nice properties because it's the expectation of a stochastic regularizer (like dropout) working with mask $\sim \text{Bernoulli}(\Phi(x))$ 
		- layer inputs tend to follow a normal distribution

**"Bilinear"/GLU activation functions**

- **GLU**: takes a standard linear and an activated linear transformation and multiplies them elementwise
	- $GLU(x, W, V, b, c) = \sigma(Wx + b) \odot (Vx + c)$ 
		- gradient is $\sigma'(Wx+b)(Wx+b)'(Vx+c) + \sigma(Wx+b)(Vx+c)'$ $= \sigma(Wx+b)(1-\sigma(Wx+b))(Vx+c)(x + \mathbf{1})$
		  $+\sigma(Wx+b)(Vx+c)'(x+\mathbf{1})$ 
		- Rewriting, $\nabla(\sigma(X) \odot X) = \sigma'(X)\nabla(X) \odot X + \sigma(X) \odot \nabla X$
	- when a part of $X$ is high, $\sigma(X_i) \approx 1$ so that gives it a nice gradient path compared to if you had a $tanh(X)$ instead of just $X$.
		- prevents vanishing gradients supposedly
	- but it gives you the 'computational benefits' of conditional routing -- easier to learn a routing function?
	- so the GLU variants (SwiGLU, ReGLU, etc.) take the activation functions (Swish, ReLU) and then allow a 'conditionality' to them by giving a separate set of weights
- **Bilinear**: remove the $\sigma$; it's just two affine transformations added together
- You get all the GLU variants by composing the nonlinearity and elementwise product.
	- Intuition: I mean, it obviously packs more into the activation function. It's something like, these weights decide how much to gate, and the other weights just need to worry about the actual values that should be taken on.
	- They perform better when you use a smaller hidden size in your FFN so that the weights stay the same? 
- How will these affect geometry? my vibe check is that it allows the model to have more separated spaces — when you have a single wet of parameters both outside and inside, you get less expressivity... even if you have larger hidden size? ie. it has to be 'continuous' 

### residual connections

two intuitions: 

- reduces vanishing gradients -- the gradient term will be slightly evil, but it will always have a direct path back to the weights even if it is extremely deep, so the gradient won't be tiny 
	- but [why doesn't normalization just solve this](https://arxiv.org/pdf/1702.08591)? 
- allows the network to learn identity more easily -- intuition of 'should work at least as well'
- allows '[ensembling](https://arxiv.org/pdf/1605.06431)' or a sort of MoE across layers functionality  ("Residual Networks Behave Like Ensembles of Relatively Shallow Networks") -- different layers can have greater specialization and can be gated

### Layernorm

- **batchnorm**: divides by average across batch; save the training average and use those values at test
- **layernorm**: takes the input vector for a single input, averages the dimensions of the vector, and computes standard deviation, then normalizes this single input using that.
	- then you also multiply by gamma and add beta so you can rescale if 0,1 is not optimal for some reason
	- removes scale-sensitivity
	- removes risk of internal covariate shift: when you update parameters early in the model, the input distribution late in the model shifts out of distribution from where it was before, making the later layers have trouble learning
	- reduces gradient vanishing/exploding
	- will perform better out of distribution since you don't rely on batchnorm
	- in a transformer: embed the sequence of tokens, initially seq_len by embed_dim. then layernorm normalizes vectors of shape (embed_dim) with a total of seq_len of them.
	- what does this do to the geometry?
	- [layernorm is a nonlinearity](https://arxiv.org/pdf/2406.01255)
	- see "Related work" from "you can replace transformers with $tanh(\beta * x_i)$"
- **rmsnorm**: root mean squared. just normalizes by the square root of the average of the input vector dimensions: divides by $\sqrt{\frac1d \sum^d x_i^2 + \varepsilon}$ so that the "variance" is standard (not literally the variance); faster but trades off in that it's not centered on 0
	- less sensitive to outliers (mean not thrown off)
- RMSnorm and LayerNorm are standard

## softmax

- takes in inputs, scales them nonlinearly. the result is a probability distribution — or, in other words, proportional allocation of weight. 
- softmax is the simplest version of 'take relative stuff only, and upweight larger scores nonlinearly, then normalize'
- $$\text{softmax}(x_i | x_1, ..., x_j) = \frac{e^{x_i}}{\sum_j e^{x_j}}$$
	- $e^x$ is positive, and when you divide by the sum you normalize to sum to 1. why specifically $e^x$? this is a vibes choice, but basically, the more a value is an outlier/the larger the gap, exponentially the more it gets special attention. as confidence goes to 1, you should exponentially overweigh -- e.g. 90% and 80% confident should drown out the rest, 10% and 20% should not.
		- squaring doesn't handle negatives. normalizing gives you negatives
	- softmax is invariant to adding 1 proof: factor out $e^{x+1} = e^x \cdot e$ and cancel in numerator/denominator
	- it works nicely with cross-entropy loss

### optimizers 

- **SGD**: just average gradient across batch, multiply the gradient by a learning rate, and you're done.
	- large batch sizes are less noisy and may converge faster; more expensive 
- **Momentum**: keeps some information about the previous timesteps' gradients according to the weight $\beta_1$: $\theta_{t} = \theta_{t-1} + \alpha m_{t}$   
	- momentum given as $m_t = \beta_1 m_{t-1} + (1-\beta_1) \frac{\partial L}{\partial \theta_t}$
- **Adagrad**
	- adjusts the learning rate adaptively: if the parameter takes small values, you increase its learning rate by dividing by a small sum. if it takes large values, you decrease it by dividing by a large sum.
	- learning rate for parameter $i$ is $lr_i = \frac{\alpha}{\sqrt{\sum_{-n}^0 (g_i)_t^2} + \epsilon}$ (where $(g_i)_t$ is the gradient of parameter $i$ at time $t$. 
		- remember: you adjust by dividing the learning rate by the *sum of squared values for the last $n$ timesteps.*
	- Then $(\theta_i)_t = (\theta_i )_{t-1}-lr_i \frac{\partial L}{\partial \theta_i}$ (don't forget that you are subtracting the gradient!) 
- **RMSProp**
	- exponentially weights the adagrad gradients: maintains a velocity term $v_t = \beta_2 v_{t-1} + (1 - \beta_2) (\frac{\partial L}{\partial \theta_t})^2$
- **Adam**
	- uses both momentum to keep information about previous timesteps, and adaptive learning rate to push things
	- $\theta_t = \theta_{t-1} - \frac{m_t}{\sqrt{v_t} + \varepsilon}$. (you can also get stuck near 0 initially depending on how big your momentum is so sometimes you also change stuff to handle that -- bias correction e.g. $\hat m_t = \frac{m_t}{1-\beta_1}$)
	- but if you incorporate $L_2$ regularization as you normally would — just adding a loss term to your loss function for $L = CE + \frac12||\theta||^2$ — adam then applies all its machinery (momentum and adaptive learning rate) to this theta term which gives you weird results  
		- the regularization term for large parameters gets reduced by adam's adaptivity; this is dumb and inefficient
		- also the history stuff — parameters that used to have large weights still get penalized for them so you momentum-ize the term, perhaps undesirable
- **AdamW** 
	- just separates out weight decay: does normal loss and then adds the weight decay $\theta_{t} = \theta_{t-1} - \alpha ( \frac{\hat m_t}{\sqrt{\hat v_t} +\varepsilon} + \lambda \theta_t)$ 
	- this way your regularization is properly decoupled and interpretable
		- more consistent regularization
- **Muon**: "[MomentUm Orthogonalized by Newton-Schultz](https://kellerjordan.github.io/posts/muon/#shampoo)"
	- your gradients for weight matrices are matrices. you do SGD+momentum and then orthogonalize these gradient matrices. that's it
	- thus it's designed just for weights (which are matrices), not biases which are vectors; those should be given adamw
	- In particular: you do regular SGD+Momentum, then your update is $O = \text{argmin}_O (||O - G||_{\text{Frobenius}}: O \text{ is orthogonal})$. You get this argmin using newton-schultz iteration, which is just a fast algorithm for this.
	- "orthonormalizing" the weight updates basically standardizes the learning so that smaller, less-used singular directions are updated similarly to the bigger, more-used weights; they believe that this tradeoff is handled by the fact that you have large batch sizes 
		- i am once again requesting you to properly understand singular values :0 
	- [Kimi K2 uses](https://x.com/Kimi_Moonshot/status/1893379158472044623) 

	> And for an empirically-flavored motivation, we observe that based on manual inspection, the updates produced by both SGD-momentum and Adam for the 2D parameters in transformer-based neural networks typically have very high condition number. That is, they are almost low-rank matrices, with the updates for all neurons being dominated by just a few directions. We speculate that orthogonalization effectively increases the scale of other “rare directions” which have small magnitude in the update but are nevertheless important for learning

*What does this sentence mean?*: 

> Modern first-order optimizers can let weight matrices drift into poorly conditioned regimes, amplifying gradient noise and forcing conservative step sizes. Muon mitigates this by orthogonalizing updates, but the weights themselves remain unconstrained. Manifold Muon takes the next step by constraining each linear layer to a geometry—e.g., the Stiefel manifold—so singular values of both the update matrix and the weight matrix are controlled by construction.

### architecture improvements since vaswani

- RoPE: rotary position encoding -- added near middle layers instead of in the front. you just rotate stuff lol
- MoE 
	- i feel like there's more to learn here but i'm not actually really sure
- Kimi K2 uses SwiGLU (which is swish + GLU)

### sparse/linear attention
- MoBA (mixture of block attention) (moonshot ai)
	- MoBA splits $K$ matrix into blocks. then for some query vector $q$ (corresponding to some token asking for information) it gets routed as $\text{Softmax}(qK_{[I]}^T) V_{[I]}$ for indices $i \in [I]$ . You pick routing without parameters: MoBA uses $\langle q, pool(K_i) \rangle$ Where $pool$ is done by averaging $K_i$ of shape `[batch, i_size, hidden_dim]` across the sequence dimension to get shape `[batch, head_dim]` which can be inner producted with `[batch, head_dim]` but "this (likely) prevents optimal routing"
	- You have hyperparameters `i_size` (e.g. 512) and `TopK` (e.g. 3) which creates 80% sparsity. Most experts probably only need to see at most 20% of the tokens!
	- you also get to attend to stuff next to you :) 
- Deepseek Native Sparse Attention (NSA)
	- **compressed** attention: take $K$ add intra-block positional encoding and compress them down, then do attention
	- **selected** attention: uses attention scores from compressed attention to pick which blocks to use real uncompressed per-token attention on
	- **window** is a sliding smaller recent context window 

[Triton kernel stuff](https://blog.tilderesearch.com/blog/sparse-attn) looks pretty fun -- figuring out how to actually optimize the performance there sounds very fun

### reviewing toy interp experiments and model inductive biases

- induction heads/multiple attention paths
	- fits nicely with residual stream&MoE intuitions: sparsity of input distribution mixed with SAEs stuff is very nice
- Mathematical framework: you get $h(x) = (A \otimes W_OW_V)X$ for a single head
	- then you get $\mathbf{T} = Id \otimes W_UW_U + \sum_{\text{heads} h} A^h \otimes W_U W_{OV}^h W_E$ for a one-layer transformer
	- the two paths are embed/unembed, and then "skip-trigram": embed, Attention weights $W_{VO}$ by attention pattern for the final token, the final token extracts some information from that token's Value 
	- 3 layers becomes embed unembed (bigram), skip-trigram (layers 1 and 2), and then composition: q-composition, k-composition, and v-composition, where the second layer's $W_{Q/K/V}$ matrix reads in something from the residual stream that was affected by the prior layer's skip-trigram stuff. $V$-composition alone is redundant, because it just moves around what information the model sees, so in theory it could be collapsed into a single move in a single attention head. 
	- So your whole thing is $$\mathbf{T} = Id \otimes W_UW_E + \sum_{h \in H_1 \cup H_2} A^h \otimes (W_UW^h_{OV}W_E) + \sum_{h_2}\sum_{h_1 \in H_1} (A^{h_2} A^{h_1}) \otimes (W_UW_{OV}^{h_2}W_{OV}^{h_1}W_E)$$ and eventually you get to a nicer thing.
	- Induction heads as $K$-composition
		- induction head sees `Pot` precedes `ter`, embeds `Pot` information into `ter`. "I follow Pot" in the attention head: when next layer solicits keys for its queries, this embedded "`pot`" information pops up
- Mamba vs. transformer vs. etc. — see things about other architectures (didn't end up doing this but i remember seeing a cool paper about this)
	- some stuff like https://arxiv.org/pdf/2402.01032
	- https://arxiv.org/html/2508.19029v1
	- i know there was some associative recall mamba vs. other ssm vs. transformer paper i saw but i don't remember which one it was 
### experiment design

detail: dataset/task, hypothesis, null/control

- "SwiGLU performs better than ReLU with the same number of parameters. How do you investigate why?"
	- hypothesis: the gating mechanism allows for more sparsity in the activations -- almost MoEish
	- so I want maybe a compound toy task?  a dataset with a couple different (similar) tasks, see if you can localize activations to a subspace and identify the gating at work
	- compare it to a model 1/2 the size (shazeer does this) 
		- confirm this is the right number
	- ablation: fixed random gate?
- "Model gets worse at a task as you scale up. How do you investigate why?"
- you find that a model trained on code has features that activate on both code syntax and natural language grammar — how do you figure out if this is a meaningful shared representation or an artifact of your method?


random notes

- computational complexity: matmuls are (outer, inner) (inner, outer2) → complexity is outer * inner * outer2 
	- attention bottleneck: $n^2, d_h$  for sequence $n$ = seq_len
- embeddings are just trained e2e 