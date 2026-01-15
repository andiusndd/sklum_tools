# Implementation Plan: License Management System (Device Locking)

## Overview
Implement a comprehensive "License Key & Device Locking" system for SKLUMToolz to prevent unauthorized sharing.
This plan uses a **Client-Server** architecture (Serverless) to minimize costs (Free Tier focus).

## Architecture
- **Client (Addon)**: Python script to fetch `Machine_ID` (HWID) and validate against Server.
- **Server**: Hosted on **Vercel** (Free). API endpoints receiving JSON.
- **Database**: Hosted on **Supabase** (Free Postgres). Stores Keys and HWIDs.
- **Security**: Logic obfuscated via **PyArmor** (Standard) or **Cython** (Advanced).

## Phasing
- **Phase 1**: Client-Side Logic (HWID & UI).
- **Phase 2**: Backend API & Database Setup.
- **Phase 3**: Integration & Security Hardening (Obfuscation).

## Status
- [ ] Phase 1: Client-Side Logic
- [ ] Phase 2: Backend API & Database
- [ ] Phase 3: Integration & Obfuscation
