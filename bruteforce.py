# CyberMap 3D - Simulateur Bruteforce SSH
# Auteur : Hugo B.
# ATTENTION : A utiliser uniquement sur ses propres systemes !

import time
import json
from datetime import datetime

# On simule une attaque contre notre propre honeypot SSH (port 2222)
# Jamais contre un vrai serveur sans autorisation !

CIBLE = "localhost"
PORT = 2222

# Dictionnaire de mots de passe courants
DICTIONNAIRE = [
    "123456", "password", "admin", "root", "toor",
    "admin123", "letmein", "qwerty", "abc123", "monkey",
    "master", "dragon", "sunshine", "princess", "welcome",
    "hugo", "azerty", "motdepasse", "bonjour", "soleil"
]

# Utilisateurs courants a tester
UTILISATEURS = ["root", "admin", "user", "hugo"]

def simuler_tentative(utilisateur, mot_de_passe):
    """Simule une tentative de connexion SSH"""
    # On simule juste — on ne fait pas de vraie connexion
    time.sleep(0.2)
    
    # Simuler un succes si on trouve admin/admin
    if utilisateur == "admin" and mot_de_passe == "admin":
        return True
    if utilisateur == "root" and mot_de_passe == "toor":
        return True
    return False

def bruteforce():
    print("=" * 55)
    print("CyberMap 3D - Simulation Bruteforce SSH")
    print("=" * 55)
    print(f"\n[*] Cible     : {CIBLE}:{PORT}")
    print(f"[*] Utilisateurs a tester : {len(UTILISATEURS)}")
    print(f"[*] Mots de passe a tester : {len(DICTIONNAIRE)}")
    print(f"[*] Total de tentatives : {len(UTILISATEURS) * len(DICTIONNAIRE)}")
    print(f"\n[*] Debut de l'attaque...\n")

    resultats = []
    debut = time.time()
    tentatives = 0

    for utilisateur in UTILISATEURS:
        print(f"\n[*] Test de l'utilisateur : {utilisateur}")
        for mot_de_passe in DICTIONNAIRE:
            tentatives += 1
            print(f"    Tentative {tentatives:03d} : {utilisateur}:{mot_de_passe}")

            succes = simuler_tentative(utilisateur, mot_de_passe)

            if succes:
                print(f"\n[+] ACCES OBTENU !")
                print(f"    Utilisateur : {utilisateur}")
                print(f"    Mot de passe : {mot_de_passe}")
                resultats.append({
                    "utilisateur": utilisateur,
                    "mot_de_passe": mot_de_passe,
                    "heure": datetime.now().strftime("%H:%M:%S")
                })

    duree = time.time() - debut
    print(f"\n" + "=" * 55)
    print(f"[*] Attaque terminee !")
    print(f"[*] Tentatives : {tentatives}")
    print(f"[*] Duree      : {duree:.1f} secondes")
    print(f"[*] Acces obtenus : {len(resultats)}")

    if resultats:
        print(f"\n[+] Mots de passe trouves :")
        for r in resultats:
            print(f"    {r['utilisateur']} : {r['mot_de_passe']}")

    with open("bruteforce_log.json", "w") as f:
        json.dump({
            "cible": f"{CIBLE}:{PORT}",
            "tentatives": tentatives,
            "duree": duree,
            "succes": resultats
        }, f, indent=4)

    print(f"\n[!] Conclusion :")
    print(f"    {tentatives} tentatives en {duree:.1f} secondes")
    print(f"    Un vrai outil comme Hydra teste des milliers")
    print(f"    de mots de passe par seconde !")
    print(f"\n    Protection : bloquer l'IP apres 3 echecs")
    print(f"    (fail2ban, authentification par cle SSH)")
    print("=" * 55)

bruteforce()