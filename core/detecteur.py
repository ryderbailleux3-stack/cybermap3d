# CyberMap 3D - Détecteur d'intrus
# Auteur : Hugo B.

import nmap
import json
import os
from datetime import datetime

FICHIER_CONNUS = "machines_connues.json"
FICHIER_ALERTES = "alertes.json"

def charger_machines_connues():
    if os.path.exists(FICHIER_CONNUS):
        with open(FICHIER_CONNUS, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_machines_connues(machines):
    with open(FICHIER_CONNUS, "w") as f:
        json.dump(machines, f, indent=4)

def scanner_reseau(plage_ip):
    print(f"\n🔍 Scan du réseau {plage_ip}...")
    scanner = nmap.PortScanner()
    scanner.scan(hosts=plage_ip, arguments='-sn')
    machines = {}
    for host in scanner.all_hosts():
        nom = scanner[host].hostname() or host
        machines[host] = {"nom": nom, "ip": host}
    return machines

def detecter_intrus(plage_ip):
    print("\n🛡 Détecteur d'intrus CyberMap 3D")
    print("=" * 40)

    machines_connues = charger_machines_connues()
    machines_actuelles = scanner_reseau(plage_ip)

    alertes = []

    # Première fois — on enregistre tout
    if not machines_connues:
        print("\n📋 Premier scan — enregistrement des machines connues :")
        for ip, m in machines_actuelles.items():
            print(f"  ✓ {m['nom']} ({ip}) enregistrée")
        sauvegarder_machines_connues(machines_actuelles)
        print(f"\n✅ {len(machines_actuelles)} machines enregistrées comme connues !")
        return

    # Comparer avec les machines connues
    print(f"\n📡 {len(machines_actuelles)} machines détectées sur le réseau")
    print(f"📋 {len(machines_connues)} machines connues\n")

    # Détecter les nouvelles machines
    for ip, machine in machines_actuelles.items():
        if ip not in machines_connues:
            alerte = {
                "type": "INTRUS",
                "ip": ip,
                "nom": machine["nom"],
                "heure": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            alertes.append(alerte)
            print(f"🚨 ALERTE INTRUS ! Nouvelle machine détectée :")
            print(f"   IP  : {ip}")
            print(f"   Nom : {machine['nom']}")
            print(f"   Heure : {alerte['heure']}\n")

    # Détecter les machines disparues
    for ip, machine in machines_connues.items():
        if ip not in machines_actuelles:
            print(f"⚠ Machine disparue : {machine['nom']} ({ip})")

    if not alertes:
        print("✅ Aucun intrus détecté — réseau sécurisé !")

    # Sauvegarder les alertes
    if alertes:
        with open(FICHIER_ALERTES, "w") as f:
            json.dump(alertes, f, indent=4)
        print(f"\n💾 {len(alertes)} alerte(s) sauvegardée(s) dans alertes.json")

    # Mettre à jour les machines connues
    sauvegarder_machines_connues(machines_actuelles)

detecter_intrus("192.168.1.0/24")