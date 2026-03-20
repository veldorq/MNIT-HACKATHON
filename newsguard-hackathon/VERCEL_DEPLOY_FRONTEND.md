# Deploy Frontend to Vercel (5 minutes)

## Prerequisites
- Backend URL from Render (e.g., `https://newsguard-api-xxxx.onrender.com`)
- This should be deployed AFTER backend

## Step 1: Go to Vercel
1. Open https://vercel.com
2. Sign up with **GitHub** (use your GitHub account)
3. Authorize Vercel to access your GitHub repositories

## Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Select **"Import Git Repository"**
3. Find and select **`newsguard-hackathon`**
4. Click **"Import"**

## Step 3: Configure Project
On the "Configure Project" page:

| Field | Value |
|-------|-------|
| **Project Name** | `newsguard-frontend` (or any name) |
| **Framework Preset** | `Other` (or leave as is) |
| **Root Directory** | `frontend` |

## Step 4: Add Environment Variables
Under **"Environment Variables"**, add:

| Name | Value |
|------|-------|
| `VITE_API_URL` | Your Render backend URL |

**Example:** If your backend URL is `https://newsguard-api-abc123.onrender.com`, set:
```
VITE_API_URL=https://newsguard-api-abc123.onrender.com
```

## Step 5: Deploy
1. Click **"Deploy"**
2. Wait 1-2 minutes for build to finish
3. **Copy your frontend URL** when ready (looks like: `https://newsguard-frontend-xxx.vercel.app`)

## Step 6: Test Frontend
1. Open your Vercel URL in browser
2. Try detecting fake news
3. Try analyzing AI-generated text
4. Verify API calls are going to your Render backend

## Save Your Frontend URL
Once deployment succeeds, you'll have a URL like:
```
https://newsguard-frontend-abc123.vercel.app
```
**This is your final production URL for judges!**
