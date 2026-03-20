"""
Enhanced fake news detection with advanced text analysis features.
Includes sentiment analysis, linguistic markers, readability metrics, and better pattern detection.
"""

import re
import string
from collections import Counter
from typing import Dict, List, Tuple

# Text analysis utilities using built-in Python libraries
class EnhancedTextAnalyzer:
    """Advanced text analysis for improved fake news detection"""
    
    def __init__(self):
        # Words indicating uncertainty/hedging
        self.hedge_words = {
            'may', 'might', 'could', 'allegedly', 'reportedly', 'supposedly',
            'possibly', 'perhaps', 'claimed', 'said to be', 'apparently',
            'seems', 'appears', 'tend to', 'likely', 'somewhat', 'relatively'
        }
        
        # Sensational/clickbait words
        self.sensational_words = {
            'shocking', 'bombshell', 'explosive', 'scandal', 'outrageous',
            'incredible', 'unbelievable', 'astounding', 'stunning', 'devastating',
            'destroyed', 'exposed', 'secret', 'coverup', 'leaked', 'exclusive'
        }
        
        # Conspiracy/misinformation keywords
        self.conspiracy_keywords = {
            'illuminati', 'reptilians', 'chemtrails', 'flat earth', 'deepfakes',
            'crisis actors', 'false flag', 'government conspiracy', 'cover up',
            'shadow government', 'new world order', 'population control',
            'bill gates', 'microchips', '5g cause', 'hoax', 'fake news',
            'mainstream media lies', 'suppressed', 'silenced'
        }
        
        # Obviously fake patterns
        self.fake_news_patterns = [
            r'(?:\w+\s+){0,3}(?:hate|secret|tricks?|hacks?|doctors?)\s+(?:this|him|her|it|them)',
            r'(?:you|them|we)\s+(?:won\'t|won\'t|won\'t|can\'t|can\'t|can\'t)\s+believe',
            r'(?:click|tap)\s+here',
            r'\d+\s+(?:doctors?|experts?|scientists?)\s+(?:hate|condemn)',
            r'(?:she|he|it)\s+(?:was|is)(?:\s+\w+){0,3}\s+(?:then|next)',
            r'(?:\[?\d+-\w+.{0,30}document|\w+\.pdf)',
            r'(?:banned|forbidden|illegal)\s+(?:video|photo|image)',
        ]
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) 
                                 for pattern in self.fake_news_patterns]
    
    def extract_linguistic_features(self, text: str) -> Dict[str, float]:
        """Extract linguistic markers that correlate with misinformation"""
        features = {}
        
        # Text statistics
        words = text.lower().split()
        features['word_count'] = len(words)
        features['avg_word_length'] = sum(len(w) for w in words) / max(1, len(words))
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]  # Remove empty
        features['sentence_count'] = len(sentences)
        features['avg_sentence_length'] = len(words) / max(1, len(sentences))
        
        # Capitalization (excessive caps often indicates misinformation)
        caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
        features['all_caps_ratio'] = caps_words / max(1, len(words))
        
        # Punctuation intensity (excessive punctuation is suspicious)
        punct_count = sum(1 for c in text if c in string.punctuation)
        features['punctuation_ratio'] = punct_count / max(1, len(text))
        
        # Number density (clickbait often uses numbers)
        numbers = re.findall(r'\d+', text)
        features['number_density'] = len(numbers) / max(1, len(words))
        
        # Question marks (questions often indicate sensationalism)
        features['question_ratio'] = text.count('?') / max(1, len(sentences))
        
        # Exclamation marks
        features['exclamation_ratio'] = text.count('!') / max(1, len(sentences))
        
        return features
    
    def extract_semantic_features(self, text: str) -> Dict[str, float]:
        """Extract semantic indicators of misinformation"""
        features = {}
        text_lower = text.lower()
        words = text_lower.split()
        
        # Hedge word usage (uncertainty indicators)
        hedge_count = sum(1 for word in words if word in self.hedge_words)
        features['hedge_word_ratio'] = hedge_count / max(1, len(words))
        
        # Sensational word usage
        sensational_count = sum(1 for word in words if word in self.sensational_words)
        features['sensational_word_ratio'] = sensational_count / max(1, len(words))
        
        # Conspiracy keywords
        conspiracy_count = sum(1 for word in words if word in self.conspiracy_keywords)
        features['conspiracy_keyword_ratio'] = conspiracy_count / max(1, len(words))
        
        # Named entity mentions (real news usually mentions specific people/places)
        capitalized_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        features['named_entity_ratio'] = len(capitalized_words) / max(1, len(words))
        
        # URL/Link references (fake news often has suspicious links)
        urls = re.findall(r'http[s]?://\S+', text)
        features['url_count'] = len(urls)
        
        # Quote usage (real news often quotes sources)
        quotes = len(re.findall(r'["\'].*?["\']', text))
        features['quote_count'] = quotes
        
        # Passive voice indicators (vague, often in fake news)
        passive_patterns = re.findall(r'\b(?:is|are|was|were)\s+\w+(?:ed|en)\b', text_lower)
        features['passive_voice_ratio'] = len(passive_patterns) / max(1, len(words))
        
        return features
    
    def calculate_readability_metrics(self, text: str) -> Dict[str, float]:
        """Calculate readability and complexity metrics"""
        metrics = {}
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {
                'flesch_kincaid_grade': 0,
                'lexical_diversity': 0,
                'complexity_score': 0
            }
        
        # Flesch-Kincaid Grade approximation
        syllable_count = self._count_syllables(text)
        fk_grade = (0.39 * (len(words) / max(1, len(sentences))) + 
                   11.8 * (syllable_count / max(1, len(words))) - 15.59)
        metrics['flesch_kincaid_grade'] = max(0, fk_grade)
        
        # Lexical diversity (unique words / total words)
        unique_words = set(w.lower() for w in words if w.isalpha())
        metrics['lexical_diversity'] = len(unique_words) / max(1, len(words))
        
        # Complexity score: easier reading often correlates with misinformation
        # (targeting broad audiences, avoiding complexity)
        metrics['complexity_score'] = metrics['flesch_kincaid_grade'] * metrics['lexical_diversity']
        
        return metrics
    
    @staticmethod
    def _count_syllables(text: str) -> int:
        """Estimate syllable count (approximation)"""
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in text.lower():
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjustments
        if text.lower().endswith('e'):
            syllable_count -= 1
        if text.lower().endswith('le') and len(text) > 2:
            syllable_count += 1
        
        return max(1, syllable_count)
    
    def detect_obvious_fake_patterns(self, text: str) -> Tuple[int, List[str]]:
        """Detect obvious fake news patterns"""
        matches = []
        
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                matches.append(pattern.pattern)
        
        return len(matches), matches
    
    def calculate_fake_score_components(self, text: str) -> Dict[str, float]:
        """
        Calculate individual component scores for fake news likelihood.
        Returns dict with scores 0-100 for different aspects.
        """
        components = {}
        
        # Linguistic features analysis
        ling_features = self.extract_linguistic_features(text)
        components['linguistic_score'] = self._score_linguistic(ling_features)
        
        # Semantic features analysis
        sem_features = self.extract_semantic_features(text)
        components['semantic_score'] = self._score_semantic(sem_features)
        
        # Readability analysis
        readability = self.calculate_readability_metrics(text)
        components['readability_score'] = self._score_readability(readability)
        
        # Pattern detection
        pattern_count, _ = self.detect_obvious_fake_patterns(text)
        components['pattern_score'] = min(100, pattern_count * 15)
        
        # Sensationalism score
        components['sensationalism_score'] = self._score_sensationalism(ling_features, sem_features)
        
        # Source credibility indicators
        components['source_indicators_score'] = self._score_source_indicators(sem_features)
        
        return components
    
    @staticmethod
    def _score_linguistic(features: Dict[str, float]) -> float:
        """Score based on linguistic features (0-100)"""
        score = 50  # Neutral baseline
        
        # Excessive caps is suspicious
        score += features.get('all_caps_ratio', 0) * 100
        
        # Excessive punctuation is suspicious
        score += features.get('punctuation_ratio', 0) * 50
        
        # Question heavy content
        score += features.get('question_ratio', 0) * 20
        
        # Exclamation heavy
        score += features.get('exclamation_ratio', 0) * 20
        
        return min(100, max(0, score))
    
    @staticmethod
    def _score_semantic(features: Dict[str, float]) -> float:
        """Score based on semantic features (0-100)"""
        score = 50  # Neutral baseline
        
        # Conspiracy keywords are major red flag
        score += features.get('conspiracy_keyword_ratio', 0) * 100
        
        # Sensational words increase suspicion
        score += features.get('sensational_word_ratio', 0) * 60
        
        # Low named entities might indicate vague claims
        if features.get('named_entity_ratio', 0) < 0.05:
            score += 20
        
        # Passive voice often vague
        score += features.get('passive_voice_ratio', 0) * 40
        
        return min(100, max(0, score))
    
    @staticmethod
    def _score_readability(metrics: Dict[str, float]) -> float:
        """Score based on readability metrics (0-100)"""
        score = 50
        
        # Very low complexity (too simple) can indicate misinformation for serious topics
        complexity = metrics.get('complexity_score', 0)
        if complexity < 0.1:
            score += 20
        elif complexity > 0.4:
            score -= 15  # More complex = likely more credible
        
        # Very low lexical diversity
        if metrics.get('lexical_diversity', 0) < 0.3:
            score += 15
        
        return min(100, max(0, score))
    
    @staticmethod
    def _score_sensationalism(ling: Dict[str, float], sem: Dict[str, float]) -> float:
        """Dedicated sensationalism scoring"""
        score = 50
        
        score += sem.get('sensational_word_ratio', 0) * 100
        score += ling.get('all_caps_ratio', 0) * 40
        
        return min(100, max(0, score))
    
    @staticmethod
    def _score_source_indicators(features: Dict[str, float]) -> float:
        """Score source credibility indicators"""
        score = 50
        
        # No quotes? Suspicious
        if features.get('quote_count', 0) == 0:
            score += 15
        
        # Few named entities? Suspicious
        if features.get('named_entity_ratio', 0) < 0.03:
            score += 20
        
        # URLs present? Could be suspicious linking
        if features.get('url_count', 0) > 2:
            score += 15
        
        return min(100, max(0, score))
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """Get comprehensive text analysis for explainability"""
        return {
            'linguistic_features': self.extract_linguistic_features(text),
            'semantic_features': self.extract_semantic_features(text),
            'readability': self.calculate_readability_metrics(text),
            'fake_score_components': self.calculate_fake_score_components(text),
            'pattern_detection': self.detect_obvious_fake_patterns(text),
        }


# Global instance
enhanced_analyzer = EnhancedTextAnalyzer()
