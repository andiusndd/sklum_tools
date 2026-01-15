# Brainstorm: License Management & Device Locking (DRM)

## 1. Problem Statement
User wants to implement a Digital Rights Management (DRM) system for a Blender Addon to:
- Enforce "1 License Key = 1 Device" policy.
- Prevent license sharing.
- Track and control usage (see who is active).

## 2. Core Constraints & Brutal Truths
- **Python is Open**: Python code (.py) is open-source by nature. Any logic written in Python can be read and deleted by a user with basic knowledge.
- **The "Lock" Illusion**: Without compiling (C++/Rust) or heavy obfuscation, client-side checks are merely "psychological barriers" for honest users, not real security against crackers.
- **Requirement for Server**: To "control" and "track", the addon MUST communicate with an online server. You cannot do this offline.

## 3. Architecture Options

### Option A: The "Gentleman's Lock" (Easiest)
- **Mechanism**: 
    - Addon generates a `Hardware ID` (Motherboard UUID / Disk Serial).
    - Sends `(LicenseKey, HardwareID)` to your Server.
    - Server checks: "Is this Key already bound to a *different* HardwareID?"
    - If Yes -> Block. If No -> Bind and Allow.
- **Protection Level**: **Low**. 
    - Users can open the source code and remove the check.
- **Cost**: Low (Simple PHP/Python script on any cheap hosting).
- **Control**: High (You see all IPs, HWIDs, and Keys on your database).

### Option B: The "Armored Python" (Recommended Balance)
- **Mechanism**: Same as Option A, BUT:
    - The critical verification logic is **Obfuscated** using **PyArmor** or compiled with **Nuitka**.
    - The entry point `__init__.py` calls this obfuscated module.
- **Protection Level**: **Medium**. 
    - Stops 99% of casual users. Hard to read/modify without dedication.
- **Cost**: Low dev cost, but need to set up build pipeline.

### Option C: The SaaS Model (Uncrackable)
- **Mechanism**: 
    - Move core features (e.g., the "Smart Check" algorithm) to the Cloud API.
    - Addon sends data to API -> API processes -> Returns result.
    - API checks License+HWID before processing.
- **Protection Level**: **Ultimate**. 
    - Code on client is useless without the server.
- **Cost**: **High**. Server costs, latency, privacy concerns from users.

## 4. Recommended Solution: Option B (PyArmor + Simple License Server)
This provides the "Control" you want (via Server) and enough "Security" (via Obfuscation) to deter sharing, while keeping costs manageable (KISS).

### Technical Stack
1.  **Client (Addon)**:
    - Logic to get Unique Machine ID (Windows `wmic csproduct get uuid`).
    - `requests` lib to call your API.
    - **PyArmor** to pack the `license_check.py`.
2.  **Server (The Control Center)**:
    - A simple Web API (Python FastAPI or PHP).
    - Database (SQLite/MySQL): `Table_Licenses [Key, HW_ID, Status, Last_IP, Updated_At]`.
    - Admin Dashboard (to view/ban users).
3.  **Payment Integration**:
    - Webhook from (SePay/Polar/Gumroad) -> Calls your Server to "Create New Key" in DB.

## 5. Implementation Roadmap
1.  **Server Setup**: Build a simple API (`/activate`, `/check`) and Database.
2.  **Addon Logic**: Implement `get_machine_id()` and API calls.
3.  **Build Pipeline**: Set up PyArmor to obfuscate the tracking code before distributing.
4.  **Admin UI**: Simple page to see your users.

## 6. Risk Assessment
- **False Positives**: User changes hardware (new disk) -> HWID changes -> Locked out. 
    - *Mitigation*: Build a "Reset License" limit (e.g., allow reset once per month).
- **Server Down**: If your server dies, no one can use the addon.
    - *Mitigation*: Fail-open (allow access if server unreachable) OR ensure high uptime.
- **Cracked**: A pro cracker can still dump the memory.
    - *Mitigation*: Accept it. You are stopping sharing, not the NSA.

## 7. Next Steps
- Determine where to host the server (VPS $5/mo or existing hosting?).
- Decide on the database technology.
- Start with a "Proof of Concept" (Phase 1) - just the Python Logic + Mock Server.
