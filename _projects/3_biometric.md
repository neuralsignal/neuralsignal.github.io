---
layout: page
title: AI for biophysical data
description: Building models to make long-term predictions on biophysical time-series data
img:
order: 30
category: machine learning
---

### Biometric time-series models for healthcare monitoring

Conditions like infections, pneumonia, and constipation show up as multi-day patterns in wearable data — but most ML models struggle with sequences that long. At Mountain Biometrics, I worked on deep state-space model architectures that scale linearly with sequence length, learning individual "biometric profiles" to detect these healthcare events from wearable devices. The goal was to make this kind of monitoring accessible in underserved communities where it currently does not exist.

### Field Casualty Management AI

In prolonged field care, medics may need to manage wounded warfighters for days to weeks without evacuation. Rationing blood or antibiotics requires predicting individual progression of blood loss or likelihood of sepsis — patterns that emerge over hours to days in heart rate, blood oxygen, and other wearable biometrics. At Mountain Biometrics, we built models for interpreting these individual-specific, long-timescale biophysical signals, designed to integrate into existing military hardware and software.

Field casualty management AI, W.W. Pettine, M. Christenson, P. Koirala, *Defense TechConnect*, 2023 \
Assessing Foundation Models' Transferability to Physiological Signals in Precision Medicine, M. Christenson, C. Geary, B. Locke, P. Koirala, W.W. Pettine, *Defense AI in Medicine*, 2024
