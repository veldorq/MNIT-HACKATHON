#!/usr/bin/env python3
"""
Comprehensive test suite for NewsGuard NLP features
Tests all modern NLP modules: sentiment, NER, semantic, linguistic analysis
"""

import sys
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample test texts
TEST_TEXTS = {
    "obvious_misinformation": """
    SHOCKING DISCOVERY! This incredible miracle cure will change EVERYTHING! 
    Doctors HATE this one weird trick discovered by scientists. 
    Government is hiding the truth. Our exclusive research shows 100% guaranteed results.
    Click here before they ban this video! Breaking news from unnamed sources reveals conspiracy.
    """,
    
    "credible_news": """
    According to a peer-reviewed study published in Nature, researchers found evidence 
    of a new mechanism in disease prevention. The team at Harvard analyzed data from 
    500 participants over five years. Officials stated that results require further verification
    through independent laboratories. The analysis indicates potential therapeutic benefits,
    though more research is needed.
    """,
    
    "polarized_opinion": """
    They're destroying our country with their lies and corruption. We versus them in this 
    devastating battle for truth. These evil conspirators will never be stopped unless 
    patriots rise up NOW. Every single politician is complicit. Always fighting, never giving up.
    """,
    
    "balanced_coverage": """
    The policy has both supporters and critics. On one hand, proponents argue it creates jobs.
    On the other hand, opponents express concerns about environmental impact. Researchers found
    mixed results in preliminary studies. While some metrics improved, others showed decline.
    Experts suggest further analysis before implementation.
    """
}


def test_ner_extractor():
    """Test Named Entity Recognition"""
    print("\n" + "="*80)
    print("TEST 1: Named Entity Recognition (NER)")
    print("="*80)
    
    try:
        from utils.ner_extractor import ner_extractor
        
        text = TEST_TEXTS["credible_news"]
        print(f"\nInput: {text[:100]}...\n")
        
        entities = ner_extractor.extract_entities(text)
        print(f"✓ Extracted Entities:")
        print(f"  - People: {entities['entities']['PERSON']}")
        print(f"  - Organizations: {entities['entities']['ORG']}")
        print(f"  - Locations: {entities['entities']['GPE']}")
        print(f"  - Entity Credibility Score: {entities['entity_credibility_score']}")
        
        verification = ner_extractor.verify_entity_claims(text)
        print(f"\n✓ Entity Claims Verification:")
        print(f"  - Verified Claims: {verification['verified_claims']}")
        print(f"  - Unverified Claims: {verification['unverified_claims']}")
        print(f"  - Verification Score: {verification['verification_score']}")
        
    except ImportError as e:
        print(f"✗ NER module not available: {e}")
        print("Install with: pip install spacy && python -m spacy download en_core_web_sm")


def test_sentiment_analyzer():
    """Test Sentiment and Bias Analysis"""
    print("\n" + "="*80)
    print("TEST 2: Sentiment & Bias Analysis")
    print("="*80)
    
    try:
        from utils.sentiment_analyzer import sentiment_analyzer
        
        for name, text in [("misinformation", TEST_TEXTS["obvious_misinformation"]), 
                          ("polarized", TEST_TEXTS["polarized_opinion"])]:
            print(f"\n--- {name.upper()} TEXT ---")
            print(f"Input: {text[:80]}...\n")
            
            # Sentiment
            sentiment = sentiment_analyzer.analyze_sentiment(text)
            print(f"✓ Sentiment:")
            print(f"  - Overall: {sentiment['overall_sentiment'].upper()}")
            print(f"  - Confidence: {sentiment['confidence']}")
            print(f"  - Emotional Intensity: {sentiment['emotional_intensity']}")
            print(f"  - Manipulation Risk: {sentiment['breakdown'].get('manipulation_score', 'N/A')}")
            
            # Bias
            bias = sentiment_analyzer.detect_bias(text)
            print(f"\n✓ Bias Detection:")
            print(f"  - Bias Score: {bias['bias_score']}")
            print(f"  - Polarization Level: {bias['polarization_level']}")
            print(f"  - Detected Biases: {len(bias['detected_biases'])} categories")
            for bias_cat in bias['detected_biases'][:2]:
                print(f"    - {bias_cat['category']}: {bias_cat['count']} instances")
            
            # Manipulation
            manipulation = sentiment_analyzer.detect_emotional_manipulation(text)
            print(f"\n✓ Emotional Manipulation:")
            print(f"  - Manipulation Score: {manipulation['manipulation_score']}")
            print(f"  - Risk Level: {manipulation['manipulation_risk']}")
            print(f"  - Techniques Found: {len(manipulation['detected_techniques'])}")
            
    except ImportError as e:
        print(f"✗ Sentiment module not available: {e}")


def test_semantic_analyzer():
    """Test Semantic Analysis"""
    print("\n" + "="*80)
    print("TEST 3: Semantic Analysis")
    print("="*80)
    
    try:
        from utils.semantic_analyzer import semantic_analyzer
        
        for name, text in [("misinformation", TEST_TEXTS["obvious_misinformation"]),
                          ("credible", TEST_TEXTS["credible_news"])]:
            print(f"\n--- {name.upper()} TEXT ---")
            print(f"Input: {text[:80]}...\n")
            
            # Semantic similarity
            similarity = semantic_analyzer.get_semantic_similarity(text)
            print(f"✓ Semantic Similarity:")
            print(f"  - Misinformation Similarity: {similarity['misinformation_similarity']}")
            print(f"  - Credible Similarity: {similarity['credible_similarity']}")
            print(f"  - Semantic Risk Score: {similarity['semantic_risk_score']}")
            
            # Coherence
            coherence = semantic_analyzer.detect_semantic_coherence(text)
            print(f"\n✓ Semantic Coherence:")
            print(f"  - Coherence Score: {coherence['coherence_score']}")
            print(f"  - Sentences: {coherence['sentence_count']}")
            print(f"  - Coherence Level: {coherence['breakdown'].get('coherence_level', 'N/A')}")
            
            # Sources
            sources = semantic_analyzer.find_claim_sources(text)
            print(f"\n✓ Claim Sourcing:")
            print(f"  - Attribution Count: {sources['source_attribution_count']}")
            print(f"  - Has URLs: {sources['has_urls']}")
            print(f"  - Source Credibility: {sources['source_credibility_score']}")
            print(f"  - Well Sourced: {sources['is_well_sourced']}")
            
    except ImportError as e:
        print(f"✗ Semantic module not available: {e}")


def test_linguistic_analyzer():
    """Test Linguistic Analysis"""
    print("\n" + "="*80)
    print("TEST 4: Linguistic Analysis")
    print("="*80)
    
    try:
        from utils.linguistic_analyzer import linguistic_analyzer
        
        for name, text in [("misinformation", TEST_TEXTS["obvious_misinformation"]),
                          ("balanced", TEST_TEXTS["balanced_coverage"])]:
            print(f"\n--- {name.upper()} TEXT ---")
            print(f"Input: {text[:80]}...\n")
            
            # Formality
            formality = linguistic_analyzer.analyze_formality(text)
            print(f"✓ Formality Analysis:")
            print(f"  - Formality Score: {formality['formality_score']} (range: -1 to 1)")
            print(f"  - Formal Markers: {formality['formal_markers']}")
            print(f"  - Informal Markers: {formality['informal_markers']}")
            print(f"  - Register Consistency: {formality['register_consistency']}")
            
            # POS Patterns
            pos = linguistic_analyzer.analyze_pos_patterns(text)
            print(f"\n✓ POS Patterns:")
            print(f"  - Adjective Ratio: {pos.get('adjective_ratio', 'N/A')}")
            print(f"  - Passive Voice: {pos.get('passive_voice_ratio', 'N/A')}")
            print(f"  - Modal Verbs: {pos.get('modal_verb_ratio', 'N/A')}")
            print(f"  - Linguistic Risk: {pos['breakdown'].get('linguistic_risk_score', 'N/A')}")
            
            # Readability
            readability = linguistic_analyzer.analyze_readability(text)
            print(f"\n✓ Readability Metrics:")
            print(f"  - Word Count: {readability['word_count']}")
            print(f"  - Flesch-Kincaid Grade: {readability['flesch_kincaid_grade']}")
            print(f"  - Lexical Diversity: {readability['lexical_diversity']}")
            print(f"  - Reading Level: {readability['breakdown']['reading_level']}")
            
            # Hedging
            hedging = linguistic_analyzer.analyze_hedging_language(text)
            print(f"\n✓ Hedging Language:")
            print(f"  - Hedging Count: {hedging['hedging_count']}")
            print(f"  - Hedging Density: {hedging['hedging_density']}")
            print(f"  - Highly Hedged: {hedging['is_highly_hedged']}")
            print(f"  - Vagueness Level: {hedging['breakdown']['vagueness_level']}")
            
    except ImportError as e:
        print(f"✗ Linguistic module not available: {e}")


def test_ensemble_pipeline():
    """Test combined NLP pipeline"""
    print("\n" + "="*80)
    print("TEST 5: Full NLP Pipeline (Ensemble)")
    print("="*80)
    
    text = TEST_TEXTS["obvious_misinformation"]
    print(f"\nAnalyzing: {text[:100]}...\n")
    
    scores = {}
    
    try:
        from utils.sentiment_analyzer import sentiment_analyzer
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        scores['sentiment_risk'] = sentiment['emotional_intensity']
        print(f"✓ Sentiment Risk Score: {scores['sentiment_risk']:.2f}")
    except:
        print("✗ Sentiment analysis failed")
    
    try:
        from utils.semantic_analyzer import semantic_analyzer
        similarity = semantic_analyzer.get_semantic_similarity(text)
        scores['misinformation_similarity'] = similarity['misinformation_similarity']
        print(f"✓ Misinformation Similarity: {scores['misinformation_similarity']:.2f}")
    except:
        print("✗ Semantic analysis failed")
    
    try:
        from utils.linguistic_analyzer import linguistic_analyzer
        readability = linguistic_analyzer.analyze_readability(text)
        scores['reading_complexity'] = readability['breakdown']['complexity_score']
        print(f"✓ Complexity Score: {scores['reading_complexity']:.2f}")
    except:
        print("✗ Linguistic analysis failed")
    
    # Average ensemble score
    if scores:
        ensemble_score = sum(scores.values()) / len(scores)
        print(f"\n📊 ENSEMBLE MISINFORMATION RISK SCORE: {ensemble_score:.2f} (0-1 scale)")
        print(f"   Interpretation: {'HIGH RISK' if ensemble_score > 0.7 else 'MODERATE RISK' if ensemble_score > 0.4 else 'LOW RISK'}")


def main():
    """Main test runner"""
    print("\n" + "="*80)
    print("NEWSGUARD NLP TEST SUITE")
    print("="*80)
    print(f"Testing {len(TEST_TEXTS)} sample texts across 5 NLP modules\n")
    
    test_ner_extractor()
    test_sentiment_analyzer()
    test_semantic_analyzer()
    test_linguistic_analyzer()
    test_ensemble_pipeline()
    
    print("\n" + "="*80)
    print("✓ ALL TESTS COMPLETE")
    print("="*80)
    print("\nInstall full NLP stack:")
    print("  pip install -r backend/requirements_nlp.txt")
    print("  python -m spacy download en_core_web_sm")
    print()


if __name__ == "__main__":
    main()
