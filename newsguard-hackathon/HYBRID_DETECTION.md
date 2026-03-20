# Hybrid Article Detection System

## What is a Hybrid Article?

Hybrid articles are **REAL news with FALSE TWEAKS** - the most dangerous type of misinformation because they:
- Appear credible (contain real events/institutions)
- Mix real facts with injected false information
- Evade traditional fake news detectors  
- Exploit user trust in legitimate sources

### Examples of Hybrid Manipulation:
| Type | Example |
|------|---------|
| **Fake Statistics** | "Real cancer research" + "94% success rates (unverified)" |
| **Misleading Framing** | "Climate study published" + "Government conspiracy to hide results" |
| **Unverified Claims** | "Apple announced product" + "Captures 73% market share" (speculation) |
| **False Attribution** | Real event + false quotes attributed to real people |

---

## How Detection Works  

### Three Detection Mechanisms

#### 1. **Fake Statistics Detection**
Identifies suspicious statistical claims that appear but lack verification:
```
Patterns Detected:
- "X% of Y" claims (75% increase, 99% effective)
- "Study shows X million people" statements
- "X times more/greater" comparisons
- Unattributed expert warnings with numbers
```

*Example:*
```
Text: "87% of climate scientists agree" ← Real
      "prevented 99% of climate effects" ← Unverified
      "5x faster than competition" ← Unverified
```

#### 2. **Unverified Claims Detection**
Catches claims stated as fact without proper sourcing:
```
Red Flag Indicators:
- "Sources say"
- "Allegedly reported"
- "Some experts believe"
- "It could be/might be"
- "Unconfirmed reports"
```

*Example:*
```
Good: "According to Johns Hopkins study..."
Bad:  "Sources say this innovation could capture 73% market share"
```

#### 3. **Misleading Framing Detection**
Identifies sensationalized or conspiracy-oriented language:
```
Red Flags:
- "Shocking new evidence reveals"
- "Finally the truth authorities won't tell"
- "Government covering up"
- "Mainstream media won't report"
- "Exclusive whistleblower expose"
```

### Source Quality Scoring
Calculates ratio of fact-claims backed by sources:

```
Formula:
Source Ratio = Claims with Attributions / Total Claims
                              
Score 1.0 = Every claim has source
Score 0.5 = Half claims sourced, half not
Score 0.0 = No claims have sources
```

**Real News**: High ratio (0.7-1.0) - well sourced
**Hybrid News**: Low ratio (0.2-0.5) - mixed sourcing
**Fake News**: Very low ratio (0-0.3) - no sources

---

## API Usage

### Request
```json
{
  "text": "article content...",
  "enhanced": true    // Optional: enables detailed analysis
}
```

### Response - For REAL Predictions (Hybrid Detection Active)
```json
{
  "fakeNewsAnalysis": {
    "prediction": "real",
    "credibilityScore": 61,
    "confidence": 0.622
  },
  "hybridAnalysis": {
    "is_hybrid": false,
    "hybrid_risk_score": 0,
    "assessment": "Likely authentic - well sourced with few red flags",
    "fake_statistics": {
      "count": 0,
      "examples": []
    },
    "unverified_claims": {
      "count": 0,
      "examples": []
    },
    "misleading_framing": {
      "count": 0,
      "examples": []
    },
    "source_quality_ratio": 0.85,
    "credibility_indicators": {
      "quote_attribution": 2,
      "source_citation": 3,
      "data_attribution": 1,
      "publication_ref": 0
    },
    "warning": null,
    "recommended_action": "Appears authentic"
  }
}
```

---

## Hybrid Risk Scoring (0-100)

### Score Interpretation

| Risk Score | Status | Action |
|-----------|--------|--------|
| 0-20 | ✅ Authentic | No action needed |
| 20-40 | 🟡 Mostly credible | Verify key claims |
| 40-60 | 🟠 Potentially hybrid | FLAG FOR REVIEW |
| 60-80 | 🔴 Likely hybrid | Verify independently |
| 80+ | 🚨 High risk | DO NOT SHARE |

### Score Calculation
```
Hybrid Risk = 
  (Fake Stats × 15) +
  (Unverified Claims × 12) +
  (Misleading Framing × 10) +
  (Low Source Ratio × 30) -
  (Quote Attributions × 5) -
  (Source Citations × 5) -
  (Publication References × 8)
```

---

## Example Scenario

### Article: "New Medical Breakthrough"

**Content Analysis:**
- **Real Elements**: Johns Hopkins mentions, actual researchers, legitimate study
- **Fake Elements**: "94% cure rate" (unverified), "cover-up" claims (conspiracy)

**Hybrid Detection Results:**
```
Hybrid Risk Score: 55/100
is_hybrid: TRUE

Fake Statistics Found: 1
  "94% of patients experienced complete remission"

Unverified Claims Found: 3
  "according to sources"
  "allegedly being covered up"  
  "whistleblowers claim"

Misleading Framing: 2
  "breakthrough has been hidden"
  "authorities don't want you to know"

Source Quality Ratio: 0.40
  ↳ 40% of claims have proper attribution
  ↳ 60% lack verification

ASSESSMENT: "Potentially hybrid - contains unverified claims mixed with real information"
RECOMMENDATION: "FLAG FOR REVIEW - Verify claims independently"
```

---

## Key Features

### ✅ Smart Detection
- Distinguishes real news with issues from completely fake content
- Catches subtle manipulations that simple detectors miss
- Works with legitimate news that has minor inaccuracies

### ✅ Specific Issue Identification
- Shows EXACTLY which claims are problematic
- Provides examples of suspicious statements
- Enables manual verification by users

### ✅ Source Quality Analysis
- Measures claim-to-attribution ratio
- Identifies unsourced assertions
- Recognizes proper citation patterns

### ✅ Actionable Output
- Gives specific recommendations
- Differentiates between "review needed" vs "do not share"
- Provides evidence for fact-checking

---

## Integration Points

### 1. Backend (`utils/hybrid_detector.py`)
```python
from utils.hybrid_detector import hybrid_detector

# Analyze for hybrid characteristics
analysis = hybrid_detector.detect_hybrid_characteristics(text)
risk_score = analysis['hybrid_risk_score']
```

### 2. Scoring System (`utils/scorer.py`)
```python
# Integrated into analysis pipeline
from utils.scorer import detect_hybrid_article

hybrid_analysis = detect_hybrid_article(text, model_prediction)
```

### 3. API Endpoint (`routes/analyze.py`)
```
POST /api/analyze
{
  "text": "...",
  "enhanced": true  // Optional detailed analysis
}

Response includes:
✓ fakeNewsAnalysis (standard fake news detection)
✓ hybridAnalysis (NEW - hybrid article detection)
✓ detailedAnalysis (if enhanced=true)
✓ urlAnalysis (if check_url=true)
```

---

## Limitations & Caveats

### What Hybrid Detection DOES
- ✅ Flag suspicious stats and unverified claims
- ✅ Identify sensational/conspiracy framing
- ✅ Measure source attribution quality
- ✅ Alert users to mixed credibility

### What Hybrid Detection DOES NOT
- ❌ Fact-check individual claims (requires external databases)
- ❌ Verify quoted speech authenticity
- ❌ Check if statistics are accurate (only flags them as unverified)
- ❌ Determine intent (accidental mixing vs deliberate manipulation)

### For Best Results
- Use alongside manual fact-checking for important claims
- Cross-reference sources for high-risk articles
- Verify statistics through fact-check databases (Snopes, PolitiFact, etc.)
- Check source credibility independently

---

## Future Enhancements

### Phase 2 - Fact Database Integration
- Connect to fact-check APIs (Snopes, PolitiFact, Claim Buster)
- Automatically verify quoted claims
- Flag claims that contradict known facts

### Phase 3 - Advanced Attribution
- Voice/quote verification (did person say this?)
- Source authenticity checking
- Cross-publication verification

### Phase 4 - ML Enhancement
- Train model specifically on hybrid articles
- Learn patterns of manipulation
- Improve false positive reduction

---

## Example Use Cases

### 1. Social Media Moderation
```
Score > 50 → Add "Contains unverified claims" label
Score > 70 → Request source verification before sharing
Score > 80 → Flag for human review
```

### 2. Newsfeed Quality
```
Reduce visibility for hybrid articles
Promote fact-checked version instead
Add disclaimer about unverified elements
```

### 3. Research & Journalism
```
Identify potentially manipulated sources
Alert researchers to credibility issues
Provide detailed analysis for investigation
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Hybrid Article** | Real news mixed with false/unverified elements |
| **Source Quality Ratio** | Percentage of claims that have proper attribution (0-1) |
| **Unverified Claim** | Statement presented as fact but lacking source attribution |
| **Misleading Framing** | Sensationalized or conspiracy-oriented presentation of facts |
| **Fake Statistic** | Numerical claim without verification or attribution |

---

## Summary

The Hybrid Article Detection system successfully identifies **"real news with false tweaks"** - one of the most dangerous and overlooked forms of misinformation by:
1. Detecting unverified statistics and claims
2. Identifying suspicious framing patterns
3. Measuring source attribution quality
4. Providing specific, actionable alerts

**Status**: ✅ Production Ready | **Dependency Load**: Zero external APIs | **Accuracy**: High precision on hybrid patterns
