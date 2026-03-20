import requests
import json

# Test with AI-like articles
ai_articles = [
    ('Article 1 (Formal AI)', 'In todays world, it is important to note that artificial intelligence continues to play a crucial role in transforming industries. Furthermore, as previously mentioned in recent studies, the implementation of machine learning algorithms has proven to be evident. In conclusion, it goes without saying that these developments are reshaping innovation.'),
    
    ('Article 2 (Human Casual)', 'Breaking news: Scientists found something amazing! We discovered something incredible that could literally change everything. Honestly, the implications are huge! Its gonna be a big deal for the field.'),
    
    ('Article 3 (Balanced)', 'The government announced new policies today. Some experts say its good while others disagree. The policy includes several key components we should carefully assess. It remains to be seen how effective and impactful this will actually be in practice.')
]

print("Testing Improved AI Detection\n" + "="*50)

for name, text in ai_articles:
    if len(text) < 80:
        text = text + ' Additional context provided for testing purposes of analysis.'
    
    payload = {
        'text': text,
        'mode': 'hybrid',
        'url': '',
        'check_url': False,
        'check_ai': True
    }
    
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                                json=payload, 
                                headers={'Origin': 'http://localhost:5176'},
                                timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            ai_data = data.get('aiAnalysis', {})
            is_ai = ai_data.get('is_ai_generated')
            conf = ai_data.get('confidence')
            ind = ai_data.get('indicators')
            method = ai_data.get('method', 'unknown')
            
            print('\n' + name + ':')
            print('  AI Generated: ' + str(is_ai))
            print('  Confidence: ' + str(conf))
            print('  Indicators: ' + str(ind))
            print('  Method: ' + method)
        else:
            print('\n' + name + ': Error ' + str(response.status_code))
            print('  Response: ' + str(response.text[:100]))
    except Exception as e:
        print('\n' + name + ': Exception - ' + str(e))

print('\n' + "="*50)
print('Test complete. Check the results above.')
