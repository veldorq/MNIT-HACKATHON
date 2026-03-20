from flask import Blueprint, jsonify, request
from typing import Any
import logging

from utils.model_loader import ModelManager
from utils.scorer import calculate_credibility_score, extract_flagged_keywords, calculate_enhanced_credibility_score, detect_hybrid_article
from utils.text_processor import clean_text
from utils.groq_analyzer import verify_url_credibility
from utils.enhanced_analyzer import enhanced_analyzer
from utils.ai_detector import AITextDetector

# ===== NEW: NLP MODULES =====
try:
    from utils.ner_extractor import ner_extractor
    from utils.sentiment_analyzer import sentiment_analyzer
    from utils.semantic_analyzer import semantic_analyzer
    from utils.linguistic_analyzer import linguistic_analyzer
    NLP_AVAILABLE = True
    logger_init = logging.getLogger(__name__)
    logger_init.info("✓ NLP modules loaded successfully")
except Exception as e:
    NLP_AVAILABLE = False
    logger_init = logging.getLogger(__name__)
    logger_init.warning(f"NLP modules not available: {e}. Install with: pip install -r requirements_nlp.txt")

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
    Main endpoint for FAKE NEWS DETECTION with optional NLP and URL verification.
    
    Features:
    1. CORE: Fake news detection (ML model) - ALWAYS performed
    2. NEW: Modern NLP analysis (sentiment, NER, semantic, linguistic) - if use_nlp=true
    3. OPTIONAL: URL credibility verification (Groq API) - if check_url=true
    """
    logger.info("=== POST /analyze endpoint called ===")
    
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    mode = payload.get("mode")
    url = payload.get("url", "")
    check_url = payload.get("check_url", False)
    enhanced = payload.get("enhanced", False)
    use_nlp = payload.get("use_nlp", False)  # NEW: Enable NLP analysis

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

    # ===== FEATURE 2: MODERN NLP ANALYSIS (NEW) =====
    if use_nlp and NLP_AVAILABLE:
        logger.info("Performing deep NLP analysis...")
        try:
            nlp_analysis = {}
            
            # 2.1: Sentiment & Bias Analysis
            logger.debug("Analyzing sentiment and bias...")
            nlp_analysis["sentiment"] = sentiment_analyzer.analyze_sentiment(cleaned_text)
            nlp_analysis["bias"] = sentiment_analyzer.detect_bias(cleaned_text)
            nlp_analysis["emotionalManipulation"] = sentiment_analyzer.detect_emotional_manipulation(cleaned_text)
            
            # 2.2: Named Entity Recognition
            logger.debug("Extracting named entities...")
            nlp_analysis["entities"] = ner_extractor.extract_entities(cleaned_text)
            nlp_analysis["entityVerification"] = ner_extractor.verify_entity_claims(cleaned_text)
            
            # 2.3: Semantic Analysis
            logger.debug("Analyzing semantic similarity and coherence...")
            nlp_analysis["semanticSimilarity"] = semantic_analyzer.get_semantic_similarity(cleaned_text)
            nlp_analysis["coherence"] = semantic_analyzer.detect_semantic_coherence(cleaned_text)
            nlp_analysis["sourceCitations"] = semantic_analyzer.find_claim_sources(cleaned_text)
            
            # 2.4: Linguistic Analysis
            logger.debug("Analyzing linguistic patterns...")
            nlp_analysis["formality"] = linguistic_analyzer.analyze_formality(cleaned_text)
            nlp_analysis["posPatterns"] = linguistic_analyzer.analyze_pos_patterns(cleaned_text)
            nlp_analysis["readability"] = linguistic_analyzer.analyze_readability(cleaned_text)
            nlp_analysis["hedgingLanguage"] = linguistic_analyzer.analyze_hedging_language(cleaned_text)
            
            response["nlpAnalysis"] = nlp_analysis
            
            logger.info("✓ NLP analysis complete")
        except Exception as e:
            logger.error(f"NLP analysis error: {e}")
            response["nlpAnalysis"] = {"error": f"NLP analysis failed: {str(e)}"}
    elif use_nlp and not NLP_AVAILABLE:
        response["nlpAnalysis"] = {
            "error": "NLP modules not available",
            "resolution": "Install with: pip install -r backend/requirements_nlp.txt && python -m spacy download en_core_web_sm"
        }

    # ===== FEATURE 3: HYBRID ARTICLE DETECTION (Real news with false tweaks) =====
    # Always perform hybrid detection for real news predictions
    if prediction == "real":
        logger.info("Performing hybrid article detection...")
        hybrid_analysis = detect_hybrid_article(cleaned_text, prediction)
        response["hybridAnalysis"] = hybrid_analysis
        
        if hybrid_analysis.get('is_hybrid'):
            logger.warning(f"HYBRID ARTICLE DETECTED: Risk score {hybrid_analysis['hybrid_risk_score']}")

    # ===== FEATURE 4: URL VERIFICATION (Optional - Groq API) =====
    if check_url and url:
        try:
            logger.info(f"Verifying URL credibility for: {url}")
            url_analysis = verify_url_credibility(url)
            response["urlAnalysis"] = url_analysis
            logger.info(f"URL analysis complete: {url_analysis.get('risk_level')}")
        except Exception as e:
            logger.error(f"URL verification failed: {str(e)}")
            response["urlAnalysis"] = {"error": f"URL verification failed: {str(e)}"}

    features_enabled = f"fake_news=true, nlp={use_nlp}, url={check_url}"
    logger.info(f"Analysis complete. Features enabled: {features_enabled}")
    return jsonify(response)
