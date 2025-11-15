# Railway Setup - IMPORTANT

## The Problem
Railway is analyzing the **root directory** instead of the `backend/` folder. You need to tell Railway to use `backend/` as the root.

## Solution: Set Root Directory in Railway

### Step-by-Step:

1. **In Railway Dashboard:**
   - Go to your service/project
   - Click on **Settings** (gear icon)

2. **Set Root Directory:**
   - Scroll down to **"Root Directory"** section
   - Enter: `backend`
   - Click **Save**

3. **Set Build/Start Commands:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click **Save**

4. **Redeploy:**
   - Go to **Deployments** tab
   - Click **"..."** menu → **Redeploy**

## After Setting Root Directory

Railway will now:
- Look in `backend/` folder
- Find `requirements.txt` (Python detection)
- Find `main.py` (FastAPI app)
- Build and deploy correctly

## Alternative: Use Render.com (Easier)

If Railway continues to have issues, Render.com is simpler:

1. Go to https://render.com
2. **New** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend` ← IMPORTANT!
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

Render.com makes it clearer where to set the root directory.

