import requests

pigeon_article = """Pigeons Officially Classified as Government Surveillance Drones, FOIA Documents Reveal

Washington D.C. — March 20, 2026

Shocking documents obtained through a Freedom of Information Act request have confirmed what conspiracy theorists have claimed for decades — common city pigeons are in fact hollow robotic drones operated by the federal government to monitor civilian activity.

The 847-page document, released by the Department of Homeland Security, reveals that real pigeons went extinct in 1986. All birds currently observed in urban areas are equipped with 4K cameras, microphones, and 5G transmitters disguised as feathers.

"We can neither confirm nor deny the existence of biological surveillance assets," said a DHS spokesperson, visibly sweating.

Bird watchers across the country have reportedly begun wearing tin foil hats during outdoor activities. Sales of breadcrumbs have plummeted 94% as citizens refuse to "feed the government."

Congress is expected to hold emergency hearings next Tuesday. The pigeons could not be reached for comment."""

payload = {
    'text': pigeon_article,
    'mode': 'hybrid',
    'url': '',
    'check_url': False,
    'check_ai': True
}

response = requests.post('http://localhost:5000/api/analyze', json=payload, headers={'Origin': 'http://localhost:5176'})
data = response.json()
fake = data.get('fakeNewsAnalysis', {})

print("Pigeon Article Results After Improvements:")
print("=" * 60)
print("Prediction:        ", fake.get('prediction').upper())
print("Confidence:        ", fake.get('confidence'))
print("Credibility Score: ", fake.get('credibilityScore'), "/100")
print("Flagged Keywords:  ", fake.get('flaggedKeywords'))
print("\nThis should now show MUCH LOWER credibility score (~20-30)")
print("and clear FAKE prediction for this obvious satire!")
