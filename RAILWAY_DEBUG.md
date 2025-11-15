# Railway Backend Not Starting - Debug Guide

## Check Railway Logs

1. In Railway Dashboard → Your Service
2. Click **"Logs"** tab (or **"Observability"** → **"Logs"**)
3. Look for error messages

Common errors to look for:
- Import errors
- Port binding errors
- Module not found errors

## Common Fixes

### Fix 1: Update Start Command in Railway

1. Go to Railway → Your Service → **Settings**
2. Find **"Deploy"** section
3. **Custom Start Command** should be:
   ```
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Or if Railway sets PORT automatically, use:
   ```
   cd backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
5. Click **Update**
6. Redeploy

### Fix 2: Check Root Directory

1. In Railway Settings → **"Source"** section
2. **Root Directory** should be: `backend`
3. If it's empty or set to `.`, change it to `backend`
4. Save and redeploy

### Fix 3: Check Build Command

1. In Railway Settings → **"Build"** section
2. **Custom Build Command** should be:
   ```
   cd backend && pip install -r requirements.txt
   ```
3. Or leave it empty if Root Directory is set to `backend`

### Fix 4: Check Environment Variables

Make sure Railway has:
- `PORT` variable (Railway usually sets this automatically)
- No conflicting variables

## Quick Test: Check Logs

The logs will tell you exactly what's wrong. Common issues:

**"Module not found"** → Dependencies not installed
- Fix: Make sure build command runs `pip install -r requirements.txt`

**"Address already in use"** → Port conflict
- Fix: Use `$PORT` environment variable

**"No module named 'main'"** → Wrong directory
- Fix: Set Root Directory to `backend` OR use `cd backend` in start command

## Recommended Railway Settings

**Source:**
- Root Directory: `backend`

**Build:**
- Build Command: (leave empty if Root Directory is `backend`)
- OR: `pip install -r requirements.txt`

**Deploy:**
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- OR: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`

## Alternative: Use Render.com

If Railway continues to have issues, Render.com is more straightforward:

1. Go to https://render.com
2. **New** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

Render.com has better error messages and is easier to configure.

