# Time-Series Foundation Models: Promise, Limits, and Better Evaluation

This repository contains my **individual short story assignment** for **CMPE 258**.  
The project reviews recent work on **time-series foundation models (TSFMs)**, summarizes the literature in my own words, reproduces a small experimental setup using an AutoResearch-style workflow, and packages all deliverables in one public GitHub directory.

## Project Summary

Large language models and foundation models have expanded far beyond text. One of the most interesting newer directions is the rise of **foundation models for time series**, where a single pretrained model is used across forecasting tasks, datasets, and domains.

This project focuses on the following central question:

> **How foundational are time-series foundation models in practice?**

The short story explores:
- what TSFMs are,
- why they matter,
- how recent survey and evaluation papers categorize them,
- where they perform well,
- where they fail,
- and why **careful evaluation and leakage-aware benchmarking** matter.

In addition to the literature review, this repository includes a small reproduction / comparison study using an **AutoResearch-inspired experimental structure**.

---

## Main Papers Reviewed

### Primary survey/background paper
- **Foundation Models for Time Series: A Survey**  
  arXiv: 2504.04011  
  https://arxiv.org/abs/2504.04011

### Supporting analysis papers
- **How Foundational are Foundation Models for Time Series Forecasting?**  
  arXiv: 2510.00742  
  https://arxiv.org/abs/2510.00742

- **Rethinking Evaluation in the Era of Time Series Foundation Models: (Un)known Information Leakage Challenges**  
  arXiv: 2510.13654  
  https://arxiv.org/abs/2510.13654

These papers together provide a strong story:
1. the survey explains the landscape,
2. the second paper questions how general TSFMs really are,
3. the third paper highlights evaluation pitfalls and information leakage.

---

## What This Repository Includes

This repository contains all required assignment deliverables:

- **Medium article**
- **Slide deck**
- **YouTube presentation video**
- **Paper review notes**
- **Experimental reproduction / comparison**
- **Figures and visualizations**
- **README with full project structure**
- **Links to all external deliverables**

---

## Deliverables

### 1. Medium Article
A rewritten, original long-form article based on the reviewed papers, with additional interpretation, diagrams, comparisons, and takeaways.

**Medium link:**  
https://medium.com/@vineeth.kandukuri/time-series-foundation-models-are-exciting-but-are-they-really-foundational-fdef06217325

### 2. Slide Deck
A presentation summarizing the short story, architecture ideas, benchmarks, ablation-style observations, and final conclusions.

**Slideshare link:**  
`https://docs.google.com/presentation/d/1EmTSOv2pqnBvulBXbX3nIMhqmxGXJlyg/edit?usp=sharing&ouid=114838902492320327270&rtpof=true&sd=true`

**PDF / PPT in repo:**  
`slides/`

### 3. Video Presentation
A 15–25 minute recorded explanation of the short story and slide deck.

**YouTube link:**  
`https://youtu.be/J6dIXRf9Z4o`

### 4. Experimental Reproduction
A small reproduction / benchmarking setup inspired by the AutoResearch template, comparing forecasting baselines and foundation-model-style approaches under clean evaluation settings.

**Code and outputs:**  
`autoresearch/` and `results/`

### 5. Spreadsheet Link
A spreadsheet containing experiment tracking, summaries, or submission-related references.

**Spreadsheet link:**  
`<ADD_SPREADSHEET_LINK_HERE>`

---

## Repository Structure

```text
.
├── README.md
├── article/
│   ├── medium_article.md
│   ├── draft_notes.md
│   └── references.md
├── slides/
│   ├── short_story_slides.pdf
│   └── short_story_slides.pptx
├── video/
│   └── video_link.md
├── paper_notes/
│   ├── survey_notes.md
│   ├── foundationality_notes.md
│   └── evaluation_leakage_notes.md
├── autoresearch/
│   ├── notebooks/
│   ├── scripts/
│   ├── configs/
│   ├── datasets/
│   └── outputs/
├── results/
│   ├── tables/
│   ├── charts/
│   └── summary.md
├── figures/
│   ├── architecture/
│   ├── benchmarks/
│   └── custom_visuals/
└── references/
    └── bibliography.bib
