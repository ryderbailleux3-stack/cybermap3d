# CyberMap 3D - Scanner de vulnérabilités CVE
# Auteur : Hugo B.

import json
import requests

def chercher_cve(service, version):
    """Cherche les CVE connues pour un service et sa version"""
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={service}+{version}&resultsPerPage=3"
        reponse = requests.get(url, timeout=10)
        data = reponse.json()
        
        cves = []
        for item in data.get("vulnerabilities", []):
            cve = item["cve"]
            cve_id = cve["id"]
            description = cve["descriptions"][0]["value"][:100] + "..."
            
            # Score de gravité
            score = "Inconnu"
            gravite = "Inconnu"
            if "metrics" in cve:
                if "cvssMetricV31" in cve["metrics"]:
                    score = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                    gravite = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
                elif "cvssMetricV2" in cve["metrics"]:
                    score = cve["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"]
                    gravite = cve["metrics"]["cvssMetricV2"][0]["baseSeverity"]
            
            cves.append({
                "id": cve_id,
                "description": description,
                "score": score,
                "gravite": gravite
            })
        return cves
    except Exception as e:
        return []

def analyser_vulnerabilites():
    print("\n🔍 Analyse des vulnérabilités en cours...")
    print("⚠ Connexion à la base CVE nationale (NIST)...\n")

    # Charger le réseau scanné
    with open("reseau.json", "r") as f:
        machines = json.load(f)

    rapport = []

    for machine in machines:
        print(f"📡 Analyse de {machine['nom']} ({machine['ip']})")
        vulns_machine = []

        if not machine.get("ports"):
            print(f"   ✓ Aucun port ouvert — pas de vulnérabilité détectable\n")
            continue

        for port in machine.get("ports", []):
            service = port["service"]
            version = port["version"]

            if not version:
                continue

            print(f"   🔎 Recherche CVE pour {service} {version}...")
            cves = chercher_cve(service, version)

            if cves:
                for cve in cves:
                    emoji = "🔴" if cve["gravite"] in ["HIGH", "CRITICAL"] else "🟡"
                    print(f"   {emoji} {cve['id']} — Score: {cve['score']} ({cve['gravite']})")
                    vulns_machine.append({
                        "port": port["port"],
                        "service": service,
                        "cve": cve
                    })
            else:
                print(f"   ✓ Aucune CVE trouvée pour {service} {version}")

        machine["vulnerabilites"] = vulns_machine
        rapport.append(machine)
        print()

    # Sauvegarder
    with open("reseau.json", "w") as f:
        json.dump(machines, f, indent=4)
    print("💾 Vulnérabilités sauvegardées dans reseau.json !")

    return machines

analyser_vulnerabilites()