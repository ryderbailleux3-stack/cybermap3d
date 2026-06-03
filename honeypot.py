# CyberMap 3D - Honeypot
# Auteur : Hugo B.

import socket
import json
from datetime import datetime
import threading

LOG_FILE = "../data/honeypot_log.json"
tentatives = []

def logger(ip, port, message):
    entree = {
        "heure": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "ip": ip,
        "port": port,
        "message": message
    }
    tentatives.append(entree)
    print(f"🚨 [{entree['heure']}] Tentative depuis {ip}:{port} → {message}")
    with open(LOG_FILE, "w") as f:
        json.dump(tentatives, f, indent=4)

def honeypot_ssh(port=2222):
    """Faux serveur SSH"""
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(("0.0.0.0", port))
    serveur.listen(5)
    print(f"🍯 Honeypot SSH actif sur le port {port}")

    while True:
        try:
            client, adresse = serveur.accept()
            ip = adresse[0]
            # Envoyer une fausse bannière SSH
            client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
            # Recevoir la réponse
            data = client.recv(1024)
            logger(ip, port, f"SSH: {data[:50]}")
            client.close()
        except:
            pass

def honeypot_http(port=8080):
    """Faux serveur HTTP"""
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(("0.0.0.0", port))
    serveur.listen(5)
    print(f"🍯 Honeypot HTTP actif sur le port {port}")

    while True:
        try:
            client, adresse = serveur.accept()
            ip = adresse[0]
            data = client.recv(1024).decode("utf-8", errors="ignore")
            # Logger la requête
            premiere_ligne = data.split("\n")[0] if data else "vide"
            logger(ip, port, f"HTTP: {premiere_ligne}")
            # Envoyer une fausse réponse
            reponse = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Admin Panel</h1>"
            client.send(reponse)
            client.close()
        except:
            pass

def honeypot_ftp(port=2121):
    """Faux serveur FTP"""
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(("0.0.0.0", port))
    serveur.listen(5)
    print(f"🍯 Honeypot FTP actif sur le port {port}")

    while True:
        try:
            client, adresse = serveur.accept()
            ip = adresse[0]
            client.send(b"220 FTP Server Ready\r\n")
            data = client.recv(1024).decode("utf-8", errors="ignore").strip()
            logger(ip, port, f"FTP: {data}")
            client.send(b"331 Password required\r\n")
            data2 = client.recv(1024).decode("utf-8", errors="ignore").strip()
            logger(ip, port, f"FTP mot de passe: {data2}")
            client.send(b"530 Login incorrect\r\n")
            client.close()
        except:
            pass

print("=" * 50)
print("🍯 CyberMap 3D - Honeypot activé !")
print("=" * 50)
print("En attente de connexions suspectes...\n")

# Lancer les 3 honeypots en parallèle
t1 = threading.Thread(target=honeypot_ssh,  daemon=True)
t2 = threading.Thread(target=honeypot_http, daemon=True)
t3 = threading.Thread(target=honeypot_ftp,  daemon=True)

t1.start()
t2.start()
t3.start()

print("💡 Pour tester le honeypot HTTP ouvre :")
print("   http://localhost:8080\n")

try:
    while True:
        pass
except KeyboardInterrupt:
    print(f"\n✅ Honeypot arrêté — {len(tentatives)} tentative(s) enregistrée(s)")