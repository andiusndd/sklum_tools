# Deployment Guide: Vercel + Supabase (Zero Cost)

This guide walks you through deploying your License Server (`server_backend/`) for free.

## Step 1: Database Setup (Supabase)
Supabase provides the free PostgreSQL database.

1.  **Sign Up/Login**: Go to [supabase.com](https://supabase.com) and log in with GitHub.
2.  **Create Project**: Click "New Project".
    -   **Name**: `sklum-license-db` (or anything).
    -   **Password**: **IMPORTANT!** Write this down (e.g., in a Notepad). You CANNOT see it again.
    -   **Region**: Singapore (for Vietnam speed) or US East.
3.  **Run SQL Schema**:
    -   After project is created (takes ~2 mins), go to the **SQL Editor** (icon looking like specific text/code on the left bar).
    -   Click "New query".
    -   Open file `server_backend/schema.sql` on your PC, copy ALL text.
    -   Paste into Supabase SQL Editor and click **RUN**.
    -   *Success check*: You should see "Success" and no errors.
4.  **Get Connection Details**:
    -   Go to **Project Settings** (Gear icon) -> **Database**.
    -   Find **Connection parameters**. Copy these:
        -   `Host` (e.g., `db.xyz.supabase.co`)
        -   `User` (usually `postgres`)
        -   `Port` (5432)
        -   `Database Name` (usually `postgres`)
    -   *Keep these for Step 3.*

---

## Step 2: Push Code to GitHub
Vercel needs your code on GitHub to deploy.

1.  **Create New Repo**: Go to [github.com/new](https://github.com/new).
    -   Name: `sklum-license-backend`.
    -   Public or Private (Private is better for security, Vercel supports both).
2.  **Push Code**:
    Open Terminal in your project folder `SKLUMToolz`:
    ```powershell
    # Move backend to a separate folder to avoid confusion (Recommended)
    cd ..
    mkdir sklum-license-backend
    cp -r SKLUMToolz/server_backend/* sklum-license-backend/
    cd sklum-license-backend
    
    # Init Git and Push
    git init
    git add .
    git commit -m "Initial backend"
    git branch -M main
    git remote add origin https://github.com/YOUR_USER/sklum-license-backend.git
    git push -u origin main
    ```
    *(Or just upload files manually via Web Interface if you are not comfortable with CLI)*

---

## Step 3: Deploy to Vercel
Vercel hosts the Python API.

1.  **Sign Up/Login**: Go to [vercel.com](https://vercel.com) (Login with GitHub).
2.  **Add New Project**: Click "Add New..." -> "Project".
3.  **Import Repo**: Find `sklum-license-backend` in the list and click **Import**.
4.  **Configure Project**:
    -   **Framework Preset**: Other (default is fine, Vercel detects Python).
    -   **Root Directory**: `./` (default).
    -   **Environment Variables** (This is CRITICAL):
        Expand the section and add the values from Supabase (Step 1):
        -   `SUPABASE_HOST`: (Paste Host)
        -   `SUPABASE_USER`: `postgres`
        -   `SUPABASE_PASS`: (The password you generated in Step 1)
        -   `SUPABASE_DB_NAME`: `postgres`
        -   `SUPABASE_PORT`: `5432`
5.  **Deploy**: Click **Deploy**.
    -   Wait ~1 minute. You should see confetti 🎉.
6.  **Get URL**:
    -   Click "Continue to Dashboard".
    -   Your domain will be something like: `https://sklum-license-backend.vercel.app`.
    -   **Test it**: Go to `https://sklum-license-backend.vercel.app/api/index`. It might say "Method Not Allowed" (because it expects POST), which means **IT IS WORKING**.

---

## Step 4: Final Integration
Come back here and tell me:
> "My URL is: https://sklum-license-backend.vercel.app"

I will then update the Addon to use this URL.
