# Vercel Deployment Guide

## Frontend Deployment (Current)

The frontend is configured to deploy on Vercel. The `vercel.json` file tells Vercel to:
- Build from the `frontend/` directory
- Use React build output
- Serve the React app with proper routing

## Backend Deployment

**Important:** The backend (FastAPI) needs to be deployed separately. Vercel doesn't natively support Python backends well. Options:

### Option 1: Deploy Backend to Railway/Render/Fly.io
1. Deploy backend to one of these services
2. Update environment variables in Vercel:
   - `REACT_APP_API_URL` = your backend URL (e.g., `https://your-backend.railway.app`)
   - `REACT_APP_WS_URL` = your WebSocket URL (e.g., `wss://your-backend.railway.app/ws/simulate`)

### Option 2: Use Vercel Serverless Functions (Advanced)
Convert the FastAPI backend to Vercel serverless functions (requires refactoring)

### Option 3: Local Development Only
For now, the app works locally. To use on Vercel:
1. Deploy backend separately
2. Add environment variables in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add `REACT_APP_API_URL` and `REACT_APP_WS_URL`

## Current Status

The frontend will deploy but will show errors because it can't connect to `localhost:8000`. You need to:
1. Deploy the backend somewhere
2. Update the environment variables
3. Redeploy the frontend

## Quick Fix for Testing

If you just want to test the frontend deployment, you can temporarily disable the backend connection or show a message that backend needs to be configured.

