# BoostMyYT Deployment Guide

## 1. Deploy the Backend (Render)
1. Go to [Render](https://render.com) and sign in.
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository (`https://github.com/23f2003763/MicroSaaSYoutube`).
4. Configure the settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. 
6. Once deployed, copy the Render backend URL (e.g., `https://boostmyyt-backend.onrender.com`).

## 2. Connect Backend to Frontend
1. Open `frontend/index.html`.
2. Find the line: `const API_URL = 'http://127.0.0.1:8000'; // PLACEHOLDER_BACKEND_URL`
3. Replace the `http://127.0.0.1:8000` with your new Render backend URL.
4. Commit and push this change to GitHub.

## 3. Deploy the Frontend (Netlify)
1. Go to [Netlify](https://www.netlify.com) and sign in.
2. Click **Add new site** > **Import an existing project**.
3. Select GitHub and choose your repository (`MicroSaaSYoutube`).
4. Netlify will automatically detect the `netlify.toml` file and set the publish directory to `frontend`.
5. Click **Deploy site**.
6. Once deployed, you will get your live frontend URL!

## 4. Setup Razorpay Payment Link
1. Go to your Razorpay Dashboard.
2. Navigate to **Payment Links**.
3. Create a new Payment Link for the "Unlock Viral Script Template" product (set price to ₹399).
4. Copy the generated Payment Link URL.
5. In `frontend/index.html`, find: `YOUR_RAZORPAY_PAYMENT_LINK_HERE`.
6. Replace it with your actual Razorpay link.
7. Commit and push the changes (Netlify will automatically redeploy).
