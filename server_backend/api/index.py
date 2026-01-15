
from http.server import BaseHTTPRequestHandler
import json
import os
import psycopg2
from urllib.parse import parse_qs, urlparse

# --- CONFIG (Use Environment Variables in Vercel) ---
DB_HOST = os.environ.get("SUPABASE_HOST")
DB_NAME = os.environ.get("SUPABASE_DB_NAME", "postgres")
DB_USER = os.environ.get("SUPABASE_USER")
DB_PASS = os.environ.get("SUPABASE_PASS")
DB_PORT = os.environ.get("SUPABASE_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

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

        # 2. Database Logic
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Check if key exists
            cur.execute("SELECT hwid, status FROM licenses WHERE key = %s", (key,))
            row = cur.fetchone()
            
            if not row:
                self._send_response(404, "Invalid License Key")
                cur.close()
                conn.close()
                return
                
            db_hwid, status = row
            
            if status != 'active':
                self._send_response(403, "License is banned or inactive")
                cur.close()
                conn.close()
                return

            # Main Logic: Locking
            if db_hwid is None or db_hwid == "":
                # First time use -> Lock to this HWID
                cur.execute("UPDATE licenses SET hwid = %s, last_check = NOW() WHERE key = %s", (hwid, key))
                conn.commit()
                self._send_response(200, "Activated successfully (Locked to new machine)")
                
            elif db_hwid == hwid:
                # Same machine -> OK
                cur.execute("UPDATE licenses SET last_check = NOW() WHERE key = %s", (key,))
                conn.commit()
                self._send_response(200, "License Valid")
                
            else:
                # Different machine -> BLOCK
                self._send_response(403, f"Key locked to another machine. Please contact support to reset.")

            cur.close()
            conn.close()
            
        except Exception as e:
            self._send_response(500, f"Database Error: {str(e)}")

    def _send_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode('utf-8'))
