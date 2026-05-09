# Draft Notes

## Working Title

Time-Series Foundation Models Are Exciting. But Are They Really “Foundational”?

## Topic

This article reviews recent work on time-series foundation models, also called TSFMs. The article focuses on the promise of TSFMs, the limits of their generalization, and the evaluation leakage problems that can make benchmark results misleading.

## Main Thesis

Time-series foundation models are promising, but they are not yet proven to be universal. Their performance depends heavily on domain alignment, clean evaluation, and whether benchmark results avoid information leakage.

## Papers Used

1. Foundation Models for Time Series: A Survey
2. How Foundational are Foundation Models for Time Series Forecasting?
3. Rethinking Evaluation in the Era of Time Series Foundation Models: (Un)known Information Leakage Challenges

## Article Structure

### 1. Introduction

Start by explaining how foundation models changed NLP and vision. Then introduce the idea that researchers are now applying the same concept to time-series forecasting.

### 2. Why Time Series Matters

Explain that time-series data appears in finance, healthcare, weather, energy, traffic, retail, and industrial systems.

### 3. Why Time Series Is Different

Explain that time-series data is more fragmented than text. A stock signal, medical signal, weather record, and factory sensor stream are all sequences, but they come from different real-world systems.

### 4. What TSFMs Are

Define time-series foundation models as pretrained models designed to transfer across time-series tasks, datasets, or domains.

### 5. Survey Paper Summary

Use the survey paper to explain the TSFM landscape:
- raw sequence vs patch-based models
- deterministic vs probabilistic forecasting
- univariate vs multivariate forecasting
- different training objectives
- different downstream tasks

### 6. Reality Check

Use the “How Foundational...” paper to explain that TSFM performance often depends on pretraining-domain similarity.

### 7. Evaluation Leakage

Use the leakage paper to explain:
- train-test sample overlap
- temporal overlap of correlated series
- why benchmark results can look better than real-world performance

### 8. Practical Takeaways

Explain that users should:
- compare against strong baselines
- use clean chronological splits
- check for leakage
- consider compute and memory cost
- avoid assuming that “foundation model” automatically means universal

### 9. Conclusion

End with the main takeaway:

Time-series foundation models are exciting and important, but the field still needs careful evaluation before claiming they are truly universal.

## Visual Ideas

1. TSFM taxonomy diagram
2. Promise vs reality comparison
3. Clean temporal split diagram
4. Leakage modes diagram
5. Forecasting experiment pipeline

## Notes for Medium

- Use a strong title.
- Add 3 to 5 visuals.
- Keep paragraphs short.
- Put references at the bottom.
- Mention that the article is based on the reviewed papers.
- Add GitHub repo link at the end.
