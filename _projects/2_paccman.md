---
layout: page
title: Probabilistic circuit model analysis
description: Predicting responses of unobserved neurons in anatomically-constraint networks
img: assets/img/paccman.png
importance: 2
category: machine learning
---

## Abstract

Sensory circuits are complex systems that process information through feedforward and recurrent interactions among a set of neurons. While these circuits have been studied extensively, modeling their underlying mechanisms and computations can be challenging when not all neurons in the circuit are recorded from and when synapse information is incomplete or inaccurate. In this study, we propose a probabilistic framework that predicts the responses of unobserved neurons using anatomical constraints. We demonstrate the effectiveness of our approach on both simulated data using randomly generated connectomes with varying complexities and real neural data from the fruit fly optic lobe. Our approach accurately predicts the responses of unobserved neurons in simulated and real data. Given our probabilistic framework, we are also able to infer what types of experiments are optimal for subsequent experiments. Overall, our method provides a useful tool for modeling the complex mechanisms underlying sensory information processing in biological circuits.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/Results_simulation.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Results for a set of simulated recurrent circuits with 5-9 recurrent units and 4 different types of inputs. Given an appropriate noise level, we are able to accurately predict the responses of up to two unobserved neurons in the circuit without a strong prior on the weight matrix.
</div>

## Presentation

Columbia Neurotheory Meeting (2020 and 2021)

## [WIP] Code