# CyberMap 3D - Scanner de ports et OS
# Auteur : Hugo B.

import nmap
import json

def scanner_ports(plage_ip):
    print(f"\n🔍 Scan avancé du réseau {plage_ip}...")
    print("⚠ Ce scan peut prendre 1-2 minutes...\n")

    scanner = nmap.PortScanner()
    # -sV = détecte les services, -O = détecte l'OS, --top-ports 20 = 20 ports les plus courants
    scanner.scan(hosts=plage_ip, arguments='-sV -O --top-ports 20')

    machines = []
    for i, host in enumerate(scanner.all_hosts()):
        print(f"📡 Machine trouvée : {host}")
        
        # Nom
        nom = scanner[host].hostname() or f"Machine-{i+1}"
        
        # Système d'exploitation
        os_name = "Inconnu"
        if "osmatch" in scanner[host] and scanner[host]["osmatch"]:
            os_name = scanner[host]["osmatch"][0]["name"]
        print(f"   💻 OS détecté : {os_name}")

        # Ports ouverts
        ports_ouverts = []
        for proto in scanner[host].all_protocols():
            for port in scanner[host][proto].keys():
                service = scanner[host][proto][port]
                if service["state"] == "open":
                    ports_ouverts.append({
                        "port": port,
                        "service": service["name"],
                        "version": service["version"]
                    })
                    print(f"   🔓 Port {port} ouvert — {service['name']} {service['version']}")

        if not ports_ouverts:
            print(f"   🔒 Aucun port ouvert détecté")

        machines.append({
            "id": i + 1,
            "nom": nom,
            "ip": host,
            "type": "pc",
            "os": os_name,
            "ports": ports_ouverts,
            "infecte": False
        })

    print(f"\n✅ Scan terminé — {len(machines)} machine(s) analysée(s)")

    with open("reseau.json", "w") as f:
        json.dump(machines, f, indent=4)
    print("💾 Résultats sauvegardés dans reseau.json !")

scanner_ports("192.168.1.173")