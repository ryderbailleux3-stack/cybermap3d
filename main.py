# CyberMap 3D - Programme principal
# Auteur : Hugo B.

import os
import sys
import json
import subprocess

# Definir les chemins absolus
RACINE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.join(RACINE, "core")
DATA = os.path.join(RACINE, "data")
WEB = os.path.join(RACINE, "web")
RAPPORTS = os.path.join(RACINE, "rapports")

def menu():
    print("=" * 55)
    print("  CyberMap 3D - Tableau de bord de securite")
    print("=" * 55)
    print("\n[1] Scanner le reseau")
    print("[2] Scanner les ports et OS")
    print("[3] Analyser les vulnerabilites CVE")
    print("[4] Detecter les intrus")
    print("[5] Generer le rapport PDF")
    print("[6] Lancer la visualisation 3D")
    print("[7] Quitter")
    print("\n" + "=" * 55)
    return input("\nChoix : ")

def lancer_script(chemin):
    """Lance un script Python depuis n'importe ou"""
    dossier = os.path.dirname(chemin)
    fichier = os.path.basename(chemin)
    subprocess.run([sys.executable, fichier], cwd=dossier)

def scanner_reseau():
    print("\n[*] Lancement du scan reseau...")
    lancer_script(os.path.join(CORE, "scanner.py"))

def scanner_ports():
    print("\n[*] Lancement du scan de ports...")
    lancer_script(os.path.join(CORE, "scanner_ports.py"))

def analyser_vulnerabilites():
    print("\n[*] Analyse des vulnerabilites...")
    lancer_script(os.path.join(CORE, "vulnerabilites.py"))

def detecter_intrus():
    print("\n[*] Detection des intrus...")
    lancer_script(os.path.join(CORE, "detecteur.py"))

def generer_rapport():
    print("\n[*] Generation du rapport PDF...")
    lancer_script(os.path.join(CORE, "rapport.py"))

def lancer_visualisation():
    print("\n[*] Lancement de la visualisation 3D...")
    print("[*] Ouvre http://localhost:8000 dans ton navigateur !")
    os.chdir(WEB)
    subprocess.run([sys.executable, "-m", "http.server", "8000"])

while True:
    choix = menu()

    if choix == "1":
        scanner_reseau()
    elif choix == "2":
        scanner_ports()
    elif choix == "3":
        analyser_vulnerabilites()
    elif choix == "4":
        detecter_intrus()
    elif choix == "5":
        generer_rapport()
    elif choix == "6":
        lancer_visualisation()
    elif choix == "7":
        print("\n[*] Au revoir !")
        break
    else:
        print("\n[-] Choix invalide !")