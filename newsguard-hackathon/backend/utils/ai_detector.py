"""
AI-generated text detector for modern LLM outputs
Detects patterns common in ChatGPT, Claude, GPT-4, etc.
"""

import re
from typing import Dict, Tuple


class AITextDetector:
    """Detect AI-generated text patterns"""
    
    def __init__(self):
        # Patterns common in AI-generated text (higher weights = more indicative of AI)
        self.patterns = {
            'perfect_structure': {
                'regex': r'\b(however|therefore|furthermore|moreover|additionally|consequently|thus|hence)\b',
                'weight': 0.25,
                'desc': 'Unnaturally frequent transition words'
            },
            'balanced_tone': {
                'regex': r'(on one hand|on the other hand|while|although|nonetheless|conversely|in contrast)',
                'weight': 0.22,
                'desc': 'Always presents multiple sides (human fake news is one-sided)'
            },
            'vague_sources': {
                'regex': r'(some experts|researchers say|studies show|it is believed|according to sources|some argue|it is thought)',
                'weight': 0.25,
                'desc': 'Vague attribution instead of specific sources'
            },
            'statistical_abundance': {
                'regex': r'\b(\d+%|\d+ out of \d+|\d+ million|\d+\.?\d+ billion|\d+\.\d+%)',
                'weight': 0.18,
                'desc': 'Too many specific statistics'
            },
            'hedging_language': {
                'regex': r'\b(may|might|could|potentially|arguably|appears to|seems to|tends to|suggests that|indicate that|potentially)\b',
                'weight': 0.28,
                'desc': 'Excessive hedging language'
            },
            'corporate_speak': {
                'regex': r'(stakeholders|synergy|leverage|optimize|best practices|moving forward|paradigm|scalable|innovative|strategic)',
                'weight': 0.20,
                'desc': 'Corporate jargon (AI trained on business text)'
            },
            'perfect_grammar': {
                'regex': r'\bit\s+is\b|\bthat\s+is\b',  # Prefers "it is" over contractions
                'weight': 0.15,
                'desc': 'Excessive "it is" over contractions (AI avoids contractions)'
            },
            'qualifiers': {
                'regex': r'(to some extent|in a sense|one might argue|it is worth noting|it is important to|it is crucial to)',
                'weight': 0.24,
                'desc': 'Excessive qualifiers and softening phrases'
            }
        }
    
    def detect_ai_indicators(self, text: str) -> Tuple[float, Dict]:
        """
        Analyze text for AI generation patterns
        
        Returns:
            (ai_probability: float 0-1, breakdown: dict with details)
        """
        if not text or len(text) < 100:
            return 0.0, {'error': 'Text too short for reliable AI detection'}
        
        breakdown = {}
        total_score = 0.0
        pattern_count_with_matches = 0
        
        text_lower = text.lower()
        word_count = len(text.split())
        sentence_count = max(1, len(re.split(r'[.!?]+', text)))
        
        for pattern_name, pattern_info in self.patterns.items():
            try:
                matches = len(re.findall(pattern_info['regex'], text_lower, re.IGNORECASE))
                
                if matches > 0:
                    # Density: occurrences per 100 words
                    density = (matches / max(1, word_count / 100))
                    
                    # Score increases exponentially with density (more aggressive detection)
                    # For every match, we scale up the contribution
                    pattern_score = min(pattern_info['weight'] * (1 + min(density, 3)), pattern_info['weight'] * 1.5)
                    
                    pattern_count_with_matches += 1
                else:
                    pattern_score = 0.0
                    density = 0.0
                
                breakdown[pattern_name] = {
                    'matches': matches,
                    'density': round(density, 2),
                    'score': round(pattern_score, 3),
                    'description': pattern_info['desc']
                }
                
                total_score += pattern_score
                
            except Exception as e:
                breakdown[pattern_name] = {'error': str(e)}
        
        # Normalize to 0-1 scale with pattern diversity bonus
        # Multiple patterns working together = stronger AI signal
        max_possible_score = sum(p['weight'] * 1.5 for p in self.patterns.values())
        
        # Base score from pattern matches
        ai_probability = min(1.0, total_score / max_possible_score) if max_possible_score > 0 else 0.0
        
        # Bonus if multiple patterns detected (AI uses multiple techniques)
        pattern_diversity_bonus = min(0.15, (pattern_count_with_matches / len(self.patterns)) * 0.25)
        ai_probability = min(1.0, ai_probability + pattern_diversity_bonus)
        
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


# Quick test
if __name__ == "__main__":
    detector = AITextDetector()
    
    # Test with AI-like text
    ai_text = """
    However, it is important to acknowledge that while some experts argue 
    this approach has merit, other researchers maintain that alternative 
    strategies may potentially yield better outcomes. Furthermore, studies 
    suggest that approximately 75% of stakeholders have begun to leverage 
    best practices in this domain. Nevertheless, the evidence remains somewhat 
    ambiguous regarding long-term effectiveness.
    """
    
    score, details = detector.detect_ai_indicators(ai_text)
    print(f"AI Score: {score:.2f} ({detector.get_ai_verdict(score)})")
    print(f"Details: {details}")
