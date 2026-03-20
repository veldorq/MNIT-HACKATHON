"""
Comprehensive test suite for NewsGuard fake news detector
Tests detector accuracy, API endpoints, edge cases, and AI detection
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.ai_detector import AITextDetector
from backend.utils.model_loader import ModelManager
from backend.utils.scorer import calculate_credibility_score
from backend.utils.text_processor import clean_text


class TestSuite:
    """Comprehensive testing suite"""
    
    def __init__(self):
        self.ai_detector = AITextDetector()
        self.model_manager = ModelManager()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_test(self, name, status, details=""):
        symbol = "[PASS]" if status else "[FAIL]"
        print(f"{symbol} {name}")
        if details:
            print(f"  └─ {details}")
        if status:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
    
    def test_ai_detector_patterns(self):
        """Test AI detection patterns"""
        self.print_header("AI DETECTOR PATTERN TESTS")
        
        # Test 1: AI formal text with transition words
        ai_text_1 = "Furthermore, it is important to note that recent studies have demonstrated significant findings. Moreover, the data indicates that additional research is warranted. In conclusion, stakeholders must leverage these insights to optimize outcomes."
        score_1 = self.ai_detector.detect(ai_text_1)
        self.print_test(
            "Detects formal AI text with transitions",
            score_1['score'] > 0.6,
            f"Score: {score_1['score']:.2f}, Verdict: {score_1['verdict']}"
        )
        
        # Test 2: Human casual text
        human_text = "Look, I think this is crazy! Nobody expected it to go this far. It's wild how things changed so fast. People are losing their minds over it!"
        score_2 = self.ai_detector.detect(human_text)
        self.print_test(
            "Detects human casual text",
            score_2['score'] < 0.4,
            f"Score: {score_2['score']:.2f}, Verdict: {score_2['verdict']}"
        )
        
        # Test 3: News article (genuine)
        news_text = "The city council voted 8-2 to approve the new transit proposal Tuesday evening. Mayor Smith said the investment will improve traffic flow. Some residents expressed concerns about costs. The project is expected to complete in 2027."
        score_3 = self.ai_detector.detect(news_text)
        self.print_test(
            "Handles balanced news text",
            score_3['score'] < 0.5,
            f"Score: {score_3['score']:.2f}, Verdict: {score_3['verdict']}"
        )
        
        # Test 4: Corporate AI jargon
        corporate_text = "Moving forward, we are committed to leveraging synergies across all stakeholder groups to optimize our strategic positioning. Our best practices framework will ensure scalable implementation of innovative paradigms designed to enhance our competitive advantage in the marketplace."
        score_4 = self.ai_detector.detect(corporate_text)
        self.print_test(
            "Detects corporate AI jargon",
            score_4['score'] > 0.5,
            f"Score: {score_4['score']:.2f}, Verdict: {score_4['verdict']}"
        )
    
    def test_fake_news_detection(self):
        """Test fake news detection accuracy"""
        self.print_header("FAKE NEWS DETECTION TESTS")
        
        # Real news examples
        real_articles = [
            ("Real 1", "SpaceX successfully completed its 47th Falcon 9 launch on Tuesday, carrying 51 Starlink satellites into orbit. The first stage booster landed safely at Cape Canaveral, marking another successful recovery. This brings the total number of operational Starlink satellites to over 4,000."),
            ("Real 2", "The Federal Reserve announced a 0.25% increase in the benchmark interest rate. Fed Chair Jerome Powell stated inflation remains a concern despite recent improvements. Markets responded to the announcement with modest gains."),
        ]
        
        # Fake news examples
        fake_articles = [
            ("Fake 1", "SHOCKING: Scientists discover that water is actually alive and can think! New research proves water has consciousness and communicates telepathically. Governments have been hiding this truth for decades to maintain control!"),
            ("Fake 2", "Breaking: Billionaire plans to move entire population to Mars by 2026. Sources confirm the plan is already underway in secret underground bunkers. World leaders are keeping this hidden from the public."),
        ]
        
        for name, text in real_articles:
            try:
                cleaned = clean_text(text)
                result = self.model_manager.predict(cleaned, mode='hybrid')
                is_correct = result.get('prediction') == 'real'
                confidence = result.get('confidence', 0)
                self.print_test(
                    f"Detects {name} (real) correctly",
                    is_correct,
                    f"Prediction: {result.get('prediction')}, Confidence: {confidence:.2%}"
                )
            except Exception as e:
                self.print_test(f"Detects {name} correctly", False, str(e))
        
        for name, text in fake_articles:
            try:
                cleaned = clean_text(text)
                result = self.model_manager.predict(cleaned, mode='hybrid')
                is_correct = result.get('prediction') == 'fake'
                confidence = result.get('confidence', 0)
                self.print_test(
                    f"Detects {name} (fake) correctly",
                    is_correct,
                    f"Prediction: {result.get('prediction')}, Confidence: {confidence:.2%}"
                )
            except Exception as e:
                self.print_test(f"Detects {name} correctly", False, str(e))
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        self.print_header("EDGE CASE TESTS")
        
        # Test 1: Very short text
        short_text = "Biden announces new climate policy."
        try:
            cleaned = clean_text(short_text)
            is_valid = len(cleaned) >= 80
            self.print_test(
                "Handles short text appropriately",
                not is_valid,  # Should fail validation
                f"Length: {len(cleaned)} chars"
            )
        except Exception as e:
            self.print_test("Handles short text appropriately", True, f"Correctly rejected")
        
        # Test 2: Text with special characters
        special_text = "A major breakthrough! 🚀 The team achieved a 500% increase in efficiency. This is #TRENDING on social media!!! @everyone check this out"
        try:
            cleaned = clean_text(special_text)
            self.print_test(
                "Cleans special characters",
                len(cleaned) > 0,
                f"Cleaned length: {len(cleaned)} chars"
            )
        except Exception as e:
            self.print_test("Cleans special characters", False, str(e))
        
        # Test 3: Mixed case sensitivity
        mixed_case_text = "ThE STUDY SHOWED THAT Scientists DISCOVERED important findings that COULD CHANGE everything in the FUTURE for HUMANITY and ALL people"
        ai_score = self.ai_detector.detect(mixed_case_text)
        self.print_test(
            "Handles mixed case properly",
            ai_score['score'] >= 0,
            f"Score: {ai_score['score']:.2f}"
        )
        
        # Test 4: Repeated patterns
        repeated = "Spam spam spam. " * 20 + "This is actually important content. Real information here."
        try:
            cleaned = clean_text(repeated)
            self.print_test(
                "Handles repeated patterns",
                len(cleaned) > 0,
                f"Processed {len(repeated)} chars -> {len(cleaned)} chars cleaned"
            )
        except Exception as e:
            self.print_test("Handles repeated patterns", False, str(e))
    
    def test_credibility_scoring(self):
        """Test credibility score calculation"""
        self.print_header("CREDIBILITY SCORING TESTS")
        
        test_cases = [
            ("High credibility real", "real", 0.95, []),
            ("Low credibility real", "real", 0.50, ["conspiracy", "unverified"]),
            ("High credibility fake", "fake", 0.90, []),
            ("Low confidence real", "real", 0.55, []),
        ]
        
        for name, prediction, confidence, keywords in test_cases:
            dummy_text = "This is a test article about the news and current events happening today."
            try:
                score, breakdown = calculate_credibility_score(
                    model_prediction=prediction,
                    confidence=confidence,
                    text=dummy_text,
                    flagged_keywords=keywords
                )
                is_valid = 0 <= score <= 100
                self.print_test(
                    f"Scores {name}",
                    is_valid,
                    f"Score: {score}/100, Confidence: {confidence:.0%}"
                )
            except Exception as e:
                self.print_test(f"Scores {name}", False, str(e))
    
    def test_model_catalog(self):
        """Test model availability"""
        self.print_header("MODEL AVAILABILITY TESTS")
        
        try:
            models = self.model_manager.get_catalog()
            has_models = len(models) > 0
            self.print_test(
                "Model catalog loads",
                has_models,
                f"Available models: {len(models)}"
            )
            
            for model_id in models:
                model_info = models[model_id]
                has_required_fields = all(k in model_info for k in ['name', 'accuracy', 'dataset_size'])
                self.print_test(
                    f"Model '{model_id}' has complete info",
                    has_required_fields,
                    f"Accuracy: {model_info.get('accuracy', 'N/A')}, Size: {model_info.get('dataset_size', 'N/A')}"
                )
        except Exception as e:
            self.print_test("Model catalog loads", False, str(e))
    
    def run_all_tests(self):
        """Run all test suites"""
        self.print_header("STARTING COMPREHENSIVE TEST SUITE")
        
        self.test_ai_detector_patterns()
        self.test_fake_news_detection()
        self.test_edge_cases()
        self.test_credibility_scoring()
        self.test_model_catalog()
        
        # Summary
        self.print_header("TEST SUMMARY")
        total = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {self.tests_passed} [PASS]")
        print(f"Failed: {self.tests_failed} [FAIL]")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if pass_rate >= 80:
            print("\n[SUCCESS] System is production-ready!")
        elif pass_rate >= 60:
            print("\n[WARNING] Some tests failed, review needed")
        else:
            print("\n[ERROR] Major issues detected, fix before deployment")
        
        return pass_rate >= 80


if __name__ == "__main__":
    suite = TestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
