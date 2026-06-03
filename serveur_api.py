# CyberMap 3D - Mini serveur API
# Auteur : Hugo B.

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import sys
import os
import json

RACINE = os.path.dirname(os.path.abspath(__file__))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/generer-rapport":
            try:
                script = os.path.join(RACINE, "core", "rapport.py")
                subprocess.run([sys.executable, script], cwd=os.path.join(RACINE, "core"))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"succes": True, "message": "Rapport genere !"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"succes": False, "message": str(e)}).encode())

        elif self.path == "/scanner":
            try:
                script = os.path.join(RACINE, "core", "scanner_ports.py")
                subprocess.run([sys.executable, script], cwd=os.path.join(RACINE, "core"))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"succes": True, "message": "Scan termine !"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"succes": False, "message": str(e)}).encode())

        elif self.path == "/alertes":
            try:
                alertes_path = os.path.join(RACINE, "data", "alertes.json")
                if os.path.exists(alertes_path):
                    with open(alertes_path, "r") as f:
                        alertes = f.read()
                else:
                    alertes = "[]"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(alertes.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"erreur": str(e)}).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[API] {args[0]} {args[1]}")

print("=" * 50)
print("CyberMap 3D - Serveur API")
print("API disponible sur http://localhost:8001")
print("=" * 50)

serveur = HTTPServer(("localhost", 8001), Handler)
serveur.serve_forever()