# 🚀 Railway Deployment - EXACT STEPS

## ✅ One-Time Setup (2 minutes)

### Step 1: Sign Up for Railway
1. Go to **https://railway.app**
2. Click **"Start Project"** button (top right)
3. Choose **"Deploy from GitHub"**
4. **Connect your GitHub account** (click "Deploy with GitHub")
   - GitHub will ask permission - approve it
5. You'll be logged into Railway

---

## 🔧 Deploy Backend API

### Step 2: Create Backend Project
1. On Railway dashboard, click **"New Project"**
2. Choose **"Deploy from GitHub Repo"**
3. Find your repo: **`newsguard-hackathon`**
4. Click to select it
5. Wait for Railway to load (30 seconds)

### Step 3: Configure Backend
Railway will show you settings. Make these changes:

1. **Root Directory**: Change to `newsguard-hackathon/backend`
   - Click in the field and type: `newsguard-hackathon/backend`
   
2. **Add Environment Variables** (click "Add Variable"):
   - **Name**: `FLASK_ENV`
   - **Value**: `production`
   - Click Add

3. **Set Port** (if asked):
   - **PORT**: `8000` or leave default
   - Railway handles this automatically usually

### Step 4: Deploy Backend
1. Click **"Deploy"** button
2. **Wait 2-3 minutes** while Railway builds
   - You'll see logs scrolling
   - Look for "✓ Build Successful"
3. Once done, copy your **Backend URL** (shown at top):
   - Example: `https://newsguard-api-prod-xxx.railway.app`
   - **SAVE THIS URL** - you need it for frontend!

---

## 🎨 Deploy Frontend on Vercel

### Step 5: Go to Vercel
1. Go to **https://vercel.com**
2. Click **"New Project"**
3. Choose **"Import an existing project"**
4. Find your GitHub repo: **`newsguard-hackathon`**
5. Click **"Import"**

### Step 6: Configure Frontend
Vercel will ask for settings:

1. **Root Directory**: Keep as `newsguard-hackathon/`
   - Or select `newsguard-hackathon/frontend` if options available

2. **Build Command**: 
   - Make sure it says: `npm run build`

3. **Output Directory**: 
   - Make sure it says: `frontend/dist`

4. **Environment Variables** - IMPORTANT:
   - Click **"Add Environment Variable"**
   - **Name**: `VITE_API_URL`
   - **Value**: `[PASTE YOUR RAILWAY BACKEND URL HERE]`
     - Example: `https://newsguard-api-prod-xxx.railway.app`
   - Click Save

### Step 7: Deploy Frontend
1. Click **"Deploy"** button
2. **Wait 2-3 minutes** for build
   - Look for green checkmark
3. Once done, you'll see your **Frontend URL** (at top):
   - Example: `https://newsguard-frontend.vercel.app`
   - **SAVE THIS URL** - this is your live site!

---

## ✅ Final Verification

### Step 8: Test Everything Works
1. Open your **Frontend URL** in browser
2. You should see NewsGuard interface
3. Try these tests:

**Test 1: Fake News Detection**
- Paste: `"Biden's secret plan will destroy America"`
- Expected: Shows fake news prediction

**Test 2: AI Detection**
- Paste: `"However, it is important to acknowledge that while experts argue this approach has merit, furthermore research suggests that potentially such initiatives could be synergistic with transformative outcomes."`
- Expected: Shows AI score (should be high, like 70-90%)

**Test 3: Real News**
- Paste: Real news article
- Expected: Low fake score, low AI score

---

## 🎉 You're Done!

**Your Live URLs:**

| Component | URL |
|-----------|-----|
| **Frontend** | `https://newsguard-frontend.vercel.app` (or custom) |
| **Backend API** | `https://newsguard-api-prod-xxx.railway.app` |
| **GitHub Repo** | Your repo (auto-synced) |

---

## 📝 What Happens Next

- **Any commits to GitHub** → Auto-deploys to both services
- **Live monitoring** → Both services show logs
- **Scaling** → Free tier handles ~1000 requests/day
- **Custom domains** → Both services support custom domains (paid)

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Build failed" on Railway | Check that you set Root Directory to `newsguard-hackathon/backend` |
| Frontend shows "Cannot reach API" | Make sure VITE_API_URL env var has your Railway URL (no trailing /) |
| AI detection not working | Verify backend deployed successfully (check Railway logs) |
| Old version still showing | Clear browser cache (Ctrl+Shift+Delete) |

---

## 🆘 Support

If any step fails:
1. **Check Railway logs**: Click your project → Logs tab
2. **Check Vercel logs**: Click your project → Logs tab
3. **Common fixes**:
   - Wrong environment variables
   - Typo in URLs
   - Browser cache issues

---

Done! You now have a production-ready NewsGuard deployment! 🚀
