# 🎯 DEPLOYMENT ACTION PLAN - START HERE

Your NewsGuard project is **100% ready to deploy**. Here's exactly what to do:

---

## ⏱️ Time Required: 10-15 minutes

---

## 📋 Step-by-Step Instructions

### Step 1️⃣: Create Accounts (2 minutes)

If you don't have these:

**Heroku (Backend)**
- Go to https://heroku.com
- Sign up for free account
- Install CLI: `npm install -g heroku`

**Vercel (Frontend)**
- Go to https://vercel.com
- Sign up with GitHub (recommended)
- CLI auto-installs with `npm install -g vercel`

---

### Step 2️⃣: Open Terminal & Navigate (1 minute)

```powershell
cd "c:\Users\Souvik\Desktop\Project\MNIT HACKATHON\newsguard-hackathon"
```

---

### Step 3️⃣: Deploy Backend to Heroku (3-5 minutes)

```powershell
# Login to Heroku
heroku login

# Go to backend
cd backend

# Create app
heroku create newsguard-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set FRONTEND_ORIGIN=https://newsguard-frontend.vercel.app
heroku config:set MODEL_VARIANT=hybrid

# Deploy
git push heroku main
```

**If git push fails**, try:
```powershell
git push heroku HEAD:main
```

**Wait for deployment to complete** (watch the output)

**Your backend URL**: `https://newsguard-api.herokuapp.com`

---

### Step 4️⃣: Deploy Frontend to Vercel (3-5 minutes)

```powershell
# Go to frontend
cd ../frontend

# Login to Vercel
vercel login

# Deploy with API URL
vercel --prod --env VITE_API_URL=https://newsguard-api.herokuapp.com
```

**When prompted**:
- Link to existing project? → **No**
- Project name → `newsguard-frontend`
- Framework → **React**
- Build → `npm run build`
- Output → `dist`

**Your frontend URL**: `https://newsguard-frontend.vercel.app` (shown at end)

---

### Step 5️⃣: Verify Deployment (2 minutes)

1. **Open frontend**: https://newsguard-frontend.vercel.app
2. **Try analyzer** with text like: *"SHOCKING news EXPOSED"*
3. **Check it works** → Results should appear!
4. **Test API**: 
   ```powershell
   curl https://newsguard-api.herokuapp.com/api/models
   ```

---

## ✅ You're Done!

Your live URLs:
- **App**: https://newsguard-frontend.vercel.app
- **API**: https://newsguard-api.herokuapp.com

**Share these with judges/team!**

---

## 🔧 If Something Goes Wrong

### Error: "Procfile not found"
→ Make sure you're in `backend/` folder when running `git push heroku main`

### Error: "CORS error" or "can't connect to API"  
→ Update Heroku backend:
```powershell
heroku config:set FRONTEND_ORIGIN=YOUR_VERCEL_URL
git push heroku main
```

### Error: "Port already in use"
→ Kill the process:
```powershell
lsof -ti:5000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Error: "Page not found" (404)
→ Your `vercel.json` handles this automatically. Refresh the page.

### Still stuck?
→ See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting

---

## 📚 Additional Resources

| File | Purpose |
|------|---------|
| [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) | Quick checklist (bookmark this) |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Full guide with all details |
| [README.md](./README.md) | Project documentation |
| [READY_FOR_DEPLOYMENT.md](./READY_FOR_DEPLOYMENT.md) | Technical summary |

---

## 🎉 What Happens After Deployment

✅ **Frontend** automatically deploys on commits (if you push to GitHub from Vercel)  
✅ **Backend** automatically redeploys on `git push heroku main`  
✅ **Stats** available in Heroku/Vercel dashboards  
✅ **Logs** accessible via CLI or dashboards  

---

## 💡 Pro Tips

1. **Bookmark your URLs** - You'll need to share them
2. **Test before sharing** - Try a few analyses first
3. **Check logs if issues** - `heroku logs --tail` is your friend
4. **Keep API URL private** - Only share frontend URL publicly
5. **Monitor costs** - Free tier is $0/month (perfect for hackathon)

---

## 🚀 Ready?

**Your 3 Options:**

**Option A: Automated (Easiest)**
```powershell
bash deploy.sh
```

**Option B: Manual (Above instructions)**
Follow Steps 1-5 above

**Option C: Detailed Reference**
See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)

---

## 📞 Quick Help

**Backend not starting?**
→ `heroku logs --tail --app newsguard-api`

**Frontend showing 404?**
→ It's normal for routes, automatically handled

**API timeout on first request?**
→ Normal (30s to start). Second request instant.

**API key errors?**
→ Check [DEPLOYMENT.md](./DEPLOYMENT.md) environment variables section

---

## ⏰ Timeline

- **5-10 min**: Create accounts + login
- **3-5 min**: Deploy backend
- **3-5 min**: Deploy frontend  
- **2 min**: Test
- **Total**: ~15 minutes ✅

---

## 🎯 Success Criteria

You've successfully deployed when:
- ✅ https://newsguard-frontend.vercel.app loads
- ✅ Analyzer accepts text input
- ✅ Backend returns credibility score
- ✅ No CORS errors in browser console
- ✅ You can share a working URL

---

**Start with Step 1️⃣ Above!**

Good luck! 🚀🎉
