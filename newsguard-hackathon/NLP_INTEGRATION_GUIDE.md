# NewsGuard NLP Integration Guide

**Status:** ✅ Complete NLP Implementation  
**Date:** March 20, 2026  
**Version:** 2.0 - Modern NLP Pipeline

---

## Overview

NewsGuard has been upgraded from classical ML (TF-IDF + Logistic Regression) to a comprehensive **modern NLP pipeline** featuring:

1. ✅ **Transformer-based Classification** (DistilBERT/BERT)
2. ✅ **Named Entity Recognition (NER)** (spaCy)
3. ✅ **Sentiment & Bias Analysis** (Transformers)
4. ✅ **Semantic Analysis** (Sentence Transformers)
5. ✅ **Linguistic Analysis** (NLTK, regex patterns)

---

## New NLP Modules

### 1. **NLP Model Loader** (`utils/nlp_model_loader.py`)
- Transformer-based classification core
- Replaces old TF-IDF vectorizer
- Uses DistilBERT for efficiency

**Usage:**
```python
from utils.nlp_model_loader import nlp_model_manager

result = nlp_model_manager.predict(text)
# Returns: {prediction, confidence, provider, ...}
```

### 2. **Named Entity Recognition** (`utils/ner_extractor.py`)
- Extracts people, organizations, locations
- Verifies entity credibility
- Checks claim attribution

**Usage:**
```python
from utils.ner_extractor import ner_extractor

entities = ner_extractor.extract_entities(text)
# Returns: {entities, suspicious_entities, entity_credibility_score, ...}
```

### 3. **Sentiment Analysis** (`utils/sentiment_analyzer.py`)
- Analyzes emotional tone using transformers
- Detects bias and polarization
- Identifies emotional manipulation tactics

**Usage:**
```python
from utils.sentiment_analyzer import sentiment_analyzer

sentiment = sentiment_analyzer.analyze_sentiment(text)
bias = sentiment_analyzer.detect_bias(text)
manipulation = sentiment_analyzer.detect_emotional_manipulation(text)
```

### 4. **Semantic Analysis** (`utils/semantic_analyzer.py`)
- Semantic similarity to known misinformation patterns
- Detects narrative coherence
- Identifies claim sourcing

**Usage:**
```python
from utils.semantic_analyzer import semantic_analyzer

similarity = semantic_analyzer.get_semantic_similarity(text)
coherence = semantic_analyzer.detect_semantic_coherence(text)
sources = semantic_analyzer.find_claim_sources(text)
```

### 5. **Linguistic Analysis** (`utils/linguistic_analyzer.py`)
- Analyzes formality and register consistency
- POS pattern analysis
- Readability metrics
- Hedging language detection

**Usage:**
```python
from utils.linguistic_analyzer import linguistic_analyzer

formality = linguistic_analyzer.analyze_formality(text)
pos = linguistic_analyzer.analyze_pos_patterns(text)
readability = linguistic_analyzer.analyze_readability(text)
hedging = linguistic_analyzer.analyze_hedging_language(text)
```

---

## Installation & Setup

### 1. Update Dependencies
```bash
pip install -r requirements_nlp.txt
```

### 2. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 3. Verify Installation
```bash
python -c "from transformers import pipeline; print('✓ Transformers OK')"
python -c "import spacy; print('✓ spaCy OK')"
python -c "from sentence_transformers import SentenceTransformer; print('✓ Sentence Transformers OK')"
```

---

## New Endpoint Response Format

```json
{
  "fakeNewsAnalysis": {
    "prediction": "fake",
    "confidence": 0.87
  },
  "nlpAnalysis": {
    "sentiment": {
      "overall_sentiment": "negative",
      "emotional_intensity": 0.85,
      "manipulation_score": 0.72,
      "polarization_level": "HIGH"
    },
    "namedEntities": {
      "entities": {
        "PERSON": ["John Smith"],
        "ORG": ["News Corp"],
        "GPE": ["USA"]
      },
      "entity_credibility_score": 0.65
    },
    "semantic": {
      "misinformation_similarity": 0.78,
      "coherence_score": 0.45,
      "is_well_sourced": false
    },
    "linguistic": {
      "formality_score": 0.5,
      "passive_voice_ratio": 0.22,
      "hedging_density": 0.08,
      "flesch_kincaid_grade": 8.5
    }
  }
}
```

---

## Migration from Classical ML

### Old Pipeline
1. Text → Regex cleaning
2. Cleaned text → TF-IDF vectorizer
3. TF-IDF features → Logistic Regression
4. Prediction + keyword matching

### New Pipeline
1. Text → Basic cleaning
2. Cleaned text → Transformers (semantic + syntactic understanding)
3. Text → NER extraction (entity analysis)
4. Text → Sentiment analysis (bias detection)
5. Text → Semantic similarity (pattern matching)
6. Text → Linguistic analysis (structure analysis)
7. **Ensemble of all signals** → Final prediction

---

## Performance Characteristics

| Aspect | Classical ML | Modern NLP |
|--------|------------|-----------|
| **Speed** | ~50ms | ~500ms (due to transformers) |
| **Accuracy** | 99.23% (TF-IDF trained) | TBD (requires fine-tuning) |
| **Understanding** | Keyword patterns | Semantic meaning |
| **Robustness** | Brittle to adversarial text | More robust |
| **Explainability** | High (TF-IDF features) | Moderate (attention) |
| **Language Depth** | Surface patterns | Deep semantic understanding |

---

## Fine-Tuning Instructions

For production, fine-tune the transformer on fake news dataset:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 1. Load fake news dataset
dataset = load_dataset("fake_news_challenge")  # or your custom dataset

# 2. Load model & tokenizer
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# 3. Tokenize dataset
def preprocess(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length')

tokenized = dataset.map(preprocess, batched=True)

# 4. Train
training_args = TrainingArguments("output", num_train_epochs=3, per_device_train_batch_size=16)
trainer = Trainer(model=model, args=training_args, train_dataset=tokenized["train"])
trainer.train()

# 5. Save
model.save_pretrained("path/to/fake_news_model")
tokenizer.save_pretrained("path/to/fake_news_model")
```

---

## Recommended Next Steps

1. **✅ DONE** - Create NLP modules
2. **TODO** - Fine-tune transformer on fake news dataset
3. **TODO** - Update `/api/analyze` endpoint to use all NLP modules
4. **TODO** - Add GPU support for faster inference
5. **TODO** - Create NLP-specific test suite
6. **TODO** - Benchmark performance vs classical ML
7. **TODO** - Update frontend to display NLP-specific insights

---

## Architecture Diagram

```
Input Text
    ↓
[Preprocessing]
    ↓
┌─────────────────────────────────────────┐
│      ┌─ Transformer Classifier          │
│      │  (BERT/DistilBERT)               │
│      │  → prediction, confidence        │
│      │                                  │
│Text  ├─ NER Extractor (spaCy)           │
│      │  → entities, credibility         │
│      │                                  │
│      ├─ Sentiment Analyzer              │
│      │  → sentiment, bias, manipulation │
│      │                                  │
│      ├─ Semantic Analyzer               │
│      │  → similarity, coherence         │
│      │                                  │
│      └─ Linguistic Analyzer              │
│         → formality, POS, readability   │
└─────────────────────────────────────────┘
    ↓
[Ensemble Signal Integration]
    ↓
Combined Credibility Score (0-100)
```

---

## Resources

- **Transformers**: https://huggingface.co/transformers/
- **spaCy**: https://spacy.io/
- **Sentence Transformers**: https://www.sbert.net/
- **NLTK**: https://www.nltk.org/
- **Fake News Datasets**: 
  - LIAR: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
  - FakeNewsNet: https://github.com/KaiDMML/FakeNewsNet
  - Fake News Challenge: https://www.fakenewschallenge.org/

---

**Status:** Ready for integration into `/api/analyze` endpoint  
**Next:** Update routes/analyze.py to call NLP modules  
**Date Created:** March 20, 2026
