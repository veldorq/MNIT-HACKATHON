"""
Hybrid Article Detector - Identifies real news that's been manipulated with false elements.

Detects:
- Fake statistics/numbers injection
- Misleading context/framing
- False claims inserted in real article
- Unverified claims without sources
"""

import re
from typing import Dict, List, Tuple

class HybridArticleDetector:
    """Detects articles that appear real but contain injected false elements"""
    
    def __init__(self):
        # Patterns for fake statistics/numbers
        self.fake_stat_patterns = [
            r'\d+%\s+(?:of|increase|rise|drop|fall|growth)',  # "75% increase"
            r'(?:new|latest|recent)\s+study\s+shows\s+\d+',    # "new study shows 80"
            r'\d+\s+(?:million|billion|thousand)\s+(?:people|cases|deaths)',
            r'(?:up to|over|nearly)\s+\d+%',                    # "up to 90%"
            r'\d+x\s+(?:more|greater|larger)',                  # "5x more likely"
            r'(?:doctors?|experts?|scientists?)\s+(?:warn|claim)\s+\d+',
        ]
        
        # Red flags for unverified claims
        self.unverified_claim_patterns = [
            r'(?:sources?\s+)?(?:say|suggest|claim|believe|think|fear)\s+(?:that)?',
            r'(?:allegedly|reportedly|supposedly|apparently)\s+',
            r'(?:some\s+)?(?:people|experts?|officials?)\s+(?:say|believe|fear)',
            r'(?:it\'s?|this|they)\s+(?:could be|might be|seems(?:\s+to be)?)',
            r'(?:unconfirmed|unverified|suspected)',
        ]
        
        # Misleading framing indicators
        self.misleading_framing = [
            r'(?:shocking|surprising|disturbing|alarming|concerning)\s+(?:new\s+)?(?:study|research|report|evidence)',
            r'(?:finally|at last|at long last)\s+(?:the\s+)?(?:truth|facts?|evidence)',
            r'(?:they\s+(?:don\'t want you to know|don\'t want us to know|won\'t tell you))',
            r'(?:mainstream\s+media|authorities|government)\s+(?:won\'t|refuses|cover up|silence)',
            r'(?:credible\s+)?(?:source|insider|whistleblower)\s+(?:reveals|exposes|warns)',
        ]
        
        # Compile patterns
        self.stat_patterns = [re.compile(p, re.IGNORECASE) for p in self.fake_stat_patterns]
        self.unverified_patterns = [re.compile(p, re.IGNORECASE) for p in self.unverified_claim_patterns]
        self.framing_patterns = [re.compile(p, re.IGNORECASE) for p in self.misleading_framing]
        
        # Real indicators (opposite signals)
        self.credibility_indicators = {
            'quote_attribution': r'(?:said\s+)?["\'].*?["\']?\s*(?:—|,)?\s*(?:according\s+to|said by|from)\s+(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            'source_citation': r'(?:according to|per|citing|from|source:)\s+(?:[A-Z]\w+|https?://)',
            'data_attribution': r'(?:data from|statistics from|according to)\s+(?:[A-Z]\w+|CDC|WHO|WHO|UN|Google)',
            'publication_ref': r'published in|appeared in|reported in|(?:The\s+)?(?:New York Times|BBC|Reuters|AP News|NPR)',
        }
    
    def detect_fake_statistics(self, text: str) -> Tuple[int, List[str]]:
        """Detect suspicious statistical claims without verification"""
        suspicious_stats = []
        
        for pattern in self.stat_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                # Extract context around the match
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                suspicious_stats.append(context)
        
        return len(suspicious_stats), suspicious_stats[:5]  # Return top 5
    
    def detect_unverified_claims(self, text: str) -> Tuple[int, List[str]]:
        """Detect claims stated without proper verification/sources"""
        unverified = []
        
        for pattern in self.unverified_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                unverified.append(context)
        
        return len(unverified), unverified[:5]
    
    def detect_misleading_framing(self, text: str) -> Tuple[int, List[str]]:
        """Detect misleading/sensational framing of claims"""
        framing_issues = []
        
        for pattern in self.framing_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 40)
                context = text[start:end].strip()
                framing_issues.append(context)
        
        return len(framing_issues), framing_issues[:5]
    
    def count_credibility_indicators(self, text: str) -> Dict[str, int]:
        """Count real credibility signals (proper sourcing, attribution)"""
        counts = {}
        
        for key, pattern_str in self.credibility_indicators.items():
            pattern = re.compile(pattern_str, re.IGNORECASE)
            matches = pattern.findall(text)
            counts[key] = len(matches)
        
        return counts
    
    def calculate_source_quality_ratio(self, text: str) -> float:
        """
        Calculate ratio of claimed facts to source citations.
        Real news has high ratio of claims with sources.
        Manipulated news has claims without sources mixed in.
        
        Returns 0-1 score where 1 = perfectly sourced, 0 = no sources
        """
        # Count claim-like sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.5  # Neutral
        
        # Sentences with numbers/stats/claims
        claim_sentences = 0
        sourced_sentences = 0
        
        for sentence in sentences:
            # Count claims (contains numbers, strong statements, etc.)
            if re.search(r'\d+[\d,%]*|(?:shows|proves|reveals|indicates|suggests)', sentence):
                claim_sentences += 1
                
                # Check if this sentence has source attribution
                if re.search(r'(?:according to|per|citing|from|said|stated|reported|published)', sentence):
                    sourced_sentences += 1
        
        if claim_sentences == 0:
            return 0.5
        
        # Higher ratio = better sourcing
        source_ratio = sourced_sentences / claim_sentences
        return source_ratio
    
    def detect_hybrid_characteristics(self, text: str) -> Dict:
        """
        Comprehensive detection of hybrid article characteristics.
        Returns indicators that article is real BUT contains false elements.
        """
        fake_stat_count, fake_stats = self.detect_fake_statistics(text)
        unverified_count, unverified = self.detect_unverified_claims(text)
        framing_count, framing = self.detect_misleading_framing(text)
        credibility_indicators = self.count_credibility_indicators(text)
        source_ratio = self.calculate_source_quality_ratio(text)
        
        # Calculate hybrid risk score (0-100)
        # High = more likely to be hybrid (real with tweaks)
        hybrid_risk = 0
        
        # Fake stats without sources = red flag
        if fake_stat_count > 0:
            hybrid_risk += fake_stat_count * 15
        
        # Unverified claims = red flag
        if unverified_count > 0:
            hybrid_risk += unverified_count * 12
        
        # Misleading framing = red flag
        if framing_count > 0:
            hybrid_risk += framing_count * 10
        
        # Low source ratio = red flag
        if source_ratio < 0.5:
            hybrid_risk += (1 - source_ratio) * 30
        
        # HIGH credibility indicators = good sign (real news with sources)
        if credibility_indicators['quote_attribution'] > 0:
            hybrid_risk -= credibility_indicators['quote_attribution'] * 5
        if credibility_indicators['source_citation'] > 0:
            hybrid_risk -= credibility_indicators['source_citation'] * 5
        if credibility_indicators['publication_ref'] > 0:
            hybrid_risk -= credibility_indicators['publication_ref'] * 8
        
        hybrid_risk = max(0, min(100, hybrid_risk))
        
        return {
            'hybrid_risk_score': hybrid_risk,
            'fake_statistics': {
                'count': fake_stat_count,
                'examples': fake_stats
            },
            'unverified_claims': {
                'count': unverified_count,
                'examples': unverified
            },
            'misleading_framing': {
                'count': framing_count,
                'examples': framing
            },
            'credibility_indicators': credibility_indicators,
            'source_ratio': round(source_ratio, 2),
            'assessment': self._assess_hybrid_likelihood(hybrid_risk, credibility_indicators)
        }
    
    @staticmethod
    def _assess_hybrid_likelihood(risk_score: float, indicators: Dict) -> str:
        """Provide human-readable assessment"""
        total_cred = sum(indicators.values())
        
        if risk_score < 20 and total_cred >= 3:
            return "Likely authentic - well sourced with few red flags"
        elif risk_score < 40 and total_cred >= 2:
            return "Mostly credible - some unverified claims but generally sourced"
        elif risk_score < 60 and total_cred >= 1:
            return "Potentially hybrid - contains unverified claims mixed with real information"
        elif risk_score < 80:
            return "Likely hybrid - multiple red flags suggest real news with false elements"
        else:
            return "High risk hybrid - extensive unverified claims and poor sourcing"


# Global instance
hybrid_detector = HybridArticleDetector()
