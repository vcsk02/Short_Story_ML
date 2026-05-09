# Paper Notes: How Foundational are Foundation Models for Time Series Forecasting?

## Paper

**Title:** How Foundational are Foundation Models for Time Series Forecasting?  
**arXiv:** 2510.00742  
**Role in my project:** This is the main critical paper that questions whether TSFMs are truly foundational.

## Why this paper matters

This paper is important because it challenges the assumption that large pretrained time-series models automatically generalize across all domains.

It asks whether these models are truly foundational or whether their performance depends heavily on the type of data they were pretrained on.

## Main argument

The main argument is that time-series foundation models may not transfer as broadly as foundation models in language or vision.

The paper argues that zero-shot performance is strongly connected to pretraining-domain alignment. In simple terms, if the target dataset looks similar to the data used during pretraining, the model is more likely to perform well.

## Important concepts

### 1. Domain alignment

Domain alignment means the downstream dataset is similar to the pretraining data.

For example, a model pretrained on many energy demand datasets may perform well on another energy forecasting task. But it may not transfer as well to a very different domain, such as medical sensor data.

### 2. Zero-shot forecasting

Zero-shot forecasting means using the pretrained model on a new forecasting task without task-specific training.

The paper suggests that zero-shot performance should be interpreted carefully because good results may depend on whether the model has already seen similar patterns before.

### 3. Model size vs practical value

Large models may require more memory and compute. If a smaller specialized model performs similarly, the larger model may not be worth the extra cost.

## What I learned from this paper

The biggest lesson is that the word "foundation" should be used carefully.

A model can be pretrained and powerful without being universally general. For time series, transfer is often conditional on the relationship between pretraining data and downstream data.

## How I used this paper in my article

I used this paper to support the "reality check" section of my article.

The article argues that TSFMs are promising but not yet proven universal. This paper provides the main evidence for that argument.

## Key takeaway

Time-series foundation models can be useful, but their success depends heavily on domain similarity. Strong performance on one benchmark does not automatically prove broad generalization.
