---
layout: page
title: Color vision neuroscience
description: Circuit mechanisms of color processing in Drosophila
img: assets/img/hue.svg
order: 10
category: neuroscience
---

### Hue selectivity from recurrent circuitry

The perception of color involves a transformation from the spectral properties of visual stimuli to derived perceptual quantities such as brightness, saturation and hue.  Although hue selective neurons, which respond to narrow regions in color space, have been reported in primates, they have not been identified in other species including more accessible organisms, which would facilitate circuit level analyses. Here we show that neurons in the *Drosophila* optic lobe have hue selective properties, with narrow tuning for both spectral and non-spectral colors. We construct a connectomics constrained circuit model that accounts for this hue selectivity. Our model, combined with genetic manipulations, shows that recurrent connections in the circuit are critical for the tuning properties of *Drosophila* hue selective neurons. Our findings reveal the circuit basis for a transition from physical detection to sensory perception in color vision.

**Hue selectivity from recurrent circuitry**, *Nature Neuroscience*, 2024

Presented at Columbia Neurotheory Meeting, 2022

### Circuit mechanisms of chromatic encoding

Spectral information is commonly processed in the brain through generation of antagonistic responses to different wavelengths. In many species, these color opponent signals arise as early as photoreceptor terminals. Here, we measure the spectral tuning of photoreceptors in Drosophila. In addition to a previously described pathway comparing wavelengths at each point in space, we find a horizontal-cell-mediated pathway similar to that found in mammals. This pathway enables additional spectral comparisons through lateral inhibition, expanding the range of chromatic encoding in the fly. Together, these two pathways enable efficient decorrelation and dimensionality reduction of photoreceptor signals while retaining maximal chromatic information. A biologically constrained model accounts for our findings and predicts a spatio-chromatic receptive field for fly photoreceptor outputs, with a color opponent center and broadband surround. This dual mechanism combines motifs of both an insect-specific visual circuit and an evolutionarily convergent circuit architecture, endowing flies with the ability to extract chromatic information at distinct spatial resolutions.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/opponency.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

[Circuit Mechanisms Underlying Chromatic Encoding in Drosophila Photoreceptors](https://www.sciencedirect.com/science/article/pii/S0960982219315775?dgcid=api_sd_search-api-endpoint), *Current Biology*, 2020

Presented at Columbia Neurotheory Meeting, 2019

### Normative models of spatio-spectral decorrelation

In line with the efficient coding hypothesis, the early visual system aims to minimize spectral and spatial redundancies arising from overlapping opsin sensitivities in retinal photoreceptors (PRs) and highly correlated structure in natural scenes. Encoding color information, or spectral information independent of intensity, requires comparing activities across different types of PRs. Mounting evidence shows that several species across the animal kingdom, such as the fruit fly *Drosophila Melanogaster*, have an uneven proportion of PR types in their retinas. However, it is unknown whether this uneven proportion is optimized for objectives relevant to the early color processing of natural scenes, as previous studies have modeled spectral and spatial processing in the early fly visual system independently. We built a collection of models incorporating both spatial and spectral information to solve tasks relevant to the fly's early visual system, such as predictive coding at the level of PR inputs for spatial decorrelation in the retina as well as spatial and spectral decorrelation at the level of PR outputs via color opponency mechanisms. Using this framework, we asked how varying the ratio of the fly's two main PR types changed performance accuracy on these tasks. From this normative approach, we were able to conclude that the optimal ratio of PR types to best solve these tasks aligns with the experimentally observed distribution and showed this for multiple opsin sensitivity profiles determined within and across labs. Moreover, shuffling either spatial or spectral information in the input natural scene predicted an even PR type ratio, suggesting that biologically observed PR type ratios are optimized for spectral and spatial decorrelation. Altogether, these results suggest that natural scene statistics may have shaped the ratio of PR types in the fly retina through evolutionary mechanisms, providing important implications for understanding sensory systems in an ecologically relevant context.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/normative.svg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Normative models of spatio-spectral decorrelation predict observed receptor distributions, *CoSyNe*, 2022
