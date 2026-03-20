"""
Named Entity Recognition (NER) for fake news detection
Extracts people, organizations, locations, and verifies their credibility
"""

import logging
from typing import Dict, List, Tuple
import spacy

logger = logging.getLogger(__name__)


class NamedEntityExtractor:
    """Extract and analyze named entities from text"""
    
    def __init__(self):
        # Load spaCy NER model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Download with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Known fake news sources and suspicious entities
        self.known_misinformation_sources = {
            "naturalhealth365", "yournewswire", "beforeitsnews", 
            "davidicke", "infowars", "activistpost", "wnd"
        }
        
        self.known_credible_sources = {
            "reuters", "ap news", "bbc", "npr", "associated press",
            "guardian", "new york times", "washington post", "wsj",
            "financial times", "economist", "science daily"
        }
        
        # Commonly faked entities in misinformation
        self.suspicious_patterns = {
            "government agencies": ["fbi", "cia", "dhs", "nsa"],
            "health claims": ["cure", "miracle", "100% effective", "natural remedy"],
            "conspiracy": ["illuminati", "reptilians", "chemtrail", "5g"]
        }
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract named entities and analyze credibility
        
        Returns: {
            'entities': [...],
            'suspicious_entities': [...],
            'entity_credibility_score': 0-1,
            'breakdown': {...}
        }
        """
        if not self.nlp:
            return {
                'entities': [],
                'suspicious_entities': [],
                'entity_credibility_score': 0.5,
                'breakdown': {'error': 'spaCy model not loaded'}
            }
        
        doc = self.nlp(text)
        
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # Geopolitical entities (locations)
            'DATE': [],
            'MONEY': []
        }
        
        # Extract all named entities
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Check entity credibility
        suspicious_count = 0
        suspicious_entities = []
        
        # Check organizations
        for org in entities['ORG']:
            org_lower = org.lower()
            if any(source in org_lower for source in self.known_misinformation_sources):
                suspicious_count += 1
                suspicious_entities.append({'entity': org, 'type': 'ORG', 'credibility': 'LOW'})
            elif any(source in org_lower for source in self.known_credible_sources):
                suspicious_entities.append({'entity': org, 'type': 'ORG', 'credibility': 'HIGH'})
        
        # Check for suspicious keywords in person mentions
        text_lower = text.lower()
        for person in entities['PERSON']:
            if any(pattern in text_lower for pattern in self.suspicious_patterns['conspiracy']):
                suspicious_count += 1
                suspicious_entities.append({'entity': person, 'type': 'PERSON', 'credibility': 'SUSPICIOUS'})
        
        # Calculate entity credibility score
        total_entities = sum(len(v) for v in entities.values())
        entity_credibility_score = 1.0 - (suspicious_count / max(1, total_entities)) if total_entities > 0 else 0.5
        entity_credibility_score = max(0.0, min(1.0, entity_credibility_score))
        
        return {
            'entities': entities,
            'suspicious_entities': suspicious_entities,
            'entity_credibility_score': round(entity_credibility_score, 3),
            'total_entities': total_entities,
            'suspicious_count': suspicious_count,
            'breakdown': {
                'people_mentioned': len(entities['PERSON']),
                'organizations_mentioned': len(entities['ORG']),
                'locations_mentioned': len(entities['GPE']),
                'dates_mentioned': len(entities['DATE']),
                'monetary_amounts': len(entities['MONEY'])
            }
        }
    
    def verify_entity_claims(self, text: str) -> Dict:
        """Verify claims made about extracted entities"""
        if not self.nlp:
            return {'verified': False, 'claims_checked': 0, 'verification_score': 0.5}
        
        doc = self.nlp(text)
        
        # Extract sentences with entities and weak language
        weak_language = ['allegedly', 'reportedly', 'claims', 'some say', 'rumored', 'supposedly']
        
        unverified_claims = 0
        verified_claims = 0
        
        for sent in doc.sents:
            has_entity = any(ent.label_ in ['PERSON', 'ORG'] for ent in sent.ents)
            has_weak_language = any(weak_word in sent.text.lower() for weak_word in weak_language)
            
            if has_entity and has_weak_language:
                unverified_claims += 1
            elif has_entity:
                verified_claims += 1
        
        total_claims = verified_claims + unverified_claims
        verification_score = verified_claims / max(1, total_claims) if total_claims > 0 else 0.5
        
        return {
            'verified_claims': verified_claims,
            'unverified_claims': unverified_claims,
            'total_claims': total_claims,
            'verification_score': round(verification_score, 3),
            'breakdown': {
                'high_confidence': verified_claims,
                'low_confidence': unverified_claims
            }
        }


# Initialize the extractor
ner_extractor = NamedEntityExtractor()


if __name__ == "__main__":
    # Test NER
    test_text = "According to Reuters, Bill Gates announced a new initiative. Critics claim it's a conspiracy."
    result = ner_extractor.extract_entities(test_text)
    print(f"NER Result: {result}")
    
    verification = ner_extractor.verify_entity_claims(test_text)
    print(f"Verification: {verification}")
