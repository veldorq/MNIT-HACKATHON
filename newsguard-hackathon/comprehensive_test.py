import requests
import json

test_articles = [
    {
        "name": "AI-Written Fake News",
        "text": "In today's world, it is important to note that a revolutionary cure for diabetes has been discovered. Furthermore, as previously mentioned in breakthrough research, scientists have developed an innovative treatment. In conclusion, it goes without saying that this discovery plays a crucial role in transforming medical science. The implementation of this technology has proven to be evident that humanity will benefit tremendously."
    },
    {
        "name": "Human-Written Fake News",
        "text": "SHOCKING: Scientists found a miracle cure! We're calling it the game-changer of the century and honestly, it's AMAZING! This isn't fake - it's absolutely real and gonna change EVERYTHING. Our sources say it works 100% of the time, no take-backs!"
    },
    {
        "name": "Real News (Balanced)",
        "text": "Scientists at MIT announced progress in diabetes research today. The findings show promise but require further testing. Experts remain cautiously optimistic about potential applications within the next five years. Further studies are needed to confirm effectiveness and safety. The research has been peer-reviewed and published in major journals."
    },
    {
        "name": "Casual Human Story",
        "text": "You won't believe what happened at the store yesterday! I went in to grab milk and ran into my old friend Sarah. We hadn't seen each other in forever, so we grabbed coffee after shopping. She's doing amazing with her new job - I'm really happy for her! We're definitely going to stay in touch this time."
    }
]

print("=" * 70)
print("COMPREHENSIVE TEST SUITE - AI + FAKE NEWS DETECTION")
print("=" * 70)

for article in test_articles:
    if len(article["text"]) < 80:
        text = article["text"] + " Additional information for testing. This makes the text longer."
    else:
        text = article["text"]
    
    payload = {
        "text": text,
        "mode": "hybrid",
        "url": "",
        "check_url": False,
        "check_ai": True
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json=payload,
            headers={'Origin': 'http://localhost:5176'},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            fake_news = data.get('fakeNewsAnalysis', {})
            ai_analysis = data.get('aiAnalysis', {})
            
            print(f"\n{article['name']}:")
            print("-" * 70)
            print(f"  Prediction: {fake_news.get('prediction').upper():20} | Confidence: {fake_news.get('confidence')}")
            print(f"  Credibility Score: {fake_news.get('credibilityScore')}/100")
            print(f"  AI Generated: {ai_analysis.get('is_ai_generated'):5} | Confidence: {ai_analysis.get('confidence')}")
            print(f"  AI Method: {ai_analysis.get('method')}")
            print(f"  AI Indicators: {ai_analysis.get('indicators')}")
            
            keywords = fake_news.get('flaggedKeywords', [])
            if keywords:
                print(f"  Flagged Keywords: {keywords}")
        else:
            print(f"\n{article['name']}: ERROR {response.status_code}")
            print(f"  {response.text[:100]}")
    except Exception as e:
        print(f"\n{article['name']}: EXCEPTION")
        print(f"  {str(e)[:100]}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
