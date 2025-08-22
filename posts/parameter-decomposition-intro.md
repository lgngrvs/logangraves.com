# Understanding the Parameter Decomposition papers
Date: 2025-07-06
Tags: technical interpretability notes
Type: post
Desc: Understanding attribution-based and stochastic parameter decomposition methods

Before reading this post, I recommend reading Lee Sharkey's post "[Mech Interp is not Pre-paradigmatic](https://www.lesswrong.com/posts/beREnXhBnzxbJtr8k/mech-interp-is-not-pre-paradigmatic)." I think the post is worthwhile in itself as a survey of mech interp methods and history; it also explains Parameter Decomposition's basic ideas. Ideally you will have familiarity with those before reading this post, because I don't spend a ton of time outlining them. This is mostly an explanation of the technical details behind what Goodfire and Sharkey are shooting for with Parameter Decomposition.

This post closely follows the content of the APD paper [Interpretability in Parameter Space: Minimizing Mechanistic Description Length with Attribution-based Parameter Decomposition](https://arxiv.org/pdf/2501.14926) and the SPD paper [Stochastic Parameter Decomposition](https://arxiv.org/abs/2506.20790). I follow the notation there, but I sometimes use my own structure.

[TOC]

## 1. Introduction to APD and SPD: what is a mechanism?
To recap, PD takes all the weight matrices of the model and flattens them into a vector in 'parameter-space'. Then it aims to turn this vector into the sum of a bunch of other, simpler weight vectors which we call *components*. We want these *components* to represent the network's *mechanisms*. We say that they're the network's mechanisms if the components have the following properties:

1. **Faithfulness**: The components sum to the network's original parameters
2. **Minimality**: we split into the minimum necessary number of components
3. **Simplicity**: the components are as simple as they can be. (We operationalize this by saying the components should span few ranks, and should straddle as few layers as possible.)

The hope is that by optimizing components to reflect these qualities, *faithfulness* ensures that components are accurate to the actual model's parameters, *minimality* means that each component plays its own distinct role and takes care of that entire role, and *simplicity* means that they are specialized to that role and don't do other hidden secret things (i.e. there are no polysemantic mechanisms). The nice thing about this is that it gives us an explicit formalizable definition of the fundamental object of interp, whereas with 'features' no one really knows what they are. Also, supposedly PD minimizes description length of mechanistic components "per data point" which seems nice. I haven't read this part of the paper because it's in an appendix and I want to go write code, but it indeed seems nice.

This is basically the whole idea, as I understand it. There's a lot more justification for it in the papers (e.g. "why should mechanisms reside in parameter-space? why does this make sense to even think about in the first place?") but I will leave that for the curious reader. The content of these two papers, [Attribution-based Parameter Decomposition](https://arxiv.org/abs/2501.14926) and [Stochastic Parameter Decomposition](https://arxiv.org/abs/2506.20790) are basically just, "how do we implement this" and "how do we make this (more) scalable and have better properties" — APD proposes the original method in a relatively naïve implementation, and SPD proposes a modified version of that method that is more efficient and scalable. 

In a basic sense, the setup for learning this decomposition is relatively similar to that of training SAEs — specifically in that you have some original model, and you instantiate a second model, then train that second model to approximate some aspect of the first by running tons of inputs through it and using a specialized loss function that gives that secondary network the properties you want. There's a big difference between them, though, in that PD is optimizing multiple separate whole-network-sized 'components' which give an output similar to that of the original network. On the other hand, SAEs just optimize a simple autoencoder to reconstruct a single layer's activations.

The hard details for APD and SPD basically come down to

1. How you implement minimality; this turns out to boil down to "how do you estimate the importance of a feature so that you can train the network to use only the important ones," and is the main difference between the two papers
2. The precise details of implementing the loss functions

APD is in some sense a naive solution to minimality: have the network only use the top-$k$ most 'important' components — lol, I'm having to train myself out of saying 'features' all the time — with importance estimated using the gradient. This has various problems (it's computationally difficult, it's hyperparameter-sensitive, and it can force the model to use more components than it wants to) so SPD provides a different way of implementing minimality which involves having a separate learned importance prediction function, and using random masking based on that importance estimate which gives the method nice properties, to be discussed.

Then each of these papers presents a compound loss function. APD's looks like $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{faithfulness}} + \mathcal{L}_{\text{minimality}} + \mathcal{L}_{\text{simplicity}}$$ which is easy enough to comprehend, you look at it and say "oh well I just wonder what the details are in how they specify $\mathcal{L}_{\text{faithfulness}}$ etc.", and then SPD's looks like $$\mathcal{L}_{\text{SPD}} = \mathcal{L}_{\text{faithfulness}} + (\beta_1 \mathcal{L}_{\text{stochastic-recon}} + \beta_2 \mathcal{L}_{\text{stochastic-recon-layerwise}}) + \beta_3 \mathcal{L}_{\text{importance-minimality}}$$and you flinch a little and are like "oh uh ok sure" and add a 5-hour block to your schedule called "understand SPD loss functions."

Let's talk this through. 

## 2. APD: sort of simple

We have three components to our loss function in APD. To train the model, you run it alongside the original model and do regular gradient backpropagation, presumably. I'll go through each component of the loss one-by-one, because I think that other than the basic PD paradigm explanation, the crux of the paper is the loss function setup.

### 2.1 Faithfulness

The faithfulness loss function is simple: $$\mathcal{L}_{\text{faithfulness}} = MSE(\theta^\*,\sum^C_{c=1}P_c)$$ where each $P_c$ is one of the parameter component vectors and $\theta^\* \in R^N$ is the original parameter vector. Thus we want to the parameter components to sum to the original parameters, as described above.

### 2.2 Minimality 

Remember that minimality means that we want the *smallest number of components possible to be used to explain network output*. This is where the "Attribution-based" part of "Attribution-based Parameter Decomposition" comes in. 

The idea, as described above, is as follows: 

1. Estimate how important each parameter component is for an output
2. Incentivize the model to use a few important components as opposed to many relatively less important or equally-important components

Ideally this means the network genuinely captures the original model's ground-truth mechanisms, which are hopefully human-comprehensible, as opposed to creating some random weird uninterpretable set of confusing and possibly meaningless components.

Beginning with $1$, first we estimate the casual importance of each $P_c$ for each datapoint $f_{\theta^*}(x)$. To do this, in theory we'd like to compute an attribution $A_c(x) \in \mathbb{R}$ for each component by simply measuring how much it alters the loss. However, to avoid confounding we would need to run a forward pass for every possible combination of component ablations, which is computationally intractable at any meaningful scale. Thus, instead we use gradient attributions as an approximation.[^1] This involves one forward pass to calculate the output and one backward pass per output dim to compute attributions with respect to parameters.

To compute your PD network's output, you simply sum the $k$ most important components (using `BatchTopK`) to create your new parameter vector $\kappa(x) \in \mathbb{R}^N$.  Then the minimality loss is given as $$\mathcal{L}_{\text{minimality}} = D(f_{\theta^*}(x), f_{\kappa(x)}(x))$$  with $D$ some distance or divergence function (minimize distance between the original network and the new thing; there are various options here.


### 2.3 Simplicity

We want our decomposed components to be simple! To do this, we penalize parameter components that span more ranks or more layers than necessary by unflattening the components back into original matrix shapes, and then minimizing the singular values of those matrices. (Ideally we'd just literally sum the ranks of all the weights, but that's not a differentiable loss; using the singular values is a common proxy.)

Recall that singular values tell you information about the geometry of the matrix multiplication — large singular values mean large stretches/shrinkages in vector length. Intuitively, if you sum across the singular values, you should get larger sums for more significant deformations. Pushing the singular values lower, even to 0 or very small values, means that the matrix operation is collapsing more dimensions down.

Now, putting it precisely: we are minimizing the simplicity loss given as $$\mathcal{L}_{\text{simplicity}}(x)=\sum^C_{c=1}s_c(x)\sum_{l,m}||\lambda_{c,l,m}||^p_p$$ with $\lambda_{c,l,m}$ the $m$-th singular value of component $c$ in layer $l$, and $s_c$  an indicator $\in {0,1}$ telling you whether component $c$ is active on the input or not. (Normally I would just use an indicator, but this is the notation given in the paper and I'd like to stick to that.) 

In theory this could incentivize a smaller weight matrix, just with with lots of dimensions and thus lots of smaller singular values, but because we have our minimality loss, we don't expect this behavior — the model is incentivized for all of its components to be 'trying to capture the important information' and since the model can only use a couple components, we expect that spreading information like that would be inefficient. There's a question here about whether high-rank transformations may be genuinely necessary for the network here that I don't feel qualified to answer, but it's an interesting one: if a transformation really does need to be high-rank, does this simplicity penalty disincentivize that behavior? how would you study it?

### 2.4 Summary 

We have all together now
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{faithfulness}} + \mathcal{L}_{\text{minimality}} + \mathcal{L}_{\text{simplicity}}$$ with $$\mathcal{L}_{\text{faithfulness}} = MSE(\theta^\*,\sum^C_{c=1}P_c)$$  $$\mathcal{L}_{\text{minimality}} = D(f_{\theta^\*}(x), f_{\kappa(x)}(x))$$ $$\mathcal{L}_{\text{simplicity}}(x)=\sum^C_{c=1}s_c(x)\sum_{l,m}||\lambda_{c,l,m}||^p_p$$
## 3. SPD: good luck have fun!

It's not *that* complicated, I'm just being dramatic.

### 3.1 Overview

APD has a couple problems: 

- it's memory-intensive and inefficient: $n$ times the memory of original model for $n$ number of components. You expect most of these matrices to be quite sparse, so that's very wasteful memorywise
- Training is highly sensitive to various hyperparameters; APD suffers from a problem slightly analogous to that of SAEs: in SAEs you need to define the dictionary size, and too large/small will make you miss or destroy important features. Here, setting your $k$ incorrectly for the `BatchTopK` will cause the model to either fail to reconstruct (not enough components), learn poorly, or on the other side use *too many components*, more than it needs. This is studied in the results section of the original APD paper.
- Attribution is inaccurate: "Gradient-based attributions, and attribution methods more generally, are often poor approximations of ground-truth causal importance (Syed et al., [2024](https://arxiv.org/html/2506.20790v1#bib.bib36)) and sometimes fail to pass basic sanity checks (Adebayo et al., [2018](https://arxiv.org/html/2506.20790v1#bib.bib1))."

So here's the new method: instead of optimizing a whole set of gigantic model-sized components, decompose each layer's weight matrix into rank-one matrices called *subcomponents*, which you expect to compose into components at the end. (There can be more of these than the rank of the decomposed matrix.) 

In more detail, instead of having a set of components $\{P_1, ... P_C\}$, all tensors shaped like the model, we take each matrix from the model $W^1...W^L$ and decompose each into low-rank matrices. These matrices are guaranteed to be low rank because they are each constructed by the outer product of two vectors $U$ and $V$, written as  $\vec{U^l_c}\vec{V}^{l\intercal}_c$ 

Intuitively, the matrix created by the outer product of two vectors has columns given by the entries in $U$, scaled by each value of $V$; you can see this just from doing the matrix multiplication with them as matrices of shape `n, 1`. This means that everything just gets projected onto the line spanned by $U$ with weighting given by $V$. Then we want to train the model so that $$W^l_{i,j} \approx \sum^C_{c=1}U^l_{i,c}V^l_{c,j}$$ i.e. the work's weight matrices approximately sum to the sum of these rank-one matrices. 

Later you will cluster the subcomponents into co-activating parameter components if they tend to activate together. You need an algorithm for this though, which is not provided by the paper since the toy models explored by the paper have obvious human-discoverable clusterings. The algorithm just needs to decide 'which ones co-activate enough to create a coherent component on their own' which is nontrivial but... hopefully shouldn't be too hard? I also wonder here whether the subcomponents themselves could be possibly interesting, or if they're too small to have obvious effects. Intuitively, if they're one part of a larger (and interpretable) component, they *should* have interpretable properties/functions.

### 3.2 A better way to work with importance

In the previous paper, `BatchTopK` and attribution were used for our 'minimality' constraint — the attribution method would guess at what the important features are for the output, and you'd then train the model, allowing it to use only the top $k$ of those features. Here, we instead train a separate model (or rather, set of models stuck in a trenchcoat together) that *predicts which subcomponents are important for a given input*. Then we randomly ablate the subcomponents based on how important they are rated to be, which gives us stochasticity.

First, let's give a more precise definition to importance: we say that something is causally important for some input, based on how much much ablating it affects the (original model) accuracy on that input.

What we want to do is train a *causal importance function* to predict the importance $g^l_c(x) \in [0,1]$ of subcomponent $c$ in layer $l$ on a given datapoint $x$. I will describe later how to compute and this causal importance function, in line with the paper; first I'll describe how it's used.

Once we have an importance value for each subcomponent on an input, we will use predicted importances to ablate unimportant subcomponents by random amounts drawn from uniform $[g_i, 1]$. We'll also construct a loss that will regularize these $g^l_c$s to be near 0 most of the time; this is how we will enforce minimality.

#### 3.2.1 Ablation Mask Details

Let $x$ be some datapoint. We want to run the model on this datapoint. However, we need to ablate our weights randomly before we do this. In other words, we need to give each layer a $W'$ matrix, $W'^l$, by summing together our randomly ablated subcomponents.

 First, let's calculate 'how much we want to ablate each subcomponent $c$ in each layer $l$.' This function will be called $m^l_c$  and will draw a datapoint from $\mathcal{U}[g^l_c(x), 1]$. This section will just describe how you implement that process. 

In order to randomly ablate, we need some randomness: for each $c$ in each $l$, let $r^l_c$ be some random scalar sampled from the uniform distribution $\mathcal{U}[0,1]$. Package all those scalars into a vector $r$. 

Recall that we want our ablation coefficient to be on the interval $[g^l_c(x), 1]$, not on the interval $[0,1]$. Thus, let's describe a function $m^l_c(x,r)$, which takes in our datapoint and our randomness vector $r$, and uses the randomness to output a random ablation coefficient for subcomponent. (For example, this function might output 0.2 for some subcomponent, in which case we ablate the subcomponent by 80%.) We define this function as $$m^l_c(x,r):=g^l_c(x)+(1-g^l_c(x))r^l_c.$$In other words, we take the predicted importance for our subcomponent on this datapoint, $g^l_c(x)$, as our minimum ablation coefficient, and then add a random nonnegative amount to it such that the result is not larger than 1.

Now having calculated this for each subcomponent, we define each element $W'^l_{i,j}$ of our randomly-ablated weight matrix for this layer $W'^l$ to be
$$W'^l_{i,j}(x,r):= \sum^C_{c=1}U^l_cm^l_c(x,r) V^l_c.$$
In English, to get the weights we'll use for this specific input $x$ we sum each rank-one subcomponent in this layer given by $U^l_{i,c}V^l_{c,j}$, but weight that sum by the amount we want to ablate it, $m^l_c(x,r)$, which we just calculated.

To foreshadow the next section, our faithfulness constraint formally speaking is that we want it to be the case that, for any $r$, $$f(x|W'^1(x,r), ... W'^L(x,r)) \approx f(x|W^1, ..., W^L)$$i.e. we want the output from our decomposed weights to be very close to the output of our original model. We will specify a loss function that incentivizes this later. 

Before covering the loss functions, I want to pause momentarily and discuss the way we actually get these $g^l_c(x)$ predictions. 

#### 3.2.2 The component importance estimation model

How do we get the $g^l_c(x)$ values? Recall that to compute this naively, we would need to compute the original model's loss for every single combination of ablations, making it intractable for any non-toy network. Thus, the authors choose to simply learn a function to predict it, lol.

A causal importance function $\Gamma: X \to [0,1]^{C \times L}$ maps from our input space to causal importance values for every single subcomponent in each layer ($C \times L$ total values). The particular implementation that the authors choose to use is as follows: 

- Each subcomponent gets its own mini function $\Gamma^l_c$.
- This function is just a small trained MLP that runs on the sum of the subcomponent's 'inner activations.' 
	- What is the inner activation? Recall that each $W^L$ in the model is the sum of multiple low-rank subcomponent matrices. Each subcomponent is low-rank because it is described by the outer product of two vectors, $\vec{U^l_c}\vec{V}^{l\intercal}_c$. We normally apply these in succession to the activation vector of the model coming into the layer, i.e. to get the output of layer $l$ we apply $W^l a^l(x) = U^l_cV^{l\intercal}_ca^l(x)$. [^2]
	- Then we can just apply the first transformation $\vec{V}^{l\intercal}_c$ and not the second. Thus, let our 'inner activation' for the subcomponent be $V^l_ca^l(x)$. 
- In particular, we sum over over this inner activation to get a scalar $h^l_c(x) := \sum_j V^l_{c,j}a^l_j(x)$ which we then pass into a small trained MLP $\gamma^l_c$ and run the result through a hard sigmoid (a sigmoid-like function that is not smooth, for the sake of efficiency) $\sigma_H$ to get the result.
	- The exact architecture is detailed in [Appendix A.1](https://arxiv.org/html/2506.20790v1#A1.SS1); it's just a GELU MLP with dimensions 1 → hidden → 1. 

Remember that these gamma functions are being used by the $m^l_c$ function to create ablation masks for the subcomponents. Thus, we can use the main network's loss function to train these $\Gamma^l_c$ functions alongside the main network! More specifically, they use a reparameterization trick from [Kingma and Welling 2013](https://arxiv.org/abs/1312.6114)(cool thing to look into more later) to propagate the gradients back through the masks and train the $\Gamma^l_c$ functions.

Now, we need to incentivize the network to only have a small number of important subcomponents on any given input. That will be our final loss function, described below.

### 3.3 SPD Loss Functions

#### 3.3.1 Faithfulness

The faithfulness loss is the same as it was in the APD paper: the MSE of the sum of the original model weights with the decomposition's weights. Now it's just rewritten with new notation:  $$\mathcal{L}_{\text{faithfulness}} = \frac{1}{N}\sum^L_{l=1}\sum_{i,j}(W_{i,j}^l-\sum^C_{c=1}U^l_{i,c}V^l_{c,j})$$
### 3.3.2 Stochastic reconstruction

Now, we also want the output of our decomposed weights to be close to the output of the original model for any set of ablations, so that the model only ablates *causally unimportant* subcomponents. It's impossible to calculate $f(x|W'^1(x,r), ... W'^L(x,r))$ for every possible value of $r$. Instead, we'll calculate it for many random values, and average them.

Sample points $r^{l,(s)}_c$ from the $\mathcal{U}(0,1)$ distribution to generate $S$ vectors $r^{(s)}$ which we use to mask subcomponents (on separate forward passes, I think) with $m_c^l(x,r^{(s)})$. Then our loss will be given by the average distance/divergence between the outputs for this randomly-ablated model and the outputs of the original model. $$\mathcal{L}_{\text{stochastic-reconstruction}} = \frac{1}{S}\sum^S_{s=1}D\bigg(f(x|W'(x,r^{(s)})), f(x|W) \bigg)$$$D$ here is whatever measure of divergence is appropriate for the model's outputs. Transformers, for example, output a probability distribution; in that case $D$ would be KL divergence, because KL divergence describes the divergence between two probability distributions.[^1] Then in the limit as $S \to \infty$, this function will optimize the weights such that $$f(x|W'^1(x,r), ... W'^L(x,r)) \approx f(x|W^1, ..., W^L)$$ as desired; presumably a large value will suffice. 

Now, theoretically this loss in the limit is great: with an infinitely large number of points it will be quite nice. Practically, though, with a more reasonable (lower) number of datapoints it will be noisy. All we get from the authors on why this might be is 

> However, this loss can be somewhat noisy because it involves a forward pass in which every subcomponent has been multiplied by a random mask.

which I interpret as, "with a large model, the noise caused by many random masks might accumulate, especially towards the end of the network, and be unreliable for accurate gradient calculations; this would slow down training."

 Remember that the reason we added random ablations was (1) to be more confident about the causal importance of the subcomponents in question by trying random combinations of them (2) to prevent us from needing to use a hyperparameter choosing how many components to use (as in APD there was a top-k parameter, and the network was highly sensitive to it). **add this above when you turn this into a blog post**

But we still want to have a model that is stable enough (with this stochasticity) to still learn accurately; our model needs to have reliable understanding of how the subcomponents relate to the outputs. Thus we add a second, layerwise version of the stochastic reconstruction loss, in which we only mask one layer at a time, leaving the rest of the layers with their original values: $$\mathcal{L}_{\text{stochastic-reconstruction-layerwise}} = \frac{1}{LS}\sum^L_{l=1}\sum^S_{s=1}D\bigg(f(x|W^1, ..., W'^l(x,r^{l,(s)}), ... W^L),  f(x|W) \bigg)$$If the subcomponents do indeed sum to the original weights, then notice that this is just a special case of $\mathcal{L}_{\text{stochastic-reconstruction}}$with $r^n_c = 1$ for $n \neq l$ since $W^n = W'^n(x,1)$ leaving us with something like $$\frac{1}{L} \sum^L \text{[$\mathcal{L}_{\text{stochastic-reconstruction}}$ just with $r^n_c = 1, n \neq l$ and $r^l_c$ random]}.$$The authors say that this "shouldn't substantially alter the global optimum of training" because it is an average across a special case of $\mathcal{L}_{\text{stochastic-reconstruction}}$. 

### 3.3.3 Minimality

The last component to our loss function is $$\mathcal{L}_{\text{importance-minimality}} = \sum^L_{l=1}\sum^C_{c=1}|g^l_c(x)|^p$$with $p$ some positive value. (You can use $p=1$ but you can also use other values.) This, in tandem with the constraints given by other losses, incentivizes the learned importance predictors to only predict high importance for a limited number of subcomponents, incentivizing the minimality that we want. (The phrase "predict importance" is a bit weird because the importance function is trained alongside, so at first it's doing something more like 'routing the computation to a specific set of the weights' or something. I'm a little confused about this, but it seems that structure indeed emerges as desired.)

## 3.4 Summary 

Our whole loss together now
$$\mathcal{L}_{\text{SPD}} = \mathcal{L}_{\text{faithfulness}} + (\beta_1 \mathcal{L}_{\text{stochastic-recon}} + \beta_2 \mathcal{L}_{\text{stochastic-recon-layerwise}}) + \beta_3 \mathcal{L}_{\text{importance-minimality}}$$ with $\beta_1, \beta_2, \beta_3$ hyperparameters

$$\mathcal{L}_{\text{faithfulness}} = \frac{1}{N}\sum^L_{l=1}\sum_{i,j}(W_{i,j}^l-\sum^C_{c=1}U^l_{i,c}V^l_{c,j})$$
 $$\mathcal{L}_{\text{stochastic-reconstruction}} = \frac{1}{S}\sum^S_{s=1}D\bigg(f(x|W'(x,r^{(s)})), f(x|W) \bigg)$$  $$ \mathcal{L}_{\text{stochastic-reconstruction-layerwise}} = \frac{1}{LS}\sum^L_{l=1}\sum^S_{s=1}D\bigg(f(x|W^1, ..., W'^l(x,r^{l,(s)}), ... W^L),  f(x|W) \bigg)$$ both with $S$ a hyperparameter and
$$\mathcal{L}_{\text{importance-minimality}} = \sum^L_{l=1}\sum^C_{c=1}|g^l_c(x)|^p$$ with $p$ a hyperparameter. In [Appendix 6](https://arxiv.org/html/2506.20790v1#A1.SS6) there is pseudocode for the training algorithm.

## 4. Conclusions

The results in the paper are pretty cool! They're able to reproduce results from [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html) and some similar toy models (up to a 3-layer residual model intended to model cross-layer distributed representations) with impressive results. SPD can decompose mechanisms that span layers! 

This approach seems interesting. I'm interested in understanding in more detail how it is similar to and different from Anthropic's cross-coders work, both technically and conceptually/paradigmatically. It seems like both of the approaches are aiming to find the same things — the "circuits" or "mechanisms" underlying model behavior — but with different approaches. The authors of SPD may be unhappy with that characterization, since they see part of their contribution as being the 'mechanisms' terminology and paradigm itself which Anthropic does not use, but they seem similar to me in that respect at the moment, having skimmed the Anthropic paper. *(Update: no, they're happy with this characterization! They just expect PD to find different things in practice than Anthropic's approach.)*. The important difference, I guess, is that Anthropic's CLT stuff is still working under the sparsity idea, which the PD approach clearly makes efforts to avoid. They also have models which don't necessarily have to reproduce the model's outputs: they get a CLT network that reproduces the outputs of the original 18-layer transformer 50% of the time — which is simultaneously exciting and encouraging. In contrast, the faithfulness and reconstruction constraints in SPD should lead to ~100% reconstruction accuracy, though it's unclear thus fa whether the approach will scale to the level that Anthropic's has, and whether, if it does, the components identified will continue make sense.

I'm still fuzzy on some details about how exactly the models are trained, and would like to spend some time implementing the SPD work from scratch. Maybe also the transcoders stuff too. I wonder if combining the approaches has any merit, or if there's either approach could shed light on the other's.

I also have a couple experiment ideas. Most of them involve trying out other toy models and seeing if SPD works on them, and whether it discovers similar circuits (e.g. induction heads) as are found in previous work that seems to find mechanism-like things. I'm also interested particularly in how SPD might or might not work with attention; right now it has only been run on MLPs. I'm guessing one important improvement would be that the $\Gamma^l_c$ importance functions might need to be more 'context-aware' in some sense given the way that the key-query-value matrices interact interdependently — or maybe the current approach would work fine, and you could just append the QKV matrices together into one big matrix and use that with the current setup.

Thanks for reading! Hope this was helpful.


[^1]: Gradient attributions have problems and can be inaccurate — you will see this below when we cover the section in the SPD paper that does something better than gradient attributions — but we're going to roll with this for now because it's relatively simple and thus nice for getting the feel for PD's method. I didn't spend too much time figuring out the details of gradient attributions because this isn't even the most up-to-date method. It's something to do some other time. 

[^2]: Models that don't do pure matmuls alone, such as the transformer, are not discussed in the paper, and I will add notes about the authors' caveats below regarding the limitations of this specific implementation of a causal importance function.
