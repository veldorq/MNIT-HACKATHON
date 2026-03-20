# API Documentation

## Base URL
- Local: `http://localhost:5000`
- Production: your deployed backend URL

## `GET /api/health`
Health check endpoint.

### Response
```json
{
  "status": "healthy",
  "message": "NewsGuard API is running"
}
```

## `POST /api/analyze`
Analyze news text and return prediction plus credibility score.

### Request
```json
{
  "text": "Paste news content here"
}
```

### Success Response
```json
{
  "prediction": "real",
  "confidence": 0.74,
  "credibilityScore": 81,
  "breakdown": {
    "modelScore": 37,
    "keywordScore": 24,
    "lengthScore": 12,
    "hedgeScore": 8,
    "wordCount": 180
  },
  "flaggedKeywords": [],
  "provider": "ml-model"
}
```

### Error Response
```json
{
  "error": "No text provided"
}
```

If model files are missing, analyze returns `503`:
```json
{
  "error": "Model artifacts are missing. Train and place fake_news_model.pkl and tfidf_vectorizer.pkl in backend/models."
}
```
