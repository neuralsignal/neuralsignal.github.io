---
layout: post
title: Evolving Distributions for the S&P 500 Returns (Part 2 of 3)
date: 2026-07-05
description: AI-generated distribution fit to S&P 500 Returns (Part 2 of 3)
tags: distributions finance evolutionary-ai
categories:
enable_vega: true
vega_base_url: /assets/blog/distributions-evolve
vega_charts:
  - id: vis-trajectory
    file: trajectory.json
  - id: vis-anomaly
    file: score_anomaly.json
---

In [the last post]({% post_url 2026-07-05-sp500-distributions-part-1 %}) I compared hand-designed distributions on the daily returns of the S&P 500. The best one, the Johnson SU, makes the observed move on a typical day about 24% more probable than the Normal does. Here, I will try to beat it by generating *novel* distributions using LLM-driven evolutionary search. 

<div class="post-figure" style="max-width: 760px; margin: 1.5rem auto;">
<svg viewBox="0 0 760 220" role="img" aria-label="The evolution loop: prompt sampler, language model, evaluator, program database, and back" style="width: 100%; height: auto; color: var(--global-text-color, #2D2D2D);">
  <defs>
    <marker id="ev-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55">
    <rect x="8" y="26" width="150" height="68" rx="8"/>
    <rect x="205" y="26" width="150" height="68" rx="8"/>
    <rect x="402" y="26" width="150" height="68" rx="8"/>
    <rect x="599" y="26" width="153" height="68" rx="8"/>
  </g>
  <g fill="currentColor" text-anchor="middle" font-family="DM Sans, sans-serif">
    <text x="83" y="56" font-size="14" font-weight="600" fill="#2D6A4F">Prompt sampler</text>
    <text x="83" y="76" font-size="11" opacity="0.8">top + diverse code</text>
    <text x="280" y="56" font-size="14" font-weight="600" fill="#3D85C6">GPT-5-mini</text>
    <text x="280" y="76" font-size="11" opacity="0.8">mutates the code</text>
    <text x="477" y="56" font-size="14" font-weight="600" fill="#E07A5F">Evaluator</text>
    <text x="477" y="76" font-size="11" opacity="0.8">CV log-lik, novelty, norm</text>
    <text x="675" y="56" font-size="14" font-weight="600" fill="#E8A838">Database</text>
    <text x="675" y="76" font-size="11" opacity="0.8">MAP-Elites, 6 islands</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#ev-arrow)">
    <line x1="160" y1="60" x2="201" y2="60"/>
    <line x1="357" y1="60" x2="398" y2="60"/>
    <line x1="554" y1="60" x2="595" y2="60"/>
    <path d="M675,96 L675,158 L83,158 L83,98"/>
  </g>
  <text x="380" y="151" fill="currentColor" opacity="0.8" text-anchor="middle" font-size="11" font-style="italic" font-family="DM Sans, sans-serif">selection and migration feed the next prompt</text>
</svg>
</div>

The diagram above shows the search loop. I used OpenEvolve, an open-source reimplementation of DeepMind's AlphaEvolve [1, 2]; FunSearch and ShinkaEvolve use similar recipes [3, 4]. The language model proposes edits to a small Python class. The class fits its parameters to data and returns a log density. Every candidate is scored with the same 5-fold time-series cross-validation from Part 1, so the numbers are directly comparable. A database keeps the best and most diverse candidates (MAP-Elites with 6 islands [5]) and feeds them back into the next prompt. The prompt gives the model mathematical primitives to combine (power-law tails, hyperbolic damping, contaminated mixtures), requires that the density integrates to one, and asks for novelty.

To support novelty, the evaluator halves the score of any candidate whose source code mentions a known distribution. This, of course, is something that is very easy to reward hack, but I kept it as a simple way to punish proposals that are clearly using existing distributions. Despite this simple attempt to enforce novelty, the search generally came back to the Student-t: the model has seen it fit fat tails thousands of times during training, and even a penalized t scored better than a badly normalized new kernel. When the string matching caught the banned words, the search swapped the Student-t for a sinh-arcsinh and a two-piece t instead. Both are real, named, published distributions, but neither contains the banned words.

<div id="vis-trajectory" style="width: 100%;"></div>

The chart above shows the progress of the search. Each gray dot is a valid candidate; the green line is the best one found so far. The line climbs past the Johnson SU and ends at a distribution that makes the typical day's move about 8% more probable than the Johnson SU (a cross-validated log-likelihood of 3.35 per day against 3.275). Most of the dots sit below the line, so most of what the search tries does not beat what it already has.

A bigger problem was that the search exploited gaps in how the score was computed. The clearest case is shown below. One candidate reported a cross-validated log-likelihood of 9.29 per day, which would make the typical day's move several hundred times more probable than any properly normalized density can. In this candidate, the `fit` function computed the normalization constant for one kernel while `log_pdf` evaluated a slightly different one. The density no longer integrated to one, and every log-density value was inflated by the same constant.

<div id="vis-anomaly" style="width: 100%;"></div>

Other candidates cheated in less obvious ways or produced some nonsense. One computed a parameter, stored it, and never used it in the density; the evolution kept "improving" this dead code because it had no effect on the score. Another reported three parameters while actually storing nine (the score penalizes parameter count, and reporting a lower count is easier than reducing it). This was Goodhart's law in action: the search optimized the score and not the fit the score was supposed to measure.

I fixed the evaluator in three ways. I now integrate the density on a fine grid and reject anything that does not come out close to one. I only require a single method and derive everything else from it, so there is a single source of truth instead of multiple functions that can disagree. And I added more names to the banned list. The common cause of all these exploits was an evaluator that trusted the code too much; whatever it does not check, the search will likely exploit. And this is really the problem with a lot of LLM-evolutionary search. It requires rigorous development of evaluations that get as close as possible to the actual "latent thing" you are trying to measure.

### Did the search find anything genuinely new?

With the fixed evaluator, the search started producing distributions that were a bit more novel and were properly normalized. In [the next post]({% post_url 2026-07-05-sp500-distributions-part-3 %}) I look at what it found.

### References

1. OpenEvolve: [algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve), an open-source implementation of AlphaEvolve.
2. DeepMind (2025). [AlphaEvolve: a Gemini-powered coding agent for designing advanced algorithms](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).
3. Romera-Paredes, B. et al. (2024). "Mathematical discoveries from program search with large language models." *Nature*, 625, 468-475. (FunSearch)
4. Sakana AI (2025). "ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution." [arXiv:2509.19349](https://arxiv.org/abs/2509.19349).
5. Mouret, J.-B. & Clune, J. (2015). "Illuminating search spaces by mapping elites." [arXiv:1504.04909](https://arxiv.org/abs/1504.04909).
