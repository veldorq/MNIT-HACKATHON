#!/usr/bin/env python3
"""Test analyze endpoint"""
import requests
import json

url = "http://localhost:5000/api/analyze"
payload = {
    "text": "This is a test article about recent developments in technology and artificial intelligence. Experts say that machine learning is transforming industries rapidly and creating new opportunities.",
    "mode": "hybrid",
    "check_ai": True,
    "check_url": False,
    "url": ""
}

try:
    print("[TEST] Sending POST request to /api/analyze")
    response = requests.post(url, json=payload, timeout=15)
    
    print(f"[TEST] Status Code: {response.status_code}")
    print(f"[TEST] Response Length: {len(response.text)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n[SUCCESS] Got valid response")
        print(f"  prediction: {data.get('prediction')}")
        print(f"  confidence: {data.get('confidence')}")
        print(f"  aiAnalysis: {data.get('aiAnalysis', {})}")
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(response.text[:300])
        
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
