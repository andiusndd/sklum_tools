# Phase 2: Backend API & Database Setup

## Context
A server is required to store the valid keys and the HWIDs they are locked to. We will use **Vercel** (Hosting) and **Supabase** (DB) as they are free and reliable.

## Architecture
- **Language**: Python (FastAPI or Flask) running on Vercel Serverless Functions.
- **Database**: PostgreSQL (Supabase).
    - Table `licenses`:
        - `key` (VARCHAR, PK)
        - `email` (VARCHAR, Nullable) - User email (optional, for support/recovery).
        - `hwid` (VARCHAR, Nullable) - Stores the locked Machine ID.
        - `status` (VARCHAR) - 'active', 'banned'.
        - `last_check` (TIMESTAMP).

## Implementation Steps
1.  **Prepare Server Code Folder**: Create a folder `server_backend/` (outside addon).
2.  **Write API Code (`api/index.py`)**:
    -   `POST /api/activate`:
        -   Input: `{ key, hwid }`
        -   Logic:
            -   Check if key exists.
            -   If key has NO hwid -> Save hwid -> Return Success.
            -   If key has hwid == input -> Return Success.
            -   If key has hwid != input -> Return Fail ("Key used on another machine").
3.  **Deployment Guide**:
    -   Instruct user to push `server_backend` to GitHub and connect Vercel.
    -   Instruct user to create Supabase project and get URL/KEY.

## Todo List
- [ ] Create `server_backend/api/index.py` skeleton.
- [ ] Defined Database Schema (SQL).
- [ ] Write `requirements.txt` for Vercel.
