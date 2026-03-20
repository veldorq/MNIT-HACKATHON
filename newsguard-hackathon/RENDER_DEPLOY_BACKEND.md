# Deploy Backend to Render (5 minutes)

## Step 1: Go to Render Dashboard
1. Open https://render.com
2. Sign up with **GitHub** (use your GitHub account)
3. Authorize Render to access your GitHub repositories

## Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Choose **`newsguard-hackathon`** repository from the list

## Step 3: Configure Service
Fill in these exact values:

| Field | Value |
|-------|-------|
| **Name** | `newsguard-api` |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| **Plan** | Free |
| **Region** | Oregon (or closest to you) |

## Step 4: Add Environment Variables
Click **"Advanced"** and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PORT` | `8000` |

## Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. **Copy your URL** when it's ready (looks like: `https://newsguard-api-xxxx.onrender.com`)

## Step 6: Test Backend
Open in browser:
```
https://newsguard-api-xxxx.onrender.com/health
```
Should return: `{"status": "ok"}`

## Troubleshooting

**Build fails with "Railpack" error?**
- This shouldn't happen with render.yaml—Render should use Python buildpack automatically

**Service times out?**
- On free tier, services sleep after 15 min of inactivity
- First request takes 10-30 seconds to wake up (normal)

**Port not found?**
- Render automatically sets `$PORT` environment variable
- Our Procfile already handles this correctly

## Save Your Backend URL
Once deployment succeeds, you'll have a URL like:
```
https://newsguard-api-abc123.onrender.com
```
**Save this for frontend deployment!**
