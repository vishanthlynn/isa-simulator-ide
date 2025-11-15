# Quick Backend Deployment Guide

## 🚀 Fastest Option: Railway (5 minutes)

### Step 1: Deploy Backend
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your `isa-simulator-ide` repository
5. In project settings, set **Root Directory** to `backend`
6. Railway will auto-detect Python and deploy!
7. Wait for deployment to complete
8. Copy your Railway app URL (e.g., `https://isa-simulator-xxxx.railway.app`)

### Step 2: Update Vercel Environment Variables
1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Click on your `isa-simulator-ide` project
3. Go to **Settings** → **Environment Variables**
4. Add these two variables:

   **Variable 1:**
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-railway-app.railway.app` (use your actual Railway URL)
   - Environment: Production, Preview, Development (select all)

   **Variable 2:**
   - Name: `REACT_APP_WS_URL`
   - Value: `wss://your-railway-app.railway.app/ws/simulate` (use `wss://` not `ws://`)
   - Environment: Production, Preview, Development (select all)

5. Click **Save**
6. Go to **Deployments** tab
7. Click the **"..."** menu on the latest deployment → **Redeploy**

### Step 3: Test
1. Wait for Vercel to redeploy (1-2 minutes)
2. Visit your Vercel site
3. The warning should disappear
4. Try clicking "Assemble" - it should work!

## ✅ That's it!

Your app should now be fully functional.

## 🔧 Alternative: Render.com

If Railway doesn't work:

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New"** → **"Web Service"**
4. Connect your GitHub repo
5. Settings:
   - **Name**: `isa-simulator-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click **"Create Web Service"**
7. Copy the Render URL
8. Follow Step 2 above to update Vercel environment variables

## 🐛 Troubleshooting

**Backend not starting?**
- Check Railway/Render logs
- Make sure `requirements.txt` is in the `backend/` folder
- Verify the start command is correct

**Still getting CORS errors?**
- Make sure your backend URL is correct in environment variables
- Check that backend CORS includes your Vercel domain (already done in code)

**WebSocket not connecting?**
- Use `wss://` (secure) not `ws://` for production
- Check backend logs for WebSocket errors

## 📝 Notes

- The backend needs to stay running 24/7 (Railway/Render free tiers have limits)
- For production, consider upgrading to paid plans
- The frontend will automatically use the environment variables after redeploy

