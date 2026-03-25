---
layout: post
title: Working with the machines
date: 2026-03-22
description: Changes in my workflow because of "AI".
tags: agentic-ai productivity
categories:
enable_vega: true
vega_base_url: /assets/blog/agentic-workflow
vega_charts:
  - id: vis-learning-curves
    file: learning_curves.json
  - id: vis-time-allocation
    file: time_allocation.json
---

### Where my work moved

What changed for me with "AI" is not just speed. I write fewer first drafts by hand now, but I spend more time specifying what I want, pruning what the model produced, and checking that I still understand it. Am I being more thorough than before? I don't quite know. My old mistakes versus the model's are usually different. Mine tended to come from moving too fast through an idea: indexing mistakes, edge cases I did not split out, or a spec that was still half in my head (I used to have a lot more just in my head than nowadays). The model fails differently. It swallows errors, picks the wrong abstraction level, or produces far more structure than the task actually needed.

The shift became clear once I split my coding work into two broad categories: exploratory analysis and production code. In exploratory analysis, I used to poke around in notebooks until the shape of the analysis emerged. Now I usually specify the analysis up front, in marimo rather than Jupyter (the model can generate and debug that more cleanly), let it build a first pass, and then spend my time pruning, checking, and editing the notebook into something coherent. The exploratory loop is still there. I just write less of the first pass myself, and I produce (i.e. let the "AI" generate) and throw away more analysis side quests.

In production code, I used to test ideas more directly in code or in small exploratory fragments (often in notebooks). Now I start with an exploratory discussion with the "AI" and then write a specification, test cases, and finally implement. The main problem is not producing usable code anymore, but rather getting the abstractions right and making my assumptions explicit. I still want to understand the generated code well enough to "own" it later. Because code is cheap to generate, I am also more willing to throw it away and restart from a cleaner spec instead of repairing an existing implementation.

### The setup tax for automating complex tasks

<div id="vis-learning-curves" style="width: 100%;"></div>

The model's ability to cheaply produce first drafts made it worthwhile to automate recurring semi-manual tasks that I previously ignored.

For example, I recently implemented tooling to generate data-heavy PowerPoint slides that had to follow an internal style guide and a specific template. Building the first version of that workflow took longer than making the slides by hand. I needed tooling for the template, tooling for the data warehouse, and a configuration format that allowed the model to describe layout, figures, and text without directly interacting with PowerPoint.

The early outputs of this workflow were buggy and not pretty (e.g. bad spacing, wrong sizing, too much stuff on one slide, overlapping text). Simply telling the model to improve them did not work. I kept trying to fix the slide by re-prompting. This doom loop was quite frustrating. Once I started concentrating on improving the tooling that produced the output, I got better results. Generating the code for specific tasks like writing tests for part of the tooling or generating a specific type of data chart was fairly straightforward with today's models (I call these "task-level" flows). Having a set of tools for agents that have sufficient flexibility but also the necessary constraints and logging all my decisions and preferences for an agent to recall later (i.e. memory) takes time and effort; and will require continued curation. I believe managing these "system-level" flows will suck up more and more time, but produce significant efficiency improvements overall for many semi-structured workflows like slide creation. The net benefit crossover point for any particular workflow, when and if it comes, is not just the tool getting better. It is also getting more structured about how I (or we) use the models.

### New type of work

<div id="vis-time-allocation" style="width: 100%;"></div>

A couple years ago my workday consisted of three main activities: doing things, reviewing what I did, and coordinating with other people. The chart above is a rough split of how that changed. "Doing" shrank to maybe 10% of the day. Three new line items appeared: context and tooling (writing the specs, configs, and environment setup that let the model produce something useful), knowledge curation (recording decisions and preferences so the model can recall them later), and agent management (starting sessions, reading logs, restarting when the model goes in circles). Taken together, these new categories take up more than half the day. Review also grew, since verifying the model's output takes more attention than checking your own. This shift happened because code got cheap to produce but expensive to specify well. The context documents I write for the model are often the clearest record of what a project actually does; I wrote them to steer the model, and they ended up being the thing I reach for when I come back to a project weeks later [5, 6].

### Deciding what matters

The model can execute. It can write code, run tests, generate charts, and refactor modules efficiently and accurately. What it cannot do well is decide what matters: which problem to solve next, which trade-off to accept, or which output is good enough [7].

One formulation of this is that AI handles most of the work, but the remaining part is the job [9]. That description feels close to what I think is happening and will continue to happen. The cheap parts will get cheaper, but the expensive parts will become even more valuable: judgment, taste, and deciding what to write down clearly enough that someone (or something) else could do it.

### References

1. [METR RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/): 19% slowdown for experienced open-source developers working on their own repositories, measured with early-2025 models.
2. [Tom Johnell](https://tomjohnell.com/llms-can-be-absolutely-exhausting/): On exhaustion doom-loops in agentic workflows.
3. [Dan Lants](https://dlants.me/ai-se.html): AI amplifies good engineering practices; structural investment compounds.
4. [Anthropic, "Building effective agents"](https://www.anthropic.com/research/building-effective-agents): Start simple, add complexity only when needed.
5. [d11r](https://blog.d11r.eu/theory-building/): Theory building and understanding debt.
6. [Joan Westenberg](https://www.joanwestenberg.com/collaboration-is-bullshit/): Individual accountability through documents.
7. [Dynomight](https://dynomight.net/coffee/): Taste and judgment about which factors matter.
8. [METR follow-up](https://metr.org/blog/2026-02-24-uplift-update/): Replication difficulties; developers refused to work without AI.
9. [Martynasm](https://martynasm.com/2026/03/22/white-collar-ai-apocalypse-narrative-is-just-another-bullshit/): Semi-decidable jobs and the 80/20 problem.
