# NewsGuard Fake News Detection System - Comprehensive Analysis

## 1. ML Models for Fake News Detection

### Available Models

The system uses **4 distinct ML models** that can be selected or combined:

| Model | Location | Accuracy | Type | Training Data |
|-------|----------|----------|------|---------------|
| **Kaggle Base** | [backend/models/](backend/models/) | 99.23% | LogisticRegression | Kaggle fake news dataset (~8,837 test samples) |
| **LIAR Model** | [backend/models/liar/](backend/models/liar/) | 62.02% | LogisticRegression | LIAR Dataset (2,559 test samples) |
| **Multi Source** | [backend/models/multi/](backend/models/multi/) | 88.80% | Mixed | Kaggle + LIAR (~45,036 training samples) |
| **Multi Best** | [backend/models/multi_best/](backend/models/multi_best/) | 89.09% | Mixed | Kaggle + FakeNewsNet (~9,078 test samples) |
| **Hybrid (Ensemble)** | [backend/utils/model_loader.py](backend/utils/model_loader.py#L160) | N/A | Weighted Ensemble | Combines Kaggle + LIAR with weighted voting |

### Model Architecture

**Algorithm**: Linear classifiers (LogisticRegression with L2 regularization, max_iter=200-250)

**File Locations**:
- Model training logic: [backend/scripts/train_model.py](backend/scripts/train_model.py)
- Multi-source training: [backend/scripts/train_multisource.py](backend/scripts/train_multisource.py)
- Model loading & prediction: [backend/utils/model_loader.py](backend/utils/model_loader.py)
- Lightweight prediction script: [backend/scripts/predict.py](backend/scripts/predict.py)

**Model Storage Format**: 
- Serialized via pickle (.pkl files)
- Each model has: `fake_news_model.pkl` (classifier) + `tfidf_vectorizer.pkl` (feature transformer)

### Confidence Calculation

The system extracts confidence from model decision boundaries:

```python
# From model_loader.py - _confidence_from_model()
- If model has decision_function: Uses sigmoid of margin
  confidence = 0.5 + (1.0 / (1.0 + exp(-margin)) - 0.5)
- If model has predict_proba: Uses max probability
  confidence = max(probabilities)
- Default fallback: 0.65
- Range: Clamped to [0.0, 1.0]
```

**Confidence Threshold**: 0.65 (configurable via `CONFIDENCE_THRESHOLD` env var, [backend/.env.example](backend/.env.example))

### Training Reports

**Kaggle Model Performance:**
```
Accuracy: 99.23%
Precision (FAKE): 0.99 | Recall: 0.99
Precision (REAL): 0.99 | Recall: 0.99
Confusion Matrix:
  True Negatives: 4515 | False Positives: 39
  False Negatives: 29 | True Positives: 4254
```
Source: [backend/models/training_report.txt](backend/models/training_report.txt)

**LIAR Model Performance:**
```
Accuracy: 62.02% (lower - uses more nuanced labels)
Precision (FAKE): 0.60 | Recall: 0.44
Precision (REAL): 0.63 | Recall: 0.76
```
Source: [backend/models/liar/training_report.txt](backend/models/liar/training_report.txt)

**Multi-Best Model Performance:**
```
Accuracy: 89.09%
F1-Score: 0.89 (both classes)
Trained on: 45,331 samples (Kaggle + FakeNewsNet + LIAR)
```
Source: [backend/models/multi_best/training_report.txt](backend/models/multi_best/training_report.txt)

---

## 2. Feature Extraction & Preprocessing Pipeline

### Text Preprocessing

**File**: [backend/utils/text_processor.py](backend/utils/text_processor.py)

**Pipeline Steps** (in order):
```python
def clean_text(text: str) -> str:
    1. Lowercase conversion
    2. URL removal (http://, www., https://)
    3. Email removal (user@domain.x)
    4. Special character removal (keep only alphanumeric + spaces + dots)
    5. Whitespace normalization (collapse multiple spaces, strip edges)
    
Returns: Cleaned, normalized text ready for vectorization
```

**Example Transformation**:
```
Input: "Breaking! Dr. Smith reveals SHOCKING truth at https://example.com #conspiracy"
Output: "breaking dr smith reveals shocking truth at conspiracy"
```

### TF-IDF Vectorization

**Configuration** (from [backend/scripts/train_model.py](backend/scripts/train_model.py#L139)):
```python
TfidfVectorizer(
    max_features=5000,        # Top 5000 most important features
    stop_words="english",      # Removes common words (the, a, is, etc.)
    ngram_range=(1, 2),       # Unigrams + Bigrams (single words + word pairs)
    min_df=2,                 # Feature must appear in ≥2 documents
    max_df=0.8                # Feature can appear in ≤80% of documents
)
```

**Feature Matrix Output**:
- Kaggle model: ~8,837 samples → 5,000 features each
- Sparse matrix (only non-zero values stored)
- Each feature is a TF-IDF weight (term frequency × inverse document frequency)

### Feature Importance Notes

**High-value features detected by models:**
- Sensational/clickbait language
- Specific conspiracy theory keywords
- Formal language vs. informal tone
- Source attribution patterns
- Hedge language (allegedly, reportedly, etc.)

---

## 3. Scoring & Credibility System

### Credibility Score Calculation

**File**: [backend/utils/scorer.py](backend/utils/scorer.py)

**Output Range**: 0-100 (higher = more credible)

**Score Composition**:
```
Total Score = Model Score + Keyword Score + Length Score + Hedge Score - Penalties
              (0-15)        (0-25)          (0-15)        (0-10)
```

#### 3a. Model Score (0-15 points)

**For FAKE predictions:**
```python
Base = max(0, int((1 - confidence) * 15))  # Lower confidence → higher points
Example: confidence=0.3 → base = 10 points
```

**For REAL predictions:**
```python
Base = int(confidence * 50) capped at 15  # Confidence already weighted differently
```

**Conspiracy/Satire Aggressive Penalty:**
```python
if model_prediction == "fake" and conspiracy_keywords >= 4:
    penalty = -conspiracy_count * 8 (very aggressive)
elif conspiracy_keywords >= 2:
    penalty = -conspiracy_count * 5 (less aggressive)

Conspiracy Keywords (23 tracked):
- "government surveillance", "drones", "foia documents"
- "conspiracy theorists", "shocking documents", "revealed"
- "cover-up", "hidden truth", "classified", "visibly sweating"
- "sources say", "breakthrough discovery", "miracle cure"
- "doctors hate", "authorities hide", "emergency"
- "847-page document", "department of homeland", "feathers"
```

#### 3b. Keyword Score (0-25 points)

```python
sensational_count = count of flagged sensational words in text
keyword_points = max(0, 25 - min(sensational_count, 10) * 2)

Example:
- 0 sensational words → 25 points ✓
- 5 sensational words → 15 points
- 10+ sensational words → 5 points ✗
```

**Flagged Keywords** ([backend/data/keywords.json](backend/data/keywords.json)):
```json
{
  "sensational_words": [
    "shocking", "unbelievable", "breaking", "urgent", "bombshell",
    "exposed", "revealed", "exclusive", "must see"
  ],
  "hedge_words": [
    "allegedly", "reportedly", "sources say", "rumored",
    "claims", "suggests", "appears to be"
  ],
  "clickbait_phrases": [
    "what happened next", "number 7 will shock you",
    "doctors hate this", "this one trick"
  ]
}
```

#### 3c. Length Score (0-15 points)

```python
if word_count >= 100:
    length_points = 15 (full points for substantial content)
else:
    length_points = (word_count / 100) * 15 (pro-rata)

Rationale: Longer articles allow more nuanced expression
```

#### 3d. Hedge Score (0-10 points)

```python
hedge_count = count of hedge-related keywords
hedge_penalty = min(10, hedge_count * 2)
hedge_points = max(0, 10 - hedge_penalty)

Example:
- 0 hedge words → 10 points
- 3 hedge words → 4 points
- 5+ hedge words → 0 points
```

### Final Score Adjustment

```python
# Aggressive conspiracy penalty for FAKE predictions
if model_prediction == "fake" and conspiracy_count >= 2:
    conspiracy_penalty = min(total - 10, conspiracy_count * 12)
    total = max(10, total - conspiracy_penalty)

# Final clamp
total = max(0, min(total, 100))
```

### Credibility Tiers (from [frontend/src/components/ResultCard.jsx](frontend/src/components/ResultCard.jsx))

| Score Range | Label | Badge | Guidance |
|-------------|-------|-------|----------|
| 80-100 | **High Credibility** | 🟢 Trusted Source | Strong alignment with verified sources |
| 60-79 | **Moderate Credibility** | 🟡 Caution Advised | Some concerns detected; verify independently |
| 0-59 | **Low Credibility** | 🔴 Unverified | High probability of misinformation |

---

## 4. Analyze Endpoint Flow

**File**: [backend/routes/analyze.py](backend/routes/analyze.py)

### Request Structure
```python
POST /api/analyze
{
    "text": string,           # Article text (80-30,000 chars required, 12+ words)
    "mode": string,           # "hybrid" | "kaggle" | "liar" | "multi" | "multi_best"
    "url": string,            # Optional: for URL credibility check
    "check_url": boolean      # Optional: Enable URL verification
}
```

### Response Structure
```python
{
    "fakeNewsAnalysis": {
        "prediction": "fake"|"real"|"needs_verification",
        "confidence": float (0-1),
        "credibilityScore": int (0-100),
        "breakdown": {
            "modelScore": int,
            "keywordScore": int,
            "lengthScore": int,
            "hedgeScore": int,
            "wordCount": int
        },
        "flaggedKeywords": list[string],
        "provider": string,      # "kaggle-model", "hybrid-ensemble", etc.
        "mode": string,          # Selected analysis mode
        "ensemble": dict         # Only for hybrid mode
    },
    "urlAnalysis": dict         # Optional: Only if check_url=true
}
```

### Analysis Flow (Step-by-Step)

```
1. VALIDATION
   ├─ Check text is provided and non-empty
   ├─ Verify length: 80-30,000 characters
   └─ Verify word count: minimum 12 words

2. TEXT PREPROCESSING
   └─ clean_text() → remove URLs, emails, special chars, normalize whitespace

3. MODEL SELECTION & PREDICTION
   ├─ If mode=="hybrid": Ensemble voting (Kaggle + LIAR)
   │  └─ _predict_hybrid() → combine predictions with weighted confidence
   └─ Otherwise: Single model prediction
      └─ _predict_single(mode) → 
         ├─ Vectorize with TF-IDF
         ├─ Get raw model prediction
         ├─ Extract confidence via decision_function or predict_proba
         ├─ KEYWORD ENHANCEMENT:
         │  ├─ Check for ≥3 obvious fake indicators → Force "fake" label
         │  ├─ For borderline cases (confidence 0.5-0.7):
         │  │  └─ Count fake-indicating keywords vs real-indicating keywords
         │  │  └─ Adjust prediction + confidence accordingly
         │  └─ For low-confidence results: Return "needs_verification"
         └─ Return {prediction, confidence, provider}

4. KEYWORD EXTRACTION & SCORING
   ├─ extract_flagged_keywords() → scan text for keywords.json matches
   ├─ calculate_credibility_score():
   │  ├─ Model score (0-15 points)
   │  ├─ Keyword score (0-25 points)
   │  ├─ Length score (0-15 points)
   │  ├─ Hedge score (0-10 points)
   │  └─ Apply conspiracy penalties if applicable

5. URL CREDIBILITY CHECK (Optional)
   ├─ If check_url=true:
   │  └─ verify_url_credibility():
   │     ├─ Extract domain from URL
   │     ├─ Check against known_safe list
   │     ├─ Check against known_fake list
   │     └─ Return {is_credible, risk_level, explanation, domain}
   └─ Otherwise: Skip

6. RESPONSE ASSEMBLY & RETURN
   └─ Return JSON with fakeNewsAnalysis ± urlAnalysis
```

### Error Handling

| Condition | HTTP Status | Message |
|-----------|------------|---------|
| No text provided | 400 | "No text provided" |
| Text too short | 400 | "Insufficient context. Please provide a longer article..." |
| Text too long | 400 | "Text is too long. Keep input under 30,000 characters." |
| Model files missing | 503 | RuntimeError: "Model artifacts are missing" |
| Invalid mode | 400 | RuntimeError: "Invalid mode" |

---

## 5. Keyword & Pattern Detection

### Pattern Detection Mechanisms

#### 5a. Obvious Fake News Detection (from [backend/utils/model_loader.py](backend/utils/model_loader.py#L146))

**23 obvious fake indicators**:
```python
[
    'foia documents reveal',          # Government access framing
    'government hiding',               # Conspiracy framing
    'shocking documents',              # Sensationalism
    'conspiracy theorists claimed',    # Conspiracy language
    'classified documents',            # Authority appeal
    'cover-up',                        # Conspiracy framing
    'emergency hearings',              # Urgency manipulation
    'could not be reached for comment', # False legitimacy
    'visibly sweating',                # Made-up details
    'department of',                   # Authority appeal
    '847-page document',               # Specific false detail
    'could not be contacted',          # False legitimacy
    'conspiracy' + 'drones',           # Conspiracy combo
    'miracles',                        # Pseudoscience
    'guaranteed cure',                 # Medical misinformation
    'doctors hate this'                # Anti-expert sentiment
]

Rule: If ≥3 indicators detected → Automatically classify as "FAKE"
      confidence boosted to min(0.95, max(0.75, confidence + 0.20))
```

#### 5b. Borderline Case Enhancement

**For model confidence between 0.5-0.7:**

**Fake-indicating keywords**:
```python
[
    'shocking', 'scientists announce', 'doctors hate',
    'secret discovered', 'miracle cure', '100% effective',
    'government hiding', 'proven', 'guaranteed', 'sources say',
    'allegedly', 'experts claim', 'leaked', 'revealed',
    'conspiracy', 'foia', 'classified'
]
```

**Real-indicating keywords**:
```python
[
    'according to', 'sources familiar', 'report', 'announced',
    'officials say', 'researchers found', 'study shows', 'review',
    'peer-reviewed', 'journal finds', 'data shows', 'analysis',
    'statement said', 'confirmed'
]
```

**Logic**:
```python
if fake_count > real_count and fake_count > 1:
    prediction = "fake"
    confidence += fake_count * 0.08
elif real_count > fake_count and real_count > 1:
    prediction = "real" 
    confidence += real_count * 0.08
```

#### 5c. Conspiracy Keyword Penalty

**24 conspiracy/satire keywords** that trigger score penalties:

```python
conspiracy_keywords = [
    'government surveillance', 'drones', 'foia documents',
    'conspiracy theorists', 'shocking documents', 'revealed',
    'cover-up', 'hidden truth', 'classified', 'visibly sweating',
    'sources say', 'breakthrough discovery', 'miracle cure',
    'doctors hate', 'authorities hide', 'emergency',
    'could not be reached for comment', '847-page document',
    'department of homeland', 'feathers', 'tin foil hat'
]

Penalty Application:
- ≥4 keywords: max(5, modelScore - (count * 8))
- 2-3 keywords: max(10, modelScore - (count * 5))
```

### URL Domain Detection

**File**: [backend/utils/groq_analyzer.py](backend/utils/groq_analyzer.py)

**Known Safe Domains** (38 domains):
```python
# Major international news
'reuters.com', 'bbc.com', 'bbc.co.uk', 'apnews.com', 'ap.org',
'nytimes.com', 'washingtonpost.com', 'theguardian.com', 'ft.com',
'aljazeera.com', 'npr.org', 'pbs.org'

# Indian news (added for regional coverage)
'timesofindia.indiatimes.com', 'hindustantimes.com', 'indianexpress.com',
'thehindu.com', 'deccanherald.com', 'ndtv.com', 'scroll.in', 'livemint.com'

# Others
'dw.com', 'france24.com', 'euronews.com', 'scmp.com', 'dawn.com'
```

**Known Fake Domains** (11 domains):
```python
'abcnews.com.co', 'cnn.co', 'foxnews.com.br', 'bbc.co.uk.org',
'nytimes.com.ru', 'theonion.com', 'infowars.com', 'beforeitsnews.com',
'naturalnews.com', 'wnd.com', 'patrickfrancis.blogspot.com'
```

**Risk Levels**:
- **Safe**: Domain in known_safe list
- **Dangerous**: Domain in known_fake list  
- **Suspicious**: Unknown domain (default conservative approach)

---

## 6. Performance Metrics & Known Limitations

### Model Performance Summary

| Metric | Kaggle | LIAR | Multi | Multi-Best |
|--------|--------|------|-------|-----------|
| Accuracy | **99.23%** ⭐ | 62.02% | 88.80% | 89.09% |
| Precision (FAKE) | 0.99 | 0.60 | 0.88 | 0.89 |
| Recall (FAKE) | 0.99 | 0.44 | 0.89 | 0.89 |
| Precision (REAL) | 0.99 | 0.63 | 0.89 | 0.89 |
| Recall (REAL) | 0.99 | 0.76 | 0.88 | 0.90 |
| F1-Score | ~0.99 | 0.60 | 0.89 | 0.89 |

**Files**:
- [backend/models/training_report.txt](backend/models/training_report.txt) (Kaggle)
- [backend/models/liar/training_report.txt](backend/models/liar/training_report.txt) (LIAR)
- [backend/models/multi_best/training_report.txt](backend/models/multi_best/training_report.txt) (Multi-Best)
- [backend/models/multi/training_report.txt](backend/models/multi/training_report.txt) (Multi)

### Known Limitations

#### 1. **Model Imbalance**
- Kaggle model significantly outperforms LIAR (99% vs 62%)
- LIAR's lower performance due to more nuanced claim-based labels
- Hybrid mode balances but may reduce precision if both needed

#### 2. **Generalization Gap**
- Models trained on dataset-specific patterns
- Kaggle dataset ≠ LIAR dataset ≠ Real-world news
- New slang, references, or domains may misclassify

#### 3. **Keyword Rule Brittleness**
- "847-page document" rule too specific - easy to evade
- Conspiracy keywords can appear in legitimate fact-checking content
- No context awareness (false positives on debunking articles)

#### 4. **Short Text Limitation**
- Requires ≥12 words and 80 characters minimum
- TF-IDF vectorizer struggles with very short texts
- No semantic understanding (only statistical patterns)

#### 5. **Confidence Calibration Issues**
- Confidence scores may not reflect true probability
- Model decision margins don't linearly map to actual accuracy
- Low confidence doesn't always mean low reliability

#### 6. **Feature Set Limitations**
- Only text features used (no image, video, source reputation)
- No temporal awareness (news cycles, evolving stories)
- No user/social signal integration
- Limited to English (trained data is English)

#### 7. **URL Verification Gaps**
- Limited to domain-level checks (no content verification)
- Known-safe/known-fake lists maintained manually
- Many reliable regional sources not in whitelist

#### 8. **No Real-time Fact-Checking**
- ML models capture training data patterns only
- Cannot verify current events or breaking news
- No integration with external fact-checking APIs

#### 9. **Adversarial Vulnerability**
- Simple keyword variations can bypass detection
- Paraphrasing can change prediction
- No robustness testing documented

---

## 7. Validation & Confidence Measures

### Confidence Extraction

**File**: [backend/utils/model_loader.py](backend/utils/model_loader.py#L51)

```python
def _confidence_from_model(model, transformed):
    confidence = 0.65  # Default fallback
    
    if hasattr(model, "decision_function"):
        # SVM-style: Use margin magnitude with sigmoid scaling
        margin = abs(model.decision_function(transformed)[0])
        confidence = 0.5 + (1.0 / (1.0 + exp(-margin)) - 0.5)
    elif hasattr(model, "predict_proba"):
        # Probabilistic: Use max class probability
        probs = model.predict_proba(transformed)[0]
        confidence = max(probs)
    
    return max(0.0, min(confidence, 1.0))  # Clamp to [0, 1]
```

### Validation Measures

#### 1. **Confidence Threshold** (0.65 default)

**File**: [backend/.env.example](backend/.env.example)

```
CONFIDENCE_THRESHOLD=0.65
```

**Applied in**:
- Low-confidence predictions → classified as "needs_verification"
- Used in hybrid ensemble weighting

#### 2. **"Needs Verification" State**

**Triggers** (from [backend/utils/model_loader.py](backend/utils/model_loader.py#L204)):
```python
if both_models_abstain or avg_confidence < 0.65:
    return {"prediction": "needs_verification", ...}

# Also for single models:
if confidence < threshold:
    prediction = "needs_verification"
```

**UI Display** ([frontend/src/components/ResultCard.jsx](frontend/src/components/ResultCard.jsx)):
```
Shows warning: "Needs Verification"
Advice: "Check multiple fact-checking sources / Verify with primary sources"
Displays model confidence + provider + mode
```

#### 3. **Ensemble Agreement Strength**

**Hybrid mode**:
```python
# Agreement confidence is average of both models for same prediction
if kaggle_pred == liar_pred and kaggle_pred != "needs_verification":
    confidence = (kaggle_confidence + liar_confidence) / 2
# Disagreement confidence uses weighted voting
else:
    confidence = max(fake_weight, real_weight) / total
```

### Manual Validation Approaches

**Recommended user verification**:
1. Check multiple independent sources
2. Verify claims against primary sources
3. Look for corroborating evidence
4. Check publication date and author
5. Search for fact-checker consensus

---

## 8. Training Data

### Primary Data Sources

#### 1. **Kaggle Fake News Dataset** ⭐ (Primary)
- **Files**: [archive/Fake.csv](archive/Fake.csv), [archive/True.csv](archive/True.csv)
- **Size**: ~30,000+ samples total
- **Split**: 20% test/80% train
- **Composition**: News articles with text column
- **Model Accuracy**: 99.23%
- **Note**: Large files (>50MB each)

#### 2. **LIAR Dataset** (Multi-label claim fact-checking)
- **Source**: Published research dataset for claim credibility
- **Location**: [liar_dataset-master/](liar_dataset-master/)
- **Files**:
  - [liar_dataset-master/train.tsv](liar_dataset-master/liar_dataset-master/train.tsv)
  - [liar_dataset-master/valid.tsv](liar_dataset-master/liar_dataset-master/valid.tsv)
  - [liar_dataset-master/test.tsv](liar_dataset-master/liar_dataset-master/test.tsv)
- **Labels**: 6-way (true, mostly-true, half-true, barely-true, false, pants-on-fire)
- **Columns**: ID, label, statement, subjects, speaker, job_title, state, party, counts
- **Binary Mapping** (in training):
  - REAL: true, mostly-true, (half-true or custom)
  - FAKE: false, barely-true, pants-on-fire
- **Model Accuracy**: 62.02%
- **Samples**: ~2,559 test samples, 45,000+ total

#### 3. **FakeNewsNet Dataset** (Social media fake news)
- **Location**: [FakeNewsNet-master/FakeNewsNet-master/](FakeNewsNet-master/FakeNewsNet-master/)
- **Files**:
  - [politifact_fake.csv](FakeNewsNet-master/FakeNewsNet-master/dataset/politifact_fake.csv)
  - [politifact_real.csv](FakeNewsNet-master/FakeNewsNet-master/dataset/politifact_real.csv)
  - [gossipcop_fake.csv](FakeNewsNet-master/FakeNewsNet-master/dataset/gossipcop_fake.csv)
  - [gossipcop_real.csv](FakeNewsNet-master/FakeNewsNet-master/dataset/gossipcop_real.csv)
- **Sources**: PolitiFact.com, Gossipcop.com news items
- **Used in**: Multi-Best model (89.09% accuracy)
- **Split**: Politifact (756 samples) + Gossipcop (14,591 samples)

#### 4. **Multi-Source Combined**
- **Train + LIAR**: 45,036 samples
  - Kaggle: 34,597
  - LIAR: 11,439
- **Train + FakeNewsNet**: 45,347 samples
  - Kaggle: 30,041
  - Gossipcop: 14,591
  - Politifact: 756
- **Class Balance**: Balanced to equal REAL/FAKE (22,694 each for multi_best)

### Data Preprocessing in Training

**File**: [backend/scripts/train_multisource.py](backend/scripts/train_multisource.py)

```python
1. LOAD: Read multiple sources with different schemas
2. MAP LABELS: Convert multi-class → binary (REAL/FAKE)
3. CLEAN: Apply text_processor.clean_text()
   ├─ Remove URLs, emails
   ├─ Remove special characters
   └─ Normalize whitespace
4. VALIDATE: Drop null/empty samples
5. DEDUPLICATE: Remove duplicate text entries
6. BALANCE: Undersample majority class to match minority class
7. SPLIT: 80/20 train/test split with stratification
```

### Dataset Statistics

| Dataset | Total Samples | FAKE | REAL | Test Size |
|---------|--------------|------|------|-----------|
| Kaggle | ~62,000 | 29,498 | 32,545 | 8,837 |
| LIAR | ~13,068 | 4,068 | 9,000 | 2,559 |
| FakeNewsNet | 15,347 | 7,712 | 7,635 | N/A |
| Multi (K+L) | 45,036 | 23,018 | 23,018 | 9,208 |
| Multi-Best (K+F) | 45,347 | 22,694 | 22,694 | 9,078 |

### Imbalanced Learning Approach

```python
# From train_multisource.py - balance_classes()
min_count = min(REAL_count, FAKE_count)
balanced_data = undersample to min_count for each class
# Result: Equal class representation
```

**Rationale**: Prevents model bias toward majority class

---

## Summary Architecture Diagram

```
Frontend (React/Vite)
    ↓
[analyzeNews(text, mode, url, checkUrl)]
    ↓
Backend API (Flask)
    ↓
POST /api/analyze
├─ Validate input (length, word count)
├─ Text Processing (clean_text)
├─ Model Prediction
│  ├─ Mode: "hybrid" → Ensemble (Kaggle + LIAR)
│  ├─ Mode: "kaggle" → Single LogisticRegression (99.23% acc)
│  ├─ Mode: "liar" → Single LogisticRegression (62% acc)
│  ├─ Mode: "multi" → Combined K+L (88.8% acc)
│  └─ Mode: "multi_best" → Combined K+F (89.09% acc)
│
├─ Keyword Enhancement
│  ├─ Obvious fake detection (23 patterns)
│  ├─ Borderline case keyword voting
│  └─ Extract flagged keywords (9 sensational, 7 hedge, 4 clickbait)
│
├─ Credibility Scoring (0-100)
│  ├─ Model Score (0-15)
│  ├─ Keyword Score (0-25)
│  ├─ Length Score (0-15)
│  ├─ Hedge Score (0-10)
│  └─ Conspiracy Penalties
│
├─ [Optional] URL Credibility Check
│  └─ Domain matching against safe/fake lists
│
└─ Return JSON
   ├─ fakeNewsAnalysis
   │  ├─ prediction (fake/real/needs_verification)
   │  ├─ confidence (0-1)
   │  ├─ credibilityScore (0-100)
   │  ├─ breakdown
   │  ├─ flaggedKeywords
   │  └─ ensemble (if hybrid mode)
   └─ urlAnalysis (optional)
        ├─ is_credible
        ├─ risk_level
        ├─ explanation
        └─ domain
```

---

## Key Files Reference

| Component | File |
|-----------|------|
| **Main API** | [backend/app.py](backend/app.py) |
| **Analyze Endpoint** | [backend/routes/analyze.py](backend/routes/analyze.py) |
| **Model Management** | [backend/utils/model_loader.py](backend/utils/model_loader.py) |
| **Scoring System** | [backend/utils/scorer.py](backend/utils/scorer.py) |
| **Text Processing** | [backend/utils/text_processor.py](backend/utils/text_processor.py) |
| **URL Verification** | [backend/utils/groq_analyzer.py](backend/utils/groq_analyzer.py) |
| **Training (Single)** | [backend/scripts/train_model.py](backend/scripts/train_model.py) |
| **Training (Multi)** | [backend/scripts/train_multisource.py](backend/scripts/train_multisource.py) |
| **Prediction Utility** | [backend/scripts/predict.py](backend/scripts/predict.py) |
| **Keyword Data** | [backend/data/keywords.json](backend/data/keywords.json) |
| **Trusted Sources** | [backend/data/trusted_sources.json](backend/data/trusted_sources.json) |
| **Frontend API Client** | [frontend/src/utils/api.js](frontend/src/utils/api.js) |
| **Results Display** | [frontend/src/components/ResultCard.jsx](frontend/src/components/ResultCard.jsx) |

---

## Configuration

**Environment Variables** ([backend/.env.example](backend/.env.example)):
```
FLASK_ENV=development
PORT=5000
FRONTEND_ORIGIN=http://localhost:5173
MODEL_VARIANT=hybrid          # Default model mode
CONFIDENCE_THRESHOLD=0.65     # Threshold for "needs_verification"
MONGODB_URI=mongodb://localhost:27017/newsguard
```

---

This comprehensive analysis covers all major aspects of the NewsGuard fake news detection system. The system is multi-faceted with 4+ ML models, rule-based keyword enhancement, credibility scoring, and URL verification capabilities.
