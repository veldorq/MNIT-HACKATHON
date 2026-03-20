"""
Sentiment and bias detection for fake news identification
Uses transformer-based sentiment analysis to detect emotional manipulation
"""

import logging
from typing import Dict, Tuple
from transformers import pipeline

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyze sentiment, bias, and emotional manipulation in text"""
    
    def __init__(self):
        try:
            # Using DistilBERT for faster inference
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # CPU (use 0 for GPU)
            )
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            self.sentiment_pipeline = None
        
        # Manipulation keywords and patterns
        self.extreme_emotion_words = {
            'shocking': 3, 'explosive': 3, 'devastating': 3, 'bombshell': 3,
            'outrageous': 2.5, 'incredible': 2.5, 'unbelievable': 2.5,
            'disgusting': 2.5, 'horrifying': 2.5, 'scandalous': 2.5,
            'urgent': 2, 'breaking': 2, 'must-watch': 2, 'can\'t miss': 2
        }
        
        self.bias_indicators = {
            'us_vs_them': ['us vs them', 'versus', 'against', 'enemy', 'battle', 'war'],
            'absolutism': ['always', 'never', 'every single', 'all of them', 'completely'],
            'delegitimization': ['fake', 'hoax', 'scam', 'conspiracy', 'coverup', 'corrupt'],
            'dehumanization': ['beast', 'animal', 'monster', 'subhuman', 'vermin']
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment using transformer model
        
        Returns: {
            'overall_sentiment': 'positive'|'negative',
            'confidence': 0-1,
            'sentences_sentiment': [...],
            'emotional_intensity': 0-1,
            'breakdown': {...}
        }
        """
        if not self.sentiment_pipeline:
            logger.warning("Sentiment model not loaded, using fallback")
            return self._fallback_sentiment(text)
        
        try:
            # Get overall sentiment
            result = self.sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens
            overall_sentiment = result['label'].lower()
            confidence = result['score']
            
            # Analyze sentence-level sentiment
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            sentence_sentiments = []
            
            for sent in sentences[:5]:  # Analyze first 5 sentences
                if sent:
                    sent_result = self.sentiment_pipeline(sent[:512])[0]
                    sentence_sentiments.append({
                        'sentence': sent[:100],
                        'sentiment': sent_result['label'].lower(),
                        'confidence': round(sent_result['score'], 3)
                    })
            
            # Calculate emotional intensity
            emotional_intensity = self._calculate_emotional_intensity(text)
            
            return {
                'overall_sentiment': overall_sentiment,
                'confidence': round(confidence, 3),
                'sentences_sentiment': sentence_sentiments,
                'emotional_intensity': round(emotional_intensity, 3),
                'breakdown': {
                    'is_highly_emotional': emotional_intensity > 0.7,
                    'manipulation_score': emotional_intensity,  # Higher = more manipulative
                    'emotional_risk_level': 'HIGH' if emotional_intensity > 0.7 else 'MEDIUM' if emotional_intensity > 0.4 else 'LOW'
                }
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._fallback_sentiment(text)
    
    def detect_bias(self, text: str) -> Dict:
        """
        Detect bias indicators and polarization language
        
        Returns: {
            'bias_score': 0-1,
            'detected_biases': [...],
            'polarization_level': 'LOW'|'MEDIUM'|'HIGH',
            'breakdown': {...}
        }
        """
        text_lower = text.lower()
        detected_biases = []
        bias_count = 0
        
        # Check each bias category
        for category, keywords in self.bias_indicators.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                bias_count += count
                detected_biases.append({
                    'category': category,
                    'count': count,
                    'severity': 'HIGH' if count > 3 else 'MEDIUM' if count > 1 else 'LOW'
                })
        
        # Calculate bias score
        word_count = len(text.split())
        bias_score = min(1.0, bias_count / max(1, word_count / 10))  # Normalized per 10 words
        
        # Determine polarization level
        if bias_score > 0.15:
            polarization_level = 'HIGH'
        elif bias_score > 0.05:
            polarization_level = 'MEDIUM'
        else:
            polarization_level = 'LOW'
        
        return {
            'bias_score': round(bias_score, 3),
            'polarization_level': polarization_level,
            'detected_biases': detected_biases,
            'breakdown': {
                'total_bias_indicators': bias_count,
                'bias_categories_detected': len(detected_biases),
                'is_polarized': polarization_level != 'LOW',
                'risk_level': 'HIGH' if polarization_level == 'HIGH' else 'MEDIUM' if polarization_level == 'MEDIUM' else 'LOW'
            }
        }
    
    def detect_emotional_manipulation(self, text: str) -> Dict:
        """Detect language designed to manipulate through emotion"""
        text_lower = text.lower()
        manipulation_score = 0.0
        detected_manipulations = []
        
        # Check for extreme emotional language
        for word, weight in self.extreme_emotion_words.items():
            if word in text_lower:
                count = text_lower.count(word)
                manipulation_score += count * (weight / 10)
                detected_manipulations.append({
                    'technique': f'Extreme language: "{word}"',
                    'instances': count,
                    'weight': weight
                })
        
        # Check for urgent/time-pressure language
        urgent_words = ['urgent', 'now', 'immediately', 'breaking', 'before it\'s too late']
        urgent_count = sum(1 for word in urgent_words if word in text_lower)
        if urgent_count > 0:
            manipulation_score += urgent_count * 0.5
            detected_manipulations.append({
                'technique': 'Artificial urgency',
                'instances': urgent_count,
                'weight': 2
            })
        
        # Clamp to 0-1
        manipulation_score = min(1.0, manipulation_score / 10)
        
        return {
            'manipulation_score': round(manipulation_score, 3),
            'detected_techniques': detected_manipulations,
            'manipulation_risk': 'HIGH' if manipulation_score > 0.6 else 'MEDIUM' if manipulation_score > 0.3 else 'LOW',
            'breakdown': {
                'total_techniques': len(detected_manipulations),
                'is_emotionally_manipulative': manipulation_score > 0.5
            }
        }
    
    def _calculate_emotional_intensity(self, text: str) -> float:
        """Calculate overall emotional intensity of text"""
        text_lower = text.lower()
        intensity = 0.0
        
        # Count emotional markers
        for word, weight in self.extreme_emotion_words.items():
            intensity += text_lower.count(word) * (weight / 10)
        
        # Count exclamation marks
        intensity += text.count('!') * 0.3
        
        # Count ALL CAPS words
        all_caps = sum(1 for word in text.split() if word.isupper() and len(word) > 1)
        intensity += all_caps * 0.2
        
        return min(1.0, intensity / 20)  # Normalize
    
    def _fallback_sentiment(self, text: str) -> Dict:
        """Fallback sentiment analysis if transformer fails"""
        positive_words = ['good', 'great', 'excellent', 'best', 'amazing', 'love', 'wonderful']
        negative_words = ['bad', 'terrible', 'worst', 'hate', 'awful', 'horrible', 'disaster']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if neg_count > pos_count:
            sentiment = 'negative'
            confidence = min(1.0, neg_count / 10)
        else:
            sentiment = 'positive'
            confidence = min(1.0, pos_count / 10) if pos_count > 0 else 0.5
        
        return {
            'overall_sentiment': sentiment,
            'confidence': round(confidence, 3),
            'sentences_sentiment': [],
            'emotional_intensity': self._calculate_emotional_intensity(text),
            'breakdown': {
                'method': 'fallback_keyword_matching',
                'positive_indicators': pos_count,
                'negative_indicators': neg_count
            }
        }


# Initialize analyzer
sentiment_analyzer = SentimentAnalyzer()


if __name__ == "__main__":
    test_text = "This SHOCKING discovery will CHANGE EVERYTHING! Call now before it's too late!"
    
    sentiment = sentiment_analyzer.analyze_sentiment(test_text)
    print(f"Sentiment: {sentiment}\n")
    
    bias = sentiment_analyzer.detect_bias(test_text)
    print(f"Bias: {bias}\n")
    
    manipulation = sentiment_analyzer.detect_emotional_manipulation(test_text)
    print(f"Manipulation: {manipulation}")
