# Paper Notes: Rethinking Evaluation in the Era of Time Series Foundation Models

## Paper

**Title:** Rethinking Evaluation in the Era of Time Series Foundation Models: (Un)known Information Leakage Challenges  
**arXiv:** 2510.13654  
**Role in my project:** This paper supports the evaluation and benchmark integrity part of my short story.

## Why this paper matters

This paper is important because it focuses on how time-series foundation models are evaluated.

As foundation models are pretrained on larger datasets, it becomes harder to know whether evaluation datasets are truly unseen. This creates a risk of information leakage.

## Main argument

The paper argues that TSFM evaluation can be misleading if there is overlap between pretraining data and test data, or if train and test series are temporally correlated.

This means a model may appear to generalize well even though the benchmark is not fully clean.

## Important concepts

### 1. Information leakage

Information leakage happens when the model has access to information during training or pretraining that it should not have during evaluation.

This can make performance look better than it really is.

### 2. Train-test sample overlap

This happens when the same or nearly identical samples appear in both the model's pretraining data and the test benchmark.

### 3. Temporal overlap of correlated series

This is more subtle. Even if the exact same samples are not repeated, different time series may be correlated because they come from the same time period, same event, or same system.

For example, two electricity demand datasets from the same region and time period may share patterns.

### 4. Clean temporal split

A clean time-series evaluation should respect chronology. Training data should come before validation data, and validation data should come before test data.

Random shuffling can create unrealistic evaluation conditions.

## What I learned from this paper

The biggest lesson is that evaluation design is not just a small detail. In time-series forecasting, evaluation design can completely change how we interpret model performance.

A benchmark result is only meaningful if the test data is truly unseen and leakage risks are controlled.

## How I used this paper in my article

I used this paper to support the section about benchmark leakage.

It helped me explain why TSFM results should be evaluated carefully and why strong benchmark numbers do not always prove true generalization.

## Key takeaway

Time-series foundation models should be evaluated with leakage-aware protocols. Without clean evaluation, benchmark results may overstate how well the model actually generalizes.
