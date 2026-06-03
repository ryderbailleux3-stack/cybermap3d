# CyberMap 3D - Intercepteur de trafic réseau
# Auteur : Hugo B.

from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR
import json
from datetime import datetime

# IP de ton téléphone — change si nécessaire
IP_TELEPHONE = "192.168.1.13"

paquets_captures = []

def analyser_paquet(paquet):
    """Analyse chaque paquet qui passe sur le réseau"""
    
    # On filtre uniquement les paquets du téléphone
    if not paquet.haslayer(IP):
        return
    
    src = paquet[IP].src
    dst = paquet[IP].dst
    
    if src != IP_TELEPHONE and dst != IP_TELEPHONE:
        return

    info = {
        "heure": datetime.now().strftime("%H:%M:%S"),
        "source": src,
        "destination": dst,
        "protocole": "?"
    }

    # Détecter le protocole
    if paquet.haslayer(DNS) and paquet.haslayer(DNSQR):
        # Requête DNS — le téléphone cherche un site
        domaine = paquet[DNSQR].qname.decode("utf-8").rstrip(".")
        info["protocole"] = "DNS"
        info["detail"] = f"Recherche : {domaine}"
        print(f"🌐 [{info['heure']}] DNS → {domaine}")

    elif paquet.haslayer(TCP):
        port = paquet[TCP].dport if src == IP_TELEPHONE else paquet[TCP].sport
        info["protocole"] = "TCP"
        info["detail"] = f"Port {port}"
        
        # Identifier le service
        services = {80: "HTTP", 443: "HTTPS", 22: "SSH", 25: "Email", 8080: "Web"}
        service = services.get(port, f"Port {port}")
        print(f"📡 [{info['heure']}] TCP → {service} ({dst if src == IP_TELEPHONE else src})")

    elif paquet.haslayer(UDP):
        port = paquet[UDP].dport if src == IP_TELEPHONE else paquet[UDP].sport
        info["protocole"] = "UDP"
        info["detail"] = f"Port {port}"
        print(f"📦 [{info['heure']}] UDP → Port {port}")

    paquets_captures.append(info)

    # Sauvegarder toutes les 10 paquets
    if len(paquets_captures) % 10 == 0:
       with open("../data/trafic.json", "w") as f:
            json.dump(paquets_captures, f, indent=4)

print("🔍 Interception du trafic de ton téléphone...")
print(f"📱 Cible : {IP_TELEPHONE}")
print("⚠ Utilise ton téléphone pour générer du trafic !")
print("   (ouvre des apps, navigue sur internet...)")
print("   Appuie sur Ctrl+C pour arrêter\n")

try:
    sniff(filter=f"host {IP_TELEPHONE}", prn=analyser_paquet, store=0)
except KeyboardInterrupt:
    print(f"\n✅ Capture terminée — {len(paquets_captures)} paquets analysés")
    with open("../data/trafic.json", "w") as f:
        json.dump(paquets_captures, f, indent=4)
    print("💾 Trafic sauvegardé dans trafic.json !")