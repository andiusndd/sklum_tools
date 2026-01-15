# Project Overview & PDR - SKLUM Tools

## 1. Introduction
**SKLUM Tools** is a comprehensive Blender Addon designed to streamline 3D production workflows. It provides a suite of utilities for Mesh checking, Material management, Batch renaming, Import/Export automation, and Object manipulation.

## 2. Product Vision
To become the "Swiss Army Knife" for 3D artists, ensuring quality control (Checking) and accelerating repetitive tasks (Automation) while protecting intellectual property via a robust Licensing System.

## 3. Key Features

### 3.1. Quality Assurance (Checker & Tools)
- **UV Checking**: Detect overlapping UVs, UVs outside 0-1 range.
- **Mesh Integrity**: Detect N-gons, Triangle counts, Sharp edges without seams.
- **Material Checks**: Validate Color Space (sRGB/Non-Color), Texture packing.
- **Origin/Transform**: Validate object origins and transform applications.

### 3.2. Workflow Acceleration
- **Auto Rename**: Batch renaming using CSV rules.
- **JPG Converter**: Mass convert PNG textures to JPG to reduce file size.
- **Import/Export**: Streamlined FBX/GLB export with automatic texture packing/cleaning.
- **Object Settings**: Quick access to common object properties (Shading, Visibility, Parenting) in one panel.

### 3.3. Licensing & DRM
- **Device Locking**: Limits usage to one machine per license key.
- **Online Validation**: Verifies keys against a cloud database (Supabase).
- **Security**: Obfuscated client-side logic to deter casual piracy.

## 4. Target Audience
- **3D Artists**: Modelers and Texture artists working on production pipelines.
- **QA Leads**: Responsible for verifying asset technical standards.

## 5. Deployment
- **Platform**: Windows (primary), macOS/Linux (supported by Blender API).
- **Distribution**: Zip File (generated via `/export` workflow).
- **Backend**: Vercel (API) + Supabase (Database).
