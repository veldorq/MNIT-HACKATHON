# Quick Deployment Checklist

## ✅ Pre-Deployment Checklist

### Backend (Heroku)
- [ ] `Procfile` exists with: `web: gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] `requirements.txt` up to date
- [ ] `.env.production` configured for production
- [ ] All ML models in `backend/models/` directory
- [ ] `app.py` imports all routes correctly

### Frontend (Vercel)
- [ ] `vercel.json` exists with SPA rewrites
- [ ] `.env.production` has correct API URL
- [ ] `dist/` builds without errors
- [ ] `package.json` has build script

### Testing
- [ ] Backend starts: `python app.py` → runs on 5000
- [ ] Frontend starts: `npm run dev` → runs on 5173
- [ ] API endpoint responds: `curl http://localhost:5000/api/models`
- [ ] Frontend connects to backend API successfully

---

## 🚀 One-Click Deployment

### Step 1: Build Frontend (Local)
```bash
cd frontend
npm install
npm run build
```

### Step 2: Deploy Backend to Heroku
```bash
cd backend
heroku create newsguard-api
heroku config:set FLASK_ENV=production
heroku config:set FRONTEND_ORIGIN=https://newsguard-frontend.vercel.app
git push heroku main
```

**Note backend URL**: `https://newsguard-api.herokuapp.com`

### Step 3: Deploy Frontend to Vercel
```bash
cd frontend
npm install -g vercel
vercel --prod \
  --env VITE_API_URL=https://newsguard-api.herokuapp.com
```

**Note frontend URL**: `https://newsguard-frontend.vercel.app`

### Step 4: Update Backend CORS
```bash
heroku config:set FRONTEND_ORIGIN=https://newsguard-frontend.vercel.app
git push heroku main
```

---

## ✨ After Deployment

1. Test frontend: https://newsguard-frontend.vercel.app
2. Try analyzer with sample text
3. Check that results load from backend
4. Share deployed URL with judges/team

---

## 📊 Status Check

### Check Backend Health
```bash
curl https://newsguard-api.herokuapp.com/api/models
```

**Expected response**: List of available models

### Check Frontend Availability
Open: https://newsguard-frontend.vercel.app

**Expected**: Landing page loads, analyzer works

### Check Logs
```bash
# Backend logs
heroku logs --tail --app newsguard-api

# Frontend logs
vercel logs [project-url]
```

---

## ⚠️ Troubleshooting

### CORS Errors?
→ Verify `FRONTEND_ORIGIN` env var on Heroku matches your Vercel URL

### 404 Page Not Found?
→ Vercel auto-handles via `vercel.json` (already configured)

### Slow First Request?
→ Normal (ML models loading). Second request is instant.

### Port Conflicts Locally?
```bash
# Kill port 5000
lsof -ti:5000 | xargs kill -9

# Kill port 5173
lsof -ti:5173 | xargs kill -9
```

---

## 🎯 Final URLs

Once deployed, share these:
- **App**: https://newsguard-frontend.vercel.app
- **API**: https://newsguard-api.herokuapp.com/api/analyze

Done! 🎉
