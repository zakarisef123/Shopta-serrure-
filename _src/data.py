# -*- coding: utf-8 -*-
"""Contenu du site : services, zones d'intervention, articles."""

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "porte-claquee",
        "nom": "Ouverture de porte claquée",
        "court": "Porte claquée",
        "icon": "i-door",
        "prix": "à partir de 49 € TTC",
        "prix_num": 49,
        "kw": "ouverture de porte",
        "resume": "Vous êtes sorti sans vos clés ? Ouverture fine sans casse, par crochetage ou à la radio, sans changer la serrure.",
        "intro": "Une porte qui claque derrière vous, les clés restées à l'intérieur : c'est l'urgence la plus fréquente en serrurerie. Dans la grande majorité des cas, nos serruriers ouvrent une porte simplement claquée (non verrouillée à clé) sans rien abîmer, en quelques minutes, et sans remplacer la serrure.",
        "sections": [
            ("Porte claquée ou porte fermée à clé : quelle différence ?",
             "Une porte <strong>claquée</strong> n'est retenue que par le pêne demi-tour, la petite languette biseautée qui s'enclenche automatiquement. Elle s'ouvre en général à la radio (une lame souple glissée entre la porte et le bâti) ou au crochetage, sans dégât. Une porte <strong>fermée à clé</strong> est retenue par les pênes dormants : l'ouverture reste possible sans casse sur la plupart des serrures, mais elle demande plus de temps et parfois un perçage du cylindre, que nous vous annonçons et chiffrons avant."),
            ("Nos techniques d'ouverture sans dégât",
             "Radio et lames souples pour les portes claquées, crochetage et outils de by-pass pour les cylindres, ouverture par l'entrebâilleur ou le judas sur certaines portes blindées. Le perçage n'est utilisé qu'en dernier recours, avec votre accord, et le cylindre est alors remplacé immédiatement par un modèle équivalent ou supérieur."),
            ("Les bons réflexes en attendant le serrurier",
             "Vérifiez qu'aucune fenêtre ou porte secondaire n'est accessible en sécurité, demandez à un voisin ou à votre gardien s'il détient un double, et ne tentez pas de forcer la porte avec une carte ou un tournevis : vous risqueriez d'endommager le bâti ou la serrure et d'alourdir la facture."),
        ],
        "faq": [
            ("Combien coûte l'ouverture d'une porte claquée ?", "Elle commence à 49 € TTC. Le prix exact dépend du type de porte (standard, blindée, multipoints) et vous est annoncé au téléphone, puis confirmé par un devis écrit sur place avant l'intervention."),
            ("Allez-vous casser la serrure ?", "Non dans la grande majorité des cas. Une porte claquée s'ouvre sans dégât. Si un perçage devait être nécessaire, il vous serait expliqué et chiffré avant, et vous restez libre de refuser."),
            ("Combien de temps dure l'ouverture ?", "Quelques minutes pour une porte simplement claquée, un peu plus pour une porte blindée ou fermée à clé."),
        ],
    },
    {
        "slug": "serrure-bloquee",
        "nom": "Déblocage de serrure",
        "court": "Serrure bloquée",
        "icon": "i-lock",
        "prix": "à partir de 49 € TTC",
        "prix_num": 49,
        "kw": "serrure bloquée",
        "resume": "Clé qui ne tourne plus, mécanisme grippé ou porte fermée à clé : diagnostic et déblocage rapide sur place.",
        "intro": "La clé entre mais ne tourne plus, la poignée force, la porte refuse de s'ouvrir ou de se fermer : une serrure bloquée peut vous laisser dehors ou vous empêcher de sécuriser votre logement. Nous diagnostiquons la cause sur place et débloquons le mécanisme, en réparant plutôt qu'en remplaçant chaque fois que c'est possible.",
        "sections": [
            ("Les causes les plus fréquentes",
             "Cylindre encrassé ou usé, clé tordue ou trop usée, pêne mal aligné avec la gâche après un affaissement de la porte, ressort cassé dans le boîtier, ou serrure multipoints dont une tringle s'est désolidarisée. Chaque cause a sa solution : nettoyage et lubrification, réglage de la gâche, remplacement d'une pièce ou, en dernier recours, du cylindre."),
            ("Ce que nous faisons sur place",
             "Ouverture de la porte si vous êtes à l'extérieur, démontage et diagnostic du mécanisme, puis réparation. Si une pièce doit être changée, le serrurier vous présente le devis et les références avant de la remplacer. Nous avons dans le véhicule les cylindres et pièces courantes pour terminer l'intervention le jour même."),
            ("Éviter que ça recommence",
             "Un entretien une fois par an avec un lubrifiant sec (graphite ou PTFE) suffit à garder un cylindre fluide. Évitez l'huile de cuisine ou le dégrippant gras, qui finissent par coller la poussière dans le mécanisme. Si votre porte frotte, faites régler les paumelles : une porte affaissée force sur le pêne et use la serrure."),
        ],
        "faq": [
            ("Ma clé tourne dans le vide, que faire ?", "C'est souvent le signe d'une came cassée ou d'un cylindre défaillant. N'insistez pas, appelez-nous : nous ouvrons la porte et remplaçons la pièce défectueuse."),
            ("Peut-on réparer une serrure multipoints ?", "Oui, dans la plupart des cas. Nous remplaçons seulement le boîtier ou la pièce en cause, sans changer toute la serrure."),
            ("Le déblocage est-il remboursé par l'assurance ?", "Cela dépend de votre contrat et de la cause (usure ou tentative d'effraction). Nous vous remettons une facture détaillée à transmettre à votre assureur."),
        ],
    },
    {
        "slug": "cle-cassee",
        "nom": "Extraction de clé cassée",
        "court": "Clé cassée",
        "icon": "i-key",
        "prix": "à partir de 49 € TTC",
        "prix_num": 49,
        "kw": "clé cassée dans la serrure",
        "resume": "Extraction du morceau de clé coincé dans le cylindre sans abîmer la serrure, puis reproduction si besoin.",
        "intro": "Une clé fatiguée finit un jour par se casser dans le cylindre, souvent au pire moment. Bonne nouvelle : dans la plupart des cas, le morceau s'extrait sans changer la serrure, avec un outillage adapté.",
        "sections": [
            ("Ne forcez pas !",
             "Pousser le morceau avec une autre clé, un tournevis ou de la colle l'enfonce plus loin et peut bloquer les goupilles. Si le bout dépasse franchement, vous pouvez essayer de le tirer droit avec une pince fine. Sinon, laissez faire un professionnel."),
            ("Notre méthode",
             "Le serrurier utilise des extracteurs fins qui accrochent le morceau de clé entre les goupilles sans les endommager. La porte est ensuite ouverte, le cylindre contrôlé, et nous pouvons vous proposer un nouveau cylindre si la clé cassée révélait une usure avancée."),
            ("Et après ?",
             "Si vous avez une autre clé en bon état, le cylindre reste utilisable. Si c'était la dernière, nous vous conseillons de faire reproduire une clé à partir de la carte de propriété (pour les cylindres de sécurité) ou de remplacer le cylindre avec plusieurs clés neuves."),
        ],
        "faq": [
            ("Faut-il changer la serrure après une clé cassée ?", "Pas forcément. Si le cylindre n'est pas endommagé et que vous avez un double, il suffit d'extraire le morceau."),
            ("Combien coûte l'extraction d'une clé cassée ?", "À partir de 49 € TTC. Le prix vous est confirmé avant intervention."),
            ("Ma clé s'est cassée dans la serrure de ma voiture ou de ma boîte aux lettres", "Nous intervenons aussi sur les boîtes aux lettres. Pour les véhicules, appelez-nous pour vérifier que nous pouvons vous aider."),
        ],
    },
    {
        "slug": "changement-serrure",
        "nom": "Changement de serrure et de cylindre",
        "court": "Changement de serrure",
        "icon": "i-cyl",
        "prix": "sur devis gratuit",
        "prix_num": None,
        "kw": "changement de serrure",
        "resume": "Remplacement de cylindre ou de serrure multipoints certifiée A2P après perte de clés, vol ou emménagement.",
        "intro": "Clés perdues ou volées, emménagement dans un logement dont vous ne connaissez pas les doubles, serrure usée ou trop facile à forcer : changer de cylindre ou de serrure est le moyen le plus sûr de reprendre le contrôle de vos accès.",
        "sections": [
            ("Cylindre seul ou serrure complète ?",
             "Le plus souvent, remplacer le <strong>cylindre</strong> (la partie où entre la clé) suffit : c'est rapide et économique. La <strong>serrure complète</strong> se change quand le boîtier est endommagé, après une effraction, ou pour passer à une serrure 3 ou 5 points plus résistante."),
            ("Comprendre la certification A2P",
             "La marque A2P, délivrée par le CNPP, classe la résistance à l'effraction : A2P* (5 minutes), A2P** (10 minutes), A2P*** (15 minutes). Certaines assurances exigent un niveau minimal : vérifiez votre contrat, nous vous conseillerons le modèle adapté. Les cylindres de sécurité sont livrés avec une carte de propriété : seul son détenteur peut faire reproduire les clés."),
            ("Un devis clair avant de commencer",
             "Le serrurier vous présente plusieurs gammes (standard, haute sécurité, A2P) avec leur prix posé, pièces et main d'œuvre comprises. Vous choisissez, il installe, vous repartez avec la facture, les clés neuves et la carte de propriété."),
        ],
        "faq": [
            ("Combien coûte un changement de cylindre ?", "Le prix dépend de la marque et du niveau de sécurité choisis. Nous vous remettons un devis gratuit, détaillé et sans engagement avant l'intervention."),
            ("Faut-il changer la serrure après un vol de clés ?", "Oui, c'est vivement conseillé, surtout si vos papiers avec votre adresse ont été volés en même temps. Votre assurance peut prendre en charge le remplacement selon votre contrat."),
            ("Propriétaire ou locataire : qui paie ?", "Le remplacement suite à la perte des clés est en général à la charge du locataire ; le remplacement d'une serrure vétuste incombe plutôt au propriétaire. Vérifiez votre bail."),
        ],
    },
    {
        "slug": "serrure-connectee",
        "nom": "Serrure connectée (Smart Lock)",
        "court": "Smart Lock",
        "icon": "i-smart",
        "prix": "à partir de 49 € TTC",
        "prix_num": 49,
        "kw": "serrure connectée",
        "resume": "Installation et dépannage de serrures connectées : ouverture par smartphone, code ou empreinte digitale.",
        "intro": "Les serrures connectées permettent d'ouvrir avec un smartphone, un code ou une empreinte, de donner un accès temporaire à un proche ou de suivre les passages. Nous les installons sur votre porte existante et intervenons en cas de panne ou de blocage.",
        "sections": [
            ("Installation sur votre porte",
             "Selon le modèle, la serrure connectée se pose côté intérieur sur votre cylindre existant, ou remplace le cylindre et la poignée. Nous vérifions la compatibilité de votre porte, installons et paramétrons l'application avec vous, puis testons chaque mode d'ouverture."),
            ("Dépannage d'une serrure connectée",
             "Pile vide, mise à jour ratée, appairage perdu, moteur qui force sur un pêne mal aligné : nous ouvrons la porte si vous êtes bloqué dehors, remettons le système en fonctionnement et réglons la porte pour éviter que la panne se reproduise."),
            ("Nos conseils de sécurité",
             "Gardez toujours une clé mécanique de secours hors du logement, choisissez un modèle avec cylindre certifié si votre porte donne sur l'extérieur, et remplacez les piles dès la première alerte de batterie faible."),
        ],
        "faq": [
            ("Ma serrure connectée ne répond plus, je suis dehors", "Appelez-nous : nous ouvrons la porte comme pour une serrure classique, puis remettons la serrure connectée en service."),
            ("Peut-on installer une serrure connectée sur une porte blindée ?", "Souvent oui, selon le cylindre en place. Envoyez-nous une photo de votre porte sur WhatsApp pour un avis rapide."),
            ("Combien coûte l'installation ?", "Le dépannage commence à 49 € TTC. L'installation dépend du modèle choisi et fait l'objet d'un devis gratuit."),
        ],
    },
    {
        "slug": "effraction",
        "nom": "Sécurisation après effraction",
        "court": "Après effraction",
        "icon": "i-tool",
        "prix": "sur devis gratuit",
        "prix_num": None,
        "kw": "serrurier après cambriolage",
        "resume": "Sécurisation provisoire, remplacement de serrure et de cylindre, renfort de porte, pose de verrou ou de blindage.",
        "intro": "Après un cambriolage ou une tentative d'effraction, la priorité est de refermer votre logement le jour même. Nous sécurisons la porte en urgence, puis vous proposons une remise en état durable, avec tous les documents nécessaires à votre déclaration d'assurance.",
        "sections": [
            ("Les étapes après une effraction",
             "1. Ne touchez à rien et appelez la police (17) pour faire constater. 2. Déposez plainte, le récépissé est demandé par votre assureur. 3. Faites sécuriser l'accès : nous intervenons 24h/24. 4. Déclarez le sinistre à votre assurance, en général dans les 2 jours ouvrés après en avoir eu connaissance."),
            ("Sécurisation immédiate",
             "Remplacement du cylindre forcé, pose d'une serrure provisoire, consolidation du bâti ou de la gâche arrachée, condamnation temporaire si la porte ne peut pas être refermée. L'objectif : que vous puissiez dormir chez vous en sécurité dès ce soir."),
            ("Remise en état et renforcement",
             "Selon les dégâts : nouvelle serrure multipoints A2P, cornières anti-pinces, protège-cylindre, renfort de bâti, blindage de porte. Nous fournissons un devis détaillé et des photos avant/après pour l'expert de votre assurance."),
        ],
        "faq": [
            ("L'assurance rembourse-t-elle le serrurier après un cambriolage ?", "Dans la plupart des contrats multirisques habitation, oui, sur présentation du dépôt de plainte et de la facture. Nous vous remettons une facture détaillée et conforme."),
            ("Pouvez-vous intervenir avant le passage de la police ?", "Il est préférable d'attendre le constat. Si la porte ne ferme plus, nous pouvons sécuriser provisoirement en préservant les traces utiles."),
            ("Faites-vous la pose de porte blindée ?", "Nous réalisons le blindage de porte existante et les renforts. Pour un bloc-porte blindé complet, demandez-nous un devis."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Zones d'intervention
# (nom affiché, code INSEE, latitude, longitude)
# ---------------------------------------------------------------------------
PARIS_ARR = {
    1: ("75101", 48.8625, 2.3363, ["Saint-Germain-l'Auxerrois", "Les Halles", "Palais-Royal", "Place Vendôme"], ["le Louvre", "Châtelet", "la rue de Rivoli"]),
    2: ("75102", 48.8683, 2.3428, ["Gaillon", "Vivienne", "Mail", "Bonne-Nouvelle"], ["la Bourse", "le Sentier", "la rue Montorgueil"]),
    3: ("75103", 48.8630, 2.3600, ["Arts-et-Métiers", "Enfants-Rouges", "Archives", "Sainte-Avoye"], ["le Haut-Marais", "la place de la République", "le Temple"]),
    4: ("75104", 48.8543, 2.3576, ["Saint-Merri", "Saint-Gervais", "Arsenal", "Notre-Dame"], ["l'Hôtel de Ville", "l'île Saint-Louis", "le Marais"]),
    5: ("75105", 48.8445, 2.3507, ["Saint-Victor", "Jardin-des-Plantes", "Val-de-Grâce", "Sorbonne"], ["le Quartier latin", "le Panthéon", "la rue Mouffetard"]),
    6: ("75106", 48.8491, 2.3329, ["Monnaie", "Odéon", "Notre-Dame-des-Champs", "Saint-Germain-des-Prés"], ["le jardin du Luxembourg", "Saint-Sulpice", "Vavin"]),
    7: ("75107", 48.8562, 2.3121, ["Saint-Thomas-d'Aquin", "Invalides", "École-Militaire", "Gros-Caillou"], ["la tour Eiffel", "les Invalides", "la rue du Bac"]),
    8: ("75108", 48.8727, 2.3125, ["Champs-Élysées", "Faubourg-du-Roule", "Madeleine", "Europe"], ["les Champs-Élysées", "la gare Saint-Lazare", "le parc Monceau"]),
    9: ("75109", 48.8771, 2.3375, ["Saint-Georges", "Chaussée-d'Antin", "Faubourg-Montmartre", "Rochechouart"], ["l'Opéra", "les Grands Boulevards", "South Pigalle"]),
    10: ("75110", 48.8761, 2.3607, ["Saint-Vincent-de-Paul", "Porte-Saint-Denis", "Porte-Saint-Martin", "Hôpital-Saint-Louis"], ["la gare du Nord", "la gare de l'Est", "le canal Saint-Martin"]),
    11: ("75111", 48.8591, 2.3800, ["Folie-Méricourt", "Roquette", "Sainte-Marguerite", "Saint-Ambroise"], ["Bastille", "Oberkampf", "la place Léon-Blum"]),
    12: ("75112", 48.8400, 2.3880, ["Bel-Air", "Picpus", "Bercy", "Quinze-Vingts"], ["la gare de Lyon", "Bercy", "Daumesnil"]),
    13: ("75113", 48.8283, 2.3622, ["Salpêtrière", "Gare", "Maison-Blanche", "Croulebarbe"], ["la place d'Italie", "la Butte-aux-Cailles", "la BnF"]),
    14: ("75114", 48.8292, 2.3266, ["Montparnasse", "Parc-de-Montsouris", "Petit-Montrouge", "Plaisance"], ["Montparnasse", "Denfert-Rochereau", "Alésia"]),
    15: ("75115", 48.8401, 2.2934, ["Saint-Lambert", "Necker", "Grenelle", "Javel"], ["Convention", "Beaugrenelle", "la rue de Vaugirard"]),
    16: ("75116", 48.8637, 2.2769, ["Auteuil", "Muette", "Porte-Dauphine", "Chaillot"], ["le Trocadéro", "Passy", "Auteuil"]),
    17: ("75117", 48.8873, 2.3067, ["Ternes", "Plaine-de-Monceaux", "Batignolles", "Épinettes"], ["les Batignolles", "les Ternes", "la place de Clichy"]),
    18: ("75118", 48.8925, 2.3484, ["Grandes-Carrières", "Clignancourt", "Goutte-d'Or", "La Chapelle"], ["Montmartre", "Barbès", "la porte de Clignancourt"]),
    19: ("75119", 48.8871, 2.3848, ["La Villette", "Pont-de-Flandre", "Amérique", "Combat"], ["les Buttes-Chaumont", "le parc de la Villette", "Jaurès"]),
    20: ("75120", 48.8634, 2.4012, ["Belleville", "Saint-Fargeau", "Père-Lachaise", "Charonne"], ["Belleville", "le Père-Lachaise", "Gambetta"]),
}

HDS = [  # Hauts-de-Seine (92)
    ("Antony", 48.7543, 2.2977), ("Asnières-sur-Seine", 48.9145, 2.2876), ("Bagneux", 48.7960, 2.3090),
    ("Bois-Colombes", 48.9177, 2.2683), ("Boulogne-Billancourt", 48.8352, 2.2410), ("Bourg-la-Reine", 48.7797, 2.3165),
    ("Châtenay-Malabry", 48.7652, 2.2638), ("Châtillon", 48.8024, 2.2905), ("Chaville", 48.8085, 2.1886),
    ("Clamart", 48.8003, 2.2668), ("Clichy", 48.9045, 2.3062), ("Colombes", 48.9226, 2.2522),
    ("Courbevoie", 48.8973, 2.2530), ("Fontenay-aux-Roses", 48.7893, 2.2870), ("Garches", 48.8456, 2.1873),
    ("La Garenne-Colombes", 48.9067, 2.2447), ("Gennevilliers", 48.9333, 2.2933), ("Issy-les-Moulineaux", 48.8240, 2.2700),
    ("Levallois-Perret", 48.8950, 2.2870), ("Malakoff", 48.8169, 2.2990), ("Marnes-la-Coquette", 48.8290, 2.1720),
    ("Meudon", 48.8130, 2.2350), ("Montrouge", 48.8162, 2.3168), ("Nanterre", 48.8924, 2.2066),
    ("Neuilly-sur-Seine", 48.8846, 2.2697), ("Le Plessis-Robinson", 48.7810, 2.2630), ("Puteaux", 48.8840, 2.2380),
    ("Rueil-Malmaison", 48.8770, 2.1800), ("Saint-Cloud", 48.8440, 2.2190), ("Sceaux", 48.7766, 2.2900),
    ("Sèvres", 48.8240, 2.2110), ("Suresnes", 48.8710, 2.2290), ("Vanves", 48.8215, 2.2900),
    ("Vaucresson", 48.8400, 2.1530), ("Ville-d'Avray", 48.8250, 2.1930), ("Villeneuve-la-Garenne", 48.9367, 2.3250),
]

VDO = [  # Val-d'Oise (95)
    ("Argenteuil", 48.9472, 2.2467), ("Arnouville", 48.9870, 2.4170), ("Auvers-sur-Oise", 49.0710, 2.1700),
    ("Beauchamp", 49.0130, 2.1900), ("Beaumont-sur-Oise", 49.1420, 2.2870), ("Bernes-sur-Oise", 49.1610, 2.3000),
    ("Bessancourt", 49.0370, 2.2090), ("Bezons", 48.9260, 2.2170), ("Boisemont", 49.0190, 2.0050),
    ("Bonneuil-en-France", 48.9700, 2.4300), ("Bouffémont", 49.0430, 2.3010), ("Bruyères-sur-Oise", 49.1580, 2.3270),
    ("Butry-sur-Oise", 49.0880, 2.1980), ("Cergy", 49.0364, 2.0761), ("Champagne-sur-Oise", 49.1400, 2.2400),
    ("Cormeilles-en-Parisis", 48.9730, 2.2010), ("Courdimanche", 49.0390, 2.0010), ("Deuil-la-Barre", 48.9700, 2.3270),
    ("Domont", 49.0270, 2.3270), ("Eaubonne", 48.9920, 2.2800), ("Écouen", 49.0190, 2.3790),
    ("Enghien-les-Bains", 48.9700, 2.3080), ("Ennery", 49.0750, 2.1080), ("Épiais-Rhus", 49.1200, 2.0700),
    ("Épinay-Champlâtreux", 49.0890, 2.4110), ("Éragny", 49.0170, 2.0920), ("Ermont", 48.9900, 2.2580),
    ("Ézanville", 49.0280, 2.3610), ("Fontenay-en-Parisis", 49.0510, 2.4520), ("Fosses", 49.0980, 2.5070),
    ("Franconville", 48.9890, 2.2290), ("Frépillon", 49.0520, 2.2050), ("Frouville", 49.1550, 2.1480),
    ("Garges-lès-Gonesse", 48.9720, 2.3990), ("Gonesse", 48.9870, 2.4490), ("Goussainville", 49.0330, 2.4650),
    ("Groslay", 48.9860, 2.3480), ("Herblay-sur-Seine", 48.9900, 2.1650), ("L'Isle-Adam", 49.1110, 2.2230),
    ("Jouy-le-Moutier", 49.0110, 2.0410), ("Louvres", 49.0440, 2.5050), ("Marly-la-Ville", 49.0820, 2.5000),
    ("Montigny-lès-Cormeilles", 48.9930, 2.1960), ("Montmagny", 48.9730, 2.3460), ("Montmorency", 48.9890, 2.3220),
    ("Osny", 49.0590, 2.0630), ("Persan", 49.1530, 2.2720), ("Pierrelaye", 49.0220, 2.1540),
    ("Pontoise", 49.0510, 2.1010), ("Puiseux-Pontoise", 49.0600, 2.0170), ("Saint-Brice-sous-Forêt", 48.9990, 2.3570),
    ("Saint-Gratien", 48.9720, 2.2850), ("Saint-Leu-la-Forêt", 49.0150, 2.2470), ("Saint-Ouen-l'Aumône", 49.0440, 2.1110),
    ("Saint-Prix", 49.0130, 2.2630), ("Sannois", 48.9720, 2.2580), ("Sarcelles", 48.9970, 2.3780),
    ("Soisy-sous-Montmorency", 48.9880, 2.3000), ("Taverny", 49.0260, 2.2220), ("Vauréal", 49.0300, 2.0330),
    ("Villiers-le-Bel", 49.0090, 2.3910),
]

DEPTS = {
    "75": ("Paris", "Paris (75)"),
    "92": ("Hauts-de-Seine", "Hauts-de-Seine (92)"),
    "95": ("Val-d'Oise", "Val-d'Oise (95)"),
}

# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "porte-claquee-que-faire",
        "titre": "Porte claquée : que faire ? Le guide pour rentrer chez vous sans arnaque",
        "court": "Porte claquée : que faire ?",
        "cat": "Urgences", "date": "2026-10-12", "icon": "i-door", "grad": "#003380,#2563eb",
        "desc": "Les bons réflexes quand la porte claque derrière vous, ce qu'un serrurier honnête doit vous annoncer, et le prix normal d'une ouverture.",
        "corps": [
            ("p", "Vous sortez sur le palier, un courant d'air, et la porte se referme derrière vous avec les clés à l'intérieur. Pas de panique : une porte <strong>claquée</strong>, c'est-à-dire non verrouillée à clé, s'ouvre presque toujours sans dégât et en quelques minutes."),
            ("h2", "1. Vérifiez les solutions gratuites"),
            ("ul", ["Un proche, un voisin ou le gardien a-t-il un double ?", "Votre propriétaire ou votre agence en conserve-t-il un ?", "Une autre porte (service, garage, terrasse) est-elle accessible sans danger ?"]),
            ("p", "N'essayez pas de passer par une fenêtre en hauteur, et évitez la technique de la carte bancaire : sur les serrures récentes, elle ne fonctionne pas et peut abîmer le joint ou la gâche."),
            ("h2", "2. Choisissez un serrurier qui annonce son prix"),
            ("p", "Le dépannage en serrurerie fait partie des secteurs les plus surveillés par la DGCCRF. Pour éviter les mauvaises surprises :"),
            ("ul", ["Appelez une entreprise locale identifiée (nom, numéro, avis vérifiables), pas un numéro trouvé sur un prospectus glissé dans la boîte aux lettres.", "Demandez le prix au téléphone : un professionnel sérieux peut l'estimer à partir de votre description.", "Exigez un devis écrit et signé avant le début de l'intervention : c'est obligatoire.", "Méfiez-vous si le serrurier veut percer ou changer la serrure d'une porte simplement claquée."]),
            ("h2", "3. Combien coûte une ouverture de porte claquée ?"),
            ("p", "Chez Shopta Serrure, l'ouverture d'une porte claquée commence à <strong>49 € TTC</strong>. Le tarif peut varier selon le type de porte (blindée, multipoints) et vous est toujours annoncé avant le déplacement, puis confirmé par écrit sur place."),
            ("h2", "4. Après l'ouverture"),
            ("p", "Profitez-en pour faire faire un double de vos clés et le confier à une personne de confiance. Si votre porte claque facilement, un groom réglable ou un réglage des paumelles évite que l'incident se reproduise."),
        ],
    },
    {
        "slug": "eviter-arnaques-serrurier",
        "titre": "Arnaques au serrurier : 7 signaux d'alerte et comment les éviter",
        "court": "Comment éviter les arnaques au serrurier",
        "cat": "Conseils", "date": "2026-09-28", "icon": "i-shield", "grad": "#0f172a,#334155",
        "desc": "Factures à plusieurs milliers d'euros, serrures changées sans raison : les pratiques abusives à connaître et vos droits face à un dépanneur.",
        "corps": [
            ("p", "Chaque année, des particuliers paient des sommes exorbitantes pour une simple ouverture de porte. Ces abus ne sont pas une fatalité : quelques réflexes suffisent à les éviter."),
            ("h2", "Les signaux d'alerte"),
            ("ol", ["Un prospectus « numéro d'urgence » imitant un document de la mairie ou du syndic.", "Un prix au téléphone flou ou « à partir de 19 € » sans autre précision.", "Pas de devis écrit avant de commencer.", "La proposition de percer ou de changer la serrure pour une porte simplement claquée.", "Un paiement exigé uniquement en espèces, sans facture.", "Une pression pour signer vite, « sinon le déplacement est facturé ».", "Une entreprise sans adresse, sans SIRET ni avis vérifiables."]),
            ("h2", "Vos droits"),
            ("p", "Pour un dépannage à domicile, le professionnel doit afficher ses tarifs et vous remettre un <strong>devis détaillé</strong> avant l'intervention lorsque le montant est connu à l'avance. Vous pouvez refuser ce devis : seul le déplacement, s'il vous a été annoncé, peut alors être dû. Une facture détaillée doit vous être remise."),
            ("h2", "En cas de litige"),
            ("p", "Gardez tous les documents, contestez par écrit, et signalez les pratiques abusives sur la plateforme publique <strong>SignalConso</strong>. Vous pouvez aussi saisir le médiateur de la consommation indiqué par l'entreprise."),
            ("h2", "Notre engagement"),
            ("p", "Chez Shopta Serrure, le prix est annoncé au téléphone, confirmé par un devis signé, et la facture est détaillée et conforme pour votre assurance. Nos avis clients sont publics et vérifiables sur notre fiche Google."),
        ],
    },
    {
        "slug": "securiser-porte-entree",
        "titre": "Comment sécuriser votre porte d'entrée ?",
        "court": "Comment sécuriser votre porte d'entrée ?",
        "cat": "Sécurité", "date": "2026-01-24", "icon": "i-shield", "grad": "#003380,#2563eb",
        "desc": "Serrure multipoints A2P, blindage, cornières, protège-cylindre : les solutions efficaces pour décourager les cambrioleurs.",
        "corps": [
            ("p", "La porte d'entrée reste le premier point de passage des cambrioleurs. La plupart abandonnent au-delà de quelques minutes de résistance : chaque élément qui les ralentit compte."),
            ("h2", "1. Une serrure multipoints certifiée"),
            ("p", "Une serrure 3 ou 5 points répartit l'ancrage sur toute la hauteur de la porte. Choisissez un modèle certifié <strong>A2P</strong> (1, 2 ou 3 étoiles selon la résistance) et un cylindre de sécurité avec carte de propriété."),
            ("h2", "2. Le cylindre, point faible fréquent"),
            ("p", "Un cylindre standard peut être cassé ou arraché. Un cylindre anti-casse, anti-perçage et anti-crochetage, associé à un protège-cylindre (rosace) en acier, ferme cette porte d'entrée aux tentatives les plus courantes."),
            ("h2", "3. Le blindage et les cornières"),
            ("p", "Le blindage d'une porte existante renforce le vantail par une tôle d'acier. Les cornières anti-pinces empêchent d'insérer un pied-de-biche entre la porte et le bâti."),
            ("h2", "4. Les petits équipements utiles"),
            ("ul", ["Un entrebâilleur pour ouvrir sans laisser entrer.", "Un judas (ou un judas numérique) pour identifier le visiteur.", "Des paumelles anti-dégondage.", "Un éclairage extérieur à détection."]),
            ("p", "Nos serruriers peuvent évaluer votre porte gratuitement et vous proposer les renforts adaptés à votre budget."),
        ],
    },
    {
        "slug": "cle-cassee-dans-la-serrure",
        "titre": "Que faire en cas de clé cassée dans la serrure ?",
        "court": "Clé cassée dans la serrure : que faire ?",
        "cat": "Urgences", "date": "2026-01-20", "icon": "i-key", "grad": "#16a34a,#22c55e",
        "desc": "Les bons réflexes avant d'appeler un professionnel, et pourquoi il ne faut surtout pas forcer.",
        "corps": [
            ("p", "Un moment de précipitation et la clé casse dans le cylindre. Pas de panique, mais surtout : ne forcez pas."),
            ("h2", "Ce qu'il ne faut pas faire"),
            ("ul", ["Pousser le morceau avec une autre clé ou un tournevis : il s'enfonce davantage.", "Mettre de la colle sur l'autre morceau pour « recoller » : la colle bloque les goupilles.", "Tourner le cylindre avec une pince : vous risquez de casser la came."]),
            ("h2", "Ce que vous pouvez essayer"),
            ("p", "Si le morceau dépasse nettement, tirez-le bien droit avec une pince plate fine, sans tourner. Un peu de lubrifiant sec (graphite) peut faciliter l'extraction."),
            ("h2", "Quand appeler un serrurier"),
            ("p", "Si le morceau est entièrement dans le cylindre, un extracteur professionnel est nécessaire. L'opération prend en général quelques minutes et ne nécessite pas de changer la serrure. Chez Shopta Serrure, elle commence à 49 € TTC."),
        ],
    },
    {
        "slug": "entretien-serrure",
        "titre": "L'importance de l'entretien de vos serrures",
        "court": "Entretenir sa serrure",
        "cat": "Entretien", "date": "2026-01-15", "icon": "i-tool", "grad": "#0f172a,#334155",
        "desc": "Quelques gestes simples une fois par an suffisent à éviter les blocages et à prolonger la vie de votre serrure.",
        "corps": [
            ("p", "La poussière, l'humidité et l'usure sont les ennemis de vos cylindres. Une serrure entretenue dure plus longtemps et vous évite un blocage au pire moment."),
            ("h2", "Le bon lubrifiant"),
            ("p", "Utilisez un lubrifiant <strong>sec</strong> : poudre de graphite ou spray PTFE. Évitez absolument l'huile de cuisine et les dégrippants gras, qui retiennent la poussière et finissent par coller les goupilles."),
            ("h2", "La routine annuelle"),
            ("ol", ["Nettoyez l'entrée du cylindre avec un pinceau sec.", "Injectez une petite dose de lubrifiant sec.", "Faites tourner la clé plusieurs fois dans les deux sens.", "Vérifiez que le pêne entre bien dans la gâche sans frotter.", "Resserrez les vis de la poignée et de la plaque."]),
            ("h2", "Les signes qui doivent alerter"),
            ("p", "Une clé qui accroche, un pêne qui force, une porte qu'il faut pousser pour fermer : ces signes annoncent souvent un blocage prochain. Une intervention préventive coûte moins cher qu'un dépannage d'urgence."),
        ],
    },
    {
        "slug": "choisir-serrure-haute-securite",
        "titre": "Comment choisir sa serrure haute sécurité ?",
        "court": "Choisir sa serrure haute sécurité",
        "cat": "Conseils", "date": "2026-01-10", "icon": "i-lock", "grad": "#b45309,#f59e0b",
        "desc": "A2P, multipoints, connectée : on décrypte les normes pour faire le meilleur choix selon votre porte et votre budget.",
        "corps": [
            ("p", "Le choix d'une serrure dépend de votre porte, de votre environnement et des exigences de votre assurance."),
            ("h2", "Les niveaux A2P"),
            ("ul", ["<strong>A2P*</strong> : résiste 5 minutes à une tentative d'effraction.", "<strong>A2P**</strong> : 10 minutes.", "<strong>A2P***</strong> : 15 minutes, le niveau souvent exigé pour les biens les plus exposés."]),
            ("p", "La certification est délivrée par le CNPP. Vérifiez dans votre contrat d'assurance habitation si un niveau minimal est requis."),
            ("h2", "Serrure en applique ou encastrée ?"),
            ("p", "La serrure en applique se fixe sur la face intérieure de la porte : idéale pour ajouter un verrou de sécurité. La serrure encastrée (à mortaiser) est intégrée dans l'épaisseur de la porte : plus discrète, elle équipe la majorité des portes récentes."),
            ("h2", "Combien de points ?"),
            ("p", "Pour une porte d'entrée, une serrure 3 points est un minimum recommandé ; 5 points pour les portes les plus exposées (rez-de-chaussée, maison)."),
            ("h2", "Et les serrures connectées ?"),
            ("p", "Pratiques au quotidien, elles doivent être associées à un cylindre mécanique de qualité. Nous installons et dépannons les principaux modèles."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Photos : déposez les originaux dans _src/images/photos/ avec ces noms
# (jpg, jpeg, png ou webp). Clé -> (nom de fichier sans extension, texte alternatif)
# ---------------------------------------------------------------------------
PHOTOS = {
    "porte-claquee": ("serrurier-ouverture-porte", "Serrurier ouvrant une porte d'entrée claquée"),
    "serrure-bloquee": ("serrurier-crochetage", "Serrurier débloquant la serrure d'une porte vitrée"),
    "cle-cassee": ("cle-serrure-porte-blindee", "Clé dans la serrure multipoints d'une porte blindée"),
    "changement-serrure": ("changement-cylindre", "Remplacement d'un cylindre de serrure par un serrurier"),
    "serrure-connectee": ("serrurier-conseil-clients", "Serrurier conseillant des clients devant une serrure connectée"),
    "effraction": ("porte-effraction", "Porte d'entrée endommagée après une tentative d'effraction"),
    "porte-rouge": ("porte-rouge", "Porte d'entrée rouge avec serrure et poignée en laiton"),
}
# Photo d'illustration par article de blog
ARTICLE_PHOTOS = {
    "porte-claquee-que-faire": "porte-claquee",
    "eviter-arnaques-serrurier": "serrure-connectee",
    "securiser-porte-entree": "porte-rouge",
    "cle-cassee-dans-la-serrure": "cle-cassee",
    "entretien-serrure": "changement-serrure",
    "choisir-serrure-haute-securite": "serrure-bloquee",
}

# ---------------------------------------------------------------------------
# Assureurs : logos dans _src/images/assureurs/<slug>.(png|jpg|webp|svg)
# (nom, slug, domaine du site officiel, couleur de secours)
# ---------------------------------------------------------------------------
INSURERS = [
    ("AXA", "axa", "axa.fr", "#00008f"), ("Allianz", "allianz", "allianz.fr", "#003781"),
    ("MAIF", "maif", "maif.fr", "#c8102e"), ("MACIF", "macif", "macif.fr", "#004b93"),
    ("MAAF", "maaf", "maaf.fr", "#e30613"), ("Groupama", "groupama", "groupama.fr", "#007a53"),
    ("Generali", "generali", "generali.fr", "#c21b17"), ("Matmut", "matmut", "matmut.fr", "#e2001a"),
    ("GMF", "gmf", "gmf.fr", "#00529b"), ("MMA", "mma", "mma.fr", "#e30613"),
    ("Crédit Agricole Assurances", "credit-agricole", "credit-agricole.fr", "#007d8f"),
    ("BNP Paribas Cardif", "bnp-paribas-cardif", "cardif.fr", "#00915a"),
    ("Société Générale Assurances", "societe-generale", "societegenerale.fr", "#e60028"),
    ("LCL", "lcl", "lcl.fr", "#002f6c"), ("Crédit Mutuel", "credit-mutuel", "creditmutuel.fr", "#0060a9"),
    ("CIC", "cic", "cic.fr", "#00a0e1"), ("La Banque Postale", "la-banque-postale", "labanquepostale.fr", "#003da5"),
    ("Caisse d'Épargne", "caisse-epargne", "caisse-epargne.fr", "#e2001a"),
    ("Banque Populaire", "banque-populaire", "banquepopulaire.fr", "#0065b1"),
    ("Covéa", "covea", "covea.com", "#1d3f8f"), ("Abeille Assurances", "abeille", "abeille-assurances.fr", "#ffb81c"),
    ("Swiss Life", "swiss-life", "swisslife.fr", "#d82034"), ("AG2R La Mondiale", "ag2r", "ag2rlamondiale.fr", "#0b3b8c"),
    ("Thélem", "thelem", "thelem-assurances.fr", "#e4002b"), ("GAN Assurances", "gan", "gan.fr", "#005eb8"),
    ("MAE", "mae", "mae.fr", "#00a19a"), ("MACSF", "macsf", "macsf.fr", "#004f9f"),
    ("Mutuelle de Poitiers", "mutuelle-poitiers", "assurance-mutuelle-poitiers.fr", "#003f7d"),
    ("Direct Assurance", "direct-assurance", "direct-assurance.fr", "#ff6a13"),
    ("Amaguiz", "amaguiz", "amaguiz.com", "#6ab023"), ("Leocare", "leocare", "leocare.eu", "#1e1e50"),
    ("Luko", "luko", "luko.eu", "#2d50e6"), ("Lovys", "lovys", "lovys.com", "#ff5a5f"),
    ("Acheel", "acheel", "acheel.com", "#6c3cff"), ("L'olivier Assurance", "lolivier", "lolivier.fr", "#78a22f"),
    ("Hiscox", "hiscox", "hiscox.fr", "#cc0000"), ("April", "april", "april.fr", "#00a3e0"),
    ("Assu 2000", "assu2000", "assu2000.fr", "#e4032e"), ("Sogessur", "sogessur", "sogessur.fr", "#e60028"),
    ("Allianz Direct", "allianz-direct", "allianz-direct.fr", "#003781"), ("MGEN", "mgen", "mgen.fr", "#00a3a6"),
    ("Euro-Assurance", "euro-assurance", "euro-assurance.com", "#1b4f9c"),
]

# ---------------------------------------------------------------------------
# Marques sur lesquelles nous intervenons : logos dans _src/images/marques/<slug>.*
# (nom, slug, catégorie)
# ---------------------------------------------------------------------------
BRANDS = [
    # Serrures et cylindres
    ("Fichet", "fichet", "serrure"), ("Point Fort Fichet", "point-fort-fichet", "serrure"),
    ("Picard Serrures", "picard", "serrure"), ("Vachette", "vachette", "serrure"), ("Bricard", "bricard", "serrure"),
    ("Héraclès", "heracles", "serrure"), ("Pollux", "pollux", "serrure"), ("JPM", "jpm", "serrure"),
    ("Thirard", "thirard", "serrure"), ("Metalux", "metalux", "serrure"), ("Laperche", "laperche", "serrure"),
    ("Stremler", "stremler", "serrure"), ("Mul-T-Lock", "mul-t-lock", "serrure"), ("Abus", "abus", "serrure"),
    ("DOM", "dom", "serrure"), ("Mauer", "mauer", "serrure"), ("EVVA", "evva", "serrure"),
    ("dormakaba", "kaba", "serrure"), ("Keso", "keso", "serrure"), ("Iseo", "iseo", "serrure"), ("Cisa", "cisa", "serrure"),
    ("Mottura", "mottura", "serrure"), ("Tesa", "tesa", "serrure"), ("Yale", "yale", "serrure"),
    ("Assa Abloy", "assa-abloy", "serrure"),
    # Portes blindées et portes d'entrée
    ("Tordjman Métal", "tordjman", "porte"), ("Bel'M", "belm", "porte"), ("K•Line", "kline", "porte"),
    ("Zilten", "zilten", "porte"), ("Lapeyre", "lapeyre", "porte"), ("Tryba", "tryba", "porte"),
    ("Dierre", "dierre", "porte"), ("Gardesa", "gardesa", "porte"), ("Hörmann", "hormann", "porte"),
    # Serrures connectées
    ("Somfy", "somfy", "connectee"), ("Netatmo", "netatmo", "connectee"), ("Linus by Yale", "linus", "connectee"),
    ("Nuki", "nuki", "connectee"), ("Ultion", "ultion", "connectee"), ("Danalock", "danalock", "connectee"),
    ("Bold", "bold", "connectee"), ("Igloohome", "igloohome", "connectee"),
]
