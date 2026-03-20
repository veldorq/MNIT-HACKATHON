"""
AI-generated text detector for modern LLM outputs (v2 - Enhanced)
Detects patterns common in ChatGPT, Claude, GPT-4, etc.
Uses hybrid approach: pattern matching + statistical analysis
"""

import re
from typing import Dict, Tuple


class AITextDetector:
    """Detect AI-generated text patterns with enhanced detection"""
    
    def __init__(self):
        # Expanded patterns for better detection
        self.patterns = {
            'perfect_structure': {
                'regex': r'\b(however|therefore|furthermore|moreover|additionally|consequently|thus|hence|ultimately|subsequently)\b',
                'weight': 0.20,
                'desc': 'Unnaturally frequent transition words'
            },
            'balanced_tone': {
                'regex': r'(on one hand|on the other hand|while|although|nonetheless|conversely|in contrast|it should be noted)',
                'weight': 0.20,
                'desc': 'Always presents multiple sides'
            },
            'vague_sources': {
                'regex': r'(some experts|researchers say|studies show|it is believed|according to sources|some argue|data suggests|evidence indicates)',
                'weight': 0.22,
                'desc': 'Vague attribution instead of specific sources'
            },
            'statistical_abundance': {
                'regex': r'\b(\d+%|\d+ out of \d+|\d+ million|\d+\.?\d+ billion|\d+\.\d+%)\b',
                'weight': 0.15,
                'desc': 'Too many specific statistics'
            },
            'hedging_language': {
                'regex': r'\b(may|might|could|potentially|arguably|appears to|seems to|tends to|suggests that|could indicate)\b',
                'weight': 0.22,
                'desc': 'Excessive hedging language'
            },
            'corporate_speak': {
                'regex': r'\b(stakeholders|synergy|leverage|optimize|best practices|moving forward|paradigm|scalable|innovative|transformative|strategic|facilitate)\b',
                'weight': 0.18,
                'desc': 'Corporate jargon and business-speak'
            },
            'qualifiers': {
                'regex': r'(to some extent|in a sense|one might argue|it is worth noting|it is important to|it is crucial to|should be noted)',
                'weight': 0.20,
                'desc': 'Excessive qualifiers and softening phrases'
            },
            'no_contractions': {
                'regex': r'\b(cannot|will not|do not|does not|did not|have not|has not)\b',
                'weight': 0.12,
                'desc': 'Avoids contractions (AI tendency)'
            },
            'ai_discourse_markers': {
                'regex': r'(in conclusion|in summary|to summarize|as discussed|as mentioned|as noted|the aforementioned)',
                'weight': 0.15,
                'desc': 'Formal academic/AI discourse markers'
            }
        }
    
    def _calculate_sentence_uniformity(self, text: str) -> float:
        """
        Calculate how uniform sentence lengths are.
        AI tends to write sentences of similar length.
        Returns score 0-1 (higher = more AI-like)
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip().split() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return 0.0
        
        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        
        # Calculate variance in sentence lengths
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        # AI tends to have low std dev (uniform sentences)
        # Human writing has higher variance
        # Normalize: high std dev (>5) = human-like, low std dev (<3) = AI-like
        uniformity_score = max(0, 1 - (std_dev / 5))
        return min(1.0, uniformity_score * 0.8)  # Cap at 0.8 influence
    
    def _calculate_vocabulary_richness(self, text: str) -> float:
        """
        Calculate vocabulary diversity.
        AI often repeats the same advanced words.
        Returns score 0-1 (higher = potentially AI)
        """
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())  # Words 4+ chars
        
        if len(words) < 10:
            return 0.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # Type-token ratio: unique/total
        # AI: lower TTR (5-30%), Human: higher TTR (30-50%)
        ttr = unique_words / total_words
        
        # If TTR is very low (<0.25), suggests repetitive/AI text
        if ttr < 0.25:
            return 0.6  # Moderate AI signal
        elif ttr < 0.3:
            return 0.3
        else:
            return 0.0
    
    def _calculate_punctuation_patterns(self, text: str) -> float:
        """
        Analyze punctuation usage.
        AI tends to use consistent, formal punctuation.
        """
        semicolon_count = text.count(';')
        dash_count = text.count('—') + text.count('--')
        comma_count = text.count(',')
        exclamation_count = text.count('!')
        
        total_chars = len(text)
        
        # AI often overuses certain punctuation
        formal_punctuation_ratio = (semicolon_count * 2 + dash_count) / max(10, total_chars / 100)
        
        # Very low exclamation marks is AI-like (formal tone)
        low_emotion_penalty = 1.0 if exclamation_count == 0 else 0.5
        
        punctuation_score = min(0.5, formal_punctuation_ratio * 0.3) + (0.2 * low_emotion_penalty)
        return min(0.5, punctuation_score)
    
    def detect_ai_indicators(self, text: str) -> Tuple[float, Dict]:
        """
        Analyze text using both pattern matching and statistical analysis.
        
        Returns:
            (ai_probability: float 0-1, breakdown: dict with details)
        """
        if not text or len(text) < 100:
            return 0.0, {'error': 'Text too short for reliable AI detection'}
        
        breakdown = {}
        pattern_score = 0.0
        pattern_count_with_matches = 0
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # ===== PATTERN MATCHING =====
        for pattern_name, pattern_info in self.patterns.items():
            try:
                matches = len(re.findall(pattern_info['regex'], text_lower, re.IGNORECASE))
                
                if matches > 0:
                    density = (matches / max(1, word_count / 100))
                    pattern_contribution = min(
                        pattern_info['weight'] * (1 + min(density, 3)),
                        pattern_info['weight'] * 1.5
                    )
                    pattern_count_with_matches += 1
                else:
                    pattern_contribution = 0.0
                    density = 0.0
                
                breakdown[pattern_name] = {
                    'matches': matches,
                    'density': round(density, 2),
                    'score': round(pattern_contribution, 3),
                    'description': pattern_info['desc']
                }
                
                pattern_score += pattern_contribution
                
            except Exception as e:
                breakdown[pattern_name] = {'error': str(e)}
        
        # ===== STATISTICAL ANALYSIS =====
        sentence_uniformity = self._calculate_sentence_uniformity(text)
        vocabulary_score = self._calculate_vocabulary_richness(text)
        punctuation_score = self._calculate_punctuation_patterns(text)
        
        breakdown['sentence_uniformity'] = {
            'matches': 0,
            'density': round(sentence_uniformity, 2),
            'score': round(sentence_uniformity * 0.15, 3),
            'description': 'Uniform sentence lengths (AI trait)'
        }
        
        breakdown['vocabulary_repetition'] = {
            'matches': 0,
            'density': round(vocabulary_score, 2),
            'score': round(vocabulary_score * 0.12, 3),
            'description': 'Low vocabulary diversity (AI trait)'
        }
        
        breakdown['punctuation_formality'] = {
            'matches': 0,
            'density': round(punctuation_score, 2),
            'score': round(punctuation_score * 0.10, 3),
            'description': 'Formal/uniform punctuation (AI trait)'
        }
        
        # ===== COMBINE SCORES =====
        max_pattern_score = sum(p['weight'] * 1.5 for p in self.patterns.values())
        normalized_pattern_score = min(1.0, pattern_score / max_pattern_score) if max_pattern_score > 0 else 0.0
        
        # Statistical signals weight
        statistical_score = (
            sentence_uniformity * 0.15 +
            vocabulary_score * 0.12 +
            punctuation_score * 0.10
        )
        
        # Combine: 70% patterns, 30% statistical
        combined_score = (normalized_pattern_score * 0.70) + (statistical_score * 0.30)
        
        # Pattern diversity bonus
        pattern_diversity_bonus = min(0.15, (pattern_count_with_matches / len(self.patterns)) * 0.25)
        
        ai_probability = min(1.0, combined_score + pattern_diversity_bonus)
        
        return ai_probability, breakdown
    
    def get_ai_verdict(self, ai_score: float) -> str:
        """Get human-readable verdict about AI likelihood"""
        if ai_score >= 0.65:
            return "Very likely AI-generated"
        elif ai_score >= 0.45:
            return "Possibly AI-generated"
        elif ai_score >= 0.25:
            return "Some AI patterns detected"
        else:
            return "Unlikely to be AI-generated"
