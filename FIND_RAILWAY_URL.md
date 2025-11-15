# How to Find Your Railway Backend URL

## Step 1: Get the URL from Railway

1. **In Railway Dashboard:**
   - Go to your service (the one that just deployed)
   - Look at the top of the service page
   - You should see a section called **"Domains"** or **"Networking"**

2. **Find the Generated Domain:**
   - Railway automatically creates a domain like: `your-app-name.up.railway.app`
   - Or you might see it in the **"Settings"** → **"Networking"** section
   - It will look something like: `https://isa-simulator-production-xxxx.up.railway.app`

3. **Copy the URL:**
   - Copy the full URL (including `https://`)

## Step 2: Update Vercel Environment Variables

1. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard
   - Click on your `isa-simulator-ide` project

2. **Go to Settings → Environment Variables:**
   - Click **Settings** tab
   - Click **Environment Variables** in the sidebar

3. **Add/Update these variables:**

   **Variable 1:**
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-railway-url.up.railway.app` (your actual Railway URL)
   - Environments: ✅ Production, ✅ Preview, ✅ Development

   **Variable 2:**
   - Name: `REACT_APP_WS_URL`
   - Value: `wss://your-railway-url.up.railway.app/ws/simulate` (use `wss://` not `ws://`)
   - Environments: ✅ Production, ✅ Preview, ✅ Development

4. **Save** the variables

5. **Redeploy Frontend:**
   - Go to **Deployments** tab
   - Click **"..."** menu on latest deployment
   - Click **Redeploy**

## Step 3: Test

1. Wait for Vercel to redeploy (1-2 minutes)
2. Visit your Vercel site
3. The warning should disappear
4. Try clicking "Assemble" - it should work!

## Quick Check: Test Your Backend URL

Before adding to Vercel, test your Railway URL:

1. Open: `https://your-railway-url.up.railway.app/`
2. You should see: `{"message":"ISA Simulator API","version":"1.0.0"}`

If you see that JSON response, your backend is working!

## If You Can't Find the URL

1. In Railway, go to your service
2. Click **Settings** → **Networking**
3. Look for **"Public Domain"** or **"Generate Domain"**
4. Railway should have auto-generated one
5. If not, click **"Generate Domain"**

