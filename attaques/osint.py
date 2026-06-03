# CyberMap 3D - OSINT (Open Source Intelligence)
# Auteur : Hugo B.
# Collecte d'informations publiques sur une cible

import requests
import json
import socket
from datetime import datetime

def rechercher_ip(domaine):
    """Trouve l'IP d'un domaine"""
    try:
        ip = socket.gethostbyname(domaine)
        print(f"[+] IP de {domaine} : {ip}")
        return ip
    except:
        print(f"[-] Impossible de resoudre {domaine}")
        return None

def infos_ip(ip):
    """Obtient les infos publiques d'une IP"""
    try:
        print(f"\n[*] Recherche infos pour {ip}...")
        reponse = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = reponse.json()

        if data["status"] == "success":
            print(f"[+] Pays        : {data.get('country', 'Inconnu')}")
            print(f"[+] Region      : {data.get('regionName', 'Inconnu')}")
            print(f"[+] Ville       : {data.get('city', 'Inconnu')}")
            print(f"[+] FAI         : {data.get('isp', 'Inconnu')}")
            print(f"[+] Organisation: {data.get('org', 'Inconnu')}")
            print(f"[+] Latitude    : {data.get('lat', 'Inconnu')}")
            print(f"[+] Longitude   : {data.get('lon', 'Inconnu')}")
            return data
        else:
            print(f"[-] IP privee ou non trouvee")
            return None
    except Exception as e:
        print(f"[-] Erreur : {e}")
        return None

def verifier_have_i_been_pwned(email):
    """Verifie si un email a ete compromis"""
    try:
        print(f"\n[*] Verification de {email} sur HaveIBeenPwned...")
        headers = {"hibp-api-key": "DEMO", "User-Agent": "CyberMap3D"}
        reponse = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers=headers,
            timeout=10
        )
        if reponse.status_code == 200:
            breaches = reponse.json()
            print(f"[!] ALERTE - {email} trouve dans {len(breaches)} fuite(s) !")
            for b in breaches[:3]:
                print(f"    - {b['Name']} ({b['BreachDate']})")
        elif reponse.status_code == 404:
            print(f"[+] Bonne nouvelle - {email} non compromis !")
        else:
            print(f"[*] API non disponible sans cle (demo)")
    except Exception as e:
        print(f"[-] Erreur : {e}")

def scanner_headers(url):
    """Analyse les headers HTTP d'un site"""
    try:
        print(f"\n[*] Analyse des headers de {url}...")
        reponse = requests.get(url, timeout=10)
        headers = reponse.headers

        print(f"[+] Code HTTP    : {reponse.status_code}")
        print(f"[+] Serveur      : {headers.get('Server', 'Cache')}")
        print(f"[+] Technologies : {headers.get('X-Powered-By', 'Non divulgue')}")

        # Verifier les headers de securite
        securite = {
            "Strict-Transport-Security": "HSTS",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "MIME Sniffing",
            "Content-Security-Policy": "XSS",
        }

        print(f"\n[*] Headers de securite :")
        for header, protection in securite.items():
            if header in headers:
                print(f"    [+] {protection} : Protege")
            else:
                print(f"    [-] {protection} : NON PROTEGE !")

    except Exception as e:
        print(f"[-] Erreur : {e}")

def osint(cible):
    print("=" * 55)
    print("CyberMap 3D - OSINT")
    print("=" * 55)
    print(f"\n[*] Cible : {cible}")
    print(f"[*] Heure : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    # 1. Trouver l'IP
    ip = rechercher_ip(cible)

    # 2. Infos sur l'IP
    if ip:
        infos = infos_ip(ip)

    # 3. Analyser les headers
    scanner_headers(f"https://{cible}")

    # 4. Sauvegarder
    rapport = {
        "cible": cible,
        "ip": ip,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }

    with open("../data/osint_rapport.json", "w") as f:
        json.dump(rapport, f, indent=4)

    print(f"\n[+] Rapport sauvegarde dans data/osint_rapport.json")
    print("=" * 55)

# Tester sur un site public
osint("google.com")