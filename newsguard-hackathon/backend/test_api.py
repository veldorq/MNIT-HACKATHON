#!/usr/bin/env python3
import urllib.request
import json

base = 'http://localhost:5000'

tests = [
    ('Long realistic', 'The Federal Reserve announced quarterly interest rate decisions following comprehensive economic analysis and market deliberation by all committee members.', 'kaggle'),
    ('Mixed signals', 'Sources claim government denies allegations about program but officials offer no comment', 'kaggle'),
    ('Clear real', 'Reuters reports parliament approves budget bill after extended committee deliberation and debate.', 'hybrid'),
]

print("API VALIDATION TEST")
print("=" * 70)

for name, text, mode in tests:
    data = json.dumps({'text': text, 'mode': mode}).encode('utf-8')
    try:
        req = urllib.request.Request(f'{base}/api/analyze', data=data, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f'{name:20} | pred={res["prediction"]:18} conf={res["confidence"]:.1%}')
    except urllib.error.HTTPError as e:
        err_text = e.read().decode('utf-8')[:90]
        print(f'{name:20} | ERROR {e.code}: {err_text}')
    except Exception as e:
        print(f'{name:20} | EXCEPTION: {str(e)[:60]}')

print("=" * 70)
print("EXPECTED RESULTS:")
print("- Long realistic:  real (high confidence)")
print("- Mixed signals:   may trigger needs_verification or fake")
print("- Clear real:      real (via hybrid ensemble)")

