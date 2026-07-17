---
layout: post
title: The Evolved Distributions for the S&P 500 Returns (Part 3 of 3)
date: 2026-07-05
description: AI-generated distributions fit to S&P 500 Returns (Part 3 of 3)
tags: distributions finance evolutionary-ai
categories:
enable_vega: true
vega_base_url: /assets/blog/distributions-discovery
vega_charts:
  - id: vis-overlay
    file: evolved_overlay.json
  - id: vis-bands
    file: band_decomposition.json
  - id: vis-baselines
    file: baseline_with_evolved.json
  - id: vis-params
    file: params_vs_fit.json
  - id: vis-holdout
    file: holdout_eval.json
---

The search found something, but not a single winning distribution so far. In [the last post]({% post_url 2026-07-05-sp500-distributions-part-2 %}) I worked on the evaluation scripts so that the evolutionary search could no longer cheat its way to a high score easily. Three evolutionary runs produced three variants. All of them descend from the seed kernel the search started from:

```
seed(z) = exp(-|z|^alpha) / (1 + z^2)^(alpha/2),      z = (x - mu) / sigma

Model 1 (4 params)   seed(z) with a different alpha on each side of zero;
                     the two exponents are derived from the quartile skew

Model 2 (4 params)   seed(z) * (1 + |z|)^(-beta) with a smooth directional
                     tilt and a small contamination term

Model 3 (5 params)   (1 - eps) * core(z) + eps * tail(z)
                     core = exp(-|z|^alpha) * sech(z)^gamma * (1 + |z|)^(-c)
                     tail = separate power law, mixed in at eps of about 5.6%
                     both evaluated on z / s(z),  s(z) = 1 + delta * tanh(z/2)
```

The seed multiplies a stretched exponential by an algebraic damping term. The first factor appears in the generalized normal, the second in the Student-t.

Model 1 changes the seed the least. It fits a location, a scale, and one tail exponent, and gets its asymmetry by deriving separate left and right exponents from the quartile skew of the data. Model 2 adds an explicit power-law damping and a directional tilt. As fitted, it spends that flexibility on the direction of moves, and its left tail comes out far heavier than its right.

Model 3 is the search's own top scorer and the furthest from the seed. It rebuilds the density as a contaminated mixture: a core that multiplies three decay terms handles the body, and a separate power-law kernel mixed in handles the outlier days. The asymmetry comes from smoothly rescaling `z` by `1 + delta*tanh(z/2)`, so unlike the skew-t from Part 1 there is no kink at the center. Every individual term shows up in some named family, but the combinations of the terms do not.

<div id="vis-overlay" style="width: 100%;"></div>

The chart above shows all three fitted to the returns, with the Johnson SU and the Normal for reference, on the log-density axis from Part 1. In the center the curves are nearly indistinguishable, but the differences are in the tails are large. Model 1 is the most generous for moves of 2-5%. Model 3 holds its mass back for the far tails: a Black Monday sized drop is about twenty times more probable under it than under the Johnson SU. Model 2 bets on direction instead: a 5% drop is about thirty times more probable under it than a 5% gain.

Judged purely as a match to the histogram the Johnson SU still looks like the best curve in the chart. It tracks the bars closely over the whole range. Model 1 sits above the bars almost everywhere for median range changes in the index. Model 2 looks completely wrong at the right tail. It makes big up days far less probable than the bars say.

<div id="vis-bands" style="width: 100%;"></div>

So how do shapes like these score well? The chart above splits the score by the size of the daily move, relative to Johnson SU, with every model fit on the full history. The log-likelihood does punish Model 2's tail on every event it gets wrong. The biggest up day in the history is about a hundred million times less probable under it than under the Johnson SU. The punishment just arrives too rarely to matter. The whole history contains 140 days beyond +4% against 12,270 days that move less than half a percent, and making each of those quiet days about 12% more probable buys the entire tail penalty back twice over.

Model 1 runs the same trade in the other direction: it gives up about 13% per day in the 0.5-1% range and earns it back with a 60% edge on the 571 days between 3% and 6%. The average log-likelihood weights every error by how often it occurs. That is the correct behavior for a proper score, and it makes a rare-event mistake of several orders of magnitude cheap. 

To better handle this during the search, I would have to update the evaluation to either overweight the intermdiate and long tail events in the loss or choose a different loss function.

<div id="vis-baselines" style="width: 100%;"></div>

On the cross-validation, all three beat every distribution from Part 1. The best of the family is not the search's top scorer but Model 1: the observed move on a typical day is about 4% more probable under it than under the Johnson SU, and almost 30% more probable than under the Normal. The other two add about 1% over the Johnson SU.

<div id="vis-params" style="width: 100%;"></div>

The scatter above plots the cross-validated score against the number of parameters (model complexity). The jump from the standard families to Model 1 is the whole gain, at the same four parameters the Johnson SU uses. The extra parameter of the bigger variant buys nothing on the cross-validation. 

### Does this hold up on new returns?

The cross-validation is not a clean test. The search never fit on the validation folds, but their scores fed back into which candidates survived, so the selection pressure pushed the winners toward those folds. The first half of 2026 carries no such feedback, because I only used data up to December 2025 for the optimization. As a held-out test, I fit every distribution on the full 1928-2025 history and scored it on the new returns (December 30, 2025 to July 2, 2026).

<div id="vis-holdout" style="width: 100%;"></div>

None of the evolved distributions win here. The top of the chart is a pile-up: the Laplace, Student-t, and Johnson SU land within a fraction of a percent of each other. Models 2 and 3 sit just below the Johnson SU. Model 1, the winner on cross-validation, does worst of the three: the typical new day is about 3% less probable under it than under the Johnson SU. The Normal keeps losing, making the typical day about 7% less probable.

The quietness of the period is the clue (despite what one might think reading the news). The new returns have a daily standard deviation of 0.9% against the 1.2% historical figure (The biggest move in the period is a single 2.8% day). Almost all of the score comes from the body of the distribution, which is exactly where the evolved kernels gave probability away.

### What did the machine optimize?

A few patterns held throughout the search. The model always estimated its parameters with robust statistics: median for location, scaled median-absolute-deviation for scale, never the mean and standard deviation. For heavy-tailed data this is the right choice (one crash day distorts the mean but barely moves the median). The model also spent far more effort improving the fitting code than the math. The kernel shape stabilized early. A better fitting code tended to raise the score more reliably than a new density (that may fail to normalize). Again, this is a sign to improve the evaluation and potentially reward some exploration of kernel shapes. 

Overall, this exercise is closer to optimization than to discovery. I defined the objective, the data, and the interface. The search could only change the functional form. AlphaEvolve and FunSearch have produced real results in combinatorics and matrix multiplication with the same recipe [1], while ShinkaEvolve and the AI Scientist try to generate the research question itself [2, 3]. The failure modes seem to carry over to these larger systems. Sakana's Darwin Godel Machine reportedly learned to delete its own hallucination checks to score better on a benchmark [4], which is the same move as the under-normalized distribution from Part 2.

The evaluator deserves the same scrutiny as the candidates. The cross-validated log-likelihood is a proper score and the search optimized it honestly. It is just a measure or proxy of what we care about. A human fitting a distribution often thinks about multiple criteria to align on in a dynamic way instead of optimizing for a score: the curve should track the histograms, the tails should be plausible, the formulation should be relatively simple and straightforward, etc.

Anyway, there are many ways to improve this little experiment. But for now I will keep it here as an "artifact" for people to read.

### References

1. Romera-Paredes, B. et al. (2024). "Mathematical discoveries from program search with large language models." *Nature*, 625, 468-475. (FunSearch)
2. Sakana AI (2025). "ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution." [arXiv:2509.19349](https://arxiv.org/abs/2509.19349).
3. Yamada, Y. et al. (2025). "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search." [arXiv:2504.08066](https://arxiv.org/abs/2504.08066).
4. Zhang, J. et al. (2025). "Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents." [arXiv:2505.22954](https://arxiv.org/abs/2505.22954).
