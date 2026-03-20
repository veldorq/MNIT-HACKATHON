#!/usr/bin/env python3
"""Quick test of Groq analyzer."""

import sys
sys.path.insert(0, '.')

from utils.groq_analyzer import detect_ai_generated_content, verify_url_credibility

print("Testing Groq integration...")

# Test AI detection
print("\n1. Testing AI Detection...")
sample_text = "In today's world, technological advancements continue to play a crucial role in society. It is important to note that artificial intelligence has become increasingly prevalent across various sectors. This article explores the implications of such developments."

try:
    result = detect_ai_generated_content(sample_text)
    print(f"   AI Generated: {result.get('is_ai_generated')}")
    print(f"   Confidence: {result.get('confidence')}")
    print(f"   Indicators: {result.get('indicators')}")
    print(f"   Explanation: {result.get('explanation')}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test URL verification
print("\n2. Testing URL Verification...")
test_url = "https://cnn.com"

try:
    result = verify_url_credibility(test_url)
    print(f"   {test_url}")
    print(f"      Credible: {result.get('is_credible')}")
    print(f"      Risk: {result.get('risk_level')}")
    print(f"      Explanation: {result.get('explanation')}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nAll tests completed!")


