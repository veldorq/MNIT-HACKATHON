"""
Linguistic analysis for fake news detection
Analyzes formality, complexity, POS patterns, and linguistic markers
"""

import logging
from typing import Dict, List, Tuple
import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class LinguisticAnalyzer:
    """Analyze linguistic patterns and formality markers"""
    
    def __init__(self):
        self.contractions = {
            "can't", "won't", "don't", "doesn't", "couldn't", "shouldn't",
            "isn't", "aren't", "wasn't", "weren't", "it's", "i'm", "we're",
            "they're", "you're", "i've", "we've", "they've", "he's"
        }
        
        self.formal_markers = {
            'would': 'formal', 'could': 'formal', 'furthermore': 'formal',
            'moreover': 'formal', 'thereby': 'formal', 'hence': 'formal',
            'thus': 'formal', 'therefore': 'formal', 'albeit': 'formal',
            'notwithstanding': 'formal', 'heretofore': 'formal'
        }
        
        self.informal_markers = {
            'gonna': 'informal', 'wanna': 'informal', 'gotta': 'informal',
            'kinda': 'informal', 'sorta': 'informal', 'ya': 'informal',
            'dude': 'informal', 'yeah': 'informal', 'nope': 'informal'
        }
    
    def analyze_formality(self, text: str) -> Dict:
        """
        Analyze formality level of text
        Fake news often has inconsistent formality
        """
        text_lower = text.lower()
        words = word_tokenize(text)
        
        formal_count = 0
        informal_count = 0
        contraction_count = len([w for w in words if w in self.contractions])
        
        for word in words:
            if word in self.formal_markers:
                formal_count += 1
            elif word in self.informal_markers:
                informal_count += 1
        
        total_words = len(words)
        formality_score = (formal_count - informal_count) / max(1, total_words / 10)
        formality_score = max(-1.0, min(1.0, formality_score))  # Clamp to [-1, 1]
        
        # Identify inconsistent mix
        has_mixed_register = (formal_count > 0 and informal_count > 0) and contraction_count > 2
        
        return {
            'formality_score': round(formality_score, 3),  # -1 = very informal, 1 = very formal
            'formal_markers': formal_count,
            'informal_markers': informal_count,
            'contractions': contraction_count,
            'register_consistency': 'INCONSISTENT' if has_mixed_register else 'CONSISTENT',
            'breakdown': {
                'is_formal': formality_score > 0.3,
                'is_casual': formality_score < -0.3,
                'mixed_register_risk': 'HIGH' if has_mixed_register else 'LOW'
            }
        }
    
    def analyze_pos_patterns(self, text: str) -> Dict:
        """
        Analyze part-of-speech patterns
        Fake news often overuses certain grammatical structures
        """
        try:
            words = word_tokenize(text)
            if len(words) > 500:
                words = words[:500]  # Limit for performance
            
            pos_tags = pos_tag(words)
            
            # Count POS frequencies
            pos_counts = {}
            for word, tag in pos_tags:
                pos_counts[tag] = pos_counts.get(tag, 0) + 1
            
            # Analyze specific patterns
            total_words = len(words)
            
            # Adjectives (often used in emotional language)
            adjective_ratio = pos_counts.get('JJ', 0) / max(1, total_words)
            
            # Passive voice markers (weak writing)
            passive_verbs = pos_counts.get('VBN', 0)  # Past participles
            passive_markers = ['is', 'are', 'was', 'were']
            passive_ratio = passive_verbs / max(1, total_words)
            
            # Question marks (sensationalism)
            questions = text.count('?')
            question_density = questions / max(1, len(text.split('.')))
            
            # Modal verbs (uncertainty/speculation)
            modal_verbs = ['MD']
            modal_count = pos_counts.get('MD', 0)
            modal_ratio = modal_count / max(1, total_words)
            
            return {
                'adjective_ratio': round(adjective_ratio, 3),
                'passive_voice_ratio': round(passive_ratio, 3),
                'modal_verb_ratio': round(modal_ratio, 3),
                'question_density': round(question_density, 3),
                'pos_distribution': {tag: count for tag, count in list(pos_counts.items())[:10]},
                'breakdown': {
                    'high_adjective_use': adjective_ratio > 0.15,  # > 15% suspicious
                    'excessive_passive': passive_ratio > 0.20,
                    'high_speculation': modal_ratio > 0.10,
                    'sensationalism_indicators': questions > 3,
                    'linguistic_risk_score': round(
                        (adjective_ratio * 0.3 + passive_ratio * 0.2 + modal_ratio * 0.25 + min(question_density, 1.0) * 0.25),
                        3
                    )
                }
            }
        except Exception as e:
            logger.error(f"POS analysis error: {e}")
            return {
                'breakdown': {'error': str(e)}
            }
    
    def analyze_readability(self, text: str) -> Dict:
        """
        Analyze readability and complexity metrics
        """
        words = text.split()
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        
        # Average word length
        avg_word_length = sum(len(w) for w in words) / max(1, word_count)
        
        # Average sentence length
        avg_sentence_length = word_count / max(1, sentence_count)
        
        # Flesch-Kincaid Grade (simplified)
        syllable_count = self._count_syllables(text)
        fk_grade = (0.39 * (word_count / max(1, sentence_count)) + 
                   11.8 * (syllable_count / max(1, word_count)) - 15.59)
        fk_grade = max(0, min(fk_grade, 18))  # Clamp 0-18
        
        # Lexical diversity
        unique_words = len(set(w.lower() for w in words if w.isalpha()))
        lexical_diversity = unique_words / max(1, word_count)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'flesch_kincaid_grade': round(fk_grade, 1),
            'lexical_diversity': round(lexical_diversity, 3),
            'breakdown': {
                'reading_level': 'COLLEGE+' if fk_grade > 12 else 'HIGH SCHOOL' if fk_grade > 9 else 'MIDDLE SCHOOL',
                'reading_ease': 'EASY' if fk_grade < 8 else 'MODERATE' if fk_grade < 12 else 'DIFFICULT',
                'is_readable': fk_grade < 12,
                'complexity_score': round(fk_grade / 18, 3)  # Normalized 0-1
            }
        }
    
    def analyze_hedging_language(self, text: str) -> Dict:
        """Detect hedging language and uncertainty markers"""
        text_lower = text.lower()
        
        hedging_words = {
            'may': 1, 'might': 1, 'could': 1, 'possibly': 2, 'apparently': 2,
            'allegedly': 2, 'reportedly': 2, 'supposedly': 2, 'seems': 1,
            'appears': 1, 'tends to': 2, 'somewhat': 1, 'relatively': 1,
            'rather': 1, 'quite': 1, 'sort of': 2, 'kind of': 2
        }
        
        hedging_count = 0
        found_hedges = []
        
        for hedge, weight in hedging_words.items():
            count = text_lower.count(hedge)
            if count > 0:
                hedging_count += count * weight
                found_hedges.append({'phrase': hedge, 'count': count})
        
        word_count = len(text.split())
        hedging_density = hedging_count / max(1, word_count)
        
        # High hedging = vague claims (potentially fake)
        is_highly_hedged = hedging_density > 0.05  # > 5% hedging
        
        return {
            'hedging_count': hedging_count,
            'hedging_density': round(hedging_density, 3),
            'is_highly_hedged': is_highly_hedged,
            'found_hedging_phrases': found_hedges,
            'breakdown': {
                'vagueness_level': 'HIGH' if is_highly_hedged else 'NORMAL',
                'claim_confidence_risk': 'HIGH' if is_highly_hedged else 'LOW',
                'hedging_risk_score': round(min(1.0, hedging_density * 20), 3)
            }
        }
    
    @staticmethod
    def _count_syllables(text: str) -> int:
        """Estimate syllable count"""
        vowels = 'aeiouy'
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


# Initialize analyzer
linguistic_analyzer = LinguisticAnalyzer()


if __name__ == "__main__":
    test_text = "This incredible discovery might possibly change everything! According to our sources, doctors could be hiding this secret cure. What are you waiting for?"
    
    formality = linguistic_analyzer.analyze_formality(test_text)
    print(f"Formality: {formality}\n")
    
    pos = linguistic_analyzer.analyze_pos_patterns(test_text)
    print(f"POS Patterns: {pos}\n")
    
    readability = linguistic_analyzer.analyze_readability(test_text)
    print(f"Readability: {readability}\n")
    
    hedging = linguistic_analyzer.analyze_hedging_language(test_text)
    print(f"Hedging: {hedging}")
