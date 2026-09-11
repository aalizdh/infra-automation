import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import pymysql

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            try:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO service_logs (service_name, status) VALUES ('backend_app', 'PING_OK');")
                    conn.commit()

                    cursor.execute("SELECT * FROM service_logs ORDER BY id DESC LIMIT 5;")
                    records = cursor.fetchall()
                conn.close()

                for r in records:
                    r['created_at'] = str(r['created_at'])

                response_data = {
                    "system_status": "OPERATIONAL",
                    "database_connection": "CONNECTED",
                    "recent_health_logs": records
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HealthHandler)
    print("Web server listening on port 8000...", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
