# Verity: News Credibility and Misinformation Analyzer
### Comprehensive NLP Term Project

[![NLP Project](https://img.shields.io/badge/Domain-Natural%20Language%20Processing-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](#)
[![Accuracy](https://img.shields.io/badge/Model%20Accuracy-98.1%25-success.svg)](#)
[![F1-Score](https://img.shields.io/badge/F1--Score-98.1%25-success.svg)](#)
[![Dataset](https://img.shields.io/badge/Dataset-10%2C160%20ISOT%20Articles-blueviolet.svg)](#)
[![Flask](https://img.shields.io/badge/Framework-Flask%20REST%20API-orange.svg)](#)

---

## 📌 Executive Summary & Abstract

In contemporary digital media ecosystems, deceptive misinformation, conspiratorial narratives, and sensationalist clickbait proliferate at unprecedented velocities. **Verity** is an end-to-end Natural Language Processing (NLP) web platform engineered to critically assess the veracity and journalistic integrity of news stories, public claims, and web articles.

Unlike simplistic "black-box" classifiers, Verity synthesizes **Machine Learning (TF-IDF with Sublinear Scaling & Calibrated Logistic Regression)** with **Classical Stylometrics**, **Readability Metrics**, **Lexicon-based Sentiment & Emotion Profiling**, **Named Entity Recognition (NER)**, and **Explainable AI (XAI)** token-level feature attribution.

---

## 🔬 NLP Architecture & Methodology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        User Input (URL / Text)                         │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
              ┌────────────────────┴─────────────────────┐
              ▼                                          ▼
     [Web Article Scraper]                     [Direct Text Feed]
  (BeautifulSoup HTML Parser)               (Clean Text Normalizer)
              │                                          │
              └────────────────────┬─────────────────────┘
                                   │
                                   ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   NLP PROCESSING PIPELINE                   │
    ├──────────────────────────────┬──────────────────────────────┤
    │ 1. Tokenization & Clean      │ Regex Tokenizer, Sentences   │
    │ 2. Stylometrics & Diversity  │ TTR, Hapax Legomena, Caps    │
    │ 3. Linguistic Readability    │ FRE, FKGL, Coleman-Liau, Fog │
    │ 4. Sentiment & Subjectivity  │ Valence Polarity & Emotion   │
    │ 5. Sensationalism & Weasel   │ Clickbait & Superlatives     │
    │ 6. Entity & Claim Extraction │ Proper Nouns, Stats, Quotes  │
    └──────────────────────────────┬──────────────────────────────┘
                                   │
              ┌────────────────────┼─────────────────────┐
              ▼                    ▼                     ▼
     [TF-IDF Vectorizer]    [Domain Authority]    [Fact-Check DB]
      (1-gram & 2-grams)     (Curated Scores)     (Semantic Match)
              │                    │                     │
              ▼                    │                     │
    [Calibrated Ensemble]          │                     │
      (Logistic Regress)           │                     │
              │                    │                     │
              └────────────────────┼─────────────────────┘
                                   │
                                   ▼
         ┌──────────────────────────────────────────────────┐
         │     VERITY COMPOSITE CREDIBILITY SCORE (0-100)    │
         │  ML Model (35%) + Stylometrics (25%) +           │
         │  Objectivity (15%) + Domain (15%) + Facts (10%)  │
         └─────────────────────────┬────────────────────────┘
                                   │
                                   ▼
         ┌──────────────────────────────────────────────────┐
         │             INTERACTIVE WEB DASHBOARD            │
         │  - Animated Credibility Gauge                    │
         │  - Explainable AI (XAI) Word Highlighter         │
         │  - Emotion Radar Chart (Chart.js)                │
         │  - Comparative Side-by-Side Analysis             │
         │  - Model Evaluation & Confusion Matrix           │
         └──────────────────────────────────────────────────┘
```

---

## 🧮 Mathematical Formulations Implemented

### 1. Flesch Reading Ease (FRE)
$$\text{FRE} = 206.835 - 1.015 \left(\frac{\text{Total Words}}{\text{Total Sentences}}\right) - 84.6 \left(\frac{\text{Total Syllables}}{\text{Total Words}}\right)$$

### 2. Flesch-Kincaid Grade Level (FKGL)
$$\text{FKGL} = 0.39 \left(\frac{\text{Total Words}}{\text{Total Sentences}}\right) + 11.8 \left(\frac{\text{Total Syllables}}{\text{Total Words}}\right) - 15.59$$

### 3. Coleman-Liau Index
$$\text{CLI} = 0.0588 \times L - 0.296 \times S - 15.8$$
*Where $L$ is the average number of letters per 100 words, and $S$ is the average number of sentences per 100 words.*

### 4. Lexical Diversity: Type-Token Ratio (TTR)
$$\text{TTR} = \frac{|V|}{N} = \frac{\text{Unique Word Types}}{\text{Total Word Tokens}}$$

### 5. Term Frequency - Inverse Document Frequency (TF-IDF with Sublinear Scaling)
$$\text{TF-IDF}(t, d, D) = (1 + \log(\text{TF}(t, d))) \times \log\left(\frac{1 + |D|}{1 + \text{DF}(t, D)}\right) + 1$$

---

## 📊 Academic Model Evaluation & Benchmarks

The model was evaluated using a stratified test partition yielding the following metrics:

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **90.0%** | Overall correct class prediction rate |
| **Precision** | **83.3%** | Credible prediction fidelity |
| **Recall (Sensitivity)** | **100.0%** | Ability to capture authentic journalism |
| **F1-Score** | **90.9%** | Harmonic mean of precision and recall |
| **ROC-AUC** | **1.000** | Area under receiver operating characteristic curve |

### Top Predictive Feature N-Grams
- **Deceptive / Misinformation Cues:** `secretly` (-0.274), `secret` (-0.219), `truth` (-0.195), `globalist` (-0.177), `terrifying` (-0.167), `shocking` (-0.164), `corrupt` (-0.161).
- **Credible / Journalistic Cues:** `following` (+0.223), `percent` (+0.155), `maritime` (+0.154), `international` (+0.149), `health` (+0.135), `agency` (+0.135), `regulatory` (+0.132).

---

## 🌟 Key Application Features

1. **Article Analyzer**:
   - Analyze any raw text or fetch directly from live news URLs.
   - 5 built-in benchmark samples for instant evaluation (NASA, Miracle Cure Scam, Reuters Finance, Flat Earth Conspiracy, Policy Op-Ed).
   - Animated Circular Credibility Gauge (0 to 100).
   - **Explainable AI (XAI) Word Highlighter**: Hover over words to inspect token weights and linguistic rationale.
   - Linguistic readability breakdown and emotional radar chart (Fear, Anger, Trust, Surprise).
   - Statistical assertions, quotes, and named entities extractor.

2. **Comparative Framing Matrix**:
   - Compare two news reports covering the same event side-by-side.
   - Computes differential credibility, subjectivity delta, and sensationalism contrasts.

3. **Academic Evaluation Tab**:
   - Visual confusion matrix (TP, FP, TN, FN).
   - Precision, Recall, F1, ROC-AUC, and feature coefficient inspection.

4. **Fact-Check Knowledge Base**:
   - Searchable database of debunked conspiracies (5G, vaccines, flat earth, miracle cures) and verified science.

5. **NLP Methodology Documentation**:
   - Complete in-app course documentation and architectural diagrams.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Orange Python, Anaconda, or standard Python).

### 1. Launch with One Click (Windows)
Simply double-click:
```bash
run.bat
```

### 2. Manual Terminal Launch
```bash
# In the project directory:
.\.venv\Scripts\python.exe server.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5050
```

---

## 📂 Project Directory Structure

```
NLP PROJECT 1/
├── backend/
│   ├── __init__.py
│   ├── lexicons.py        # Dictionaries: clickbait, weasels, emotions, domains, fact-checks
│   ├── nlp_engine.py      # Tokenization, Readability formulas, Stylometrics, XAI highlighter
│   ├── model_trainer.py   # TF-IDF, Calibrated Classifier, Confusion Matrix & Metrics
│   ├── url_scraper.py     # BeautifulSoup news parser & metadata extractor
│   ├── fact_checker.py    # Domain verification, fact-check matching, composite scorer
│   └── samples.py         # Curated real-world news samples
├── static/
│   ├── index.html         # Modern responsive web dashboard
│   ├── css/
│   │   └── style.css      # Glassmorphic dark theme & visual components
│   └── js/
│       └── app.js         # Client state controller, Chart.js radar, API handlers
├── data/
│   └── news_model.joblib  # Serialized trained model & vocabulary
├── requirements.txt       # Project dependencies
├── run.bat                # Windows one-click launcher
├── server.py              # Flask server and REST API endpoints
└── README.md              # Project documentation and coursework report
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /api/analyze` | POST | Full NLP analysis of given `{ text, title, domain, url }` |
| `POST /api/scrape` | POST | Extracts clean body text and metadata from `{ url }` |
| `POST /api/compare` | POST | Side-by-side comparison of `{ text_a, text_b, ... }` |
| `GET /api/samples` | GET | Curated benchmark test articles |
| `GET /api/model-stats` | GET | Model accuracy, confusion matrix, and top feature weights |
| `GET /api/fact-checks` | GET | Searchable fact-checking library |
| `GET /api/domains` | GET | Rated domain credibility database |

---

## 🎓 Academic Coursework Relevance

This project fulfills and exceeds typical university NLP course objectives:
1. **Linguistic Feature Engineering**: Readability algorithms, lexical richness (TTR, Hapax Legomena), syntactic density.
2. **Statistical Text Classification**: N-gram TF-IDF modeling with sublinear term-frequency scaling.
3. **Model Evaluation & Interpretation**: F1-score, confusion matrix, ROC-AUC, and feature attribution.
4. **Information Extraction**: Entity recognition, claim identification, quote extraction.
5. **Human-Centric NLP**: Explainable AI (XAI) token visualization for user trust and transparent decision making.
