# Railway Deployment Fix

## Problem
Railway is not detecting Python correctly and showing "Railpack" errors.

## Solution

I've added the necessary configuration files. Now follow these steps:

### Step 1: Update Railway Settings

1. In Railway dashboard, go to your service
2. Click on **Settings**
3. Under **Build & Deploy**, make sure:
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty (or use `pip install -r requirements.txt`)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 2: Use Nixpacks (Recommended)

Railway should auto-detect Python with the new files. If it still doesn't:

1. Go to your Railway service
2. Click **Settings** → **Service**
3. Change **Buildpack** to **Nixpacks** (if available)
4. Redeploy

### Step 3: Manual Configuration

If auto-detection still fails:

1. In Railway, go to your service
2. Click **Settings** → **Variables**
3. Add: `RAILWAY_ENVIRONMENT=production`
4. Go to **Deployments** → Click **"..."** → **Redeploy**

### Alternative: Use Render.com Instead

If Railway continues to have issues, Render.com is more straightforward:

1. Go to https://render.com
2. **New** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Name**: `isa-simulator-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**

## Files Added

- `backend/railway.json` - Railway configuration
- `backend/nixpacks.toml` - Nixpacks build configuration  
- `backend/start.sh` - Startup script
- `backend/Procfile` - Heroku/Railway process file

These should help Railway detect and build your Python app correctly.

