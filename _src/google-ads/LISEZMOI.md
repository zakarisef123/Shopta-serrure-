# Campagne Google Ads Search – Shopta Serrure (CPC manuel)

Fichiers générés par `python3 _src/google-ads/generer_campagne.py` (à relancer après modification).
Le dossier `_src/` n'est pas publié sur le site.

| Fichier | Contenu |
|---|---|
| `1-campagnes.csv` | 3 campagnes Search, CPC manuel, réseau Google Search uniquement, en pause |
| `2-groupes.csv` | 18 groupes d'annonces avec leur enchère max. |
| `3-mots-cles.csv` | ~1 600 mots clés (exact + expression), URL finale propre à chaque ville / combinaison |
| `4-annonces.csv` | 18 annonces responsives (15 titres, 4 descriptions) |
| `5-mots-cles-negatifs.csv` | ~90 mots clés négatifs par campagne |
| `6-composants.csv` | Appel, 6 liens annexes, 10 accroches, extrait structuré « Services » |

## Structure

1. **Urgences serrurier** (40 €/jour) : 9 groupes thématiques (serrurier Paris, urgence/24h, ouverture de porte,
   serrure bloquée, clé cassée, changement de serrure, effraction, tarifs, serrure connectée). Chaque groupe pointe vers sa page.
2. **Serrurier par ville** (35 €/jour) : « serrurier paris 15 », « serrurier 75015 », « serrurier boulogne billancourt »,
   « serrurier 92100 »… Chaque mot clé envoie sur la page de sa ville.
3. **Service x ville** (25 €/jour) : « ouverture porte boulogne billancourt », « cle cassee paris 11 »…
   Chaque mot clé envoie sur la page combinée `/depannage/<service>/<ville>/`.

## Enchères de départ (CPC max)

| Groupe | Exact | Expression |
|---|---|---|
| Serrurier Paris | 9,00 € | 7,20 € |
| Serrurier urgence | 8,50 € | 6,80 € |
| Ouverture de porte | 8,00 € | 6,40 € |
| Après effraction | 6,50 € | 5,20 € |
| Serrure bloquée / clé cassée | 6,00 € | 4,80 € |
| Changement de serrure | 5,50 € | 4,40 € |
| Tarifs | 5,00 € | 4,00 € |
| Villes : Paris arr. / 92 / 95 | 7 € / 6 € / 4 € | ×0,8 |
| Service x ville | 1,50 à 5,00 € | – |

Le serrurier est l'un des métiers les plus chers sur Google Ads en France : environ 8 à 18 € le clic en moyenne nationale,
et beaucoup plus à Paris sur « serrurier paris » ou « serrurier urgence paris ». Ces enchères visent donc une position correcte
sur la longue traîne (arrondissement, ville, service + ville), qui coûte moins cher et convertit mieux, plutôt que la 1re place
à n'importe quel prix sur les mots génériques. **Avant de lancer, vérifiez les CPC « haut de page » dans le Planificateur de mots clés**
(Outils > Planificateur de mots clés > Obtenir le volume de recherche, zone Paris + 92 + 95) et ajustez.

## Mise en ligne, étape par étape

1. **Conversions d'abord** (sinon impossible d'optimiser) — Outils > Conversions > Nouvelle action :
   - « Appels depuis les annonces » (composant Appel, durée min. 60 s),
   - « Clic sur un numéro de téléphone du site » (balise site Web),
   - « Envoi de formulaire » et « Clic WhatsApp » (balise site Web).
   Puis renseignez dans `_src/build.py` : `"ads_id": "AW-XXXXXXXXX"` et les libellés dans `"ads_conv"`
   (`call`, `wa`, `form`). Le site enverra alors les conversions automatiquement.
2. Ouvrez **Google Ads Editor**, téléchargez le compte, puis *Compte > Importer > À partir d'un fichier* :
   importez les CSV dans l'ordre 1 → 6 et vérifiez l'aperçu avant de valider.
3. Contrôlez dans chaque campagne : réseau **Recherche Google uniquement** (décocher partenaires et Display),
   ciblage **« Présence : personnes se trouvant dans vos zones »**, langue français, stratégie **CPC manuel**.
4. Associez la **fiche Google Business Profile** (composant Lieu) : affiche l'adresse, les avis et l'itinéraire.
5. Publiez, puis activez les campagnes.

## Réglages qui font convertir

- **Ajustements d'enchères** : mobile +20 % (les urgences se font au téléphone), 20h–8h +15 % et week-end +10 % si les appels
  y sont rentables ; Paris et proche couronne en priorité.
- **Calendrier** : 24h/24 seulement si quelqu'un décroche vraiment 24h/24. Un appel manqué = un clic payé pour rien.
- Les annonces mettent en avant ce qui rassure (prix annoncé avant départ, devis signé, facture pour l'assurance) :
  c'est ce qui fait la différence face aux arnaques du secteur.

## Routine d'optimisation

- **Tous les 2–3 jours (les 2 premières semaines)** : Mots clés > *Termes de recherche*. Ajoutez en négatif tout ce qui
  est hors sujet (DIY, emploi, autres villes, voiture…), ajoutez en exact les bonnes requêtes qui convertissent.
- **Chaque semaine** : baissez de 10–20 % l'enchère des mots clés qui dépensent sans convertir, montez de 10–20 % ceux qui
  convertissent avec un taux d'impressions perdues (classement) élevé.
- **Chaque mois** : mettez en pause les titres « Faible » des annonces et remplacez-les.
- Objectif : coût par appel/lead inférieur à environ 30 % du panier moyen d'une intervention.
