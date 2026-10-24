# -*- coding: utf-8 -*-
"""Campagne Google Ads Search (CPC manuel) pour Shopta Serrure.

Usage : python3 _src/google-ads/generer_campagne.py
Génère dans _src/google-ads/ des fichiers CSV à importer dans Google Ads Editor
(Compte > Importer > À partir d'un fichier) :
  1-campagnes.csv, 2-groupes.csv, 3-mots-cles.csv, 4-annonces.csv,
  5-mots-cles-negatifs.csv, 6-composants.csv
Les enchères sont des points de départ à ajuster après 7 à 14 jours de données.
"""
import csv
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from build import SERVICES, ZONES, URL, TEL  # noqa: E402

BUDGET = {"Urgences": 40, "Villes": 35, "Services x Villes": 25}  # €/jour, à adapter
CAMPAGNES = {
    "Urgences": "Shopta | Search | Urgences serrurier",
    "Villes": "Shopta | Search | Serrurier par ville",
    "Services x Villes": "Shopta | Search | Service x ville",
}


def kw(s):
    """Mot clé normalisé : minuscules, sans accents ni tirets ni apostrophes."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return " ".join(s.replace("-", " ").replace("'", " ").split())


# ---------------------------------------------------------------------------
# Groupes d'annonces thématiques (campagne Urgences)
# (nom, url, enchère €, mots clés exacts, mots clés expression)
# ---------------------------------------------------------------------------
GROUPES = [
    ("Serrurier Paris", "/villes/paris/", 9.00,
     ["serrurier paris", "serrurier a paris", "serrurier paris pas cher", "serrurier paris urgence", "serrurier paris 24h 24",
      "serrurier sur paris", "serrurier paris prix", "bon serrurier paris", "serrurier pas cher paris"],
     ["serrurier paris"]),
    ("Serrurier urgence", "/", 8.50,
     ["serrurier urgence", "serrurier en urgence", "serrurier 24h 24", "serrurier 24h", "serrurier dimanche", "serrurier nuit",
      "serrurier de nuit", "serrurier ouvert maintenant", "serrurier jour ferie", "depannage serrurier", "depannage serrurerie",
      "serrurier rapide", "serrurier express", "urgence serrurier", "sos serrurier", "serrurier proche", "serrurier a proximite",
      "serrurier pres de chez moi", "serrurier autour de moi", "serrurier ile de france"],
     ["serrurier urgence", "serrurier 24h", "depannage serrurier", "serrurier pres de chez moi", "serrurier proche"]),
    ("Ouverture de porte", "/depannage/porte-claquee/", 8.00,
     ["ouverture de porte", "ouverture porte", "ouverture de porte paris", "ouverture porte claquee", "porte claquee",
      "porte claquee cle a l interieur", "porte claquee que faire", "porte fermee cle a l interieur", "j ai claque ma porte",
      "enferme dehors", "ouvrir porte claquee", "ouvrir une porte claquee", "serrurier porte claquee", "ouverture porte blindee",
      "ouverture de porte blindee", "ouverture porte fermee a cle", "cle oubliee a l interieur", "cles perdues serrurier",
      "perdu mes cles", "porte bloquee"],
     ["ouverture de porte", "porte claquee", "ouverture porte", "porte blindee claquee", "cles perdues"]),
    ("Serrure bloquee", "/depannage/serrure-bloquee/", 6.00,
     ["serrure bloquee", "serrure coincee", "cle ne tourne plus", "cle qui ne tourne pas", "serrure grippee",
      "porte qui ne s ouvre plus", "porte bloquee serrure", "deblocage serrure", "debloquer serrure", "serrure porte bloquee",
      "serrure qui tourne dans le vide", "cylindre bloque"],
     ["serrure bloquee", "serrure coincee", "debloquer serrure", "cle ne tourne"]),
    ("Cle cassee", "/depannage/cle-cassee/", 6.00,
     ["cle cassee dans la serrure", "cle cassee serrure", "cle cassee", "cle coincee dans la serrure", "cle bloquee dans la serrure",
      "extraction cle cassee", "retirer cle cassee", "enlever cle cassee serrure", "cle cassee dans le cylindre"],
     ["cle cassee", "cle coincee", "cle bloquee dans"]),
    ("Changement serrure", "/depannage/changement-serrure/", 5.50,
     ["changement de serrure", "changer serrure", "changement serrure", "changer cylindre", "changement cylindre",
      "remplacement serrure", "remplacement cylindre", "changer barillet", "changement barillet", "serrure a2p",
      "serrure 3 points", "serrure multipoints", "pose serrure", "installation serrure", "changer serrure porte d entree",
      "prix changement serrure", "changement serrure apres perte de cle", "changer serrure demenagement"],
     ["changement de serrure", "changer serrure", "changer cylindre", "remplacement serrure", "changer barillet"]),
    ("Apres effraction", "/depannage/effraction/", 6.50,
     ["serrurier effraction", "serrurier apres cambriolage", "porte fracturee", "porte forcee", "tentative d effraction",
      "securisation apres effraction", "serrure forcee", "cambriolage porte", "fermeture provisoire porte", "serrurier assurance"],
     ["effraction", "cambriolage", "porte forcee", "serrure forcee"]),
    ("Tarifs serrurier", "/tarifs/", 5.00,
     ["prix serrurier", "tarif serrurier", "serrurier pas cher", "devis serrurier", "combien coute un serrurier",
      "prix ouverture de porte", "tarif ouverture porte", "serrurier prix", "serrurier honnete", "serrurier de confiance"],
     ["prix serrurier", "tarif serrurier", "serrurier pas cher", "devis serrurier"]),
    ("Serrure connectee", "/depannage/serrure-connectee/", 2.50,
     ["serrure connectee", "installation serrure connectee", "pose serrure connectee", "serrure connectee bloquee",
      "smart lock installation"],
     ["serrure connectee"]),
]

# Annonces responsives : 15 titres (30 car. max), 4 descriptions (90 car. max)
# Pas de numéro de téléphone dans le texte (refusé par Google) : il passe par le composant Appel
COMMUNS_T = ["Shopta Serrure", "Prix Annoncé Avant Départ", "Devis Gratuit et Signé", "Ouvert 24h/24 et 7j/7",
             "Facture Pour Votre Assurance", "Sans Frais Cachés", "Ouverture Sans Dégât", "Paiement CB Accepté"]
COMMUNS_D = [
    "Prix annoncé au téléphone avant le déplacement, devis signé avant travaux. Appelez-nous !",
    "Serrurier qualifié 24h/24 et 7j/7. Ouverture sans dégât dans la plupart des cas. Dès 49 €.",
    "Facture détaillée reconnue par les assureurs. Paiement CB, espèces ou virement accepté.",
    "Paris, Hauts-de-Seine, Val-d'Oise : un serrurier part tout de suite. Avis Google publics.",
]
ANNONCES = {
    "Serrurier Paris": ["Serrurier Paris 24h/24", "Serrurier à Paris Dès 49 €", "Chez Vous en ~30 min à Paris",
                        "Serrurier Tous Arrondissements", "{KeyWord:Serrurier Paris}", "Appelez-Nous 24h/24", "Serrurier Paris Pas Cher"],
    "Serrurier urgence": ["Serrurier Urgence 24h/24", "Un Serrurier Part Maintenant", "Nuit, Dimanche et Jours Fériés",
                          "{KeyWord:Serrurier Urgence}", "Arrivée en ~30 min en Moyenne", "Appelez-Nous 24h/24", "Dépannage Serrurerie Rapide"],
    "Ouverture de porte": ["Ouverture de Porte Dès 49 €", "Porte Claquée ? On Arrive", "Ouverture Porte Sans Casse",
                           "{KeyWord:Ouverture de Porte}", "Porte Blindée Aussi", "Sans Changer la Serrure", "Appelez-Nous 24h/24"],
    "Serrure bloquee": ["Serrure Bloquée ? Dès 49 €", "Déblocage de Serrure 24h/24", "Clé Qui Ne Tourne Plus ?",
                        "{KeyWord:Serrure Bloquée}", "Diagnostic Sur Place", "Pièces en Stock", "Appelez-Nous 24h/24"],
    "Cle cassee": ["Clé Cassée ? Dès 49 €", "Extraction de Clé Cassée", "Clé Coincée dans la Serrure",
                   "{KeyWord:Clé Cassée}", "Sans Démonter la Serrure", "Intervention 24h/24", "Appelez-Nous 24h/24"],
    "Changement serrure": ["Changement de Serrure", "Cylindre et Serrure A2P", "Changement de Cylindre",
                           "{KeyWord:Changement Serrure}", "Pose le Jour Même", "Matériel Certifié A2P", "Devis Gratuit Sur Place"],
    "Apres effraction": ["Serrurier Après Effraction", "Porte Forcée ? On Sécurise", "Fermeture Provisoire 24h/24",
                         "{KeyWord:Serrurier Effraction}", "Documents Pour l'Assurance", "Renfort et Blindage", "Appelez-Nous 24h/24"],
    "Tarifs serrurier": ["Serrurier Prix Clair Dès 49 €", "Tarif Annoncé Au Téléphone", "Aucune Mauvaise Surprise",
                         "{KeyWord:Prix Serrurier}", "Devis Écrit Avant Travaux", "Serrurier Honnête à Paris", "Appelez-Nous 24h/24"],
    "Serrure connectee": ["Serrure Connectée Paris", "Installation Smart Lock", "Dépannage Serrure Connectée",
                          "{KeyWord:Serrure Connectée}", "Compatibilité Vérifiée", "Conseil et Pose Soignée", "Appelez-Nous 24h/24"],
}

NEGATIFS = [
    # emploi / formation
    "emploi", "recrutement", "offre d emploi", "salaire", "formation", "devenir serrurier", "cap serrurier", "apprenti",
    "apprentissage", "alternance", "stage", "ecole", "cours", "metier", "fiche metier", "cv", "interim", "indeed",
    # bricolage / do it yourself
    "tuto", "tutoriel", "video", "youtube", "soi meme", "seul", "sans serrurier", "astuce", "comment faire", "radiographie",
    "carte de credit", "trombone", "epingle", "crochetage tuto", "kit crochetage", "outil", "outils", "pied de biche",
    # achat produits
    "acheter", "achat", "vente", "leroy merlin", "castorama", "brico depot", "bricomarche", "mr bricolage", "amazon",
    "manomano", "cdiscount", "pdf", "notice", "schema",
    # hors sujet
    "voiture", "auto", "moto", "scooter", "velo", "cadenas", "valise", "casier", "coffre fort", "boite aux lettres",
    "double de cle", "reproduction cle", "copie cle", "cle minute", "cordonnier", "cordonnerie", "badge", "bip",
    "telecommande", "porte de garage", "portail", "volet", "wikipedia", "definition", "synonyme", "film", "jeu",
    "gratuit", "arnaque", "plainte", "avis negatif", "litige",
    # autres villes hors zone
    "lyon", "marseille", "toulouse", "bordeaux", "lille", "nice", "nantes", "strasbourg", "montpellier", "rennes",
]

COMPOSANTS = {
    "liens": [("Porte claquée dès 49 €", "/depannage/porte-claquee/", "Ouverture sans casse", "Radio ou crochetage"),
              ("Nos tarifs", "/tarifs/", "Prix annoncé à l'avance", "Devis gratuit et signé"),
              ("Changement de serrure", "/depannage/changement-serrure/", "Cylindres A2P en stock", "Pose le jour même"),
              ("Après une effraction", "/depannage/effraction/", "Sécurisation 24h/24", "Facture pour l'assurance"),
              ("Nos zones d'intervention", "/villes/", "Paris, 92 et 95", "118 villes et arrondissements"),
              ("Devis gratuit", "/contact/", "Rappel rapide 7j/7", "Formulaire ou WhatsApp")],
    "accroches": ["Ouvert 24h/24 et 7j/7", "Prix annoncé avant départ", "Devis gratuit et signé", "Ouverture sans dégât",
                  "Facture pour l'assurance", "Paiement CB accepté", "Matériel certifié A2P", "Sans frais cachés",
                  "Jours fériés compris", "Arrivée ~30 min en moy."],
    "extraits": ("Services", ["Ouverture de porte", "Serrure bloquée", "Clé cassée", "Changement de serrure",
                              "Changement de cylindre", "Après effraction", "Serrure connectée"]),
}


def check(texts, n, label):
    for t in texts:
        longueur = len(t.replace("{KeyWord:", "").replace("}", "")) if t.startswith("{KeyWord:") else len(t)
        assert longueur <= n, f"{label} trop long ({longueur} > {n}) : {t}"


def rsa_row(campagne, groupe, url, titres, path1, path2):
    titres = (titres + COMMUNS_T)[:15]
    check(titres, 30, "Titre")
    check(COMMUNS_D, 90, "Description")
    assert len(set(titres)) == 15, groupe
    row = {"Campaign": campagne, "Ad Group": groupe, "Ad type": "Responsive search ad", "Final URL": URL + url,
           "Path 1": path1[:15], "Path 2": path2[:15], "Status": "Enabled"}
    for i, t in enumerate(titres, 1):
        row[f"Headline {i}"] = t
        if i == 1:
            row["Headline 1 position"] = "1"  # titre principal épinglé en position 1
    for i, d in enumerate(COMMUNS_D, 1):
        row[f"Description {i}"] = d
    return row


def city_titles(nom, cp):
    nom_c = nom if len(nom) <= 20 else nom.split("-")[0]
    t = [f"Serrurier {nom_c}", f"Serrurier {cp} 24h/24", f"Serrurier {nom_c} Dès 49 €"[:30],
         "Arrivée Rapide, Prix Clair", "Appelez-Nous 24h/24", "Ouverture de Porte Dès 49 €", "Porte Claquée ? On Arrive"]
    return [x for x in t if len(x) <= 30]


def main():
    campagnes, groupes, mots, annonces = [], [], [], []
    for key, nom in CAMPAGNES.items():
        campagnes.append({"Campaign": nom, "Campaign Type": "Search", "Networks": "Google search",
                          "Budget": BUDGET[key], "Budget type": "Daily", "Bid Strategy Type": "Manual CPC",
                          "Enhanced CPC": "Disabled", "Languages": "fr", "Location": "Paris;Hauts-de-Seine;Val-d'Oise",
                          "Location targeting": "Presence", "Ad Schedule": "(Monday-Sunday[00:00-24:00])",
                          "Campaign Status": "Paused"})

    # 1) Urgences : groupes thématiques
    c = CAMPAGNES["Urgences"]
    for nom, url, bid, exacts, phrases in GROUPES:
        groupes.append({"Campaign": c, "Ad Group": nom, "Max CPC": f"{bid:.2f}", "Status": "Enabled"})
        for k in exacts:
            mots.append({"Campaign": c, "Ad Group": nom, "Keyword": k, "Criterion Type": "Exact", "Max CPC": f"{bid:.2f}", "Final URL": ""})
        for k in phrases:
            mots.append({"Campaign": c, "Ad Group": nom, "Keyword": k, "Criterion Type": "Phrase", "Max CPC": f"{bid * 0.8:.2f}", "Final URL": ""})
        p = url.strip("/").split("/")
        annonces.append(rsa_row(c, nom, url, ANNONCES[nom], p[-1] if p[0] else "serrurier", "24h-24"))

    # 2) Villes : un groupe par département, une URL par mot clé
    c = CAMPAGNES["Villes"]
    deps = {"75": ("Paris arrondissements", 7.00), "92": ("Hauts-de-Seine 92", 6.00), "95": ("Val-d Oise 95", 4.00)}
    for dep, (g, bid) in deps.items():
        groupes.append({"Campaign": c, "Ad Group": g, "Max CPC": f"{bid:.2f}", "Status": "Enabled"})
        for z in ZONES:
            if z["dep"] != dep or z["slug"] == "paris":
                continue
            if z["arr"]:
                n = z["arr"]
                variantes = [f"serrurier paris {n}", f"serrurier paris {n}e", f"serrurier paris {n}eme", f"serrurier {z['cp'][0]}",
                             f"serrurier paris {n} arrondissement", f"ouverture de porte paris {n}"]
            else:
                v = kw(z["nom"])
                variantes = [f"serrurier {v}", f"serrurier {z['cp'][0]}", f"serrurier urgence {v}"]
            for k in variantes:
                mots.append({"Campaign": c, "Ad Group": g, "Keyword": k, "Criterion Type": "Exact", "Max CPC": f"{bid:.2f}", "Final URL": URL + z["url"]})
            mots.append({"Campaign": c, "Ad Group": g, "Keyword": variantes[0], "Criterion Type": "Phrase", "Max CPC": f"{bid * 0.8:.2f}", "Final URL": URL + z["url"]})
        titres = {"75": ["Serrurier Paris 24h/24", "Serrurier Dans Votre Quartier", "Tous Arrondissements de Paris"],
                  "92": ["Serrurier Hauts-de-Seine 24h", "Serrurier 92 Dès 49 €", "Serrurier Près de Chez Vous"],
                  "95": ["Serrurier Val-d'Oise 24h/24", "Serrurier 95 Dès 49 €", "Serrurier Près de Chez Vous"]}[dep]
        titres += ["{KeyWord:Serrurier 24h/24}", "Arrivée Rapide, Prix Clair", "Appelez-Nous 24h/24", "Ouverture de Porte Dès 49 €"]
        annonces.append(rsa_row(c, g, "/villes/", titres, "serrurier", dep))

    # 3) Service x ville : un groupe par service, une URL par combinaison
    c = CAMPAGNES["Services x Villes"]
    termes = {"porte-claquee": ["ouverture porte", "porte claquee"], "serrure-bloquee": ["serrure bloquee"],
              "cle-cassee": ["cle cassee"], "changement-serrure": ["changement serrure", "changer serrure"],
              "serrure-connectee": ["serrure connectee"], "effraction": ["serrurier effraction"]}
    enchere = {"porte-claquee": 5.00, "serrure-bloquee": 4.00, "cle-cassee": 4.00, "changement-serrure": 3.50,
               "serrure-connectee": 1.50, "effraction": 4.00}
    for s in SERVICES:
        g = s["court"]
        bid = enchere[s["slug"]]
        groupes.append({"Campaign": c, "Ad Group": g, "Max CPC": f"{bid:.2f}", "Status": "Enabled"})
        for z in ZONES:
            ville = f"paris {z['arr']}" if z["arr"] else kw(z["nom"])
            for t in termes[s["slug"]]:
                mots.append({"Campaign": c, "Ad Group": g, "Keyword": f"{t} {ville}", "Criterion Type": "Phrase",
                             "Max CPC": f"{bid:.2f}", "Final URL": f"{URL}/depannage/{s['slug']}/{z['slug']}/"})
        annonces.append(rsa_row(c, g, f"/depannage/{s['slug']}/", ANNONCES[GROUPE_PAR_SERVICE[s["slug"]]], s["slug"], "24h-24"))

    negs = [{"Campaign": nom, "Keyword": k, "Criterion Type": "Negative Phrase"} for nom in CAMPAGNES.values() for k in NEGATIFS]

    comps = []
    for nom in CAMPAGNES.values():
        comps.append({"Campaign": nom, "Type": "Call", "Text": TEL, "Final URL": "", "Line 2": "", "Line 3": "", "Country": "FR"})
        for txt, url, l2, l3 in COMPOSANTS["liens"]:
            check([txt], 25, "Lien annexe"); check([l2, l3], 35, "Description lien")
            comps.append({"Campaign": nom, "Type": "Sitelink", "Text": txt, "Final URL": URL + url, "Line 2": l2, "Line 3": l3, "Country": ""})
        for a in COMPOSANTS["accroches"]:
            check([a], 25, "Accroche")
            comps.append({"Campaign": nom, "Type": "Callout", "Text": a, "Final URL": "", "Line 2": "", "Line 3": "", "Country": ""})
        en_tete, vals = COMPOSANTS["extraits"]
        comps.append({"Campaign": nom, "Type": "Structured snippet", "Text": en_tete, "Final URL": "", "Line 2": ";".join(vals), "Line 3": "", "Country": ""})

    def dump(name, rows):
        cols = list(dict.fromkeys(k for r in rows for k in r))
        with open(os.path.join(HERE, name), "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, cols)
            w.writeheader()
            w.writerows(rows)
        print(f"{name} : {len(rows)} lignes")
    dump("1-campagnes.csv", campagnes)
    dump("2-groupes.csv", groupes)
    dump("3-mots-cles.csv", mots)
    dump("4-annonces.csv", annonces)
    dump("5-mots-cles-negatifs.csv", negs)
    dump("6-composants.csv", comps)


GROUPE_PAR_SERVICE = {"porte-claquee": "Ouverture de porte", "serrure-bloquee": "Serrure bloquee", "cle-cassee": "Cle cassee",
                      "changement-serrure": "Changement serrure", "serrure-connectee": "Serrure connectee", "effraction": "Apres effraction"}

if __name__ == "__main__":
    main()
