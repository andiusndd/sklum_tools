
from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from datetime import datetime

# --- CONFIG (Use Environment Variables in Vercel) ---
# Supabase REST API Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")  # e.g., https://pmemvmwnfrnvzbizdzii.supabase.co
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")  # Anon/Public key from Supabase

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Parse Input
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        try:
            data = json.loads(body)
            key = data.get('key')
            hwid = data.get('hwid')
        except:
            self.send_error(400, "Invalid JSON")
            return

        if not key or not hwid:
            self._send_response(400, "Missing key or hwid")
            return

        # 2. Database Logic via Supabase REST API
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            # Check if key exists
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/licenses?key=eq.{key}&select=hwid,status",
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                self._send_response(500, f"Database query failed: {response.status_code}")
                return
                
            rows = response.json()
            
            if not rows or len(rows) == 0:
                self._send_response(404, "Invalid License Key")
                return
                
            license_data = rows[0]
            db_hwid = license_data.get('hwid')
            status = license_data.get('status')
            
            if status != 'active':
                self._send_response(403, "License is banned or inactive")
                return

            # Main Logic: Locking
            if db_hwid is None or db_hwid == "":
                # First time use -> Lock to this HWID
                update_response = requests.patch(
                    f"{SUPABASE_URL}/rest/v1/licenses?key=eq.{key}",
                    headers=headers,
                    json={"hwid": hwid, "last_check": datetime.utcnow().isoformat()},
                    timeout=10
                )
                
                if update_response.status_code in [200, 204]:
                    self._send_response(200, "Activated successfully (Locked to new machine)")
                else:
                    self._send_response(500, f"Failed to update license: {update_response.status_code}")
                
            elif db_hwid == hwid:
                # Same machine -> OK
                update_response = requests.patch(
                    f"{SUPABASE_URL}/rest/v1/licenses?key=eq.{key}",
                    headers=headers,
                    json={"last_check": datetime.utcnow().isoformat()},
                    timeout=10
                )
                
                if update_response.status_code in [200, 204]:
                    self._send_response(200, "License Valid")
                else:
                    self._send_response(500, f"Failed to update last_check: {update_response.status_code}")
                
            else:
                # Different machine -> BLOCK
                self._send_response(403, "Key locked to another machine. Please contact support to reset.")
            
        except requests.exceptions.Timeout:
            self._send_response(500, "Database connection timeout")
        except requests.exceptions.RequestException as e:
            self._send_response(500, f"Database Error: {str(e)}")
        except Exception as e:
            self._send_response(500, f"Unexpected Error: {str(e)}")

    def _send_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode('utf-8'))
