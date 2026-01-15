# URGENT: Update Vercel Environment Variables

## What Changed
We switched from direct PostgreSQL connection (`psycopg2`) to **Supabase REST API** to completely fix the IPv6 issue.

## Action Required
You need to update Vercel environment variables **NOW** before the new deployment works.

### Step 1: Get Supabase Anon Key
1. Go to [supabase.com](https://supabase.com/dashboard)
2. Open your project `sklum-license-db`
3. Go to **Settings** (gear icon) → **API**
4. Find **Project API keys** section
5. Copy the **`anon` `public`** key (it's safe to expose, starts with `eyJ...`)

### Step 2: Update Vercel Environment Variables
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Open your `sklum-license-backend` project
3. Go to **Settings** → **Environment Variables**
4. **DELETE** the old variables:
   - `SUPABASE_HOST`
   - `SUPABASE_USER`
   - `SUPABASE_PASS`
   - `SUPABASE_DB_NAME`
   - `SUPABASE_PORT`

5. **ADD** new variables:
   - **Name**: `SUPABASE_URL`
     **Value**: `https://pmemvmwnfrnvzbizdzii.supabase.co`
   
   - **Name**: `SUPABASE_ANON_KEY`
     **Value**: (Paste the anon key from Step 1)

### Step 3: Redeploy
1. Go to **Deployments** tab
2. Click the **three dots** on the latest deployment
3. Click **Redeploy**
4. Wait ~1 minute

### Step 4: Test
Try activating your license from Blender again.

## Why This Works
- REST API uses HTTPS (port 443) which always works
- No direct PostgreSQL connection (no port 5432 issues)
- No IPv4/IPv6 confusion
- More serverless-friendly (connection pooling handled by Supabase)

## Security Note
The `anon` key is **safe to expose publicly** - it only allows Row Level Security (RLS) operations. Since we don't have RLS enabled on the `licenses` table, it works like a service key for our use case.
