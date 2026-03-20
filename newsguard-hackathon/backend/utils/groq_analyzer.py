"""
Groq API Integration for URL Credibility Verification.
Uses Groq for fast LLM inference to analyze if a URL/domain is from a fake news source.
This is a SEPARATE check from the ML-based fake news detection on article content.
"""

import os
import re

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = None

def _init_client():
    global client, api_key
    if not GROQ_AVAILABLE:
        raise ImportError("groq package is not installed")
    if client is None:
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        client = Groq(api_key=api_key, timeout=8)
    return client


def verify_url_credibility(url: str) -> dict:
    """
    Verify if a URL domain is from a credible or fake news website.
    Uses Groq LLM for intelligent domain reputation analysis.
    
    Args:
        url: The article URL to verify
        
    Returns:
        dict with:
        - is_credible: bool (True if trusted source, False if fake/suspicious)
        - risk_level: str ("safe", "suspicious", or "dangerous")
        - explanation: str (human-readable reason)
        - domain: str (extracted domain)
    """
    try:
        # Extract domain from URL
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        domain = domain_match.group(1) if domain_match else url
        
        # Quick lookup for known sources (fast fallback if Groq fails)
        known_safe = {
            # International Major News
            'reuters.com', 'bbc.com', 'bbc.co.uk', 'apnews.com', 'ap.org',
            'nytimes.com', 'washingtonpost.com', 'theguardian.com', 'ft.com',
            'aljazeera.com', 'npr.org', 'pbs.org', 'bbc.news', 'bbc.world',
            # News Aggregators
            'news.google.com', 'google.com/news',
            # Indian News Sources
            'timesofindia.indiatimes.com', 'indiatimes.com', 'toi.in',
            'hindustantimes.com', 'indianexpress.com', 'thehindu.com',
            'deccanherald.com', 'firstpost.com', 'ndtv.com', 'theprint.in',
            'scroll.in', 'livemint.com', 'business-standard.com',
            # Other reputable international
            'bbc.world', 'dw.com', 'france24.com', 'euronews.com',
            'scmp.com', 'straits-times.com', 'dawn.com'
        }
        
        known_fake = {
            'abcnews.com.co', 'cnn.co', 'foxnews.com.br', 'bbc.co.uk.org',
            'nytimes.com.ru', 'theonion.com', 'infowars.com', 'beforeitsnews.com',
            'naturalnews.com', 'wnd.com', 'patrickfrancis.blogspot.com'
        }
        
        domain_lower = domain.lower()
        
        # Check for exact domain match or parent domain match
        def is_safe_domain(domain_to_check):
            # Exact matches
            if domain_to_check in known_safe:
                return True
            # Parent domain checks (e.g., timesofindia.indiatimes.com matches indiatimes.com)
            parts = domain_to_check.split('.')
            for i in range(1, len(parts)):
                parent = '.'.join(parts[i:])
                if parent in known_safe:
                    return True
            # Substring check for some cases (e.g., contains 'bbc' for bbc variants)
            for safe in known_safe:
                if safe in domain_to_check:
                    return True
            return False
        
        def is_fake_domain(domain_to_check):
            if domain_to_check in known_fake:
                return True
            # Parent domain checks
            parts = domain_to_check.split('.')
            for i in range(1, len(parts)):
                parent = '.'.join(parts[i:])
                if parent in known_fake:
                    return True
            return False
        
        # Immediate return for known domains
        if is_safe_domain(domain_lower):
            return {
                "is_credible": True,
                "risk_level": "safe",
                "explanation": f"{domain} is a recognized established news source",
                "domain": domain,
                "method": "known_source"
            }
        
        if is_fake_domain(domain_lower):
            return {
                "is_credible": False,
                "risk_level": "dangerous",
                "explanation": f"{domain} is a known fake news source",
                "domain": domain,
                "method": "known_fake"
            }
        
        # For unknown domains, mark as suspicious (safe default)
        # Groq API verification disabled due to quota/API issues
        return {
            "is_credible": False,
            "risk_level": "suspicious",
            "explanation": f"{domain} could not be verified. Please check the source independently.",
            "domain": domain,
            "method": "unverified_domain"
        }
        
    except Exception as e:
        # Fallback on any error
        return {
            "is_credible": False,
            "risk_level": "suspicious",
            "explanation": f"Unable to verify domain: {str(e)[:50]}",
            "domain": url,
            "method": "error_fallback"
        }
