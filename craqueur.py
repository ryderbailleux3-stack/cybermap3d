# CyberMap 3D - Craqueur de hash
# Auteur : Hugo B.

import hashlib
import time

def hasher(mot_de_passe, algorithme="md5"):
    h = hashlib.new(algorithme)
    h.update(mot_de_passe.encode("utf-8"))
    return h.hexdigest()

def craquer_hash(hash_cible, algorithme="md5"):
    dictionnaire = [
        "123456", "password", "123456789", "12345678", "12345",
        "1234567", "admin", "123123", "qwerty", "abc123",
        "monkey", "1234567890", "letmein", "trustno1", "dragon",
        "master", "sunshine", "princess", "welcome", "shadow",
        "superman", "michael", "football", "jesus", "ninja",
        "mustang", "password1", "root", "toor", "admin123",
        "hugo", "azerty", "motdepasse", "soleil", "bonjour"
    ]

    print(f"\n[*] Tentative de craquage : {hash_cible}")
    print(f"[*] Algorithme : {algorithme.upper()}")
    print(f"[*] Dictionnaire : {len(dictionnaire)} mots\n")

    debut = time.time()

    for i, mot in enumerate(dictionnaire):
        hash_essai = hasher(mot, algorithme)
        print(f"   Essai {i+1:02d} : {mot:20} -> {hash_essai[:20]}...")

        if hash_essai == hash_cible:
            duree = time.time() - debut
            print(f"\n[+] MOT DE PASSE TROUVE !")
            print(f"    Mot de passe : {mot}")
            print(f"    Trouve en    : {duree:.3f} secondes")
            print(f"    Tentatives   : {i+1}")
            return mot

        time.sleep(0.1)

    print(f"\n[-] Mot de passe non trouve dans le dictionnaire")
    return None

def demo():
    print("=" * 50)
    print("CyberMap 3D - Craquage de hash")
    print("=" * 50)

    mots_de_passe = ["admin", "hugo", "123456"]

    for mdp in mots_de_passe:
        print(f"\n[*] Mot de passe original : '{mdp}'")
        print(f"    MD5    : {hasher(mdp, 'md5')}")
        print(f"    SHA1   : {hasher(mdp, 'sha1')}")
        print(f"    SHA256 : {hasher(mdp, 'sha256')}")

    print("\n" + "=" * 50)
    print("[*] Tentative de craquage...")
    print("=" * 50)

    mdp_cible = "admin"
    hash_cible = hasher(mdp_cible, "md5")
    print(f"\n[*] Hash cible MD5 : {hash_cible}")

    craquer_hash(hash_cible, "md5")

    print("\n" + "=" * 50)
    print("[!] Conclusion :")
    print("    Un mot de passe comme 'admin' se craque")
    print("    en moins d'une seconde !")
    print("    Utilisez toujours des mots de passe complexes.")
    print("=" * 50)

demo()