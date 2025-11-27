# Better gradient attributions from Integrated Gradients to ReIP
Date: 2025-11-26
Tags: technical interp notes
Type: post
Desc: Explaining integrated gradients and ReIP, an alternative method

Transluce just published [a cool paper](https://transluce.org/neuron-circuits) doing circuit tracing with MLP neurons instead of SAEs or CLTs. One interesting part of the paper is that instead of Integrated Gradients (a standard causal attribution technique) they use a new method called ReIP (apparently developed concurrently in [Jafari et al 2025](https://arxiv.org/abs/2508.21258), from whom they get the name, though the Transluce people apply it differently) for attribution. I have three questions: 

- How did IG actually work? (I never bothered to actually read the paper and figured I'd get around to it when I needed to use it)
- How does ReIP work? 
- What are the mathematical reasons that ReIP should perform better, as it seems to emprically?

Also, the transluce paper builds up a lot of notation and describes various measurement quantities across the paper that on my first read I didn't fully internalize. This blog post plans to be an explanation of at least some of these questions and uncertainties. (I write posts like this in order to effortfully process the material, because I have bit of a hard time getting myself to process math fully if I don't write it out myself.)

*Disclosure of conflict of interest: the lead authors of the Transluce paper are PhD students at Stanford who I know and admire.*

[TOC]

## 1. How does IG work?

There are variants on IG; I'm going to re-explain the version used in this paper, which is `IG-activations`. Our goal is to understand how much a particular 'node' in our neural network contributes to a change in output when the input changes. In our example, this is how much a given neuron in an MLP contributes to the change in an output token when the input changes — for example, how much a particular neuron is involved in changing the output from "hot" to "cold" when the input changes from "is fire hot or cold?" to "is ice hot or cold?". If a neuron is highly involved in that output change, you think that it is causally relevant to the model's internal computations about temperature. (This should match your intuition, I think.) Note that this bakes in a supposition that the thing you're looking at is the right 'unit' or 'kind of thing', e.g. MLP neurons as opposed to are indeed a 'canonical' unit on which we should be doing circuit tracing as opposed to the units given by previous work like CLTs or SAEs.[^1] If that assumption fails, your attribution won't tell you much, and if anything will lead you astray (?).

### 1.1 Input IG
Integrated gradients is a method of computing a number for this 'involved'-ness metric. The method comes from two axioms, given in the [original paper](https://proceedings.mlr.press/v70/sundararajan17a.html). Be careful here; this method was designed for the context of *input* attributions (not internal feature attributions) so we'll start there and move forward. For a moment, put away the hot-cold example above in your head; instead think, 'which pixels in an image are most responsible for the output prediction?'. Here are the two axioms.

1. **Sensitivity.** If an input has different predictions from a baseline input, and its activations differ in one feature from that baseline input, that feature should have a nonzero attribution.
2. **Implementation invariance.** Two networks are functionally identical if giving them identical inputs always results in identical outputs. Thus, we want our attribution to yield the same value on two functionally identical networks, even if they vary in their internal structure. (You can see why this doesn't immediately translate into use in the context of activations.)

In the input features context, this looks like the following. Take an input and a baseline $x, x' \sim \mathcal{D}$, like an image of a dog and the baseline all-black or all-gray image. We want to know how much the value of some input dimension $i$ (e.g. a single white/black pixel) is causally implicated in the output. Let $F: \mathbb{R}^n \to [0,1]$ be your neural network represented as a function.

You know how to take the gradient of the output prediction $F(x)$ with respect to $i$. Integrated gradients, just walks in a straight line (interpolates) from $x$ to $x'$ in input-space and accumulates the gradients along that line. Formally, this looks like changing $\alpha$ from 0 to 1 in $x' + \alpha(x-x')$. 

We need the $(x_i - x'_i)$ term on the front for path integral reasons, but there's also at least one easy intuitive reason: if you have a high-gradient input that doesn't change much, it should be downweighted compared to a medium-gradient input that changes a lot. Formally, the function is
$$\text{IGoriginal}_{i}(x, x')= (x_i-x'_i)\int^1_{\alpha=0}\frac{\partial F(x' + \alpha(x-x'))}{\partial x_i}d\alpha$$
which you numerically approximate with a Riemann sum as$$ \approx (x_i - x_i') \frac1n \sum^n_{j=1} \frac{\partial F(x + \frac{j}{n}(x-x') )}{\partial x_i}.$$It would be nice to talk more about why this indeed satisfies the axioms discussed above. It appears to be due to nice properties of path integrals and gradients (since this is actually just a path integral).
### 1.2 Feature IG
The generalization from this to model internals is non-obvious. Implementation invariance seems complicated to use as an axiom when... the implementation seems to be the *whole point* when we're doing interpretability.

What you do is just *not care about implementation invariance, lol.* In the words of the Transluce authors: 

> the lack of application of IG to internals in the original paper has led to a profusion of differing techniques for internals attribution, which need not satisfy the original IG axioms.

One thing you can do is assume that the gradients flow through an intermediate feature $v(x)$ and use the chain rule ("arguably the most principled application of IG to internals"). This is called the **conductance**. Another way you could adjust is to basically treat $v(x)$ like an input feature. This is $\text{IGacts}$, which gets used in the paper. The cited reason for using this version over conductance is that "conductance is not used in recent benchmarks of gradient-based attribution; subtly different techniques have been proposed and adopted recently" (i.e. $\text{IGacts}$.)

So what we're looking at now is: you have an input data distribution $\mathcal{D}$ and two points $x, x' \sim \mathcal{D}$. Now, let your language model be a function $M: \text{vocab\_size}^{\text{max\_context\_length}} \to \mathbb{R}^{\text{vocab\_size}}$ (takes in token ids in indices, outputs logit distribution) seen as a **graph** of connected subunits. A **circuit** $C = (V,E)$ is a sub-graph of that graph, consisting of a set of nodes $V$ (in this case MLP neurons) and edges $E$. To "run" a circuit as a function $C(x)$, you run $M(x)$ but replace all the values of nodes not in $V$ (i.e. with their average across the whole dataset. Formally, $$C(x) := M(x; \text{do } v = \mathbb{E}_{d \sim D}[v(d)] \text{ for } v \not \in V)$$where $\text{do}$ may be the Judea pearl do thing but I don't know about that right now so I can't say. This yields a distribution 

<!-- Typo in the C(x) definition? -->

Now we need one more thing before we get to the implementation the paper uses. We need something to take the derivative of so we can accumulate gradients! Previously this was just the classification probability or something like that (I think). We're working with single output tokens, but the model gives us logits over the whole vocabulary. Let's return to the "cold" vs. "hot" example: what we need is some way to see how the model's predictions of "cold" vs. "hot" change. Let $y$ be the original output token ("hot") and $y'$ the counterfactual ("cold") output token. Thus we define the metric $$m(C,x) :=[C(x)]_y - [C(x)]_{y'}$$ so that we have a single real quantity of which we can take the gradient. To look at the whole model's difference in logits (not just a circuit's) we just run $m(M, x)$, which is what actually gets used in IG. (We defined the notation for later.) 

Finally, we're here at our formulation of $\text{IGact}$ that the paper uses. For a given feature $v \in V$, we have $$\text{IGact}_v(x, x') = (v(x)-v(x'))\int^1_{\alpha = 0} \frac{\partial m(M,x; \text{do }v = v(x') + \alpha(v(x)-v(x')))}{\partial v}d\alpha $$ which looks almost exactly like the original input-feature IG did, just that now we're running it on the metric $m$ with our intervention, interpolating the value of our feature $v$ from $v(x')$ to $v(x)$. It's approximated the same way as well: 
$$\approx (v(x)-v(x')) \frac1n \sum^n_{j=1}m\big(M,x; \text{do } v = v(x') + \frac{i}n(v(x)-v(x'))\big)$$

Great, we've defined integrated gradients!

<!-- ## 2. Yang et al. metrics (faithfulness and completeness ## 3. How does ReIP work? -->


[^1]: The authors of the Transluce paper make it very clear that they do not necessarily feel confident that this is the case, but wanted to showcase that it's worth exploring. I think this is well-borne out by their results. I also think that the argument that nonlinear activation functions privilege the canonical basis of the MLP latent layer is not totally persuasive but very reasonable
