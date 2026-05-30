# CyberMap 3D - Simulation de réseau
# Auteur : Hugo B.

import time
import json

machines = [
    {"id": 1, "nom": "PC-Bureau",   "ip": "192.168.1.10", "type": "pc",      "infecte": False},
    {"id": 2, "nom": "Serveur-Web", "ip": "192.168.1.20", "type": "serveur", "infecte": False},
    {"id": 3, "nom": "Routeur",     "ip": "192.168.1.1",  "type": "routeur", "infecte": False},
    {"id": 4, "nom": "PC-Portable", "ip": "192.168.1.11", "type": "pc",      "infecte": False},
]

def afficher_reseau():
    print("\n=== État du réseau ===")
    for machine in machines:
        statut = "⚠ INFECTÉ" if machine["infecte"] else "✓ Sain"
        print(f"[{machine['type'].upper()}] {machine['nom']} - {machine['ip']} - {statut}")

def lancer_attaque(id_cible):
    print(f"\n🔴 Attaque lancée sur la machine {id_cible} !")
    for machine in machines:
        if machine["id"] == id_cible:
            machine["infecte"] = True
            print(f"   💀 {machine['nom']} est infectée !")
            time.sleep(1)
            for victime in machines:
                if not victime["infecte"]:
                    victime["infecte"] = True
                    print(f"   ☣ Propagation vers {victime['nom']}...")
                    time.sleep(1)

def sauvegarder_json():
    with open("reseau.json", "w") as fichier:
        json.dump(machines, fichier, indent=4)
    print("\n💾 Réseau sauvegardé dans reseau.json !")

afficher_reseau()
lancer_attaque(1)
afficher_reseau()
sauvegarder_json()