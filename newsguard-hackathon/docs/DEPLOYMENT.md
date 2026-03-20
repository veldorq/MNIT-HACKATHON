# Deployment Guide

## Frontend on Vercel
1. Push repo to GitHub.
2. Import project in Vercel.
3. Set root directory to `frontend`.
4. Framework preset: Vite.
5. Add env variable:
   - `VITE_API_URL=https://<your-backend-url>`
6. Deploy.

## Backend on Railway or Render
1. Create new project from GitHub repo.
2. Set root directory to `backend`.
3. Build command:
   - `pip install -r requirements.txt`
4. Start command:
   - `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add env variables:
   - `FLASK_ENV=production`
   - `FRONTEND_ORIGIN=https://<your-frontend-url>`
6. Upload model files (`fake_news_model.pkl`, `tfidf_vectorizer.pkl`) into `backend/models` during build/deploy process.

## Post-Deploy Checks
- Open frontend URL and run one sample analysis.
- Hit backend `/api/health` URL.
- Validate CORS by triggering analysis from frontend.
