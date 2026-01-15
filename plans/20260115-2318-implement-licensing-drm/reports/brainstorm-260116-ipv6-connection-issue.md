# Database Connection Error Analysis (IPv6 Issue)

## Problem Statement
The Vercel serverless function is failing to connect to Supabase PostgreSQL with error:
```
connection to server at "db.pmemvmwnfrnvzbizdzii.supabase.co" (2406:da12:b78:de09:d571:a2dd:5c51:e641), port 5432 failed: Cannot assign requested address
```

## Root Cause Analysis

### Key Observations
1. **IPv6 Address**: The error shows `2406:da12:...` which is an IPv6 address
2. **"Cannot assign requested address"**: This typically means the client (Vercel) cannot establish an outbound connection using that address family
3. **Vercel Serverless Environment**: Vercel's serverless functions may have limited or no IPv6 support depending on region/configuration

### Why This Happens
- Supabase DNS returns both IPv4 and IPv6 addresses
- `psycopg2` (PostgreSQL driver) attempts to connect using the first resolved address
- If that's IPv6 and Vercel's network doesn't support IPv6 outbound connections, it fails
- The error occurs **before** reaching Supabase (network layer issue, not auth/firewall)

## Solution Approaches

### Option 1: Force IPv4 Connection (Recommended - Quick Fix)
**Approach:** Modify the connection string to use IPv4 explicitly.

**Implementation:**
```python
# In server_backend/api/index.py
# Instead of using hostname, resolve to IPv4 first
import socket

def get_ipv4_address(hostname):
    """Force IPv4 resolution"""
    try:
        # Get all addresses, filter for IPv4
        addrs = socket.getaddrinfo(hostname, None, socket.AF_INET)
        if addrs:
            return addrs[0][4][0]  # First IPv4 address
    except:
        pass
    return hostname  # Fallback to hostname

# Then in connection:
host = get_ipv4_address(os.environ.get('SUPABASE_HOST'))
conn = psycopg2.connect(
    host=host,  # Use resolved IPv4
    user=...,
    # ...
)
```

**Pros:**
- Simple, immediate fix
- No infrastructure changes needed
- Works within current Vercel/Supabase setup

**Cons:**
- Adds DNS resolution overhead (minimal)
- Hardcodes IPv4 preference (acceptable for now)

### Option 2: Use Supabase Connection Pooler (Better Long-term)
**Approach:** Use Supabase's built-in connection pooler which handles IPv4/IPv6 transparently.

**Implementation:**
Instead of direct PostgreSQL connection, use Supabase's pooler endpoint:
- **Direct:** `db.pmemvmwnfrnvzbizdzii.supabase.co:5432`
- **Pooler:** `db.pmemvmwnfrnvzbizdzii.supabase.co:6543` (port 6543)

Or use the REST API endpoint instead of raw SQL:
```python
# Use Supabase REST API instead of psycopg2
import requests

SUPABASE_URL = "https://pmemvmwnfrnvzbizdzii.supabase.co"
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')

response = requests.post(
    f"{SUPABASE_URL}/rest/v1/licenses?key=eq.{key}",
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
)
```

**Pros:**
- More robust (Supabase handles connection pooling)
- Better for serverless (connection reuse)
- No IPv4/IPv6 issues (HTTPS always works)

**Cons:**
- Requires code refactor (switch from `psycopg2` to REST API)
- Need to add Supabase API key to environment variables
- Slightly different query syntax

### Option 3: Check Vercel Region Settings
**Approach:** Ensure Vercel function is deployed in a region with proper IPv6 support or force IPv4.

**Implementation:**
- Check `vercel.json` for region settings
- Some regions have better IPv4/IPv6 support than others
- Add explicit region preference

**Pros:**
- Infrastructure-level fix
- May improve overall performance

**Cons:**
- May not solve the issue if Vercel fundamentally lacks IPv6
- Requires redeployment

## Recommended Solution

**Immediate Fix (Option 1):** Add IPv4 resolution helper to `server_backend/api/index.py`.

**Long-term (Option 2):** Migrate to Supabase REST API for better serverless compatibility.

## Implementation Priority

1. **Now:** Implement Option 1 (IPv4 forcing) - 5 minutes
2. **Next Week:** Consider Option 2 (REST API) if scaling issues arise
3. **Monitor:** Check Vercel logs for any other network issues

## Testing Steps
1. Deploy updated code with IPv4 fix
2. Test activation from Blender addon
3. Check Vercel function logs for successful connection
4. Verify license locking works correctly

## Risk Assessment
- **Low Risk:** IPv4 forcing is a safe, proven workaround
- **No Breaking Changes:** Existing functionality preserved
- **Fallback:** If IPv4 resolution fails, falls back to hostname (current behavior)
