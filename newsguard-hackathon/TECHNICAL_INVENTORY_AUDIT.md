# NewsGuard Project — Complete Technical Inventory Audit

**Date:** March 20, 2026  
**Project:** NewsGuard Fake News Detection System (MNIT Hackathon)  
**Scope:** Full codebase including backend (Python/Flask), frontend (React/Vite), ML models, and deployment configs

---

## Part 1 — Full Technical Inventory

### 1.1 Languages & Runtimes

| Language | Version | Purpose | Files |
|----------|---------|---------|-------|
| Python | 3.10.5 | Backend API, ML models, data processing | `backend/app.py`, `backend/routes/`, `backend/utils/`, `backend/scripts/` |
| JavaScript (ES6+) | Implicit (Node runtime > 16) | Frontend SPA with React | `frontend/src/` |
| JSON | N/A | Config, data storage | `package.json`, `backend/data/keywords.json`, `.env.example`, etc. |
| YAML | N/A | Deployment configs | `render.yaml`, `.github/workflows` (if present) |
| Plaintext | N/A | Documentation, environment | `.env.example`, `runtime.txt`, `Procfile` |

---

### 1.2 Frameworks & Libraries

#### **Backend Dependencies**

| Library | Version | Used In | Role |
|---------|---------|---------|------|
| **Flask** | 3.0.3 | `backend/app.py`, `backend/routes/analyze.py` | HTTP REST API framework, route handling, CORS support |
| **flask-cors** | 4.0.1 | `backend/app.py` | CORS middleware for handling cross-origin requests from frontend |
| **python-dotenv** | 1.0.1 | `backend/app.py` | Environment variable management (API keys, model paths, config) |
| **scikit-learn** | 1.5.1 | `backend/utils/model_loader.py` | TF-IDF vectorizer, classifier inference, calibration |
| **pandas** | 2.2.2 | `backend/scripts/train_multisource.py` | Data loading, preprocessing, DataFrame operations |
| **numpy** | 2.0.1 | `backend/scripts/train_multisource.py` | Numerical operations, array handling |
| **nltk** | 3.9.1 | **NOT USED** ⚠️ | _(Installed but no imports found in codebase; unused dependency)_ |
| **gunicorn** | 22.0.0 | `Dockerfile`, deployment | Production WSGI HTTP server for Flask app |

#### **Frontend Dependencies**

| Library | Version | Used In | Role |
|---------|---------|---------|------|
| **React** | 18.3.1 | `frontend/src/pages/`, `frontend/src/components/` | Component-based UI framework |
| **react-dom** | 18.3.1 | `frontend/src/main.jsx` | React rendering to DOM |
| **react-router-dom** | 6.20.0 | `frontend/src/App.jsx`, pages | Client-side routing (6 pages: Landing, Analyzer, About, Methodology, Extended About) |
| **axios** | 1.7.2 | `frontend/src/utils/api.js` | HTTP client for backend API calls (`/analyze`, `/models`) |
| **recharts** | 2.12.7 | `frontend/src/components/ScoreBreakdown.jsx` | Data visualization library (score charts, breakdown visualization) |
| **three** | 0.183.2 | `frontend/src/` | 3D graphics rendering (if used in visual effects) |
| **Vite** | 5.4.0 | Build system | Modern frontend build tool (ESM-first) |
| **Tailwind CSS** | 3.4.10 | `frontend/src/`, PostCSS | Utility-first CSS framework for responsive styling |

#### **Dev & Build Tools**

| Tool | Version | Purpose |
|------|---------|---------|
| **@vitejs/plugin-react** | 4.3.1 | Vite React JSX plugin |
| **autoprefixer** | 10.4.20 | PostCSS plugin for vendor prefixes |
| **postcss** | 8.4.41 | CSS transformation pipeline |

---

### 1.3 Machine Learning Components

#### **Model Architecture**

| Component | Details |
|-----------|---------|
| **Algorithm Type** | Supervised binary classification (Fake/Real) |
| **Base Algorithm** | Logistic Regression with SVM fallback (inferred from scikit-learn usage) |
| **Vectorization Method** | **TF-IDF (Term Frequency-Inverse Document Frequency)** |
| **Vectorizer Config** | Loaded from `tfidf_vectorizer.pkl` (max_features, ngram_range pre-fitted) |
| **Model Calibration** | `scikit-learn.calibration.CalibratedClassifierCV` for confidence estimation |
| **Confidence Calculation** | Decision function margin or predict_proba, clamped to [0, 1] |

#### **Model Variants Available**

| Mode | Model Path | Vectorizer Path | Accuracy | Provider | Status |
|------|-----------|-----------------|----------|----------|--------|
| **kaggle** | `backend/models/fake_news_model.pkl` | `backend/models/tfidf_vectorizer.pkl` | 99.23% | kaggle-model | ✓ Active |
| **liar** | `backend/models/liar/fake_news_model.pkl` | `backend/models/liar/tfidf_vectorizer.pkl` | N/A (not in report) | liar-model | ✓ Active |
| **multi_best** | `backend/models/multi_best/fake_news_model.pkl` | `backend/models/multi_best/tfidf_vectorizer.pkl` | N/A | multi-best-model | ✓ Active |
| **multi** | `backend/models/multi/fake_news_model.pkl` | `backend/models/multi/tfidf_vectorizer.pkl` | N/A | multi-model | ✓ Active |
| **hybrid** | Ensemble of kaggle + liar | Ensemble voting | N/A | hybrid-ensemble | ✓ Default |

#### **Training Data Sources**

| Source | Dataset | Reference Files |
|--------|---------|-----------------|
| Kaggle | Fake News Challenge dataset | `backend/models/training_report.txt` |
| LIAR | Social media claims dataset | `liar_dataset-master/` folder |
| FakeNewsNet | News articles with labels | `FakeNewsNet-master/` folder |
| CREDBANK | Credibility assessment dataset | `CREDBANK-data-master/` folder |
| Multi-source | Combined from above | `backend/scripts/train_multisource.py` |

#### **Saved Artifacts**

| File | Location | Purpose |
|------|----------|---------|
| `fake_news_model.pkl` | `backend/models/[mode]/` | Trained Logistic Regression classifier |
| `tfidf_vectorizer.pkl` | `backend/models/[mode]/` | Fitted TF-IDF vectorizer with learned vocabulary |
| `training_report.txt` | `backend/models/kaggle/` | Classification metrics (Accuracy: 99.23%, precision/recall by class) |
| `sample_predictions.csv` | `backend/models/` | Example model outputs for validation |

#### **Preprocessing Pipeline**

| Stage | Implementation | Code |
|-------|-----------------|------|
| **URL Removal** | Regex: `https?://\S+\|www\.\S+` | `backend/utils/text_processor.py:4` |
| **Email Removal** | Regex: `\b[\w\.-]+@[\w\.-]+\.\w+\b` | `backend/utils/text_processor.py:5` |
| **Special Char Removal** | Regex: `[^a-zA-Z0-9\.\s]` | `backend/utils/text_processor.py:6` |
| **Whitespace Normalization** | Regex: `\s+` → single space | `backend/utils/text_processor.py:7` |
| **Lowercasing** | Python `.lower()` | `backend/utils/text_processor.py:3` |
| **Vectorization** | TF-IDF (fitted vocabulary) | `backend/utils/model_loader.py` |

#### **Fallback & Rule-Based Logic**

| Condition | Rule | Confidence Adjustment |
|-----------|------|----------------------|
| **Obvious fake patterns** | 3+ matches in predefined phrases | Force "fake" prediction, +20% confidence |
| **Borderline confidence** | 0.55–0.70 range | Keyword matching: +8% per matched keyword |
| **Both models abstain** | Hybrid ensemble, both < threshold | Return "needs_verification" |
| **Single model unavailable** | Attempt fallback to alternative | RuntimeError if no models available |

#### **Keyword Matching (Rule-Based Fallback)**

**Fake Indicators (checked when confidence < 0.70):**
- `shocking`, `scientists announce`, `doctors hate`, `secret discovered`, `miracle cure`, `100% effective`, `government hiding`, `proven`, `guaranteed`, `sources say`, `allegedly`, `experts claim`, `leaked`, `revealed`, `conspiracy`, `foia`, `classified`

**Real Indicators (checked when confidence < 0.70):**
- `according to`, `sources familiar`, `report`, `announced`, `officials say`, `researchers found`, `study shows`, `review`, `peer-reviewed`, `journal finds`, `data shows`, `analysis`, `statement said`, `confirmed`

---

### 1.4 Frontend Components & Features

#### **Main UI Structure**

| Page/Component | Path | Purpose |
|----------------|------|---------|
| **App Router** | `frontend/src/App.jsx` | Main route dispatcher (6 routes) |
| **HomePage (Analyzer)** | `frontend/src/pages/HomePage.jsx` | Primary analyzer interface ← **Main feature** |
| **LandingPage** | `frontend/src/pages/LandingPage.jsx` | Marketing/intro page |
| **AboutPage** | `frontend/src/pages/AboutPage.jsx` | Team/project info |
| **MethodologyPage** | `frontend/src/pages/MethodologyPage.jsx` | Technical explanation |
| **AboutExtendedPage** | `frontend/src/pages/AboutExtendedPage.jsx` | Additional details |

#### **Interactive Components**

| Component | File | Features |
|-----------|------|----------|
| **InputBox** | `frontend/src/components/InputBox.jsx` | Text input, URL field, mode selector dropdown, submit button |
| **ResultCard** | `frontend/src/components/ResultCard.jsx` | Score display, prediction badge, breakdown details, URL analysis if present |
| **ScoreBreakdown** | `frontend/src/components/ScoreBreakdown.jsx` | Recharts visualization of score components |
| **Header** | `frontend/src/components/Header.jsx` | Navigation bar, branding, mode info |
| **LoadingSpinner** | `frontend/src/components/LoadingSpinner.jsx` | Progress animation during analysis |

#### **State Variables (HomePage.jsx)**

| State | Type | Purpose |
|-------|------|---------|
| `result` | Object\|null | Stores API response (prediction, score, breakdown) |
| `isLoading` | Boolean | Shows loading spinner during request |
| `error` | String | Error message display |
| `mode` | String | Selected model variant ("hybrid", "kaggle", "liar", etc.) |
| `modelOptions` | Array | Available models fetched from `/api/models` |
| `isDark` | Boolean | Dark/light theme toggle |
| `particles` | Array | Animated background particles (20 particles with random properties) |

#### **UI Animations & Effects**

| Effect | Implementation |
|--------|-----------------|
| **Background Particles** | CSS `@keyframes float` animation, 20 divs with random opacity/duration |
| **Loading Spinner** | SVG ring spinner with `animate-spin` CSS |
| **Score Progress Bar** | Animated gradient bar during analysis |
| **Score Gauge** | SVG circle with stroke-dasharray animation |
| **Theme Transitions** | Smooth class transitions between light/dark |

#### **API Calls Made**

| Method | Endpoint | Parameters | Response Fields |
|--------|----------|-----------|-----------------|
| **POST** | `/api/analyze` | `text`, `mode`, `url`, `check_url`, `enhanced` | `fakeNewsAnalysis`, `aiGenerationAnalysis`, `hybridAnalysis`, `urlAnalysis`, `detailedAnalysis` |
| **GET** | `/api/models` | None | Array of model objects with `mode`, `label`, `accuracy` |

#### **Response Rendering**

When `/api/analyze` completes:
- **Main Section:** Shows credibility score (0–100) with badge (High/Moderate/Low)
- **Confidence Display:** Percentage confidence from model
- **Breakdown Tabs:** Model score, keyword score, length score, hedge score (if available)
- **Flagged Keywords:** Highlighted sensational/clickbait words found
- **AI Generation Analysis:** Score and verdict if `aiGenerationAnalysis` present
- **Hybrid Analysis:** Warnings if article is "real but hybrid-manipulated"
- **URL Analysis:** Domain credibility and risk level if `check_url=true`

---

### 1.5 Backend Endpoints

#### **Core Endpoints**

| Method | Path | Input Validation | Processing Logic | Response Structure |
|--------|------|-----------------|------------------|-------------------|
| **POST** | `/api/analyze` | `text` (string, 80–30000 chars, ≥12 words) | 1. Clean text (remove URLs/emails/special chars) 2. Run ML model prediction 3. Extract flagged keywords 4. Calculate credibility score 5. Detect AI patterns 6. Detect hybrid articles 7. Optional URL verification (Groq) | `fakeNewsAnalysis`: { `prediction` (fake/real/needs_verification), `confidence` (0-1), `credibilityScore` (0-100), `breakdown` (dict), `flaggedKeywords` (array), `provider` (model name), `mode` (selected mode), `ensemble` (if hybrid) }, `aiGenerationAnalysis`: {...}, `hybridAnalysis`: {...}, `urlAnalysis`: {...}, `detailedAnalysis`: {...} |
| **GET** | `/api/models` | None | 1. Load model catalog 2. Sort by accuracy 3. Add hybrid entry if 2+ models available | `models`: Array of { `mode`, `label`, `accuracy`, `provider` } |
| **GET** | `/api/health` | None | Return service status | `{"status": "healthy", "message": "NewsGuard API is running"}` |

#### **Request/Response Details**

**POST /api/analyze Request:**
```json
{
  "text": "Article content here...",
  "mode": "hybrid",                // optional, default from env MODEL_VARIANT
  "url": "https://example.com",   // optional, for URL verification
  "check_url": false,             // optional default false
  "enhanced": false               // optional, enables detailed analysis
}
```

**POST /api/analyze Response (Full):**
```json
{
  "fakeNewsAnalysis": {
    "prediction": "fake",
    "confidence": 0.8765,
    "credibilityScore": 25,
    "breakdown": {
      "modelScore": 10,
      "keywordScore": 15,
      "lengthScore": 0,
      "hedgeScore": 0,
      "wordCount": 95
    },
    "flaggedKeywords": ["shocking", "breaking"],
    "provider": "hybrid-ensemble",
    "mode": "hybrid",
    "ensemble": {
      "kaggle": {"prediction": "fake", "confidence": 0.92},
      "liar": {"prediction": "fake", "confidence": 0.83},
      "weights": {"fake": 1.75, "real": 0.0}
    }
  },
  "aiGenerationAnalysis": {
    "aiScore": 0.245,
    "verdict": "Unlikely to be AI-generated",
    "indicators": {
      "perfect_structure": {"matches": 2, "score": 0.056},
      ...
    }
  },
  "hybridAnalysis": {
    "is_hybrid": false,
    "hybrid_risk_score": 0.1
  }
}
```

---

### 1.6 Data & Configuration Files

#### **JSON Data Files**

| File | Location | Purpose | Sample Content |
|------|----------|---------|-----------------|
| `keywords.json` | `backend/data/` | Predefined flagged keywords for matching | `{"sensational_words": ["shocking", ...], "hedge_words": ["allegedly", ...], "clickbait_phrases": [...]}` |
| `trusted_sources.json` | `backend/data/` | Domain reputation database | (not shown, but used for URL verification) |
| `package.json` | `frontend/` | NPM dependencies, scripts, metadata | React 18.3.1, Vite, Tailwind config |

#### **Pickle Files (ML Artifacts)**

| File | Location | Contains | Size |
|------|----------|----------|------|
| `fake_news_model.pkl` | `backend/models/[mode]/` | Serialized classifier (trained on TF-IDF features) | ~2-5 MB typical |
| `tfidf_vectorizer.pkl` | `backend/models/[mode]/` | Fitted TF-IDF vectorizer with vocabulary | ~1-2 MB typical |

#### **Configuration Files**

| File | Location | Purpose |
|------|----------|---------|
| `.env.example` | `backend/`, `frontend/` | Template for environment variables |
| `.env.production` | `backend/`, `frontend/` | Production secrets (not in repo) |
| `runtime.txt` | `backend/` | Python version for Render/Heroku (`python-3.10.5`) |
| `Procfile` | `backend/` | Process definition for Heroku-like platforms |
| `render.yaml` | Root | Render deployment configuration |
| `railway.json` | Root | Railway deployment configuration (deprecated) |
| `Dockerfile` | Root | Docker image specification (Python 3.10-slim) |
| `.dockerignore` | Root | Files to exclude from Docker build |
| `vite.config.js` | `frontend/` | Vite build configuration |
| `tailwind.config.js` | `frontend/` | Tailwind CSS customization |
| `postcss.config.js` | `frontend/` | PostCSS plugin chain for CSS |
| `vercel.json` | `frontend/` | Vercel deployment config |

#### **Text/Report Files**

| File | Location | Contents |
|------|----------|----------|
| `training_report.txt` | `backend/models/kaggle/` | Classification metrics: Accuracy 99.23%, precision/recall/f1 by class, confusion matrix |
| `README.md` | Root | Project overview and setup |
| `DOCUMENTATION.md` | Root | Comprehensive technical documentation |
| `JUDGING_GUIDE.md` | Root | Guide for hackathon judges |
| Various deployment guides | Root | Railway, Render, Vercel specific docs |

---

## Part 2 — NLP Audit

### NLP Audit Questions

| # | Question | Answer | Evidence | Explanation |
|---|----------|--------|----------|-------------|
| 1 | Is NLTK used in this project? | **NO** ⚠️ | `nltk==3.9.1` is in `requirements.txt` but **zero imports found** in backend code via grep search. Unused dependency. | NLTK is installed but never imported or used anywhere. This is dead code/dependency bloat. |
| 2 | Are NLTK stopwords applied during preprocessing? | **NO** | No `from nltk.corpus import stopwords` or similar found; text preprocessing in `text_processor.py` uses only regex rules. | Preprocessing is regex-based, not NLTK-based. No stopword filtering performed. |
| 3 | Is tokenization performed (word or sentence level)? | **PARTIAL** | Simple whitespace splitting in `text.split()` (word-level only) at multiple places (`model_loader.py`, `enhanced_analyzer.py`). No sentence tokenizer used. | Tokenization is trivial string splitting. No proper linguistic tokenization (NLTK, spaCy) used. |
| 4 | Is any named entity recognition (NER) present? | **NO** | `enhanced_analyzer.py` mentions "Named entity mentions" but only counts **capitalized sequences via regex** `r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'`, not true NER. | Regex pattern matching for capitalized words ≠ NER. No NLP library (spaCy, NLTK, transformers) used for entity recognition. |
| 5 | Is part-of-speech (POS) tagging used? | **NO** | No `nltk.pos_tag()`, spaCy `.pos_`, or similar POS tagging methods found in code. | Zero POS tagging infrastructure present. |
| 6 | Is sentiment analysis implemented? | **NO** | No sentiment library (VADER, TextBlob, transformers) imported or used. No sentiment scoring in code. | Absence of sentiment analysis; scoring is based on keyword flags and ML model, not sentiment. |
| 7 | Is TF-IDF used? (Note: this is text feature extraction, not full NLP) | **YES** ✓ | `backend/utils/model_loader.py` loads `tfidf_vectorizer.pkl`; `model.predict(transformed)` where `transformed = vectorizer.transform([text])`. | TF-IDF is the **sole vectorization method**. All text is converted to TF-IDF sparse vectors before ML classification. |
| 8 | Are word embeddings (Word2Vec, GloVe, BERT) used? | **NO** | No embedding imports; models use TF-IDF (count-based), not neural embeddings. No `word2vec`, `gensim`, `transformers`, `torch` imports. | No deep learning embeddings. TF-IDF is a shallow feature extraction method. |
| 9 | Is any transformer or deep learning NLP model present? | **NO** | No PyTorch, TensorFlow, Hugging Face transformers, or similar deep learning frameworks imported. Models are Logistic Regression + TF-IDF (2010s-era methods). | No modern deep learning. Architecture is classical ML, not neural. |
| 10 | Is keyword matching implemented? (rule-based, not ML) | **YES** ✓ | `backend/utils/scorer.py`: `extract_flagged_keywords()` matches against `keywords.json` list. Also `backend/utils/model_loader.py` has explicit fake/real keyword lists for fallback rules. Extensive regex pattern matching throughout. | Heavy reliance on predefined keyword lists + rule-based scoring. Rules are applied before and after ML prediction. |

---

### NLP Verdict

#### **Classification Result: BASIC TEXT PROCESSING**

---

#### **Explanation for Hackathon Judges**

NewsGuard implements **basic text processing and classical machine learning**, NOT a genuine modern NLP system.

**What IS Present:**
1. **TF-IDF Vectorization** — Text is converted to sparse numeric features using term frequency and inverse document frequency weighting (scikit-learn). This is a standard 1990s–2000s feature engineering method.
2. **Logistic Regression Classification** — The core classifier is a linear model trained on TF-IDF features. This is simple, interpretable, but does not understand language semantics.
3. **Extensive Keyword Matching** — Hardcoded lists of sensational words, hedge language, conspiracy keywords, and fake news phrases are matched via string/regex operations. This is rule-based, not learned.
4. **Heuristic Scoring** — The credibility score combines ML confidence with rule counts (flagged keywords, text length, hedging metrics) in a weighted formula, not end-to-end learning.

**What is NOT Present:**
- ❌ **No NLTK usage** — Despite being in requirements.txt, NLTK (popular for NLP) is completely unused.
- ❌ **No deep learning models** — No transformers (BERT, GPT, RoBERTa), no neural networks, no attention mechanisms.
- ❌ **No word embeddings** — No Word2Vec, GloVe, FastText, or contextual embeddings.
- ❌ **No linguistic preprocessing** — No POS tagging, NER, syntactic parsing, or semantic role labeling.
- ❌ **No sentiment analysis** — Scoring is lexicon-based flag matching, not sentiment detection.
- ❌ **No language understanding** — The system does not truly "understand" text; it counts features and matches patterns.

**Technical Summary:**  
The system is essentially a **Logistic Regression classifier trained on TF-IDF features**, combined with hand-crafted heuristics and keyword matching. While effective for fake news detection (99.23% accuracy on training data), this is an application of classical machine learning, not NLP in the modern sense. Modern NLP systems would employ transformer-based architectures (BERT, GPT, RoBERTa), contextual embeddings, or at minimum LSTM/CNN neural networks. NewsGuard's approach is transparent, fast, and deployable, but linguistically shallow — it does not extract meaning, intent, or context from text the way true NLP systems do.

---

### Supplementary Notes

#### **Unused/Incomplete Features** ⚠️

| Component | Status | Note |
|-----------|--------|------|
| NLTK library | Unused | Installed in requirements.txt but never imported or used. Safe to remove. |
| three.js | Unclear | `three@0.183.2` in package.json but no usage found in frontend code (may be orphaned). |
| Groq API (URL verification) | Optional | Used only if `check_url=true` in request; not core functionality. API key required. |
| Enhanced analyzer modes | Partially used | Available but only activated if `enhanced=true` in request; not default. |
| AI detection model (v2) | Alternative | `ai_detector_v2.py` exists but `ai_detector.py` is used; v2 not called by any endpoint. |

#### **Data sourcing**

- Kaggle dataset: `FakeNewsNet-master/`, `liar_dataset-master/`, `CREDBANK-data-master/` directories present but archived; actual training data not in repo (too large, .gitignore'd).
- Models pre-trained and serialized as `.pkl` files; no live training in production.

---

### Audit Conclusion

**Overall Assessment:** This is a **well-engineered classical ML system for fake news detection**, not a modern NLP pipeline. The project successfully uses scikit-learn, rule-based heuristics, and ensemble methods to achieve high accuracy, but does not employ NLP techniques like syntactic analysis, semantic embeddings, or transformer-based models.

**Recommendations for judges:**
- ✓ **Strengths:** High accuracy (99.23%), explainability, fast inference, clean architecture, multiple model variants, comprehensive rule-based fallbacks.
- ⚠️ **Limitations:** Shallow language understanding, keyword-dependent, potential brittleness to adversarial text, limited context awareness.
- 💡 **Enhancement Path:** Replace TF-IDF + Logistic Regression with a fine-tuned BERT or RoBERTa model for semantic understanding; add transformer-based NER for extracting claim entities.

---

**Audit completed:** March 20, 2026  
**Auditor:** Technical Inventory System
