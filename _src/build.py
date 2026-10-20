# -*- coding: utf-8 -*-
"""Générateur du site Shopta Serrure.

Usage : python3 _src/build.py
Génère toutes les pages HTML et les fichiers SEO à la racine du dépôt.
"""
import datetime
import html
import json
import math
import os
import re
import shutil
import unicodedata

from data import ARTICLE_PHOTOS, ARTICLES, BRANDS, DEPTS, HDS, INSURERS, PARIS_ARR, PHOTOS, SERVICES, VDO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src")

# ---------------------------------------------------------------------------
# Configuration : à vérifier avant mise en ligne
# ---------------------------------------------------------------------------
CONFIG = {
    "site_url": "https://shoptaserrure.netlify.app",  # remplacer par le nom de domaine définitif, sans / final
    "nom": "Shopta Serrure",
    "tel": "06 20 54 66 93",
    "tel_intl": "+33620546693",
    "wa": "33620546693",
    "email": "shoptaserrure@gmail.com",
    "lat": 48.910553,
    "lng": 2.311311,
    # Adresse postale affichée sur la fiche Google (laisser vide si la fiche masque l'adresse)
    "adresse": {"rue": "", "cp": "", "ville": ""},
    "maps_url": "https://www.google.com/maps/place/Serrurier+-+Shopta+serrure/@48.910553,2.3087361,17z/data=!3m1!4b1!4m6!3m5!1s0xa8d45bcb80f455ff:0xa96d71eb2e26af41!8m2!3d48.910553!4d2.311311!16s%2Fg%2F11mz7xq9zy",
    "maps_cid": "12208539419776823105",
    # Lien « Demander des avis » de la fiche Google Business Profile (ex. https://g.page/r/XXXX/review)
    "avis_url": "",
    "instagram": "https://www.instagram.com/shoptaserrure/",
    "tiktok": "https://www.tiktok.com/@shopta.serrure",
    "ga_id": "G-0VFWJ86Y1C",
    "indexnow_key": "8f3c1a6e2b7d4f90a5c3e1b2d4f6a8c0",
    # Mentions légales
    "raison_sociale": "Shopta Serrure",
    "siret": "",
    "responsable": "",
}
TODAY = datetime.date.today().isoformat()

with open(os.path.join(SRC, "communes.json"), encoding="utf-8") as f:
    COMMUNES = json.load(f)
with open(os.path.join(SRC, "avis.json"), encoding="utf-8") as f:
    AVIS = json.load(f)
with open(os.path.join(SRC, "sprite.svg"), encoding="utf-8") as f:
    SPRITE = f.read()

E = html.escape
URL = CONFIG["site_url"]
TEL = CONFIG["tel"]
TEL_HREF = "tel:" + CONFIG["tel_intl"]
WA = "https://wa.me/" + CONFIG["wa"]
MAPS = CONFIG["maps_url"]
AVIS_URL = CONFIG["avis_url"] or MAPS
BUSINESS_ID = URL + "/#business"


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fmt_int(n):
    return f"{n:,}".replace(",", " ")


def km(a, b):
    dlat = math.radians(b[0] - a[0])
    dlng = math.radians(b[1] - a[1]) * math.cos(math.radians((a[0] + b[0]) / 2))
    return 6371 * math.hypot(dlat, dlng)


def ico(name, cls="ico"):
    return f'<svg class="{cls}"><use href="#{name}"/></svg>'


def wa_link(text):
    from urllib.parse import quote
    return WA + "?text=" + quote(text)


# ---------------------------------------------------------------------------
# Images : optimisation des originaux de _src/images/
# ---------------------------------------------------------------------------
IMG_SRC = os.path.join(SRC, "images")
IMG_OUT = os.path.join(ROOT, "assets", "img")
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".svg")


def find_src(folder, name):
    for ext in EXTS:
        p = os.path.join(IMG_SRC, folder, name + ext)
        if os.path.exists(p):
            return p
    return None


def process_photos():
    """Redimensionne, renforce la netteté et exporte en WebP + JPEG."""
    out = {}
    try:
        from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    except ImportError:
        print("Pillow absent : photos non traitées (pip install pillow)")
        return out
    os.makedirs(os.path.join(IMG_OUT, "photos"), exist_ok=True)
    for key, (name, alt) in PHOTOS.items():
        src = find_src("photos", name)
        if not src or src.endswith(".svg"):
            continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        w, h = im.size
        # vise ~1200 px de large : agrandit les petites images (x3 max), réduit les grandes
        target = 1200 if w < 1200 else min(w, 1600)
        target = min(target, w * 3)
        if target != w:
            im = im.resize((target, round(h * target / w)), Image.LANCZOS)
        if target > w * 1.6:
            im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=2))
        elif target > w:
            im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=2))
        else:
            im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=50, threshold=2))
        im = ImageEnhance.Contrast(im).enhance(1.04)
        im = ImageEnhance.Color(im).enhance(1.05)
        base = os.path.join(IMG_OUT, "photos", name)
        im.save(base + ".webp", "WEBP", quality=84, method=6)
        im.save(base + ".jpg", "JPEG", quality=86, optimize=True, progressive=True)
        out[key] = {"src": f"/assets/img/photos/{name}", "w": im.size[0], "h": im.size[1], "alt": alt}
    return out


def process_logos(folder="assureurs", items=None):
    """Recadre les marges, normalise la hauteur et exporte en WebP + PNG."""
    items = items if items is not None else [(nom, slug) for nom, slug, _, _ in INSURERS]
    out = {}
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return out
    os.makedirs(os.path.join(IMG_OUT, folder), exist_ok=True)
    for nom, slug in items:
        src = find_src(folder, slug)
        if not src:
            continue
        if src.endswith(".svg"):
            shutil.copy(src, os.path.join(IMG_OUT, folder, slug + ".svg"))
            out[slug] = f"/assets/img/{folder}/{slug}.svg"
            continue
        im = Image.open(src).convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        flat = Image.alpha_composite(bg, im).convert("RGB")
        diff = ImageChops.difference(flat, Image.new("RGB", im.size, (255, 255, 255)))
        bbox = diff.point(lambda v: 255 if v > 18 else 0).getbbox()
        if bbox:
            im = im.crop(bbox)
        h = 160
        im = im.resize((max(1, round(im.size[0] * h / im.size[1])), h), Image.LANCZOS)
        base = os.path.join(IMG_OUT, folder, slug)
        im.save(base + ".webp", "WEBP", quality=90, method=6)
        im.save(base + ".png", "PNG", optimize=True)
        out[slug] = f"/assets/img/{folder}/{slug}.webp"
    return out


PHOTO = process_photos()
LOGOS = process_logos()
BRAND_LOGOS = process_logos("marques", [(nom, slug) for nom, slug, _ in BRANDS])


def fig(key, caption=None, eager=False):
    pic = picture(key, "", "(max-width: 1080px) 100vw, 760px", eager)
    if not pic:
        return ""
    cap = f"<figcaption>{E(caption)}</figcaption>" if caption else ""
    return f'<figure class="photo">{pic}{cap}</figure>'


# Photo de remplacement tant qu'une photo n'est pas fournie
PHOTO_FALLBACK = {"serrure-bloquee": "changement-serrure", "porte-rouge": "cle-cassee"}


def picture(key, cls="", sizes="(max-width: 720px) 100vw, 600px", eager=False):
    p = PHOTO.get(key) or PHOTO.get(PHOTO_FALLBACK.get(key))
    if not p:
        return ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source type="image/webp" srcset="{p["src"]}.webp">'
            f'<img src="{p["src"]}.jpg" alt="{E(p["alt"])}" width="{p["w"]}" height="{p["h"]}" {load} decoding="async"></picture>')


# ---------------------------------------------------------------------------
# Zones
# ---------------------------------------------------------------------------
ALIAS = {"Éragny": "Éragny-sur-Oise"}  # nom usuel -> nom officiel INSEE


def build_zones():
    by_name = {}
    for code, c in COMMUNES.items():
        by_name.setdefault((c["nom"], c["dep"]), code)
    zones = []
    zones.append({
        "slug": "paris", "nom": "Paris", "court": "Paris", "dep": "75", "insee": "75056",
        "lat": 48.8566, "lng": 2.3522, "a": "à Paris", "de": "de Paris",
        "cp": ["75001 à 75020"], "pop": COMMUNES["75056"]["pop"], "groupes": [], "arr": None,
    })
    for n, (code, lat, lng, quartiers, lieux) in PARIS_ARR.items():
        c = COMMUNES[code]
        suf = "er" if n == 1 else "e"
        zones.append({
            "slug": f"paris-{n}", "nom": f"Paris {n}{suf} arrondissement", "court": f"Paris {n}{suf}",
            "dep": "75", "insee": code, "lat": lat, "lng": lng,
            "a": f"dans le {n}{suf} arrondissement", "de": f"du {n}{suf} arrondissement",
            "cp": c["cp"], "pop": c["pop"], "groupes": [], "arr": n, "quartiers": quartiers, "lieux": lieux,
        })
    for dep, lst in (("92", HDS), ("95", VDO)):
        for nom, lat, lng in lst:
            code = by_name[(ALIAS.get(nom, nom), dep)]
            c = COMMUNES[code]
            if nom.startswith("Le "):
                a, de = "au " + nom[3:], "du " + nom[3:]
            elif nom.startswith("La "):
                a, de = "à " + nom, "de " + nom
            elif nom.startswith("L'"):
                a, de = "à " + nom, "de " + nom
            else:
                a, de = "à " + nom, ("d'" + nom if nom[0] in "AEIOUÉÈ" else "de " + nom)
            zones.append({
                "slug": slugify(nom), "nom": nom, "court": nom, "dep": dep, "insee": code,
                "lat": lat, "lng": lng, "a": a, "de": de, "cp": c["cp"], "pop": c["pop"],
                "groupes": [g for g in c["groupes"] if g[0] != "METRO"], "arr": None,
            })
    for z in zones:
        others = [o for o in zones if o is not z and o["slug"] != "paris"]
        z["voisins"] = sorted(others, key=lambda o: km((z["lat"], z["lng"]), (o["lat"], o["lng"])))[:8]
        z["url"] = f"/villes/{z['slug']}/"
        z["proche"] = z["dep"] in ("75", "92")
    return zones


ZONES = build_zones()
ZONE_BY_SLUG = {z["slug"]: z for z in ZONES}


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------
STAR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'
GOOGLE = ('<svg viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
          '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
          '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
          '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>')


def btn_call(label=None, cls="btn btn-call", track="call"):
    return f'<a class="{cls}" href="{TEL_HREF}" data-track="{track}">{ico("i-phone")}{E(label or TEL)}</a>'


def btn_wa(text="Bonjour, j'ai besoin d'un serrurier.", label="WhatsApp", cls="btn btn-ghost", track="wa"):
    return f'<a class="{cls}" href="{E(wa_link(text))}" target="_blank" rel="noopener" data-track="{track}">{ico("i-wa")}{E(label)}</a>'


def checks(items):
    return '<div class="checks">' + "".join(f'<span>{ico("i-checkc", "")}{E(i)}</span>' for i in items) + "</div>"


def crumbs(items):
    """items = [(label, url or None)]"""
    parts = ['<a href="/">Accueil</a>']
    for label, url in items:
        parts.append('<span aria-hidden="true">›</span>')
        parts.append(f'<a href="{url}">{E(label)}</a>' if url else f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + "".join(parts) + "</nav>"


def ld_breadcrumb(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": URL + "/"}]
    for i, (label, url) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": label, **({"item": URL + url} if url else {})})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
        for q, a in faq]}


def ld_business(full=True):
    d = {
        "@context": "https://schema.org",
        "@type": "Locksmith",
        "@id": BUSINESS_ID,
        "name": CONFIG["nom"],
        "url": URL + "/",
        "telephone": CONFIG["tel_intl"],
        "email": CONFIG["email"],
        "image": URL + "/assets/img/og.png",
        "logo": URL + "/assets/img/logo.svg",
        "priceRange": "€€",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Carte bancaire, Espèces, Virement",
        "geo": {"@type": "GeoCoordinates", "latitude": CONFIG["lat"], "longitude": CONFIG["lng"]},
        "hasMap": MAPS,
        "sameAs": [MAPS, CONFIG["instagram"], CONFIG["tiktok"]],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"},
        "address": {"@type": "PostalAddress", "addressRegion": "Île-de-France", "addressCountry": "FR"},
    }
    a = CONFIG["adresse"]
    if a["rue"]:
        d["address"].update({"streetAddress": a["rue"], "postalCode": a["cp"], "addressLocality": a["ville"]})
    if full:
        d["areaServed"] = [{"@type": "City", "name": z["nom"]} for z in ZONES if z["slug"] == "paris" or z["dep"] != "75"]
        d["hasOfferCatalog"] = {
            "@type": "OfferCatalog", "name": "Dépannage serrurerie",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"], "url": f"{URL}/depannage/{s['slug']}/"},
                                 **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}} if s["prix_num"] else {})}
                                for s in SERVICES]}
    if AVIS.get("note") and AVIS.get("nombre"):
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": AVIS["note"], "reviewCount": AVIS["nombre"], "bestRating": 5}
    return d


def insurers_block():
    return '''<div class="insurers" id="assurances" aria-label="Assureurs qui reconnaissent nos factures">
  <div class="insurers-head">
    <p>Nos factures sont <span>reconnues et remboursables</span> par les assurances habitation</p>
    <span class="pill">Remboursement selon votre contrat</span>
  </div>
  <div class="marquee" data-row="1"><div class="track"></div></div>
  <div class="marquee reverse" data-row="2"><div class="track"></div></div>
  <p class="insurers-note">Shopta Serrure est une entreprise indépendante, sans partenariat avec ces compagnies. Les noms et logos cités appartiennent à leurs propriétaires respectifs.</p>
</div>'''


def brands_block(soft=False):
    def chip(nom, slug):
        logo = BRAND_LOGOS.get(slug)
        if logo:
            return f'<span class="ins has-logo" title="{E(nom)}"><img src="{logo}" alt="{E(nom)}" loading="lazy" decoding="async"></span>'
        return f'<span class="ins brand-name">{E(nom)}</span>'
    # marques avec logo en premier, puis les autres
    ordered = [b for b in BRANDS if b[1] in BRAND_LOGOS] + [b for b in BRANDS if b[1] not in BRAND_LOGOS]
    half = (len(ordered) + 1) // 2
    rows = ""
    for i, part in enumerate((ordered[:half], ordered[half:])):
        items = "".join(chip(n, s) for n, s, _ in part)
        rows += (f'<div class="marquee{" reverse" if i else ""}"><div class="track">{items}'
                 f'<span class="dup" aria-hidden="true">{items}</span></div></div>')
    noms = ", ".join(n for n, _, _ in BRANDS)
    return f'''<div class="insurers brands{" soft" if soft else ""}" aria-label="Marques de serrures et de portes">
  <div class="insurers-head">
    <p>Nous intervenons sur <span>toutes les grandes marques</span></p>
    <span class="pill">Serrures · cylindres · portes blindées · serrures connectées</span>
  </div>
  {rows}
  <p class="insurers-note">Marques prises en charge : {E(noms)}. Les marques citées appartiennent à leurs propriétaires ; Shopta Serrure est indépendant.</p>
</div>'''


def map_iframe():
    from urllib.parse import quote
    q = quote(f"Serrurier - Shopta serrure @{CONFIG['lat']},{CONFIG['lng']}")
    return (f'<div class="map-frame"><iframe title="Shopta Serrure sur Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://maps.google.com/maps?q={q}&amp;z=15&amp;hl=fr&amp;output=embed"></iframe></div>')


def reviews_section(title="Ce que disent nos clients", soft=False):
    if AVIS.get("note"):
        score = (f'<div class="score"><b>{str(AVIS["note"]).replace(".", ",")}</b><div><span class="stars">{STAR * 5}</span>'
                 f'<p>{E(str(AVIS.get("nombre", "")))} avis Google</p></div></div>')
    else:
        score = f'<div class="score"><span class="stars">{STAR * 5}</span></div>'
    cards = ""
    if AVIS.get("avis"):
        items = "".join(
            f'<article class="review"><header><span class="av">{E(r["auteur"][:1].upper())}</span><div><strong>{E(r["auteur"])}</strong>'
            f'<small>{E(r.get("date", ""))}</small></div><span class="g-mini">{GOOGLE}</span></header>'
            f'<span class="stars" aria-label="{int(r.get("note", 5))} sur 5">{STAR * int(r.get("note", 5))}</span>'
            f'<p>{E(r["texte"])}</p></article>' for r in AVIS["avis"])
        cards = f'''<div class="carousel reveal" data-carousel>
      <button class="car-btn prev" type="button" aria-label="Avis précédent">{ico("i-arrow")}</button>
      <div class="car-track" tabindex="0" aria-label="Avis clients Google">{items}</div>
      <button class="car-btn next" type="button" aria-label="Avis suivant">{ico("i-arrow")}</button>
    </div>'''
    return f'''<section id="avis" class="{'soft' if soft else ''}" aria-labelledby="avis-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Avis clients</span>
      <h2 id="avis-title">{E(title)}</h2>
      <p>Nos avis sont publiés par nos clients sur notre fiche Google : ils sont publics et vérifiables.</p>
    </div>
    <div class="reviews-wrap">
      <div class="rating-card reveal">
        <div class="g">{GOOGLE}<span>Avis Google<br><small style="font-weight:500;color:var(--muted);font-size:14px">Serrurier - Shopta serrure</small></span></div>
        {score}
        <p>Vous avez fait appel à nous ? Votre avis aide d'autres personnes à trouver un serrurier honnête.</p>
        <a class="btn btn-blue" href="{E(MAPS)}" target="_blank" rel="noopener">Voir tous nos avis sur Google</a>
        <a class="btn btn-wa" style="border-color:var(--line)" href="{E(AVIS_URL)}" target="_blank" rel="noopener">{ico("i-award")}Laisser un avis</a>
      </div>
      {map_iframe()}
    </div>
    {cards}
  </div>
</section>'''


FORM_COUNT = [0]


def contact_form(source, service=None, titre="Demande de devis gratuit", sous_titre="Nous vous rappelons rapidement, 7j/7.", ville=""):
    """Formulaire Netlify Forms (nom « contact »), identique sur toutes les pages."""
    FORM_COUNT[0] += 1
    n = FORM_COUNT[0]
    opts = "".join(f'<option{" selected" if service and s["court"] == service else ""}>{E(s["court"])}</option>' for s in SERVICES)
    return f'''<form class="card lead-form" name="contact" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="contact">
  <input type="hidden" name="page" value="{E(source)}">
  <p hidden><label>Ne pas remplir <input name="bot-field"></label></p>
  <h3>{E(titre)}</h3>
  <p>{E(sous_titre)}</p>
  <div class="row2">
    <div class="field"><label for="nom-{n}">Nom *</label><input id="nom-{n}" name="nom" autocomplete="name" required placeholder="Jean Dupont"></div>
    <div class="field"><label for="tel-{n}">Téléphone *</label><input id="tel-{n}" name="telephone" type="tel" inputmode="tel" autocomplete="tel" required pattern="[0-9+ .()-]{{10,}}" placeholder="06 00 00 00 00"></div>
  </div>
  <div class="row2">
    <div class="field"><label for="svc-{n}">Besoin</label><select id="svc-{n}" name="service">{opts}<option{" selected" if not service else ""}>Autre / je ne sais pas</option></select></div>
    <div class="field"><label for="ville-{n}">Ville / arrondissement</label><input id="ville-{n}" name="ville" autocomplete="address-level2" value="{E(ville)}" placeholder="Paris 15e"></div>
  </div>
  <div class="field"><label for="mail-{n}">E-mail (facultatif)</label><input id="mail-{n}" name="email" type="email" autocomplete="email" placeholder="vous@exemple.fr"></div>
  <div class="field"><label for="msg-{n}">Votre message</label><textarea id="msg-{n}" name="message" rows="3" placeholder="Type de porte, serrure, situation…"></textarea></div>
  <button class="btn btn-blue btn-lg" type="submit">{ico("i-mail")}Envoyer ma demande</button>
  <p class="legal">Urgence ? Appelez directement le <a href="{TEL_HREF}">{TEL}</a>. Vos données servent uniquement à traiter votre demande (<a href="/politique-confidentialite/">confidentialité</a>).</p>
  <div class="form-ok" role="status" hidden>{ico("i-checkc", "")}<div><strong>Demande envoyée !</strong><span>Nous vous rappelons très vite. Pour une urgence, appelez le {TEL}.</span></div></div>
</form>'''


def cta_final(titre="Bloqué dehors ? On arrive.", texte="Un serrurier qualifié chez vous rapidement, prix annoncé avant de partir.",
              source="/", service=None, ville=""):
    form_titre = f"Devis gratuit : {service.lower()}" if service else "Demande de devis ou de rappel"
    return f'''<section class="final" id="devis" aria-label="Contact" style="padding-top:96px">
  <div class="container">
    <div class="box final-grid reveal">
      <div class="final-text">
        <h2>{E(titre).replace(" ?", "&nbsp;?")}</h2>
        <p>{E(texte)}</p>
        <div class="ctas">{btn_call(cls="btn btn-call btn-lg pulse", track="call_final")}{btn_wa(cls="btn btn-ghost btn-lg", track="wa_final")}</div>
        <ul class="final-list">
          <li>{ico("i-check", "")}Prix annoncé avant le déplacement</li>
          <li>{ico("i-check", "")}Devis gratuit, signé avant travaux</li>
          <li>{ico("i-check", "")}Facture remboursable par votre assurance</li>
        </ul>
      </div>
      {contact_form(source, service, form_titre, ville=ville)}
    </div>
  </div>
</section>'''


def aside_card(titre="Besoin d'un serrurier ?", texte="Prix annoncé au téléphone, devis signé avant travaux."):
    return f'''<aside class="aside-card">
  <div class="avail" style="display:flex;gap:8px;align-items:center;color:var(--green-600);font-weight:600;font-size:14px;margin-bottom:6px"><span class="dot"></span>Disponible 24h/24</div>
  <h3>{E(titre)}</h3>
  <p>{E(texte)}</p>
  {btn_call(cls="btn btn-call", track="call_aside")}
  {btn_wa(cls="btn btn-wa", label="Envoyer une photo", track="wa_aside")}
  <a class="btn btn-wa" href="#devis">{ico("i-mail")}Demander un devis écrit</a>
  <ul>
    <li>{ico("i-check", "")}Devis gratuit et sans engagement</li>
    <li>{ico("i-check", "")}Ouverture sans dégât dans la majorité des cas</li>
    <li>{ico("i-check", "")}Facture remboursable par votre assurance</li>
    <li>{ico("i-check", "")}Paiement CB, espèces, virement</li>
  </ul>
</aside>'''


def price_table():
    rows = "".join(f'<tr><td><a href="/depannage/{s["slug"]}/">{E(s["nom"])}</a></td><td>{E(s["prix"].replace(" TTC", ""))}</td></tr>' for s in SERVICES)
    return f'''<div class="price-table">
  <header><h3>Nos tarifs de dépannage</h3><p>Prix de départ TTC, main d'œuvre incluse</p></header>
  <table>{rows}<tr><td>Devis</td><td style="color:var(--green-600)">Gratuit</td></tr></table>
  <div class="note">{ico("i-info", "")}Le prix final dépend du type de porte et de serrure. Il vous est toujours confirmé par écrit avant le début des travaux.</div>
</div>'''


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq)) + "</div>"


# ---------------------------------------------------------------------------
# Gabarit
# ---------------------------------------------------------------------------
NAV = [("Dépannage", "/depannage/"), ("Tarifs", "/tarifs/"), ("Zones", "/villes/"), ("Avis", "/avis/"), ("Blog", "/blog/"), ("Contact", "/contact/")]


def footer():
    svc = "".join(f'<li><a href="/depannage/{s["slug"]}/">{E(s["court"])}</a></li>' for s in SERVICES)
    top = ["paris", "clichy", "asnieres-sur-seine", "levallois-perret", "neuilly-sur-seine", "boulogne-billancourt", "nanterre", "argenteuil", "cergy"]
    zl = "".join(f'<li><a href="{ZONE_BY_SLUG[s]["url"]}">Serrurier {E(ZONE_BY_SLUG[s]["court"])}</a></li>' for s in top)
    arr = " · ".join(f'<a href="/villes/paris-{n}/">Paris {n}</a>' for n in range(1, 21))
    return f'''<footer>
  <div class="container">
    <div class="foot-grid">
      <div>
        <a href="/" class="logo"><svg><use href="#i-logo"/></svg><span>Shopta<b>Serrure</b><small>Serrurier d'urgence</small></span></a>
        <p>Serrurier d'urgence à Paris et en Île-de-France. Intervention rapide 24h/24 et 7j/7, prix annoncés avant déplacement, factures reconnues par les assurances.</p>
        <p style="margin-top:14px"><a href="{TEL_HREF}" style="color:#fff;font-family:var(--head);font-weight:700;font-size:20px">{TEL}</a><br><a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></p>
        <p style="margin-top:14px"><a class="social" href="{CONFIG['instagram']}" target="_blank" rel="noopener me" aria-label="Instagram Shopta Serrure">{ico("i-insta", "")}@shoptaserrure</a>
        <a class="social" href="{CONFIG['tiktok']}" target="_blank" rel="noopener me" aria-label="TikTok Shopta Serrure">{ico("i-tiktok", "")}@shopta.serrure</a></p>
      </div>
      <div><h4>Dépannages</h4><ul>{svc}</ul></div>
      <div><h4>Zones</h4><ul>{zl}<li><a href="/villes/">Toutes nos zones →</a></li></ul></div>
      <div><h4>Informations</h4><ul><li><a href="/tarifs/">Tarifs</a></li><li><a href="/assurances/">Assurances</a></li><li><a href="/avis/">Avis clients</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li><li><a href="{E(MAPS)}" target="_blank" rel="noopener">Notre fiche Google</a></li></ul></div>
    </div>
    <p style="font-size:13px;line-height:2;margin-bottom:28px">Serrurier par arrondissement : {arr}</p>
    <div class="foot-bottom">
      <span>© <span id="year">{TODAY[:4]}</span> Shopta Serrure. Tous droits réservés.</span>
      <nav><a href="/mentions-legales/">Mentions légales</a><a href="/politique-confidentialite/">Confidentialité</a><a href="/plan-du-site/">Plan du site</a></nav>
    </div>
  </div>
</footer>'''


def page(path, title, desc, body, ld=(), active=None, robots="index, follow", og_type="website"):
    canonical = URL + path
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == active else ""}>{E(l)}</a>' for l, u in NAV)
    mnav = "".join(f'<a href="{u}">{E(l)}</a>' for l, u in [("Accueil", "/")] + NAV)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in ld)
    ga = CONFIG["ga_id"]
    doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#003380">
<meta name="geo.region" content="FR-IDF">
<meta name="geo.position" content="{CONFIG['lat']};{CONFIG['lng']}">
<meta name="ICBM" content="{CONFIG['lat']}, {CONFIG['lng']}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Shopta Serrure">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{URL}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{ga}');</script>
{ld_html}</head>
<body>
{SPRITE}
<div class="topbar">
  <div class="container">
    <div class="live"><span class="dot"></span> Serruriers disponibles maintenant<span class="full">&nbsp;— Paris & Île-de-France</span></div>
    <div class="items">
      <span>{ico("i-clock", "")}24h/24 · 7j/7 · jours fériés</span>
      <span>{ico("i-shield", "")}Facture remboursable par votre assurance</span>
      <span>{ico("i-euro", "")}Prix annoncé avant déplacement</span>
    </div>
  </div>
</div>
<header class="site" id="top">
  <div class="container">
    <a href="/" class="logo" aria-label="Shopta Serrure – accueil"><svg><use href="#i-logo"/></svg><span>Shopta<b>Serrure</b><small>Serrurier d'urgence</small></span></a>
    <nav class="main" aria-label="Navigation principale">{nav}</nav>
    <div class="head-cta">
      <div class="head-phone"><small>Urgence 24h/24</small><strong>{TEL}</strong></div>
      <a class="btn btn-call" href="{TEL_HREF}" data-track="call_header">{ico("i-phone")}<span>Appeler</span></a>
      <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
    </div>
  </div>
</header>
<nav class="mobile-nav" id="mnav" aria-label="Navigation mobile">{mnav}</nav>
<main>
{body}
</main>
{footer()}
<div class="callbar">
  <a class="btn btn-call pulse" href="{TEL_HREF}" data-track="call_sticky">{ico("i-phone")}Appeler · 24h/24</a>
  <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp" data-track="wa_sticky"><svg class="ico" style="width:26px;height:26px"><use href="#i-wa"/></svg></a>
</div>
<script src="/assets/js/assureurs.js" defer></script>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    if robots.startswith("index"):
        SITEMAP.append(path)
        imgs = list(dict.fromkeys(re.findall(r'<img src="(/assets/img/photos/[^"]+)"', body)))
        if imgs:
            SITEMAP_IMAGES[path] = imgs


SITEMAP = []
SITEMAP_IMAGES = {}


def page_hero(crumb_items, h1, lead, extra=""):
    return f'''<section class="page-hero">
  <div class="container">
    {crumbs(crumb_items)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="ctas">{btn_call(cls="btn btn-call btn-lg pulse", track="call_hero")}{btn_wa(cls="btn btn-ghost btn-lg", track="wa_hero")}</div>
    {extra}
  </div>
</section>'''


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def svc_cards(zone=None):
    out = []
    for i, s in enumerate(SERVICES):
        hl = " highlight" if i == 0 else ""
        tag = '<span class="tag">Le plus demandé</span>' if i == 0 else ""
        ph = picture(s["slug"], "svc-photo", "(max-width: 720px) 100vw, 380px")
        out.append(f'''<a class="service{hl}{" has-photo" if ph else ""} reveal" href="/depannage/{s["slug"]}/">
  {ph}{tag}<div class="ic">{ico(s["icon"], "")}</div>
  <h3>{E(s["court"])}</h3>
  <p>{E(s["resume"])}</p>
  <div class="foot"><div class="price">{"à partir de" if s["prix_num"] else "sur devis"}<b>{"%d € TTC" % s["prix_num"] if s["prix_num"] else "Gratuit"}</b></div><span class="go">{ico("i-arrow")}</span></div>
</a>''')
    return '<div class="services-grid">' + "".join(out) + "</div>"


def zones_tabs():
    tabs, panels = [], []
    for i, (dep, (_, label)) in enumerate(DEPTS.items()):
        tabs.append(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" data-zone="z{dep}">{E(label)}</button>')
        links = "".join(f'<a href="{z["url"]}">Serrurier {E(z["court"])}</a>' for z in ZONES if z["dep"] == dep)
        panels.append(f'<div class="zone-panel{" active" if i == 0 else ""}" id="z{dep}" role="tabpanel">{links}</div>')
    return '<div class="zones-tabs" role="tablist">' + "".join(tabs) + "</div>" + "".join(panels)


HOME_FAQ = [
    ("Combien coûte une ouverture de porte claquée ?", "L'ouverture d'une porte claquée commence à 49 € TTC. Le prix exact vous est annoncé au téléphone avant le déplacement, puis confirmé par un devis écrit sur place avant toute intervention."),
    ("Mon assurance peut-elle rembourser l'intervention ?", "Oui, dans de nombreux cas (effraction, perte ou vol de clés selon votre contrat). Nous vous remettons une facture détaillée et conforme, reconnue par les assureurs habitation en France. Vérifiez les garanties de votre contrat multirisque habitation."),
    ("En combien de temps intervenez-vous ?", "En moyenne en moins de 30 minutes dans Paris et la proche banlieue, 24h/24 et 7j/7, jours fériés compris. Le délai précis vous est annoncé au téléphone."),
    ("Le devis est-il vraiment gratuit ?", "Oui. Le devis est gratuit et sans engagement. Si vous le refusez, vous ne payez rien d'autre que ce qui vous a été annoncé au téléphone."),
    ("Allez-vous casser ma serrure ?", "Non, sauf cas exceptionnel. Nous privilégions toujours l'ouverture fine (crochetage, radio, by-pass). Si un remplacement est nécessaire, il vous est expliqué et chiffré avant."),
    ("Quels moyens de paiement acceptez-vous ?", "Carte bancaire, espèces et virement. Une facture détaillée vous est systématiquement remise."),
]


def about_block():
    pic = picture("serrure-connectee", "", "(max-width: 1080px) 100vw, 520px")
    if not pic:
        return ""
    return f'''<section aria-labelledby="about-title">
  <div class="container about">
    <div class="about-photo reveal">{pic}<div class="about-badge"><strong>Devis signé</strong><span>avant chaque intervention</span></div></div>
    <div class="reveal">
      <span class="eyebrow">Notre façon de travailler</span>
      <h2 id="about-title" style="font-size:clamp(28px,3.6vw,40px);margin-bottom:16px">Un serrurier qui explique avant d'intervenir</h2>
      <p style="color:var(--muted);font-size:18px;margin-bottom:22px">Avant de toucher à votre porte, notre serrurier vous explique ce qu'il va faire, pourquoi, et combien cela coûte. Vous signez le devis, puis il intervient. Pas de jargon, pas de surprise.</p>
      <ul class="commit-list" style="margin-top:0">
        <li><span class="ck">{ico("i-check")}</span><div><strong>Diagnostic expliqué</strong><span>On vous montre la panne et les solutions possibles.</span></div></li>
        <li><span class="ck">{ico("i-check")}</span><div><strong>Le choix vous appartient</strong><span>Plusieurs gammes proposées, du standard à l'A2P.</span></div></li>
        <li><span class="ck">{ico("i-check")}</span><div><strong>Conseils pour la suite</strong><span>Entretien, sécurité, démarches avec votre assurance.</span></div></li>
      </ul>
    </div>
  </div>
</section>'''


def build_home():
    blog = "".join(f'''<article class="post reveal">
  {cover(a)}
  <div class="body"><div class="meta"><b>{E(a["cat"])}</b><time datetime="{a["date"]}">{fr_date(a["date"])}</time></div>
  <h3><a href="/blog/{a["slug"]}/">{E(a["court"])}</a></h3><p>{E(a["desc"])}</p><a class="more" href="/blog/{a["slug"]}/">Lire l'article →</a></div>
</article>''' for a in ARTICLES[:4])
    body = f'''<section class="hero" aria-labelledby="hero-title">
  <div class="container">
    <div>
      <span class="badge"><span class="dot"></span> Un serrurier près de chez vous en ce moment</span>
      <h1 id="hero-title">Serrurier d'urgence à Paris, <em>chez vous en 30&nbsp;minutes</em></h1>
      <p class="lead">Porte claquée, serrure bloquée, clé cassée ou effraction : un serrurier qualifié intervient 24h/24 dans tout Paris et l'Île-de-France. Prix annoncé au téléphone, devis signé avant travaux, facture remboursable par votre assurance.</p>
      <div class="ctas">{btn_call(cls="btn btn-call btn-lg pulse", track="call_hero")}{btn_wa(cls="btn btn-ghost btn-lg", track="wa_hero")}</div>
      {checks(["Devis gratuit", "Aucun frais caché", "Matériel certifié A2P", "Paiement CB accepté"])}
    </div>
    <aside class="hero-card reveal" aria-label="Ouverture de porte">
      <div class="avail"><span class="dot"></span> Disponible maintenant</div>
      <h2>Porte claquée ?</h2>
      <p class="sub">Ouverture sans dégât dans la majorité des cas.</p>
      <div class="price-row"><span class="from">à partir de</span><span class="amount">49&nbsp;€</span><span class="ttc">TTC</span></div>
      <div class="mini-steps">
        <div><b>1</b>Vous appelez : on vous annonce le prix tout de suite</div>
        <div><b>2</b>Un serrurier arrive en ~30 min</div>
        <div><b>3</b>Devis signé, intervention, facture pour l'assurance</div>
      </div>
      {btn_call("Appeler un serrurier", cls="btn btn-call", track="call_card")}
      <a class="btn btn-wa" href="{E(wa_link("Bonjour, ma porte est claquée."))}" target="_blank" rel="noopener" data-track="wa_card"><svg class="ico" style="color:#25d366"><use href="#i-wa"/></svg>Envoyer une photo sur WhatsApp</a>
    </aside>
  </div>
</section>
<div class="stats">
  <div class="container">
    <div class="stats-grid">
      <div class="stat"><div class="ic">{ico("i-clock", "")}</div><div><strong>30 min</strong><span>Délai moyen d'arrivée</span></div></div>
      <div class="stat"><div class="ic">{ico("i-euro", "")}</div><div><strong>à partir de 49 €</strong><span>TTC, prix annoncé</span></div></div>
      <div class="stat"><div class="ic">{ico("i-shield", "")}</div><div><strong>24h/24</strong><span>7j/7, jours fériés</span></div></div>
      <div class="stat"><div class="ic">{ico("i-award", "")}</div><div><strong>Garantie</strong><span>Pièces & main d'œuvre</span></div></div>
    </div>
  </div>
</div>
{insurers_block()}
<section id="services" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Nos dépannages</span>
      <h2 id="services-title">Une solution pour chaque urgence</h2>
      <p>Nos serruriers interviennent sur tous types de portes et de serrures : appartement, maison, local commercial, porte blindée ou cave.</p>
    </div>
    {svc_cards()}
  </div>
</section>
{brands_block()}
<section class="soft" aria-labelledby="steps-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Comment ça marche</span>
      <h2 id="steps-title">Simple, rapide, sans mauvaise surprise</h2>
      <p>Vous savez exactement ce que vous allez payer avant que le serrurier ne se déplace.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="n">1</div><h3>Vous appelez</h3><p>Décrivez votre situation au téléphone ou envoyez une photo sur WhatsApp.</p></div>
      <div class="step reveal"><div class="n">2</div><h3>Prix annoncé</h3><p>On vous donne immédiatement une estimation claire du tarif, TTC.</p></div>
      <div class="step reveal"><div class="n">3</div><h3>Devis sur place</h3><p>Le serrurier confirme le prix par écrit. Rien n'est fait sans votre accord.</p></div>
      <div class="step reveal"><div class="n">4</div><h3>Intervention & facture</h3><p>Travail soigné, facture détaillée à transmettre à votre assureur.</p></div>
    </div>
  </div>
</section>
<section id="tarifs" aria-labelledby="tarifs-title">
  <div class="container commit">
    <div class="reveal">
      <span class="eyebrow">Tarifs transparents</span>
      <div class="section-head" style="margin-bottom:0">
        <h2 id="tarifs-title">Des prix justes, annoncés avant de venir</h2>
        <p>Une urgence ne doit jamais être synonyme d'arnaque. Nous nous engageons sur une politique de prix claire.</p>
      </div>
      <ul class="commit-list">
        <li><span class="ck">{ico("i-check")}</span><div><strong>Devis gratuit et détaillé</strong><span>Signé avant chaque intervention, conformément à la réglementation.</span></div></li>
        <li><span class="ck">{ico("i-check")}</span><div><strong>Déplacement offert</strong><span>En cas de travaux réalisés.</span></div></li>
        <li><span class="ck">{ico("i-check")}</span><div><strong>Facture conforme pour votre assurance</strong><span>Reconnue par les assureurs habitation, remboursable selon votre contrat.</span></div></li>
        <li><span class="ck">{ico("i-check")}</span><div><strong>Matériel certifié et garanti</strong><span>Serrures et cylindres de marques reconnues, normes A2P.</span></div></li>
      </ul>
    </div>
    <div class="reveal">{price_table()}</div>
  </div>
</section>
{reviews_section(soft=True)}
{about_block()}
<section class="soft" aria-labelledby="why-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Pourquoi nous choisir</span>
      <h2 id="why-title">Une entreprise locale, des artisans de confiance</h2>
    </div>
    <div class="why-grid">
      <div class="why reveal"><div class="ic">{ico("i-clock", "")}</div><h3>Intervention rapide</h3><p>Nos serruriers sont répartis dans Paris et la banlieue pour arriver chez vous en moins de 30 minutes en moyenne.</p></div>
      <div class="why reveal"><div class="ic">{ico("i-euro", "")}</div><h3>Transparence totale</h3><p>Aucun frais caché. Tarif annoncé au téléphone et validé par un devis avant l'intervention.</p></div>
      <div class="why reveal"><div class="ic">{ico("i-award", "")}</div><h3>Serruriers qualifiés</h3><p>Des professionnels formés aux techniques d'ouverture fine pour préserver votre porte et votre serrure.</p></div>
      <div class="why reveal"><div class="ic">{ico("i-shield", "")}</div><h3>Travail garanti</h3><p>Pièces certifiées et main d'œuvre garanties. Nous revenons gratuitement en cas de souci.</p></div>
      <div class="why reveal"><div class="ic">{ico("i-door", "")}</div><h3>Ouverture sans dégât</h3><p>Dans la majorité des cas, nous ouvrons votre porte sans casser ni remplacer la serrure.</p></div>
      <div class="why reveal"><div class="ic">{ico("i-phone", "")}</div><h3>Joignable à toute heure</h3><p>Nuit, week-end, jours fériés : un interlocuteur vous répond directement, sans plateforme.</p></div>
    </div>
  </div>
</section>
<section id="zones" aria-labelledby="zones-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Zones d'intervention</span>
      <h2 id="zones-title">Paris et l'Île-de-France</h2>
      <p>Nous intervenons dans les 20 arrondissements de Paris, tout le département des Hauts-de-Seine et une large partie du Val-d'Oise.</p>
    </div>
    {zones_tabs()}
    <p class="zones-note">Votre ville n'est pas listée ? Appelez-nous : hors zone, des frais de déplacement supplémentaires peuvent s'appliquer et vous sont annoncés à l'avance.</p>
  </div>
</section>
<section id="faq" class="soft" aria-labelledby="faq-title">
  <div class="container faq-wrap">
    <div class="section-head reveal" style="margin-bottom:0">
      <span class="eyebrow">Questions fréquentes</span>
      <h2 id="faq-title">Vous avez des questions ?</h2>
      <p>Les réponses aux questions que l'on nous pose le plus souvent. Pour le reste, on est joignable 24h/24.</p>
      <a class="btn btn-blue" style="margin-top:24px" href="/faq/">Toutes les questions</a>
    </div>
    <div class="reveal">{faq_html(HOME_FAQ)}</div>
  </div>
</section>
<section id="blog" aria-labelledby="blog-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Le Mag Sécurité</span>
      <h2 id="blog-title">Conseils & astuces pour protéger votre foyer</h2>
      <p>Guides pratiques rédigés par nos serruriers. <a href="/blog/" style="color:var(--blue);font-weight:600">Tous les articles →</a></p>
    </div>
    <div class="blog-grid">{blog}</div>
  </div>
</section>
{cta_final(source="/")}'''
    ld = [ld_business(), ld_faq(HOME_FAQ),
          {"@context": "https://schema.org", "@type": "WebSite", "name": "Shopta Serrure", "url": URL + "/", "inLanguage": "fr-FR",
           "publisher": {"@id": BUSINESS_ID}}]
    page("/", "Serrurier Paris 24h/24 – Intervention 30 min, à partir de 49 € | Shopta Serrure",
         "Serrurier d'urgence à Paris et en Île-de-France 24h/24 et 7j/7. Ouverture de porte à partir de 49 € TTC, prix annoncé avant déplacement, devis gratuit, facture remboursable par votre assurance.",
         body, ld)


def cover(a):
    pic = picture(ARTICLE_PHOTOS.get(a["slug"]), "", "(max-width: 720px) 100vw, 300px")
    if pic:
        return f'<div class="cover photo-cover">{pic}</div>'
    return f'<div class="cover" style="background:linear-gradient(140deg,{a["grad"]})">{ico(a["icon"], "")}</div>'


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def build_services():
    # Hub
    items = "".join(f'''<div class="svc-item reveal"><div class="ic">{ico(s["icon"], "")}</div>
  <div><h3><a href="/depannage/{s["slug"]}/">{E(s["nom"])}</a></h3><p>{E(s["resume"])}</p></div>
  <div class="pr">{E(s["prix"])}<a href="/depannage/{s["slug"]}/">En savoir plus →</a></div></div>''' for s in SERVICES)
    body = page_hero([("Dépannage", None)], "Dépannage serrurerie <em>24h/24</em> à Paris et en Île-de-France",
                     "Ouverture de porte, déblocage, clé cassée, changement de serrure, serrure connectée, sécurisation après effraction : toutes nos interventions, avec leurs prix de départ.")
    body += f'<section><div class="container layout"><div class="svc-list">{items}</div>{aside_card()}</div></section>'
    body += brands_block() + insurers_block() + cta_final(source="/depannage/")
    page("/depannage/", "Dépannage serrurerie 24h/24 Paris & IDF – Tous nos services | Shopta Serrure",
         "Tous nos dépannages de serrurerie à Paris et en Île-de-France : ouverture de porte à partir de 49 €, serrure bloquée, clé cassée, changement de serrure, après effraction.",
         body, [ld_business(False), ld_breadcrumb([("Dépannage", "/depannage/")])], active="/depannage/")

    for s in SERVICES:
        path = f"/depannage/{s['slug']}/"
        secs = "".join(f"<h2>{E(t)}</h2><p>{c}</p>" for t, c in s["sections"])
        arr_links = "".join(f'<a href="/villes/paris-{n}/">{E(s["court"])} Paris {n}</a>' for n in range(1, 21))
        near = [z for z in ZONES if z["dep"] in ("92",)][:36]
        hds_links = "".join(f'<a href="{z["url"]}">{E(z["court"])}</a>' for z in near)
        vdo_links = "".join(f'<a href="{z["url"]}">{E(z["court"])}</a>' for z in ZONES if z["dep"] == "95")
        others = "".join(f'<a href="/depannage/{o["slug"]}/">{E(o["court"])}</a>' for o in SERVICES if o is not s)
        prix_txt = f"à partir de <strong>{s['prix_num']} € TTC</strong>" if s["prix_num"] else "<strong>sur devis gratuit</strong>"
        content = f'''<div class="prose">
  <p>{s["intro"]}</p>
  {fig(s["slug"])}
  <p class="callout">Tarif : {prix_txt}. Le prix exact vous est annoncé au téléphone avant le déplacement et confirmé par un devis écrit avant toute intervention.</p>
  {secs}
  <h2>{E(s["court"])} : où intervenons-nous ?</h2>
  <p>Nous intervenons pour ce service dans tout Paris, les Hauts-de-Seine et une grande partie du Val-d'Oise, 24h/24 et 7j/7.</p>
  <h3>Paris</h3><div class="link-grid">{arr_links}</div>
  <h3>Hauts-de-Seine (92)</h3><div class="link-grid">{hds_links}</div>
  <h3>Val-d'Oise (95)</h3><div class="link-grid">{vdo_links}</div>
  <h2>Questions fréquentes</h2>
  {faq_html(s["faq"])}
  <h2>Nos autres dépannages</h2><div class="link-grid">{others}</div>
</div>'''
        body = page_hero([("Dépannage", "/depannage/"), (s["court"], None)], f'{E(s["nom"])} <em>à Paris & Île-de-France</em>',
                         f'{E(s["resume"])} Intervention 24h/24, {"à partir de %d € TTC" % s["prix_num"] if s["prix_num"] else "devis gratuit"}.',
                         checks(["Prix annoncé avant déplacement", "Devis signé avant travaux", "Facture remboursable par l'assurance"]))
        body += f'<section><div class="container layout">{content}{aside_card()}</div></section>'
        body += brands_block() + insurers_block() + reviews_section(soft=True) + cta_final(
            f"{s['court']} ? On s'en occupe.", "Appelez-nous ou laissez vos coordonnées : nous vous rappelons avec un prix clair.",
            source=path, service=s["court"])
        title = f'{s["nom"]} Paris 24h/24 – {s["prix"].replace(" TTC", "").replace("sur devis gratuit", "Devis gratuit")} | Shopta Serrure'
        desc = f'{s["nom"]} à Paris et en Île-de-France, 24h/24 et 7j/7. {s["resume"]} Prix annoncé avant déplacement.'
        ld = [ld_business(False), ld_breadcrumb([("Dépannage", "/depannage/"), (s["court"], path)]), ld_faq(s["faq"]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["nom"], "serviceType": s["nom"], "url": URL + path,
               "provider": {"@id": BUSINESS_ID}, "areaServed": [{"@type": "City", "name": "Paris"}, {"@type": "AdministrativeArea", "name": "Hauts-de-Seine"}, {"@type": "AdministrativeArea", "name": "Val-d'Oise"}],
               **({"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}}} if s["prix_num"] else {})}]
        page(path, title, desc, body, ld, active="/depannage/")


# --- Pages villes -----------------------------------------------------------
INTROS_PARIS = [
    "Vous êtes bloqué devant votre porte {a} ? Shopta Serrure envoie un serrurier qualifié 24h/24, en moyenne en moins de 30 minutes, dans les quartiers {quartiers}. Le prix vous est annoncé au téléphone avant le départ du technicien.",
    "Porte claquée près de {lieux}, serrure bloquée ou clé cassée : nos serruriers interviennent {a} jour et nuit, week-ends et jours fériés compris, avec un devis signé avant toute intervention.",
    "Dans un arrondissement de {pop} habitants comme le {n}{suf}, les urgences de serrurerie sont quotidiennes. Nos serruriers connaissent les immeubles du secteur ({quartiers}) et les serrures qui les équipent.",
    "Besoin d'un serrurier {a} ? De {lieux} aux rues résidentielles des quartiers {quartiers}, nous intervenons rapidement avec un tarif annoncé à l'avance et une facture reconnue par votre assurance.",
]
INTROS_VILLE = [
    "Vous cherchez un serrurier {a} ({cp}) ? Shopta Serrure intervient 24h/24 et 7j/7 pour l'ouverture de porte, le déblocage de serrure ou le remplacement de cylindre, avec un prix annoncé avant le déplacement.",
    "Porte claquée, clé cassée ou serrure forcée {a} : un serrurier qualifié se déplace jour et nuit dans toute la commune et dans les villes voisines comme {voisins}. Devis signé avant toute intervention.",
    "{nom} compte {pop} habitants : appartements, pavillons, commerces… Nos serruriers interviennent sur tous types de portes {a}, de la serrure standard à la porte blindée multipoints.",
    "Bloqué dehors {a} ? Appelez-nous : nous vous annonçons le prix au téléphone, un serrurier part immédiatement et ouvre votre porte sans dégât dans la grande majorité des cas.",
]


def city_photo(idx):
    keys = [k for k in PHOTOS if k in PHOTO]
    return keys[idx % len(keys)] if keys else None


def zone_faq(z):
    delai = ("Nous visons une arrivée en moins de 30 minutes en moyenne {a}. Le délai précis dépend de la circulation et de la disponibilité de nos serruriers : il vous est annoncé au téléphone avant le départ."
             if z["proche"] else
             "Le délai dépend de la distance et de la circulation : il vous est annoncé au téléphone, avant le départ du serrurier, pour que vous sachiez exactement quand il arrivera {a}.")
    return [
        (f"Combien coûte un serrurier {z['a']} ?", f"L'ouverture d'une porte claquée {z['a']} commence à 49 € TTC. Le changement de cylindre ou de serrure se fait sur devis gratuit. Le prix est toujours annoncé avant le déplacement et confirmé par écrit avant les travaux."),
        (f"En combien de temps un serrurier peut-il arriver {z['a']} ?", delai.format(a=z["a"])),
        (f"Intervenez-vous la nuit et le week-end {z['a']} ?", "Oui, nous intervenons 24h/24 et 7j/7, y compris les dimanches et jours fériés. Le tarif vous est annoncé à l'avance, sans surprise."),
        ("Ma facture sera-t-elle remboursée par mon assurance ?", "Nos factures sont détaillées et conformes : elles sont reconnues par les assureurs habitation. Le remboursement dépend des garanties de votre contrat (effraction, vol ou perte de clés…)."),
    ]


def build_zones_pages():
    # Hub
    blocks = ""
    for dep, (nom, label) in DEPTS.items():
        lst = [z for z in ZONES if z["dep"] == dep]
        links = "".join(f'<a href="{z["url"]}">Serrurier {E(z["court"])}</a>' for z in lst)
        blocks += f'<h2>{E(label)}</h2><div class="link-grid">{links}</div>'
    body = page_hero([("Zones d'intervention", None)], "Nos zones d'intervention <em>en Île-de-France</em>",
                     f"Shopta Serrure intervient 24h/24 dans {len(ZONES) - 1} communes et arrondissements : Paris, Hauts-de-Seine et Val-d'Oise.")
    body += f'<section><div class="container layout"><div class="prose">{blocks}<p class="callout">Votre ville n\'est pas listée ? Appelez-nous au {TEL} : hors zone, des frais de déplacement supplémentaires peuvent s\'appliquer et vous sont annoncés à l\'avance.</p></div>{aside_card()}</div></section>'
    body += reviews_section(soft=True) + cta_final(source="/villes/")
    page("/villes/", "Zones d'intervention – Serrurier Paris, 92 et 95 | Shopta Serrure",
         "Liste des villes et arrondissements où Shopta Serrure intervient 24h/24 : Paris 1 à 20, Hauts-de-Seine (92) et Val-d'Oise (95).",
         body, [ld_business(False), ld_breadcrumb([("Zones d'intervention", "/villes/")])], active="/villes/")

    for idx, z in enumerate(ZONES):
        path = z["url"]
        dep_nom, dep_label = DEPTS[z["dep"]]
        cp = ", ".join(z["cp"])
        cp_short = z["cp"][0] if z["slug"] != "paris" else "75"
        voisins = z["voisins"][:6]
        vtxt = ", ".join(v["court"] for v in voisins[:3])
        if z["slug"] == "paris":
            intro = ("Shopta Serrure intervient dans les 20 arrondissements de Paris, 24h/24 et 7j/7. Ouverture de porte claquée à partir de 49 € TTC, "
                     "déblocage de serrure, extraction de clé cassée, changement de cylindre ou sécurisation après effraction : "
                     "le prix vous est annoncé au téléphone, puis confirmé par un devis signé avant toute intervention.")
            local = "<h2>Choisissez votre arrondissement</h2><div class=\"link-grid\">" + "".join(
                f'<a href="/villes/paris-{n}/">Serrurier Paris {n}{"er" if n == 1 else "e"}</a>' for n in range(1, 21)) + "</div>"
        elif z["arr"]:
            n = z["arr"]
            suf = "er" if n == 1 else "e"
            intro = INTROS_PARIS[idx % 4].format(a=z["a"], quartiers=", ".join(z["quartiers"][:-1]) + " et " + z["quartiers"][-1],
                                                  lieux=" et ".join([", ".join(z["lieux"][:-1]), z["lieux"][-1]]), pop=fmt_int(z["pop"]), n=n, suf=suf)
            local = (f"<h2>Quartiers desservis {z['a']}</h2><p>Nous intervenons dans les quatre quartiers administratifs de l'arrondissement : "
                     f"<strong>{', '.join(z['quartiers'])}</strong>, autour de {', '.join(z['lieux'])}. "
                     f"Immeubles haussmanniens, résidences récentes, commerces ou bureaux : nos serruriers sont équipés pour les portes standard comme pour les portes blindées et multipoints.</p>")
        else:
            intro = INTROS_VILLE[idx % 4].format(a=z["a"], cp=cp, voisins=vtxt, nom=z["nom"], pop=fmt_int(z["pop"]))
            grp = [g[1] for g in z["groupes"]]
            grp_txt = f" La commune fait partie de l'intercommunalité <strong>{E(grp[0])}</strong>." if grp else ""
            local = (f"<h2>Serrurier {E(z['nom'])} et alentours</h2><p>{E(z['nom'])} ({cp}) est une commune du département {E(dep_label)} "
                     f"qui compte {fmt_int(z['pop'])} habitants.{grp_txt} Nos serruriers y interviennent pour les particuliers, les syndics, "
                     f"les propriétaires bailleurs et les commerçants, ainsi que dans les communes voisines : "
                     + ", ".join(f'<a href="{v["url"]}">{E(v["court"])}</a>' for v in voisins) + ".</p>")
        facts = f'''<div class="facts">
  <div class="fact"><small>Code postal</small><strong>{E(cp if len(z["cp"]) < 3 else z["cp"][0] + "…")}</strong></div>
  <div class="fact"><small>Disponibilité</small><strong>24h/24 · 7j/7</strong></div>
  <div class="fact"><small>Ouverture de porte</small><strong>à partir de 49 € TTC</strong></div>
  <div class="fact"><small>Délai</small><strong>{"~30 min en moyenne" if z["proche"] else "annoncé au téléphone"}</strong></div>
</div>'''
        svc = "".join(f'''<div class="svc-item"><div class="ic">{ico(s["icon"], "")}</div>
  <div><h3>{E(s["nom"])} {E(z["a"])}</h3><p>{E(s["resume"])}</p></div>
  <div class="pr">{E(s["prix"])}<a href="/depannage/{s["slug"]}/">Détails →</a></div></div>''' for s in SERVICES)
        faq = zone_faq(z)
        near_links = "".join(f'<a href="{v["url"]}">Serrurier {E(v["court"])}</a>' for v in z["voisins"])
        content = f'''<div class="prose">
  <p>{intro}</p>
  {facts}
  {fig(city_photo(idx), f"Intervention de serrurerie {z['a']}")}
  <h2>Nos dépannages {E(z["a"])}</h2>
  <div class="svc-list">{svc}</div>
  {local}
  <h2>Pourquoi faire appel à Shopta Serrure {E(z["a"])} ?</h2>
  <ul>
    <li><strong>Prix annoncé avant le déplacement</strong>, puis devis écrit et signé avant toute intervention.</li>
    <li><strong>Ouverture sans dégât</strong> dans la grande majorité des cas (radio, crochetage, by-pass).</li>
    <li><strong>Facture détaillée</strong> reconnue par les assureurs habitation, remboursable selon votre contrat.</li>
    <li><strong>Avis clients publics</strong> et vérifiables sur <a href="{E(MAPS)}" target="_blank" rel="noopener">notre fiche Google</a>.</li>
  </ul>
  <h2>Questions fréquentes {E(z["a"])}</h2>
  {faq_html(faq)}
  <h2>Nous intervenons aussi à proximité</h2>
  <div class="link-grid">{near_links}</div>
</div>'''
        h1 = f'Serrurier {E(z["court"])} <em>24h/24</em>' + (f' – {E(cp_short)}' if z["slug"] != "paris" else "")
        lead = f'Ouverture de porte à partir de 49 € TTC, serrure bloquée, clé cassée, changement de serrure {E(z["a"])}. Prix annoncé avant déplacement, devis gratuit, facture remboursable par votre assurance.'
        crumb_items = [("Zones d'intervention", "/villes/")]
        if z["arr"]:
            crumb_items.append(("Paris", "/villes/paris/"))
        crumb_items.append((f'Serrurier {z["court"]}', None))
        body = page_hero(crumb_items, h1, lead, checks(["Devis gratuit", "Sans frais cachés", "Nuit, week-end et jours fériés"]))
        body += f'<section><div class="container layout">{content}{aside_card(f"Serrurier {z["court"]}")}</div></section>'
        body += insurers_block() + reviews_section(title=f"Avis de nos clients", soft=True) + cta_final(f"Bloqué dehors {z['a']} ?", "Appelez-nous : prix annoncé au téléphone, serrurier en route immédiatement.",
                                                                                                                         source=path, ville=z["court"] if z["slug"] != "paris" else "")
        if z["slug"] == "paris":
            title = "Serrurier Paris 24h/24 – Tous arrondissements, à partir de 49 € | Shopta Serrure"
        else:
            title = f'Serrurier {z["court"]} ({cp_short}) 24h/24 – à partir de 49 € | Shopta Serrure'
        desc = (f'Serrurier {z["court"]} ({cp_short if z["slug"] != "paris" else "75"}) disponible 24h/24 et 7j/7 : ouverture de porte à partir de 49 € TTC, serrure bloquée, '
                f'clé cassée, changement de serrure. Prix annoncé avant déplacement, facture remboursable par l\'assurance.')
        bc = [(c[0], c[1] if c[1] else path) for c in crumb_items]
        ld = [ld_business(False), ld_breadcrumb(bc), ld_faq(faq),
              {"@context": "https://schema.org", "@type": "Service", "name": f"Serrurier {z['nom']}", "serviceType": "Serrurerie, dépannage 24h/24",
               "url": URL + path, "provider": {"@id": BUSINESS_ID},
               "areaServed": {"@type": "City" if not z["arr"] else "AdministrativeArea", "name": z["nom"],
                              **({"postalCode": z["cp"][0]} if z["slug"] != "paris" else {})},
               "offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 49, "priceCurrency": "EUR"}}}]
        page(path, title, desc, body, ld, active="/villes/")


# --- Pages simples ----------------------------------------------------------
def simple(path, crumb, h1, lead, prose, title, desc, extra_ld=(), active=None, after="", aside=True, robots="index, follow"):
    body = page_hero([(crumb, None)], h1, lead)
    inner = f'<div class="prose">{prose}</div>' + (aside_card() if aside else "")
    body += f'<section><div class="container{" layout" if aside else ""}">{inner}</div></section>' + after
    page(path, title, desc, body, [ld_business(False), ld_breadcrumb([(crumb, path)]), *extra_ld], active=active, robots=robots)


def build_static():
    # Tarifs
    rows = "".join(f'<tr><td><a href="/depannage/{s["slug"]}/">{E(s["nom"])}</a></td><td>{E(s["prix"])}</td></tr>' for s in SERVICES)
    simple("/tarifs/", "Tarifs", "Tarifs serrurier <em>clairs et annoncés</em>",
           "Nos prix de départ, nos engagements et ce que comprend le prix. Aucun frais caché : tout est annoncé avant le déplacement.",
           f'''<h2>Nos prix de départ</h2>
<table><thead><tr><th>Intervention</th><th>Prix</th></tr></thead><tbody>{rows}<tr><td>Devis</td><td><strong>Gratuit</strong></td></tr></tbody></table>
<p class="callout">Le prix final dépend du type de porte (standard, blindée, multipoints) et du matériel éventuellement remplacé. Il vous est annoncé au téléphone, puis confirmé par un devis écrit et signé avant le début des travaux.</p>
<h2>Ce que comprend le prix</h2>
<ul><li>La main d'œuvre du serrurier.</li><li>Le déplacement, offert en cas de travaux réalisés dans notre zone d'intervention.</li><li>La TVA : nos prix sont indiqués TTC.</li><li>La facture détaillée, conforme pour votre assurance.</li></ul>
<h2>Nos engagements</h2>
<ul><li><strong>Prix annoncé avant le départ</strong> du technicien.</li><li><strong>Devis écrit et signé</strong> avant toute intervention : rien n'est fait sans votre accord.</li><li><strong>Aucune majoration surprise</strong> : si un supplément s'applique (nuit, hors zone), il vous est annoncé au téléphone.</li><li><strong>Matériel certifié</strong> et garanti, cylindres et serrures de marques reconnues.</li></ul>
<h2>Moyens de paiement</h2><p>Carte bancaire, espèces et virement.</p>''',
           "Tarifs serrurier Paris – Ouverture de porte à partir de 49 € TTC | Shopta Serrure",
           "Tarifs Shopta Serrure : ouverture de porte claquée à partir de 49 € TTC, déblocage, clé cassée, changement de serrure sur devis gratuit. Prix annoncé avant déplacement.",
           active="/tarifs/", after=insurers_block() + cta_final(source="/tarifs/"))

    # Assurances
    simple("/assurances/", "Assurances", "Serrurier et assurance : <em>votre facture remboursable</em>",
           "Nos factures sont reconnues par les assureurs habitation. Voici comment se faire rembourser une intervention de serrurerie.",
           '''<h2>Quand l'assurance rembourse-t-elle le serrurier ?</h2>
<p>La plupart des contrats multirisques habitation prennent en charge les frais de serrurerie en cas de <strong>cambriolage ou de tentative d'effraction</strong>. Certains contrats couvrent aussi le <strong>vol</strong> ou la <strong>perte des clés</strong>, parfois en option. Une porte simplement claquée est rarement couverte, sauf garantie d'assistance spécifique : vérifiez votre contrat.</p>
<h2>Les documents à fournir</h2>
<ul><li>Le <strong>récépissé de dépôt de plainte</strong> en cas d'effraction ou de vol.</li><li>Notre <strong>facture détaillée</strong> (nature de l'intervention, matériel remplacé, prix TTC).</li><li>Le <strong>devis signé</strong> et, sur demande, les <strong>photos avant/après</strong>.</li></ul>
<h2>Les délais à respecter</h2>
<p>En cas de vol ou de cambriolage, la déclaration à l'assureur doit en général être faite dans les <strong>2 jours ouvrés</strong> après en avoir eu connaissance. Pour les autres sinistres, le délai est souvent de 5 jours ouvrés. Référez-vous à votre contrat.</p>
<h2>Notre accompagnement</h2>
<p>Nous vous remettons tous les documents nécessaires et vous conseillons sur votre déclaration. Si un expert doit passer, nous pouvons sécuriser provisoirement votre porte en attendant la remise en état définitive.</p>
<p class="callout">Shopta Serrure est une entreprise indépendante, sans partenariat avec les compagnies d'assurance. Nos factures sont conformes et reconnues par les assureurs ; le remboursement dépend des garanties de votre contrat.</p>''',
           "Serrurier et assurance habitation – Facture remboursable | Shopta Serrure",
           "Comment se faire rembourser un serrurier par son assurance habitation : garanties, documents, délais. Nos factures sont reconnues par les assureurs.",
           active=None, after=insurers_block() + cta_final(source="/assurances/"))

    # FAQ
    allfaq = HOME_FAQ + [q for s in SERVICES for q in s["faq"]]
    simple("/faq/", "FAQ", "Questions <em>fréquentes</em>",
           "Prix, délais, assurance, techniques d'ouverture : les réponses à vos questions sur nos interventions.",
           "<h2>Général</h2>" + faq_html(HOME_FAQ) + "".join(f'<h2>{E(s["court"])}</h2>' + faq_html(s["faq"]) for s in SERVICES),
           "FAQ serrurier – Prix, délais, assurance | Shopta Serrure",
           "Toutes les réponses à vos questions : prix d'une ouverture de porte, délai d'intervention, remboursement par l'assurance, ouverture sans dégât.",
           extra_ld=[ld_faq(allfaq)], after=cta_final(source="/faq/"))

    # Avis
    body = page_hero([("Avis clients", None)], "Avis clients <em>vérifiés sur Google</em>",
                     "Nos avis sont publiés par nos clients sur notre fiche Google Maps. Ils sont publics, vérifiables et nous ne pouvons pas les modifier.")
    body += reviews_section(title="Notre réputation sur Google") + cta_final(source="/avis/")
    page("/avis/", "Avis clients Shopta Serrure – Serrurier Paris", "Consultez les avis Google de nos clients et laissez le vôtre. Serrurier d'urgence à Paris et en Île-de-France.",
         body, [ld_business(False), ld_breadcrumb([("Avis clients", "/avis/")])], active="/avis/")

    # Contact
    form = contact_form("/contact/", titre="Écrivez-nous", sous_titre="Devis, rappel, question : réponse rapide, 7j/7.")
    body = page_hero([("Contact", None)], "Contactez <em>un serrurier</em>", "Pour une urgence, appelez directement : c'est le plus rapide. Pour un devis ou des travaux, écrivez-nous.")
    body += f'''<section class="soft"><div class="container contact">
    <div class="contact-info reveal">
      <h2>Shopta Serrure</h2>
      <p>Serrurier d'urgence à Paris et en Île-de-France, 24h/24 et 7j/7.</p>
      <div class="c-line"><span class="ic">{ico("i-phone", "")}</span><div><small>Téléphone 24h/24</small><strong><a href="{TEL_HREF}">{TEL}</a></strong></div></div>
      <div class="c-line"><span class="ic">{ico("i-mail", "")}</span><div><small>E-mail</small><strong><a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></strong></div></div>
      <div class="c-line"><span class="ic">{ico("i-insta", "")}</span><div><small>Instagram</small><strong><a href="{CONFIG['instagram']}" target="_blank" rel="noopener me">@shoptaserrure</a></strong></div></div>
      <div class="c-line"><span class="ic">{ico("i-tiktok", "")}</span><div><small>TikTok</small><strong><a href="{CONFIG['tiktok']}" target="_blank" rel="noopener me">@shopta.serrure</a></strong></div></div>
      <div class="c-line"><span class="ic">{ico("i-pin", "")}</span><div><small>Zone d'intervention</small><strong>Paris, Hauts-de-Seine, Val-d'Oise</strong></div></div>
      {btn_call("Appeler maintenant", cls="btn btn-call btn-lg", track="call_contact")}
    </div>
    {form}
  </div></section>''' + reviews_section(title="Où nous trouver")
    page("/contact/", "Contact – Serrurier Paris 24h/24 | Shopta Serrure", f"Contactez Shopta Serrure au {TEL}, 24h/24 et 7j/7, par WhatsApp ou par e-mail. Devis gratuit, intervention rapide à Paris et en Île-de-France.",
         body, [ld_business(), ld_breadcrumb([("Contact", "/contact/")])], active="/contact/")

    # Mentions légales
    na = "<em>[à compléter]</em>"
    simple("/mentions-legales/", "Mentions légales", "Mentions légales", "Informations légales relatives au site et à l'entreprise.",
           f'''<h2>Éditeur du site</h2>
<p>{E(CONFIG["raison_sociale"])}<br>Responsable de la publication : {E(CONFIG["responsable"]) or na}<br>SIRET : {E(CONFIG["siret"]) or na}<br>
Adresse : {E(", ".join(v for v in CONFIG["adresse"].values() if v)) or na}<br>Téléphone : {TEL}<br>E-mail : {CONFIG["email"]}</p>
<h2>Hébergement</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, États-Unis – www.netlify.com</p>
<h2>Propriété intellectuelle</h2><p>Les textes, illustrations et éléments graphiques de ce site sont la propriété de Shopta Serrure, sauf mention contraire. Les noms et logos des compagnies d'assurance appartiennent à leurs propriétaires respectifs et sont cités à titre informatif ; ils n'impliquent aucun partenariat.</p>
<h2>Médiation de la consommation</h2><p>Conformément à l'article L612-1 du Code de la consommation, vous pouvez recourir gratuitement à un médiateur de la consommation : {na}</p>''',
           "Mentions légales | Shopta Serrure", "Mentions légales du site Shopta Serrure, serrurier à Paris et en Île-de-France.", aside=False)

    simple("/politique-confidentialite/", "Confidentialité", "Politique de confidentialité", "Comment nous traitons vos données personnelles.",
           '''<h2>Données collectées</h2><p>Lorsque vous nous contactez par téléphone, WhatsApp, e-mail ou via le formulaire, nous recueillons uniquement les informations nécessaires au traitement de votre demande : nom, numéro de téléphone, adresse d'intervention et description du problème.</p>
<h2>Finalité</h2><p>Ces données servent exclusivement à organiser l'intervention, établir le devis et la facture. Elles ne sont ni vendues ni cédées à des tiers.</p>
<h2>Formulaire et WhatsApp</h2><p>Le formulaire de contact ouvre l'application WhatsApp avec votre message pré-rempli. L'envoi est alors soumis aux conditions de WhatsApp (Meta).</p>
<h2>Mesure d'audience</h2><p>Ce site utilise Google Analytics pour mesurer sa fréquentation (pages vues, clics sur les boutons d'appel). Ces données sont anonymisées et agrégées.</p>
<h2>Durée de conservation</h2><p>Les données liées aux factures sont conservées pendant la durée légale de 10 ans. Les autres données sont supprimées au plus tard 3 ans après le dernier contact.</p>
<h2>Vos droits</h2><p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition. Pour l'exercer, écrivez à shoptaserrure@gmail.com. Vous pouvez également introduire une réclamation auprès de la CNIL.</p>''',
           "Politique de confidentialité | Shopta Serrure", "Politique de confidentialité et traitement des données personnelles du site Shopta Serrure.", aside=False)


def build_merci():
    body = f'''<section class="notfound"><div class="container">
<div style="display:inline-grid;place-items:center;width:84px;height:84px;border-radius:50%;background:var(--green-50);color:var(--green-600);margin-bottom:18px">{ico("i-checkc", "ok-ic")}</div>
<h1 style="font-size:clamp(32px,5vw,48px)">Merci, demande reçue !</h1>
<p style="color:var(--muted);margin:14px auto 28px;max-width:560px;font-size:18px">Nous vous rappelons très rapidement. Pour une urgence (porte claquée, effraction), appelez-nous directement : c'est le plus rapide.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">{btn_call(cls="btn btn-call btn-lg", track="call_merci")}<a class="btn btn-blue btn-lg" href="/">Retour à l'accueil</a></div></div></section>'''
    page("/merci/", "Demande envoyée | Shopta Serrure", "Votre demande a bien été envoyée.", body, robots="noindex, nofollow")


def build_blog():
    cards = "".join(f'''<article class="post reveal">
  {cover(a)}
  <div class="body"><div class="meta"><b>{E(a["cat"])}</b><time datetime="{a["date"]}">{fr_date(a["date"])}</time></div>
  <h3><a href="/blog/{a["slug"]}/">{E(a["court"])}</a></h3><p>{E(a["desc"])}</p><a class="more" href="/blog/{a["slug"]}/">Lire l'article →</a></div>
</article>''' for a in ARTICLES)
    body = page_hero([("Blog", None)], "Le Mag Sécurité <em>Shopta Serrure</em>", "Conseils, guides pratiques et actualités pour la sécurité de votre logement, rédigés par nos serruriers.")
    body += f'<section><div class="container"><div class="blog-grid">{cards}</div></div></section>' + cta_final(source="/blog/")
    page("/blog/", "Blog sécurité & serrurerie – Conseils de serruriers | Shopta Serrure",
         "Conseils de serruriers : porte claquée, clé cassée, éviter les arnaques, choisir une serrure A2P, entretenir sa serrure.",
         body, [ld_business(False), ld_breadcrumb([("Blog", "/blog/")])], active="/blog/")

    for a in ARTICLES:
        path = f"/blog/{a['slug']}/"
        parts = []
        for kind, val in a["corps"]:
            if kind in ("ul", "ol"):
                parts.append(f"<{kind}>" + "".join(f"<li>{v}</li>" for v in val) + f"</{kind}>")
            else:
                parts.append(f"<{kind}>{val}</{kind}>")
        rel = "".join(f'<a href="/blog/{o["slug"]}/"><small>{E(o["cat"])}</small><strong>{E(o["court"])}</strong></a>' for o in [o for o in ARTICLES if o is not a][:3])
        prose = fig(ARTICLE_PHOTOS.get(a["slug"])) + "".join(parts) + f'<h2>Besoin d\'un serrurier maintenant ?</h2><p>Shopta Serrure intervient 24h/24 à Paris et en Île-de-France. Appelez le <a href="{TEL_HREF}">{TEL}</a> : le prix vous est annoncé au téléphone. Consultez aussi nos <a href="/depannage/">dépannages</a> et nos <a href="/tarifs/">tarifs</a>.</p>'
        body = page_hero([("Blog", "/blog/"), (a["court"], None)], E(a["titre"]), E(a["desc"]),
                         f'<div class="article-meta"><span>{E(a["cat"])}</span><span>·</span><time datetime="{a["date"]}">Publié le {fr_date(a["date"])}</time><span>·</span><span>Par l\'équipe Shopta Serrure</span></div>')
        body += f'<section><div class="container layout"><article class="prose">{prose}</article>{aside_card()}</div></section>'
        body += f'<section class="soft" style="padding:64px 0"><div class="container"><h2 style="font-size:26px;margin-bottom:20px">À lire aussi</h2><div class="related">{rel}</div></div></section>' + cta_final(source=path)
        ld = [ld_business(False), ld_breadcrumb([("Blog", "/blog/"), (a["court"], path)]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"], "description": a["desc"],
               "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "fr-FR", "mainEntityOfPage": URL + path,
               "author": {"@type": "Organization", "name": "Shopta Serrure", "url": URL + "/"}, "publisher": {"@id": BUSINESS_ID},
               "image": URL + "/assets/img/og.png"}]
        page(path, f'{a["titre"]} | Shopta Serrure', a["desc"], body, ld, active="/blog/", og_type="article")


def build_sitemap_page():
    groups = [("Pages principales", [("Accueil", "/"), ("Dépannage", "/depannage/"), ("Tarifs", "/tarifs/"), ("Assurances", "/assurances/"),
                                     ("Avis clients", "/avis/"), ("FAQ", "/faq/"), ("Contact", "/contact/"), ("Blog", "/blog/"), ("Zones", "/villes/")]),
              ("Dépannages", [(s["nom"], f"/depannage/{s['slug']}/") for s in SERVICES]),
              ("Articles", [(a["court"], f"/blog/{a['slug']}/") for a in ARTICLES])]
    for dep, (_, label) in DEPTS.items():
        groups.append((f"Serrurier {label}", [(f"Serrurier {z['court']}", z["url"]) for z in ZONES if z["dep"] == dep]))
    prose = "".join(f'<h2>{E(t)}</h2><div class="link-grid">' + "".join(f'<a href="{u}">{E(l)}</a>' for l, u in lst) + "</div>" for t, lst in groups)
    simple("/plan-du-site/", "Plan du site", "Plan du site", "Toutes les pages du site Shopta Serrure.", prose,
           "Plan du site | Shopta Serrure", "Plan du site Shopta Serrure : services, zones d'intervention, articles.", aside=False)


def build_404():
    body = f'''<section class="notfound"><div class="container"><h1>404</h1><h2 style="font-size:28px;margin:10px 0 14px">Cette page n'existe pas</h2>
<p style="color:var(--muted);margin-bottom:28px">Elle a peut-être été déplacée. Besoin d'un serrurier ? On est joignable 24h/24.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">{btn_call(cls="btn btn-call btn-lg")}<a class="btn btn-blue btn-lg" href="/">Retour à l'accueil</a></div></div></section>'''
    page("/404.html", "Page introuvable | Shopta Serrure", "Cette page n'existe pas.", body, robots="noindex, follow")


# ---------------------------------------------------------------------------
# Fichiers SEO
# ---------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)


# Logos réduits au symbole : le nom de l'assureur est affiché à côté
LOGO_SANS_NOM = set()


def build_insurers_js():
    data = [{"n": n, "d": d, "c": c, **({"logo": LOGOS[slug]} if slug in LOGOS else {}),
             **({"label": 1} if slug in LOGO_SANS_NOM else {})} for n, slug, d, c in INSURERS]
    write("assets/js/assureurs.js", "window.ASSUREURS=" + json.dumps(data, ensure_ascii=False) + ";\n")


def build_seo_files():
    def prio(p):
        if p == "/":
            return "1.0"
        if p.startswith("/depannage/") or p in ("/villes/paris/", "/tarifs/", "/contact/"):
            return "0.9"
        if p.startswith("/villes/"):
            return "0.8"
        return "0.6"

    def freq(p):
        return "weekly" if p in ("/", "/avis/", "/blog/") else "monthly"

    def url_entry(p):
        imgs = "".join(f"<image:image><image:loc>{URL}{i}</image:loc></image:image>" for i in SITEMAP_IMAGES.get(p, [])[:5])
        return (f"  <url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq(p)}</changefreq>"
                f"<priority>{prio(p)}</priority>{imgs}</url>\n")
    urls = "".join(url_entry(p) for p in SITEMAP)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
          f"{urls}</urlset>\n")

    bots = ["*", "Googlebot", "Bingbot", "Applebot", "DuckDuckBot", "YandexBot", "Qwantbot",
            "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Mistralai-User", "Meta-ExternalAgent"]
    write("robots.txt", "# Shopta Serrure – moteurs de recherche et assistants IA autorisés\n"
          + "".join(f"User-agent: {b}\n" for b in bots)
          + "Allow: /\nDisallow: /_src/\nDisallow: /merci/\n\n"
          + f"Sitemap: {URL}/sitemap.xml\n")

    svc = "\n".join(f"- [{s['nom']}]({URL}/depannage/{s['slug']}/) : {s['prix']}. {s['resume']}" for s in SERVICES)
    arts = "\n".join(f"- [{a['court']}]({URL}/blog/{a['slug']}/) : {a['desc']}" for a in ARTICLES)
    deps = "\n\n".join(f"### {label}\n" + "\n".join(f"- [Serrurier {z['court']}]({URL}{z['url']})" for z in ZONES if z["dep"] == dep)
                       for dep, (_, label) in DEPTS.items())
    note = (f"- Note Google : {AVIS['note']}/5 sur {AVIS['nombre']} avis\n" if AVIS.get("note") else "")
    write("llms.txt", f"""# Shopta Serrure

> Serrurier d'urgence à Paris et en Île-de-France (Paris 75, Hauts-de-Seine 92, Val-d'Oise 95), disponible 24h/24 et 7j/7. Ouverture de porte claquée à partir de 49 € TTC, prix annoncé au téléphone avant le déplacement, devis écrit signé avant toute intervention, facture détaillée reconnue par les assureurs habitation.

## Informations clés
- Nom : Shopta Serrure (fiche Google : « Serrurier - Shopta serrure »)
- Téléphone : {TEL} ({CONFIG['tel_intl']}), joignable 24h/24, 7j/7, jours fériés compris
- WhatsApp : {WA}
- E-mail : {CONFIG['email']}
- Site : {URL}/
- Fiche Google Maps : {MAPS}
- Instagram : {CONFIG['instagram']}
- TikTok : {CONFIG['tiktok']}
- Délai d'intervention : moins de 30 minutes en moyenne dans Paris et la proche couronne
- Paiement : carte bancaire, espèces, virement
- Assurance : facture conforme, remboursable selon le contrat d'assurance habitation. Entreprise indépendante, sans partenariat avec les assureurs.
- Devis écrit gratuit : formulaire sur chaque page et sur {URL}/contact/, ou par WhatsApp
{note}
## Services et prix
{svc}

## Zones d'intervention
{deps}

## Pages utiles
- [Tarifs]({URL}/tarifs/)
- [Serrurier et assurance]({URL}/assurances/)
- [Avis clients]({URL}/avis/)
- [FAQ]({URL}/faq/)
- [Contact et demande de devis]({URL}/contact/)
- [Plan du site]({URL}/plan-du-site/)

## Guides
{arts}
""")

    write("manifest.webmanifest", json.dumps({
        "name": "Shopta Serrure – Serrurier 24h/24", "short_name": "Shopta Serrure", "lang": "fr", "start_url": "/",
        "display": "standalone", "background_color": "#ffffff", "theme_color": "#003380",
        "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))

    write(f"{CONFIG['indexnow_key']}.txt", CONFIG["indexnow_key"])


def main():
    build_home()
    build_services()
    build_zones_pages()
    build_static()
    build_blog()
    build_merci()
    build_sitemap_page()
    build_404()
    build_seo_files()
    build_insurers_js()
    print(f"Photos : {len(PHOTO)}/{len(PHOTOS)} · logos assureurs : {len(LOGOS)}/{len(INSURERS)}")
    print(f"{len(SITEMAP)} pages indexables générées.")


if __name__ == "__main__":
    main()
