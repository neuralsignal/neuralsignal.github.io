---
layout: page
title: AI for medical data
description: Time-series models for wearable biometrics, electronic health records, and clinical decision support
img:
order: 30
category: machine learning
---

Medical decisions rely on data from different sources: wearable sensors, electronic health records, and bedside monitors. Each comes with its own challenges around sequence length, irregular sampling, and individual variability. Across these projects, we are building models that learn temporal patterns from each modality, with the longer-term goal of combining them into unified patient representations.

### Biometric time-series models

Conditions like infections, pneumonia, and constipation show up as multi-day patterns in wearable data, but most ML models struggle with sequences that long. At Mountain Biometrics, we worked on deep state-space model architectures that scale linearly with sequence length, learning individual "biometric profiles" to detect these healthcare events from wearable devices. The goal was to make this kind of monitoring accessible in underserved communities where it currently does not exist.

### EHR foundation models

Electronic health records pose a similar challenge at a different scale: the sequences are longer, irregularly sampled, and mix different data types. We are working on a transformer-based foundation model with Mixture-of-Experts routing, trained on ~298M timeline positions from MIMIC-IV. The tokenization follows previous EHR encoding approaches: patient demographics, quantized lab values, time interval tokens, and medical event codes get mapped into a unified sequence.

### Field casualty management AI

Prolonged field care combines both problems: medics need to interpret wearable biometrics over hours to days, in conditions where EHR-style clinical context is unavailable. At Mountain Biometrics, we built models for predicting individual progression of blood loss and likelihood of sepsis from heart rate, blood oxygen, and other wearable signals, designed to integrate into existing military hardware and software.

Field casualty management AI, W.W. Pettine, M. Christenson, P. Koirala, *Defense TechConnect*, 2023 \
Assessing Foundation Models' Transferability to Physiological Signals in Precision Medicine, M. Christenson, C. Geary, B. Locke, P. Koirala, W.W. Pettine, *Defense AI in Medicine*, 2024
Efficient EHR Foundational Models: A Mixture-of-Experts Approach for Patient Timeline Prediction, Athreya, M. Christenson, W.W. Pettine, *AI Summit, University of Utah*, 2025
