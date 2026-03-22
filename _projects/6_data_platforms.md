---
layout: page
title: Research data platforms
description: Python packages for lab data management and dataframe manipulation
img: assets/img/loris_icon.jpg
order: 60
category: data tools
---

### Loris

I built Loris as a database system for the Behnia lab at Columbia. The lab used it daily for data entry, maintenance, and analysis. It was designed for a Drosophila lab but flexible enough for other research labs. The lab has since moved to a different tech stack, so this project is no longer maintained.

[neuralsignal/loris](https://github.com/neuralsignal/loris)

### Puffbird

A pandas extension for handling DataFrames with complex nested cells. I built it because I kept running into multi-valued columns that were painful to work with. Some features have become redundant since pandas added `explode` and similar methods, but the library still fills gaps for certain workflows. Maintained at an irregular rate.

[neuralsignal/puffbird](https://github.com/neuralsignal/puffbird)
