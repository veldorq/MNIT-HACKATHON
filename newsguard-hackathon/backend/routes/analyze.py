from flask import Blueprint, jsonify, request
from typing import Any
import logging

from utils.model_loader import ModelManager
from utils.scorer import calculate_credibility_score, extract_flagged_keywords, calculate_enhanced_credibility_score, detect_hybrid_article
from utils.text_processor import clean_text
from utils.groq_analyzer import verify_url_credibility
from utils.enhanced_analyzer import enhanced_analyzer
from utils.ai_detector import AITextDetector

# Setup logging
logger = logging.getLogger(__name__)

analyze_bp = Blueprint("analyze", __name__)
model_manager = ModelManager()
ai_detector = AITextDetector()


@analyze_bp.get("/models")
def list_models():
    return jsonify({"models": model_manager.get_catalog()})


@analyze_bp.post("/analyze")
def analyze_news():
    """
    Main endpoint for FAKE NEWS DETECTION with optional URL verification.
    
    Two INDEPENDENT features:
    1. CORE: Fake news detection (ML model) - ALWAYS performed
    2. OPTIONAL: URL credibility verification (Groq API) - if check_url=True
    """
    logger.info("=== POST /analyze endpoint called ===")
    
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    mode = payload.get("mode")
    url = payload.get("url", "")
    check_url = payload.get("check_url", False)
    enhanced = payload.get("enhanced", False)  # Enable detailed analysis

    # Validate text input
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "No text provided"}), 400

    word_count = len(text.strip().split())
    if len(text.strip()) < 80 or word_count < 12:
        return (
            jsonify(
                {
                    "error": "Insufficient context. Please provide a longer article excerpt (at least 80 characters and 12 words)."
                }
            ),
            400,
        )

    if len(text) > 30000:
        return jsonify({"error": "Text is too long. Keep input under 30,000 characters."}), 400

    cleaned_text = clean_text(text)
    
    # ===== FEATURE 1: FAKE NEWS DETECTION (MAIN - Always performed) =====
    try:
        model_output = model_manager.predict(cleaned_text, mode=mode)
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    confidence_value: Any = model_output.get("confidence", 0.5)
    prediction = str(model_output.get("prediction", "fake"))
    confidence = float(confidence_value)
    provider = str(model_output.get("provider", "unknown"))
    selected_mode = str(model_output.get("mode", mode or "hybrid"))

    flagged = extract_flagged_keywords(cleaned_text)
    
    # Use enhanced scoring if requested, otherwise use standard scoring
    if enhanced:
        score, breakdown = calculate_enhanced_credibility_score(
            model_prediction=prediction,
            confidence=confidence,
            text=cleaned_text,
            flagged_keywords=flagged,
        )
    else:
        score, breakdown = calculate_credibility_score(
            model_prediction=prediction,
            confidence=confidence,
            text=cleaned_text,
            flagged_keywords=flagged,
        )

    # Build MAIN response (Fake News Detection)
    response = {
        "fakeNewsAnalysis": {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "credibilityScore": score,
            "breakdown": breakdown,
            "flaggedKeywords": flagged,
            "provider": provider,
            "mode": selected_mode,
            "ensemble": model_output.get("ensemble"),
        }
    }
    
    # Add detailed analysis if enhanced mode is requested
    if enhanced:
        detailed_analysis = enhanced_analyzer.get_detailed_analysis(cleaned_text)
        response["detailedAnalysis"] = {
            "linguisticFeatures": detailed_analysis.get("linguistic_features", {}),
            "semanticFeatures": detailed_analysis.get("semantic_features", {}),
            "readabilityMetrics": detailed_analysis.get("readability", {}),
            "fakeScoreComponents": detailed_analysis.get("fake_score_components", {}),
            "patternDetection": {
                "count": detailed_analysis.get("pattern_detection", [0])[0],
                "patterns": detailed_analysis.get("pattern_detection", [0, []])[1]
            }
        }

    # ===== FEATURE 1.5: AI GENERATION DETECTION =====
    # Detect if text appears to be AI-generated (ChatGPT, Claude, etc.)
    ai_score, ai_breakdown = ai_detector.detect_ai_indicators(cleaned_text)
    ai_verdict = ai_detector.get_ai_verdict(ai_score)
    
    response["aiGenerationAnalysis"] = {
        "aiScore": round(ai_score, 3),
        "verdict": ai_verdict,
        "indicators": ai_breakdown,
        "disclaimer": "This model detects patterns common in modern LLMs. Best on 2016-2018 data. May misclassify well-written real news or human-written sophisticated articles."
    }

    # ===== FEATURE 3: HYBRID ARTICLE DETECTION (Real news with false tweaks) =====
    # Always perform hybrid detection for real news predictions
    if prediction == "real":
        logger.info("Performing hybrid article detection...")
        hybrid_analysis = detect_hybrid_article(cleaned_text, prediction)
        response["hybridAnalysis"] = hybrid_analysis
        
        if hybrid_analysis.get('is_hybrid'):
            logger.warning(f"HYBRID ARTICLE DETECTED: Risk score {hybrid_analysis['hybrid_risk_score']}")

    # ===== FEATURE 2: URL VERIFICATION (Optional - Groq API) =====
    if check_url and url:
        try:
            logger.info(f"Verifying URL credibility for: {url}")
            url_analysis = verify_url_credibility(url)
            response["urlAnalysis"] = url_analysis
            logger.info(f"URL analysis complete: {url_analysis.get('risk_level')}")
        except Exception as e:
            logger.error(f"URL verification failed: {str(e)}")
            response["urlAnalysis"] = {"error": f"URL verification failed: {str(e)}"}

    logger.info(f"Analysis complete. Features enabled: fake_news=true, url={check_url}")
    return jsonify(response)
