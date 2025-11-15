# Backend Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `isa-simulator-ide` repository
5. Set Root Directory to `backend`
6. Railway will auto-detect Python and install dependencies
7. Add environment variable: `PORT=8000` (Railway sets this automatically)
8. Deploy!

**After deployment:**
- Copy your Railway app URL (e.g., `https://your-app.railway.app`)
- In Vercel, go to Project Settings → Environment Variables
- Add:
  - `REACT_APP_API_URL` = `https://your-app.railway.app`
  - `REACT_APP_WS_URL` = `wss://your-app.railway.app/ws/simulate`
- Redeploy frontend

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Sign up/login
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Settings:
   - **Name**: isa-simulator-backend
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `PORT=8000`
7. Deploy!

**After deployment:**
- Copy your Render URL
- Update Vercel environment variables as above

### Option 3: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. In `backend/` directory, run: `fly launch`
3. Follow prompts
4. Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
5. Deploy: `fly deploy`

### Option 4: PythonAnywhere (Free tier available)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your backend files
3. Configure web app
4. Set up virtual environment and install dependencies
5. Update Vercel environment variables

## Update CORS in Backend

Make sure your backend `main.py` allows your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://isa-simulator-ide.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables Checklist

After deploying backend, add these in Vercel (Project Settings → Environment Variables):

- ✅ `REACT_APP_API_URL` = `https://your-backend-url.com`
- ✅ `REACT_APP_WS_URL` = `wss://your-backend-url.com/ws/simulate` (note: `wss://` for secure WebSocket)

**Important:** Use `wss://` (secure WebSocket) not `ws://` for production!

## Testing

1. Deploy backend
2. Test backend URL: `https://your-backend-url.com/` should return JSON
3. Update Vercel environment variables
4. Redeploy frontend (or wait for auto-deploy)
5. Test the full app!

## Troubleshooting

**CORS errors?**
- Make sure backend CORS includes your Vercel domain
- Check backend logs

**WebSocket not connecting?**
- Use `wss://` not `ws://` for production
- Check backend WebSocket endpoint is accessible

**Backend not starting?**
- Check logs in your hosting platform
- Verify `requirements.txt` is correct
- Make sure port is configured correctly

