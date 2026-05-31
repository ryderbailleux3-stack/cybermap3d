# CyberMap 3D - Scanner réseau réel
# Auteur : Hugo B.

import nmap
import json

def scanner_reseau(plage_ip):
    print(f"\n🔍 Scan du réseau {plage_ip} en cours...")
    
    scanner = nmap.PortScanner()
    scanner.scan(hosts=plage_ip, arguments='-sn')
    
    machines = []
    for i, host in enumerate(scanner.all_hosts()):
        nom = scanner[host].hostname() or f"Machine-{i+1}"
        statut = scanner[host].state()
        print(f"  ✓ Trouvé : {host} - {nom} - {statut}")
        machines.append({
            "id": i + 1,
            "nom": nom if nom else f"Machine-{i+1}",
            "ip": host,
            "type": "pc",
            "infecte": False
        })
    
    print(f"\n📡 {len(machines)} machine(s) trouvée(s) sur le réseau !")
    
    # Sauvegarder en JSON
    with open("reseau.json", "w") as f:
        json.dump(machines, f, indent=4)
    print("💾 Réseau sauvegardé dans reseau.json !")
    
    return machines

# Trouver ta plage IP
# La plupart des box françaises utilisent 192.168.1.0/24
scanner_reseau("192.168.1.0/24")