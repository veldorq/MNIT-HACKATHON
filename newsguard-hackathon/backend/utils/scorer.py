import json
from pathlib import Path
from typing import Any
from utils.enhanced_analyzer import enhanced_analyzer
from utils.hybrid_detector import hybrid_detector

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
KEYWORDS_PATH = DATA_DIR / "keywords.json"


def _load_keywords() -> dict[str, list[str]]:
    if not KEYWORDS_PATH.exists():
        return {"sensational_words": [], "hedge_words": [], "clickbait_phrases": []}

    with KEYWORDS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    return {
        "sensational_words": data.get("sensational_words", []),
        "hedge_words": data.get("hedge_words", []),
        "clickbait_phrases": data.get("clickbait_phrases", []),
    }


def extract_flagged_keywords(text: str) -> list[str]:
    keyword_dict = _load_keywords()
    candidates = (
        keyword_dict["sensational_words"]
        + keyword_dict["hedge_words"]
        + keyword_dict["clickbait_phrases"]
    )

    lowered = text.lower()
    matched = [token for token in candidates if token.lower() in lowered]
    return sorted(set(matched))


def calculate_credibility_score(
    model_prediction: str,
    confidence: float,
    text: str,
    flagged_keywords: list[str],
) -> tuple[int, dict[str, Any]]:
    confidence = max(0.0, min(confidence, 1.0))

    # Conspiracy/satire detection for aggressive penalty
    conspiracy_keywords = [
        'government surveillance', 'drones', 'foia documents', 'conspiracy theorists',
        'shocking documents', 'revealed', 'cover-up', 'hidden truth', 'classified',
        'visibly sweating', 'sources say', 'breakthrough discovery', 'miracle cure',
        'doctors hate', 'authorities hide', 'emergency', 'could not be reached for comment',
        '847-page document', 'department of homeland', 'feathers', 'tin foil hat'
    ]
    
    text_lower = text.lower()
    conspiracy_count = sum(1 for keyword in conspiracy_keywords if keyword in text_lower)
    
    # For FAKE predictions: aggressive low scoring
    if model_prediction == "fake":
        # Start very low for fake news
        model_points = max(0, int(round((1 - confidence) * 15)))
        
        # Apply VERY aggressive penalty for conspiracy/satire patterns
        if conspiracy_count >= 4:
            model_points = max(5, model_points - (conspiracy_count * 8))
        elif conspiracy_count >= 2:
            model_points = max(10, model_points - (conspiracy_count * 5))
    else:
        # For REAL predictions: normal scoring
        model_points = int(round(confidence * 50))

    words = text.split()
    word_count = len(words)

    sensational_count = len([k for k in flagged_keywords if " " not in k])
    keyword_points = max(0, 25 - min(sensational_count, 10) * 2)

    length_points = 15 if word_count >= 100 else int(round((word_count / 100) * 15))

    hedge_count = len([k for k in flagged_keywords if "alleg" in k or "report" in k])
    hedge_penalty = min(10, hedge_count * 2)
    hedge_points = max(0, 10 - hedge_penalty)

    total = model_points + keyword_points + length_points + hedge_points
    
    # Aggressive conspiracy/satire penalty for FAKE predictions
    if model_prediction == "fake" and conspiracy_count >= 2:
        conspiracy_penalty = min(total - 10, conspiracy_count * 12)  # Heavy penalty
        total = max(10, total - conspiracy_penalty)
    
    total = max(0, min(total, 100))

    breakdown = {
        "modelScore": model_points,
        "keywordScore": keyword_points,
        "lengthScore": length_points,
        "hedgeScore": hedge_points,
        "wordCount": word_count,
    }

    return total, breakdown


def calculate_enhanced_credibility_score(
    model_prediction: str,
    confidence: float,
    text: str,
    flagged_keywords: list[str],
) -> tuple[int, dict[str, Any]]:
    """
    ENHANCED scoring that integrates linguistic, semantic, and readability analysis.
    More robust and explainable than the basic scoring.
    
    Returns credibility score (0-100) and detailed breakdown for explainability.
    """
    confidence = max(0.0, min(confidence, 1.0))
    
    # Get detailed analysis from enhanced analyzer
    detailed_analysis = enhanced_analyzer.get_detailed_analysis(text)
    fake_score_components = detailed_analysis.get('fake_score_components', {})
    
    # ===== ML MODEL COMPONENT (0-30 points) =====
    conspiracy_keywords = [
        'government surveillance', 'drones', 'foia documents', 'conspiracy theorists',
        'shocking documents', 'revealed', 'cover-up', 'hidden truth', 'classified',
        'visibly sweating', 'sources say', 'breakthrough discovery', 'miracle cure',
        'doctors hate', 'authorities hide', 'emergency', 'could not be reached for comment',
        '847-page document', 'department of homeland', 'feathers', 'tin foil hat'
    ]
    
    text_lower = text.lower()
    conspiracy_count = sum(1 for keyword in conspiracy_keywords if keyword in text_lower)
    
    if model_prediction == "fake":
        model_points = max(0, int(round((1 - confidence) * 30)))
    else:
        model_points = int(round(confidence * 30))
    
    # ===== ENHANCED TEXT ANALYSIS COMPONENT (0-30 points) =====
    # Average the major linguistic/semantic indicators
    linguistic_score = fake_score_components.get('linguistic_score', 50)
    semantic_score = fake_score_components.get('semantic_score', 50)
    pattern_score = fake_score_components.get('pattern_score', 0)
    
    # Misinformation likelihood based on multiple features
    enhanced_points = int((linguistic_score + semantic_score + pattern_score) / 3 * 0.3)
    enhanced_points = min(30, max(0, enhanced_points))
    
    # ===== READABILITY/COMPLEXITY COMPONENT (0-15 points) =====
    readability_score = fake_score_components.get('readability_score', 50)
    readability_points = int(readability_score * 0.15)
    readability_points = min(15, max(0, readability_points))
    
    # ===== KEYWORD/CONTENT COMPONENT (0-15 points) =====
    words = text.split()
    word_count = len(words)
    sensational_count = len([k for k in flagged_keywords if " " not in k])
    keyword_points = max(0, 15 - min(sensational_count, 10) * 1.5)
    keyword_points = int(keyword_points)
    
    # ===== LENGTH/SUBSTANCE COMPONENT (0-10 points) =====
    length_points = 10 if word_count >= 150 else int((word_count / 150) * 10)
    length_points = min(10, max(0, length_points))
    
    # ===== APPLY PENALTIES =====
    total = model_points + enhanced_points + readability_points + keyword_points + length_points
    
    # Aggressive conspiracy penalty for FAKE predictions
    if model_prediction == "fake" and conspiracy_count >= 2:
        conspiracy_penalty = min(total - 5, conspiracy_count * 8)
        total = max(5, total - conspiracy_penalty)
    
    # Source credibility indicators
    source_indicators_score = fake_score_components.get('source_indicators_score', 50)
    if source_indicators_score > 60 and model_prediction == "fake":
        # Additional penalty if source indicators are poor
        total = max(5, int(total * 0.85))
    
    total = max(0, min(total, 100))
    
    # Calculate confidence in the prediction
    prediction_confidence = confidence if model_prediction == "fake" else (1 - confidence)
    
    # Create detailed breakdown for explainability
    breakdown = {
        "modelScore": model_points,
        "enhancedAnalysisScore": enhanced_points,
        "readabilityScore": readability_points,
        "keywordScore": keyword_points,
        "lengthScore": length_points,
        "totalWeightedScore": total,
        "predictedClass": model_prediction,
        "predictionConfidence": round(prediction_confidence, 4),
        "wordCount": word_count,
        "flaggedIssues": _identify_issues(detailed_analysis, model_prediction, conspiracy_count),
    }
    
    return total, breakdown


def _identify_issues(analysis: dict, prediction: str, conspiracy_count: int) -> list[str]:
    """Identify specific issues that contribute to fake news classification"""
    issues = []
    
    components = analysis.get('fake_score_components', {})
    ling_features = analysis.get('linguistic_features', {})
    sem_features = analysis.get('semantic_features', {})
    
    # Check linguistic issues
    if ling_features.get('all_caps_ratio', 0) > 0.05:
        issues.append("Excessive capitalization detected")
    
    if ling_features.get('punctuation_ratio', 0) > 0.1:
        issues.append("Unusual punctuation patterns")
    
    if ling_features.get('question_ratio', 0) > 0.3:
        issues.append("Excessive questioning (sensationalism)")
    
    # Check semantic issues
    if sem_features.get('conspiracy_keyword_ratio', 0) > 0.01:
        issues.append("Conspiracy-related language detected")
    
    if sem_features.get('sensational_word_ratio', 0) > 0.02:
        issues.append("Sensational language detected")
    
    if sem_features.get('passive_voice_ratio', 0) > 0.3:
        issues.append("Excessive passive voice (vague claims)")
    
    if sem_features.get('named_entity_ratio', 0) < 0.03:
        issues.append("Lack of specific named entities")
    
    if sem_features.get('quote_count', 0) == 0:
        issues.append("No direct quotes or sources cited")
    
    # Check pattern-based issues
    if analysis.get('pattern_detection', [None, []])[1]:
        issues.append("Obvious fake news patterns detected")
    
    # Check conspiracy keywords
    if conspiracy_count >= 2:
        issues.append("Multiple conspiracy indicators")
    
    return issues[:5]  # Return top 5 issues


def detect_hybrid_article(text: str, model_prediction: str) -> dict:
    """
    Detect if article is REAL NEWS but with FALSE TWEAKS injected.
    
    Hybrid articles are the most dangerous because they appear credible
    but contain fake statistics, misleading framing, or false claims.
    
    Returns analysis with hybrid_risk_score and recommendations.
    """
    hybrid_analysis = hybrid_detector.detect_hybrid_characteristics(text)
    
    # Convert to analysis format
    analysis = {
        'is_hybrid': hybrid_analysis['hybrid_risk_score'] > 40,
        'hybrid_risk_score': hybrid_analysis['hybrid_risk_score'],
        'assessment': hybrid_analysis['assessment'],
        'fake_statistics': hybrid_analysis['fake_statistics'],
        'unverified_claims': hybrid_analysis['unverified_claims'],
        'misleading_framing': hybrid_analysis['misleading_framing'],
        'source_quality_ratio': hybrid_analysis['source_ratio'],
        'credibility_indicators': hybrid_analysis['credibility_indicators'],
    }
    
    # Adjust prediction if hybrid detected and model says "real"
    if model_prediction == "real" and hybrid_analysis['hybrid_risk_score'] > 50:
        analysis['warning'] = "Article appears real but contains unverified/fake elements"
        analysis['recommended_action'] = "FLAG FOR REVIEW - Verify claims independently"
    elif model_prediction == "real" and hybrid_analysis['hybrid_risk_score'] > 35:
        analysis['warning'] = "Article has some unverified claims"
        analysis['recommended_action'] = "Verify key claims before sharing"
    else:
        analysis['warning'] = None
        analysis['recommended_action'] = "Appears authentic"
    
    return analysis
