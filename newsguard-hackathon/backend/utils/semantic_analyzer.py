"""
Semantic embeddings and similarity detection for fake news
Uses sentence transformers for semantic understanding beyond keyword matching
"""

import logging
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer, util
import numpy as np

logger = logging.getLogger(__name__)


class SemanticAnalyzer:
    """Analyze semantic similarity and deep meaning in text"""
    
    def __init__(self):
        try:
            # Fast and efficient model for semantic search
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to load semantic model: {e}")
            self.model = None
        
        # Known misinformation claim patterns (semantic templates)
        self.misinformation_patterns = [
            "miracle cure for serious disease",
            "government hiding evidence",
            "banned by authorities",
            "doctors don't want you to know",
            "secret ingredient discovered",
            "overnight success formula",
            "100% guaranteed results",
            "ancient remedy forgotten by science"
        ]
        
        # Credible claim indicators
        self.credible_claim_markers = [
            "study shows results",
            "researchers found evidence",
            "peer-reviewed research",
            "according to official sources",
            "data demonstrates correlation",
            "multiple sources confirm"
        ]
        
        self.misinformation_embeddings = None
        self.credible_embeddings = None
        self._cache_embeddings()
    
    def _cache_embeddings(self):
        """Pre-compute embeddings for known patterns"""
        if self.model:
            try:
                self.misinformation_embeddings = self.model.encode(self.misinformation_patterns)
                self.credible_embeddings = self.model.encode(self.credible_claim_markers)
            except Exception as e:
                logger.error(f"Failed to cache embeddings: {e}")
    
    def get_semantic_similarity(self, text: str) -> Dict:
        """
        Calculate semantic similarity to known misinformation patterns
        
        Returns: {
            'misinformation_similarity': 0-1,
            'similar_patterns': [...],
            'credibility_signal': 0-1,
            'breakdown': {...}
        }
        """
        if not self.model or self.misinformation_embeddings is None:
            logger.warning("Semantic model not available")
            return {
                'misinformation_similarity': 0.5,
                'similar_patterns': [],
                'credibility_signal': 0.5,
                'breakdown': {'error': 'Model not loaded'}
            }
        
        try:
            # Get embedding for input text
            text_embedding = self.model.encode(text)
            
            # Calculate similarity to misinformation patterns
            misinformation_scores = util.pytorch_cos_sim(
                text_embedding, 
                self.misinformation_embeddings
            )[0]
            
            # Calculate similarity to credible patterns
            credible_scores = util.pytorch_cos_sim(
                text_embedding,
                self.credible_embeddings
            )[0]
            
            # Get top similar patterns
            similar_misinformation = []
            for idx, score in enumerate(misinformation_scores):
                if score > 0.5:  # Significant similarity
                    similar_misinformation.append({
                        'pattern': self.misinformation_patterns[idx],
                        'similarity': round(float(score), 3)
                    })
            
            # Calculate overall scores
            avg_misinformation = float(misinformation_scores.max()) if len(misinformation_scores) > 0 else 0.0
            avg_credible = float(credible_scores.max()) if len(credible_scores) > 0 else 0.0
            
            # Credibility signal: how much like known credible patterns
            credibility_signal = min(1.0, avg_credible)
            
            return {
                'misinformation_similarity': round(min(1.0, avg_misinformation), 3),
                'credible_similarity': round(credibility_signal, 3),
                'similar_patterns': similar_misinformation,
                'semantic_risk_score': round(avg_misinformation - avg_credible, 3),
                'breakdown': {
                    'matches_known_fake_patterns': len(similar_misinformation) > 0,
                    'semantic_consistency': 'HIGH' if avg_credible > avg_misinformation else 'LOW'
                }
            }
        except Exception as e:
            logger.error(f"Error in semantic similarity: {e}")
            return {
                'misinformation_similarity': 0.5,
                'similar_patterns': [],
                'credibility_signal': 0.5,
                'breakdown': {'error': str(e)}
            }
    
    def detect_semantic_coherence(self, text: str) -> Dict:
        """
        Detect overall semantic coherence and logical consistency
        Fake news often has scattered, incoherent arguments
        """
        if not self.model:
            return {
                'coherence_score': 0.5,
                'breakdown': {'error': 'Model not loaded'}
            }
        
        try:
            # Split into sentences
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if len(sentences) < 2:
                return {
                    'coherence_score': 0.7,
                    'sentence_count': len(sentences),
                    'breakdown': {'note': 'Too few sentences'}
                }
            
            # Encode all sentences
            sentence_embeddings = self.model.encode(sentences)
            
            # Calculate pairwise similarity
            coherence_scores = []
            for i in range(len(sentence_embeddings) - 1):
                similarity = util.pytorch_cos_sim(
                    sentence_embeddings[i],
                    sentence_embeddings[i + 1]
                )
                coherence_scores.append(float(similarity[0][0]))
            
            # Average coherence
            avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.5
            
            # High coherence = consistent narrative
            # Low coherence = jumping between unrelated ideas (suspicious)
            coherence_signal = min(1.0, avg_coherence)
            
            return {
                'coherence_score': round(coherence_signal, 3),
                'sentence_count': len(sentences),
                'avg_sentence_similarity': round(np.mean(coherence_scores), 3) if coherence_scores else 0.5,
                'is_coherent': coherence_signal > 0.5,
                'breakdown': {
                    'coherence_level': 'HIGH' if coherence_signal > 0.6 else 'MEDIUM' if coherence_signal > 0.4 else 'LOW',
                    'narrative_consistency': coherence_signal
                }
            }
        except Exception as e:
            logger.error(f"Error in coherence detection: {e}")
            return {
                'coherence_score': 0.5,
                'breakdown': {'error': str(e)}
            }
    
    def find_claim_sources(self, text: str) -> Dict:
        """
        Detect presence of source citations and attributions
        Fake news often makes claims without proper sourcing
        """
        text_lower = text.lower()
        
        attribution_phrases = [
            'according to', 'research shows', 'study found', 'data indicates',
            'sources say', 'officials stated', 'survey showed', 'analysis reveals',
            'experts conclude', 'evidence suggests', 'report indicates'
        ]
        
        # Count attribution instances
        attributions = sum(1 for phrase in attribution_phrases if phrase in text_lower)
        
        # Check for specific citations (URLs, reference numbers)
        has_urls = 'http' in text_lower or 'www.' in text_lower
        has_citations = any(f'[{i}]' in text for i in range(1, 20))
        
        # Calculate source credibility indicator
        attribution_density = attributions / max(1, len(text.split()) / 100)  # Per 100 words
        source_score = min(1.0, attribution_density / 5)  # Normalized
        
        if has_urls or has_citations:
            source_score = min(1.0, source_score + 0.3)
        
        is_well_sourced = source_score > 0.5
        
        return {
            'source_attribution_count': attributions,
            'has_urls': has_urls,
            'has_citations': has_citations,
            'source_credibility_score': round(source_score, 3),
            'is_well_sourced': is_well_sourced,
            'breakdown': {
                'attribution_phrases': attributions,
                'citation_density': round(attribution_density, 3),
                'source_risk_level': 'LOW' if is_well_sourced else 'HIGH'
            }
        }


# Initialize analyzer
semantic_analyzer = SemanticAnalyzer()


if __name__ == "__main__":
    test_text = "Our revolutionary formula is banned by doctors. Secret research shows it cures everything. Government doesn't want you to know. Buy now before they silence us!"
    
    sim = semantic_analyzer.get_semantic_similarity(test_text)
    print(f"Semantic Similarity: {sim}\n")
    
    coherence = semantic_analyzer.detect_semantic_coherence(test_text)
    print(f"Coherence: {coherence}\n")
    
    sources = semantic_analyzer.find_claim_sources(test_text)
    print(f"Sources: {sources}")
