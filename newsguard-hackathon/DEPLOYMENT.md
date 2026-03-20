# NewsGuard Deployment Guide

## 🚀 Full Stack Deployment: Heroku (Backend) + Vercel (Frontend)

### Quick Summary
- **Backend**: Flask API → Heroku
- **Frontend**: React + Vite → Vercel  
- **Database**: None (ML models & data loaded from pickles)
- **Environment**: Free tier compatible

---

## Step 1: Deploy Backend to Heroku

### Prerequisites
- Heroku CLI installed (`npm install -g heroku`)
- Heroku account (free tier available)
- Git repository initialized

### Deploy Backend

```bash
# Navigate to backend directory
cd backend

# Login to Heroku
heroku login

# Create Heroku app (choose a unique name)
heroku create newsguard-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set FRONTEND_ORIGIN=https://newsguard-frontend.vercel.app
heroku config:set MODEL_VARIANT=hybrid

# Deploy
git push heroku main
# (or git push heroku HEAD:main if on different branch)

# Check logs
heroku logs --tail
```

**Your backend will be available at**: `https://newsguard-api.herokuapp.com`

### Backend Environment Variables (Set in Heroku Dashboard)
```
FLASK_ENV=production
FRONTEND_ORIGIN=https://your-vercel-frontend.vercel.app
MODEL_VARIANT=hybrid
CONFIDENCE_THRESHOLD=0.65
```

---

## Step 2: Deploy Frontend to Vercel

### Prerequisites
- Vercel account (free tier available)
- Frontend GitHub repo connected

### Option A: Deploy via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/import
2. Select your GitHub repository
3. Set Project Name: `newsguard-frontend`
4. Framework: **React**
5. Build Command: `npm run build`
6. Output Directory: `dist`
7. Environment Variables:
   ```
   VITE_API_URL=https://newsguard-api.herokuapp.com
   ```
8. Click **Deploy**

### Option B: Deploy via Vercel CLI

```bash
# Navigate to frontend directory
cd frontend

# Install Vercel CLI globally
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# When prompted:
# - Link existing project? No
# - Project name: newsguard-frontend
# - Framework: React
# - Build Command: npm run build
# - Output Directory: dist
# - Environment variables:
#   VITE_API_URL=https://newsguard-api.herokuapp.com

# Get deployment URL (will be printed at end)
```

**Your frontend will be available at**: `https://newsguard-frontend.vercel.app`

---

## Step 3: Connect Frontend → Backend

### Update Environment Variables

After deploying backend to Heroku:

1. **For Vercel Frontend**:
   - Go to Vercel Dashboard
   - Select project → Settings → Environment Variables
   - Add: 
     ```
     VITE_API_URL = https://newsguard-api.herokuapp.com
     ```
   - Redeploy

2. **For Heroku Backend**:
   - Go to Heroku Dashboard
   - Select app → Settings → Config Vars
   - Add:
     ```
     FRONTEND_ORIGIN = https://newsguard-frontend.vercel.app
     ```

---

## Step 4: Test Deployment

### Test Backend API
```bash
# Check if backend is alive
curl https://newsguard-api.herokuapp.com/api/models

# Test analyzer endpoint
curl -X POST https://newsguard-api.herokuapp.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news: shocking revelation revealed. Exclusive story never told before."}'
```

### Test Frontend
1. Open https://newsguard-frontend.vercel.app
2. Try analyzing some text
3. Check that results load from the backend

---

## Step 5: Custom Domain (Optional)

### Add Custom Domain to Vercel
1. Go to Vercel Dashboard → Project Settings
2. Add Domain: `yourdomain.com`
3. Follow DNS setup instructions

### Add Custom Domain to Heroku
1. Go to Heroku Dashboard → Settings
2. Add domain: `api.yourdomain.com`
3. Update DNS records

---

## Common Issues & Solutions

### ❌ CORS Errors
**Problem**: Frontend can't connect to backend

**Solution**:
```bash
# Update Heroku config
heroku config:set FRONTEND_ORIGIN=https://your-frontend-domain

# Redeploy backend
git push heroku main
```

### ❌ 404 Errors on Frontend Routes
**Problem**: Page not found when accessing `/analyzer`

**Solution**: Vercel config already handles this with `vercel.json`

### ❌ Slow ML Model Loading
**Problem**: First request takes 30+ seconds

**Solution**: Normal for first load. Models are cached after. Use Heroku's paid tier for faster dynos if needed.

### ❌ Port Already in Use (Local)
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

---

## Monitoring & Logs

### Heroku Backend Logs
```bash
# Real-time logs
heroku logs --tail

# Last 50 lines
heroku logs -n 50

# Restart dyno
heroku restart
```

### Vercel Frontend Logs
- Go to Vercel Dashboard → Project → Deployments
- Click deployment → Logs

---

## Cost Breakdown (Free Alternatives)

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Heroku Backend | $0 (1 free dyno per account) | Dyno sleeps after 30min inactivity |
| Vercel Frontend | $0 (unlimited deployments) | Always active |
| **Total** | **$0/month** | Perfect for hackathon |

**Pro Tip**: For production use beyond free tier:
- Heroku $7/mo (basic dyno, always running)
- Vercel $20/mo (pro features, always fast)

---

## Updated After Deployment

Once deployed, update these in your code:

### Frontend API URL
Already configured in `src/utils/api.js` to use `VITE_API_URL` env variable.

### Backend CORS
Already configured in `app.py` to accept requests from `FRONTEND_ORIGIN`.

---

## Rollback if Needed

### Rollback Heroku
```bash
heroku releases
heroku rollback v3  # where v3 is previous version
```

### Rollback Vercel
- Dashboard → Deployments → click previous deployment → **Redeploy**

---

## Delete Deployments

### Delete Heroku App
```bash
heroku apps:destroy --app newsguard-api
```

### Delete Vercel Project
- Vercel Dashboard → Project Settings → Danger Zone → Delete Project

---

## What's Next

- 📊 Monitor API performance in Heroku Dashboard
- 🔔 Set up error logs/alerts
- 🎯 Share deployed URL: `https://newsguard-frontend.vercel.app`
- 🚀 Celebrate! 🎉

---

## Support

For issues:
1. Check Heroku logs: `heroku logs --tail`
2. Check Vercel logs: Dashboard → Deployments → Logs
3. Verify environment variables are set correctly
4. Test API endpoint directly with curl

Happy Deploying! 🚀
