# CyberMap 3D - Générateur de rapport PDF
# Auteur : Hugo B.

import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generer_rapport():
    # Charger les données
    with open("../data/reseau.json", "r") as f:
        machines = json.load(f)

    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    nom_fichier = f"../rapports/rapport_cybermap_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    doc = SimpleDocTemplate(nom_fichier, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()

    # Styles personnalisés
    titre_style = ParagraphStyle("titre", fontSize=22, textColor=colors.HexColor("#00ff88"),
                                  spaceAfter=6, alignment=TA_CENTER, fontName="Helvetica-Bold")
    sous_titre_style = ParagraphStyle("sous_titre", fontSize=12, textColor=colors.HexColor("#888888"),
                                       spaceAfter=20, alignment=TA_CENTER)
    section_style = ParagraphStyle("section", fontSize=14, textColor=colors.HexColor("#0066cc"),
                                    spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold")
    machine_style = ParagraphStyle("machine", fontSize=12, textColor=colors.black,
                                    spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
    normal_style = ParagraphStyle("normal", fontSize=10, textColor=colors.HexColor("#333333"),
                                   spaceAfter=4)
    danger_style = ParagraphStyle("danger", fontSize=10, textColor=colors.red, spaceAfter=4)
    ok_style = ParagraphStyle("ok", fontSize=10, textColor=colors.HexColor("#009900"), spaceAfter=4)

    contenu = []

    # En-tête
    contenu.append(Paragraph("🔐 CyberMap 3D", titre_style))
    contenu.append(Paragraph("Rapport d'audit de sécurité réseau", sous_titre_style))
    contenu.append(Paragraph(f"Généré le : {date}", sous_titre_style))
    contenu.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#00ff88")))
    contenu.append(Spacer(1, 0.5*cm))

    # Résumé
    total_machines = len(machines)
    total_ports = sum(len(m.get("ports", [])) for m in machines)
    total_vulns = sum(len(m.get("vulnerabilites", [])) for m in machines)

    contenu.append(Paragraph("📊 Résumé de l'audit", section_style))

    resume_data = [
        ["Indicateur", "Valeur"],
        ["Machines détectées", str(total_machines)],
        ["Ports ouverts", str(total_ports)],
        ["Vulnérabilités trouvées", str(total_vulns)],
        ["Niveau de risque global", "FAIBLE" if total_vulns == 0 else "MOYEN" if total_vulns < 5 else "ÉLEVÉ"],
    ]

    resume_table = Table(resume_data, colWidths=[10*cm, 6*cm])
    resume_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a0a1a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#00ff88")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    contenu.append(resume_table)
    contenu.append(Spacer(1, 0.5*cm))

    # Détail par machine
    contenu.append(Paragraph("🖥 Détail des machines", section_style))

    for machine in machines:
        contenu.append(Paragraph(f"► {machine['nom']} — {machine['ip']}", machine_style))
        contenu.append(Paragraph(f"Système d'exploitation : {machine.get('os', 'Inconnu')}", normal_style))

        ports = machine.get("ports", [])
        if ports:
            for port in ports:
                contenu.append(Paragraph(
                    f"🔓 Port {port['port']} ouvert — {port['service']} {port['version']}",
                    normal_style
                ))
        else:
            contenu.append(Paragraph("🔒 Aucun port ouvert détecté", ok_style))

        vulns = machine.get("vulnerabilites", [])
        if vulns:
            for v in vulns:
                gravite = v["cve"]["gravite"]
                score = v["cve"]["score"]
                cve_id = v["cve"]["id"]
                style = danger_style if gravite in ["HIGH", "CRITICAL"] else normal_style
                contenu.append(Paragraph(
                    f"⚠ {cve_id} — Score: {score} ({gravite})",
                    style
                ))
        else:
            contenu.append(Paragraph("✓ Aucune vulnérabilité CVE détectée", ok_style))

        contenu.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))

    # Recommandations
    contenu.append(Paragraph("💡 Recommandations", section_style))
    recommandations = [
        "Maintenir tous les systèmes d'exploitation à jour (Windows Update activé)",
        "Fermer les ports inutilisés via le pare-feu Windows",
        "Le port 445 (SMB) doit être surveillé — vecteur d'attaque WannaCry",
        "Activer l'authentification à deux facteurs sur tous les comptes",
        "Effectuer un audit de sécurité régulier (tous les 3 mois)",
    ]
    for r in recommandations:
        contenu.append(Paragraph(f"• {r}", normal_style))

    contenu.append(Spacer(1, 0.5*cm))
    contenu.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#00ff88")))
    contenu.append(Paragraph("Rapport généré par CyberMap 3D — Projet personnel Hugo B.", sous_titre_style))

    doc.build(contenu)
    print(f"\n✅ Rapport PDF généré : {nom_fichier}")

generer_rapport()