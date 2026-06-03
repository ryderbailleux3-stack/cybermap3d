# CyberMap 3D - Chiffrement AES
# Auteur : Hugo B.

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import json
from datetime import datetime

def chiffrer(message, cle):
    cle_bytes = cle.encode("utf-8").ljust(32)[:32]
    iv = get_random_bytes(16)
    cipher = AES.new(cle_bytes, AES.MODE_CBC, iv)
    message_chiffre = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return {
        "iv": base64.b64encode(iv).decode("utf-8"),
        "data": base64.b64encode(message_chiffre).decode("utf-8")
    }

def dechiffrer(message_chiffre, cle):
    cle_bytes = cle.encode("utf-8").ljust(32)[:32]
    iv = base64.b64decode(message_chiffre["iv"])
    data = base64.b64decode(message_chiffre["data"])
    cipher = AES.new(cle_bytes, AES.MODE_CBC, iv)
    message = unpad(cipher.decrypt(data), AES.block_size)
    return message.decode("utf-8")

print("=" * 55)
print("CyberMap 3D - Chiffrement AES")
print("=" * 55)

messages = [
    "Bonjour Hugo !",
    "Mot de passe : SuperSecret123",
    "IP cible : 192.168.0.25",
]

cle = "MaCleSecrete"

for msg in messages:
    print(f"\n[*] Message original  : {msg}")
    chiffre = chiffrer(msg, cle)
    print(f"[+] Message chiffre   : {chiffre['data'][:30]}...")
    print(f"[+] IV                : {chiffre['iv']}")
    dechiffre = dechiffrer(chiffre, cle)
    print(f"[+] Message dechiffre : {dechiffre}")

print("\n" + "=" * 55)
print("[*] Test avec mauvaise cle...")
print("=" * 55)

msg = "Message secret"
chiffre = chiffrer(msg, "BonneCle")

try:
    dechiffre = dechiffrer(chiffre, "MauvaiseCle")
    print(f"[+] Dechiffre : {dechiffre}")
except Exception as e:
    print(f"[-] ERREUR - Mauvaise cle : impossible de dechiffrer !")
    print(f"    C'est normal - AES protege bien les donnees !")

print("\n" + "=" * 55)
print("[*] Sauvegarde d'un message chiffre...")
print("=" * 55)

message_important = "Rapport confidentiel CyberMap 3D - Hugo B."
chiffre = chiffrer(message_important, cle)

with open("message_chiffre.json", "w") as f:
    json.dump({
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "auteur": "Hugo B.",
        "message": chiffre
    }, f, indent=4)

print(f"\n[+] Message chiffre sauvegarde dans message_chiffre.json")
print(f"[+] Sans la cle '{cle}' ce fichier est illisible !")
print("\n[!] Conclusion :")
print("    AES est le standard mondial du chiffrement.")
print("    HTTPS, WhatsApp, Signal utilisent tous AES.")
print("=" * 55)