#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Run scoring-prospects — pipeline 7 etapes, fidele a la spec POST-MERGE :
#   - skills/scoring-prospects/SKILL.md (pipeline + garde-fous)
#   - skills/scoring-prospects/references/scoring-formula.md (calcul, SOURCE DE VERITE)
#   - skills/scoring-prospects/references/chaines-nationales.md (exclusions)
#   - skills/scoring-prospects/references/argument-library.md (top 3 arguments)
#   - prospects/README.md (restaurants.yml = source de verite, vues regenerees)
# Reutilise les caches valides (Overpass/Nominatim/Lighthouse/Wayback).
# Places API officielle : sondee 1x ; si refus/desactivee -> defauts conformes
# (scoring-formula.md "Donnees manquantes"), JAMAIS de chiffre invente.
# LOCAL : prospects/ versionne dans le repo prive, cache/ gitignore.
import json, os, re, time, urllib.parse, subprocess, datetime, unicodedata, sys
from concurrent.futures import ThreadPoolExecutor
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROS = os.path.join(ROOT, "prospects")
CACHE = os.path.join(PROS, "cache")
DATE = datetime.date.today().isoformat()
OUT = os.path.join(PROS, f"chartres-{DATE}")
os.makedirs(OUT, exist_ok=True)
for d in ("lighthouse", "wayback", "places"):
    os.makedirs(os.path.join(CACHE, d), exist_ok=True)
UA = "MB-Studio-Scoring/1.0 (contact: kroostiyummy@gmail.com)"
LOG = open(os.path.join(OUT, "_run.log"), "w", encoding="utf-8")
def log(m):
    line = f"{datetime.datetime.now():%H:%M:%S} {m}"
    LOG.write(line + "\n"); LOG.flush()
    print(line, flush=True)

def secret(name):
    sp = os.path.join(os.path.expanduser("~"), ".mb-studio", "secrets.env")
    if os.path.exists(sp):
        for ln in open(sp, encoding="utf-8"):
            if ln.strip().startswith(name + "="):
                return ln.split("=", 1)[1].strip()
    return ""

PKEY = secret("GOOGLE_PAGESPEED_API_KEY")
PLKEY = secret("GOOGLE_PLACES_API_KEY")
DEGRADE = not bool(PKEY)            # mode degrade = cle PageSpeed absente
log(f"PageSpeed: {'ABSENTE -> MODE DEGRADE' if DEGRADE else 'OK -> mode normal'}")

def curl(args, timeout=90):
    # capture en bytes puis decode UTF-8 (Windows: text=True force cp1252 -> crash)
    try:
        r = subprocess.run(["curl", "-s", "--max-time", str(timeout)] + args,
                            capture_output=True, timeout=timeout + 15)
        return (r.stdout or b"").decode("utf-8", errors="replace")
    except Exception as e:
        log(f"curl err: {e}"); return ""

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

slug_re = re.compile(r"[^a-z0-9]+")
def slugify(s):
    return slug_re.sub("-", strip_accents(s).lower()).strip("-")[:50]

# --- opt-out RGPD (garde-fou) ---
OPTOUT = set()
of = os.path.join(PROS, "opt-out.txt")
if os.path.exists(of):
    for ln in open(of, encoding="utf-8"):
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            OPTOUT.add(strip_accents(ln).lower())

# --- chaines-nationales.md (liste statique fidele a la reference) ---
CHAINES = [
 "mcdonald", "burger king", "quick", "kfc", "five guys", "o'tacos", "otacos",
 "tacos avenue", "subway", "pomme de pain", "brioche doree", "paul",
 "la mie caline", "class'croute", "pizza hut", "domino's pizza", "domino's",
 "domino", "sushi shop", "planet sushi", "eat sushi", "pokawa", "bagelstein",
 "big fernand", "factory & co", "buffalo grill", "hippopotamus",
 "leon de bruxelles", "leon", "courtepaille", "flunch", "crocodile",
 "la boucherie", "au bureau", "cafe leffe", "3 brasseurs", "les 3 brasseurs",
 "bistro regent", "del arte", "pizza del arte", "memphis coffee",
 "poivre rouge", "tablapizza", "vapiano", "starbucks", "columbus cafe",
 "costa coffee", "marie blachere", "ange", "sophie lebreuilly",
]
def is_chaine(nom):
    low = strip_accents(nom).lower()
    for c in CHAINES:
        cl = strip_accents(c).lower()
        # match marque comme segment (frontiere de mot), pas sous-chaine hasardeuse
        if re.search(r"(^|[^a-z0-9])" + re.escape(cl) + r"([^a-z0-9]|$)", low):
            return True
    return False

# === ETAPE 1 — Overpass (cache, TTL 30j) ===========================
ovf = os.path.join(CACHE, "overpass-chartres-5000.json")
if not (os.path.exists(ovf) and time.time() - os.path.getmtime(ovf) < 30 * 86400):
    log("Overpass cache absent/perime -> fetch")
    q = ('[out:json][timeout:25];('
         'node["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"]'
         '(around:5000,48.4439,1.4892);'
         'way["amenity"~"restaurant|cafe|fast_food|bar|pub"]["name"]'
         '(around:5000,48.4439,1.4892););out center tags;')
    out = curl(["-G", "https://overpass-api.de/api/interpreter",
                "-H", f"User-Agent: {UA}", "--data-urlencode", "data=" + q], 60)
    open(ovf, "w", encoding="utf-8").write(out)
ov = json.load(open(ovf, encoding="utf-8"))
seen = {}
restos = []
for e in ov["elements"]:
    t = e.get("tags", {})
    nom = (t.get("name") or "").strip()
    if not nom:
        continue
    sl = slugify(nom)
    if sl in seen:                       # dedup node/way meme resto
        continue
    seen[sl] = True
    restos.append({
        "nom": nom, "slug": sl,
        "rue": " ".join(x for x in [t.get("addr:housenumber"),
                                    t.get("addr:street")] if x),
        "cp": t.get("addr:postcode", ""),
        "ville": t.get("addr:city", "Chartres"),
        "tel": t.get("phone") or t.get("contact:phone") or "",
        "cuisine": (t.get("cuisine") or "").replace(";", " "),
        "website": (t.get("website") or t.get("contact:website") or "").strip(),
        "note": None, "avis": None, "gmb": None,
    })
# opt-out RGPD
restos = [r for r in restos if strip_accents(r["nom"]).lower() not in OPTOUT]
log(f"ETAPE 1: {len(restos)} restos uniques depuis Overpass (cache)")

# === ETAPE 2 — Nominatim (cache TTL 30j) + Places (sonde 1x) =======
nb_nom = 0
for r in restos:
    if r["website"]:
        continue
    cf = os.path.join(CACHE, f"nominatim-{r['slug']}.json")
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 30 * 86400:
        data = open(cf, encoding="utf-8").read()
    else:
        data = curl(["-H", f"User-Agent: {UA}",
            "https://nominatim.openstreetmap.org/search?q="
            + urllib.parse.quote(f"{r['nom']} Chartres")
            + "&format=json&extratags=1&limit=1"], 30)
        open(cf, "w", encoding="utf-8").write(data or "[]")
        nb_nom += 1
        time.sleep(1.2)                  # rate-limit Nominatim strict
    try:
        j = json.loads(data or "[]")
        if j and j[0].get("extratags", {}).get("website"):
            r["website"] = j[0]["extratags"]["website"].strip()
    except Exception:
        pass
log(f"ETAPE 2: Nominatim interroge {nb_nom}x (reste en cache)")

# Sonde Places API (officielle, garde-fou #4). 1 appel test.
PLACES_OK = False
if PLKEY:
    probe = curl(["-X", "POST", "https://places.googleapis.com/v1/places:searchText",
        "-H", "Content-Type: application/json",
        "-H", f"X-Goog-Api-Key: {PLKEY}",
        "-H", "X-Goog-FieldMask: places.id,places.rating",
        "-d", '{"textQuery":"restaurant Chartres","languageCode":"fr","maxResultCount":1}'], 30)
    try:
        pj = json.loads(probe or "{}")
        PLACES_OK = "places" in pj
        if not PLACES_OK:
            log("ETAPE 2: Places INDISPONIBLE ("
                + str(pj.get("error", {}).get("status", "?"))
                + ") -> enrichissement GMB SKIP, defauts conformes scoring-formula.md")
    except Exception:
        log("ETAPE 2: Places reponse non-JSON -> SKIP")
else:
    log("ETAPE 2: pas de cle Places -> enrichissement GMB SKIP")

def places_enrich(r):
    """Place Details officiel : note, nb avis, signaux GMB completude.
    Cache prospects/cache/places/{slug}.json TTL 30j. Plafonne aux donnees
    manquantes. Aucune valeur inventee : echec -> None (defauts formule)."""
    cf = os.path.join(CACHE, "places", f"{r['slug']}.json")
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 30 * 86400:
        try:
            d = json.load(open(cf, encoding="utf-8"))
            r["note"], r["avis"], r["gmb"] = d.get("note"), d.get("avis"), d.get("gmb")
            if d.get("website") and not r["website"]:
                r["website"] = d["website"]
            return
        except Exception:
            pass
    if not PLACES_OK:
        return
    fm = ("places.id,places.displayName,places.rating,places.userRatingCount,"
          "places.websiteUri,places.regularOpeningHours,places.photos,"
          "places.editorialSummary,places.primaryType,places.types")
    body = json.dumps({"textQuery": f"restaurant {r['nom']} Chartres",
                       "languageCode": "fr", "maxResultCount": 1})
    out = curl(["-X", "POST", "https://places.googleapis.com/v1/places:searchText",
        "-H", "Content-Type: application/json", "-H", f"X-Goog-Api-Key: {PLKEY}",
        "-H", f"X-Goog-FieldMask: {fm}", "-d", body], 30)
    try:
        p = json.loads(out).get("places", [None])[0]
        if not p:
            return
        nb_photos = len(p.get("photos", []) or [])
        gmb = 0
        gmb += 30 if nb_photos >= 10 else (15 if nb_photos >= 5 else 0)
        if p.get("regularOpeningHours"):
            gmb += 20
        desc = (p.get("editorialSummary") or {}).get("text", "")
        if len(desc) > 100:
            gmb += 20
        if len(p.get("types", []) or []) >= 2:
            gmb += 15
        gmb = min(100, gmb)
        d = {"note": p.get("rating"), "avis": p.get("userRatingCount"),
             "gmb": gmb, "website": p.get("websiteUri", ""),
             "source": "google_places_api", "date_collecte": DATE}
        json.dump(d, open(cf, "w", encoding="utf-8"))
        r["note"], r["avis"], r["gmb"] = d["note"], d["avis"], d["gmb"]
        if d["website"] and not r["website"]:
            r["website"] = d["website"]
        time.sleep(0.15)
    except Exception as e:
        log(f"Places parse err {r['slug']}: {e}")

if PLACES_OK:
    for r in restos:
        places_enrich(r)
    log("ETAPE 2: enrichissement Places termine")
else:
    for r in restos:                     # tente le cache places meme si API down
        places_enrich(r)

# --- Buckets ---
# Decision Mike 2026-05-17 : un lien vers une plateforme agregateur/livraison/
# linktree n'est PAS un site a soi -> bucket pas-de-site (valeur 90, cible
# prime), pas autre-site. Corrige aussi les faux matchs Nominatim partages.
AGGREGATEURS = ("ubereats.", "deliveroo.", "just-eat.", "justeat.",
                "privateaser.", "bento.me", "linktr.ee", "linktree.",
                "beacons.ai", "allmylinks.", "smartlink.", "tripadvisor.",
                "thefork.", "lafourchette.", "facebook.com", "instagram.com")
for r in restos:
    w = r["website"].lower()
    plat = next((a.rstrip(".") for a in AGGREGATEURS if a in w), None)
    if plat:
        r["agg"] = plat                 # garde la trace de la plateforme
        r["website"] = ""               # pas de site a soi
        w = ""
    if is_chaine(r["nom"]):
        r["bucket"] = "exclu-chaine"
    elif "eatbu.com" in w:
        r["bucket"] = "eatbu"
    elif w:
        r["bucket"] = "autre-site"
    else:
        r["bucket"] = "pas-de-site"
from collections import Counter
log("Buckets: " + str(dict(Counter(r["bucket"] for r in restos))))

# === ETAPE 3 — Lighthouse PageSpeed (cache TTL 30j, lots de 4) =====
def lighthouse(r):
    cf = os.path.join(CACHE, "lighthouse", f"{r['slug']}.json")
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 30 * 86400:
        try:
            return json.load(open(cf, encoding="utf-8"))
        except Exception:
            pass
    if DEGRADE:
        return None
    u = urllib.parse.quote(r["website"], safe="")
    out = curl([f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
                f"url={u}&strategy=mobile&category=PERFORMANCE&category=ACCESSIBILITY"
                f"&category=SEO&category=BEST_PRACTICES&key={PKEY}"], 80)
    try:
        d = json.loads(out)
        if "lighthouseResult" not in d:
            return None
        cat = d["lighthouseResult"]["categories"]
        au = d["lighthouseResult"]["audits"]
        res = {
            "perf": round(cat["performance"]["score"] * 100),
            "seo": round(cat["seo"]["score"] * 100),
            "a11y": round(cat["accessibility"]["score"] * 100),
            "bp": round(cat["best-practices"]["score"] * 100),
            "lcp": round(au.get("largest-contentful-paint", {})
                         .get("numericValue", 0) / 1000, 1),
            "cls": round(au.get("cumulative-layout-shift", {})
                         .get("numericValue", 0), 3),
            "poids_kb": round(au.get("total-byte-weight", {})
                              .get("numericValue", 0) / 1024),
        }
        json.dump(res, open(cf, "w", encoding="utf-8"))
        return res
    except Exception as e:
        log(f"LH parse err {r['slug']}: {e}")
        return None

sites = [r for r in restos if r["bucket"] in ("eatbu", "autre-site")]
log(f"ETAPE 3: Lighthouse sur {len(sites)} sites (lots de 4)...")
with ThreadPoolExecutor(max_workers=4) as ex:
    for r, lh in zip(sites, ex.map(lighthouse, sites)):
        r["lh"] = lh
for r in restos:
    r.setdefault("lh", None)

# === ETAPE 4 — Wayback CDX (cache TTL 90j) =========================
def wayback_age(r):
    cf = os.path.join(CACHE, "wayback", f"{r['slug']}.json")
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 90 * 86400:
        data = open(cf, encoding="utf-8").read()
    else:
        u = urllib.parse.quote(r["website"], safe="")
        data = curl(["-H", f"User-Agent: {UA}",
            f"https://web.archive.org/cdx/search/cdx?url={u}"
            f"&output=json&limit=1&from=2010"], 30)
        open(cf, "w", encoding="utf-8").write(data or "")
        time.sleep(0.4)
    try:
        j = json.loads(data)
        if len(j) > 1:
            ts = j[1][1]
            first = datetime.date(int(ts[:4]), int(ts[4:6]), 1)
            return round((datetime.date.today() - first).days / 365.25, 1)
    except Exception:
        pass
    return None

for r in sites:
    r["age"] = wayback_age(r)
for r in restos:
    r.setdefault("age", None)
log("ETAPE 4: Wayback termine")

# === ETAPE 5 — Exclusions (chaines deja faites + sites modernes) ===
for r in restos:
    if r["bucket"] == "autre-site" and r.get("lh"):
        if r["lh"]["perf"] >= 85 and r["lh"]["seo"] >= 85:
            r["bucket"] = "exclu-moderne"
log("ETAPE 5: " + str(dict(Counter(r["bucket"] for r in restos))))

# === ETAPE 6 — Scoring (scoring-formula.md, SOURCE DE VERITE) ======
def calc_valeur(r):
    b = r["bucket"]
    if b == "pas-de-site":
        return 90.0
    lh = r.get("lh")
    age = r.get("age")
    age = 2.0 if age is None else age              # defaut median
    gmb = r["gmb"] if r["gmb"] is not None else 50  # defaut median neutre
    if lh and not DEGRADE:
        v = (0.30 * (100 - lh["perf"]) + 0.25 * (100 - lh["seo"])
             + 0.10 * (100 - lh["a11y"]) + 0.15 * min(age * 10, 50)
             + 0.20 * (100 - gmb))
    else:                                          # mode degrade
        v = 0.43 * min(age * 10, 50) + 0.57 * (100 - gmb)
    if b == "autre-site":
        v -= 15
    return max(0.0, min(100.0, v))

def calc_proba(r):
    p = 0
    note = r["note"]
    if note is not None:
        p += 25 if note >= 4.0 else (10 if note >= 3.5 else 0)
    # note absente -> traiter < 3.5 -> 0 (conservateur)
    avis = r["avis"]
    if avis is None:
        p += 5                                     # < 20 -> +5 (conservateur)
    else:
        p += 20 if avis >= 100 else (15 if avis >= 50 else
                                     (10 if avis >= 20 else 5))
    # repond aux avis : non mesure -> 0 ; Instagram : non detecte -> 0
    if r["gmb"] is not None and r["gmb"] >= 65:    # proxy "fiche complete"
        p += 15
    age = r.get("age")
    if r["bucket"] == "eatbu" and age is not None:
        if age >= 3:
            p += 10
        if age < 0.5:
            p -= 20
    return max(0, min(100, p))

scored = [r for r in restos if r["bucket"] in ("eatbu", "autre-site", "pas-de-site")]
for r in scored:
    r["valeur"] = round(calc_valeur(r))
    r["proba"] = round(calc_proba(r))
    r["score"] = round(0.5 * r["valeur"] + 0.5 * r["proba"])
    r["tier"] = "A" if r["score"] >= 75 else ("B" if r["score"] >= 50 else "C")
    # drapeau rouge (argument-library.md)
    fl = "aucun"
    age = r.get("age")
    if age is not None and age < 0.5:
        fl = "Site tres recent (<6 mois) : vient d'investir, refusera. Ne pas visiter avant 12 mois."
    elif r["note"] is not None and r["note"] < 3.5:
        fl = "Note Google basse : sujet sensible, ne pas aborder le site frontalement."
    elif (r["bucket"] == "autre-site" and r.get("lh")
          and 70 <= r["lh"]["perf"] <= 84):
        fl = "Site deja correct : plus dur a convaincre, garder pour quand tu seras rode."
    r["drapeau"] = fl
    # donnees partielles : note/avis/gmb non mesures (Places indispo)
    r["partiel"] = (r["note"] is None and r["avis"] is None
                    and r["gmb"] is None and r["bucket"] != "pas-de-site")
log(f"ETAPE 6: {len(scored)} restos scores")

# === ETAPE 7 — Sync restaurants.yml + vues =========================
def args_pitch(r):
    lh = r.get("lh")
    a = []
    if lh and lh["perf"] < 50:
        a.append(f"Son site charge en {float(lh['lcp']):.1f}s sur mobile (score "
                 f"vitesse {lh['perf']}/100) : ~30 % des visiteurs partent avant "
                 f"d'avoir vu le menu. On peut le rendre instantane.")
    if r["bucket"] == "eatbu":
        a.append(f"Son adresse web est `{r['website']}` : un client voit tout "
                 f"de suite qu'il loue son site. Un resto comme le sien merite "
                 f"sa propre adresse, a lui, a vie.")
    if lh and lh["seo"] < 60:
        cu = r["cuisine"] or "resto"
        a.append(f"SEO {lh['seo']}/100 : sur 'restaurant {cu} Chartres' il est "
                 f"introuvable. Le client va chez un autre sans savoir qu'il existe.")
    if r["bucket"] == "pas-de-site" and r.get("agg"):
        a.append(f"Sa seule presence web est une page {r['agg']} : il ne possede "
                 f"rien, ni le site ni l'adresse. Un client qui tombe la-dessus ne "
                 f"voit pas SON resto. On lui fait un vrai site a lui, a vie.")
    elif r["bucket"] == "pas-de-site":
        a.append("Aucun site : invisible sur Google hors de sa fiche. Les clients "
                 "veulent voir le menu et l'ambiance avant de se deplacer.")
    age = r.get("age")
    if age is not None and age >= 3:
        a.append(f"Site qui date (~{age} ans sans refonte visible). Une remise "
                 f"a neuf se verrait immediatement face au resto d'a cote.")
    if lh and 50 <= lh["perf"] < 75 and not any("vitesse" in x for x in a):
        a.append(f"Son site traine ({lh['perf']}/100). Le passer au vert = "
                 f"1-2 s gagnees, et chaque seconde compte sur mobile.")
    if r["gmb"] is not None and r["gmb"] < 50:
        a.append("Sa fiche Google est sous-exploitee (peu de photos / pas de "
                 "description). On l'optimise en meme temps que le site, inclus.")
    if not a:
        a = ["Presence numerique en dessous de ce que MB Studio livre "
             "(details a confirmer sur place)."]
    return a[:3]

# Decision Mike 2026-05-17 : 3 listes SEPAREES, chacune avec un bloc
# « Criteres de cette liste » (definition + angle strategique + tri annonce),
# tri propre par liste, fiches a libelles francais. JAMAIS de top global melange.
CRITERES = {
 "eatbu": {
   "def": "Site hébergé sur **eatbu.com** — adresse louée, modèle mutualisé "
          "identique à des milliers d'autres restos. Le patron ne possède ni "
          "le site, ni vraiment son adresse.",
   "angle": "C'est le pitch le plus fort de MB Studio. Lui montrer que "
            "`son-nom.eatbu.com` crie « site loué », que si eatbu ferme ou "
            "augmente il perd tout, et qu'on lui fait un site **à lui, à vie, "
            "qu'il modifie seul**. Ces restos sortent souvent en Tier C "
            "(mécanique de la formule) mais c'est LE cœur de cible : juge à la "
            "stratégie, pas au tier brut.",
   "tri": "du site **le plus mauvais au moins mauvais** (sous-score « ce qu'on "
          "peut lui apporter » décroissant) — commence par ceux où la "
          "démonstration sera la plus parlante.",
 },
 "autre-site": {
   "def": "A déjà **son propre site** (autre qu'eatbu, et pas une simple page "
          "de plateforme). Le patron a déjà investi dans une présence web.",
   "angle": "Plus dur à convaincre (il a déjà payé un site). Ne jamais "
            "critiquer frontalement : s'appuyer sur des **chiffres mesurés** "
            "(vitesse, SEO) et le gain concret visible. Si le site est déjà "
            "correct, le garder pour quand tu seras rodé.",
   "tri": "du site **le plus faible au moins faible** (sous-score « ce qu'on "
          "peut lui apporter » décroissant).",
 },
 "pas-de-site": {
   "def": "**Aucun site à lui** : soit rien du tout, soit seulement une page "
          "agrégateur / livraison / réseau social (UberEats, Deliveroo, "
          "Facebook…). Aucune vitrine web qui lui appartienne.",
   "angle": "**Valeur maximale** : on part de zéro, tout est gain et tout est "
            "bien fait du premier coup. Cible prime. Beaucoup d'avis Google = "
            "resto établi, qui tourne, capable d'investir 490 €.",
   "tri": "par **nombre d'avis Google décroissant** (la popularité prouve la "
          "santé du resto et sa capacité à payer).",
 },
}

def presence_web(r):
    if r["bucket"] == "eatbu":
        return f"Site **eatbu** (loué) — {r['website']}"
    if r["bucket"] == "autre-site":
        return f"Site perso — {r['website']}"
    if r.get("agg"):
        return f"**Aucun site à lui** — seulement une page **{r['agg']}**"
    return "**Aucune présence web** (hors fiche Google)"

def fiche(r, n):
    cu = r["cuisine"] or "cuisine non précisée"
    note = "note non mesurée" if r["note"] is None else f"{r['note']}"
    avis = "?" if r["avis"] is None else r["avis"]
    L = [f"### {n}. {r['nom']} — {cu} — ⭐ {note} / {avis} avis", "",
         f"**Adresse :** {r['rue'] or 'inconnue'}, {r['cp']} {r['ville']} · "
         f"**Téléphone :** {r['tel'] or 'inconnu'}",
         f"**Présence web actuelle :** {presence_web(r)}"]
    lh = r.get("lh")
    if r["bucket"] in ("eatbu", "autre-site"):
        if lh:
            L.append(f"**Vitesse du site actuel :** {float(lh['lcp']):.1f} s "
                     f"pour s'afficher sur mobile (score vitesse "
                     f"{lh['perf']}/100)")
        else:
            L.append("**Vitesse du site actuel :** non mesurée "
                     "(site injoignable au test)")
    L += [f"**Ce qu'on peut lui apporter :** {r['valeur']}/100",
          f"**Probabilité qu'il accepte :** {r['proba']}/100 — "
          f"**Tier {r['tier']}**", "",
          "**Les 3 arguments concrets à lui dire :**"]
    L += [f"{i}. {a}" for i, a in enumerate(args_pitch(r), 1)]
    L.append("")
    if r["partiel"]:
        L.append("> ℹ️ Note/avis/fiche Google non mesurés pour ce resto — "
                 "sous-score « probabilité » approximatif.")
    if DEGRADE or (not lh and r["bucket"] in ("eatbu", "autre-site")):
        L.append("> ⚠️ Vitesse non mesurée — sous-score « valeur » approximatif.")
    L += [f"**Drapeau rouge :** {r['drapeau']}", "", "---", ""]
    return "\n".join(L) + "\n"

def entete_liste(bucket, titre, n):
    c = CRITERES[bucket]
    return (f"# {titre}\n\n"
            f"**Chartres — rayon 5 km — {DATE}** · {n} restaurants\n\n"
            f"## 📋 Critères de cette liste\n\n"
            f"- **Ce qui définit cette catégorie :** {c['def']}\n\n"
            f"- **Angle stratégique (pourquoi / comment pitcher ce type) :** "
            f"{c['angle']}\n\n"
            f"- **Tri de cette liste :** {c['tri']}\n\n---\n\n")

def md_to_txt(md):
    out = []
    for ln in md.splitlines():
        s = re.sub(r"^#{1,6}\s*", "", ln).replace("**", "").replace("`", "")
        s = re.sub(r"^>\s?", "  ", s)
        out.append("-" * 60 if s.strip() == "---" else s)
    return "\n".join(out)

def ecrire_liste(bucket, base, titre):
    lst = [r for r in scored if r["bucket"] == bucket]
    if bucket == "pas-de-site":                 # popularite : avis decroissant
        lst.sort(key=lambda x: (-(x["avis"] if x["avis"] is not None else -1),
                                -(x["note"] or 0)))
    else:                                       # site le plus mauvais d'abord
        lst.sort(key=lambda x: (-x["valeur"], -x["score"]))
    md = entete_liste(bucket, titre, len(lst))
    for i, r in enumerate(lst, 1):
        md += fiche(r, i)
    open(os.path.join(OUT, base + ".md"), "w", encoding="utf-8").write(md)
    open(os.path.join(OUT, base + ".txt"), "w", encoding="utf-8").write(
        md_to_txt(md))
    return lst

# nettoyage des anciens noms de fichiers (format pre-2026-05-17)
for old in ("prospects-avec-site-eatbu.md", "prospects-avec-site-autre.md",
            "prospects-sans-site.md"):
    op = os.path.join(OUT, old)
    if os.path.exists(op):
        os.remove(op)

L_e = ecrire_liste("eatbu", "liste-eatbu", "Prospects — site eatbu (loué)")
L_a = ecrire_liste("autre-site", "liste-autre-site",
                   "Prospects — site perso existant")
L_s = ecrire_liste("pas-de-site", "liste-sans-site",
                   "Prospects — sans site à eux")
n_e, n_a, n_s = len(L_e), len(L_a), len(L_s)

exc = [r for r in restos if r["bucket"].startswith("exclu")]
with open(os.path.join(OUT, "prospects-exclus.md"), "w", encoding="utf-8") as f:
    f.write(f"# Prospects exclus — Chartres, {DATE}\n\n{len(exc)} exclus.\n\n")
    for r in sorted(exc, key=lambda x: x["nom"].lower()):
        raison = ("Chaîne nationale (pas la main sur son site)"
                  if r["bucket"] == "exclu-chaine"
                  else "Site custom moderne (Lighthouse ≥85 perf+SEO, rien à apporter)")
        f.write(f"- **{r['nom']}** — {raison}\n")

# tableau-recap.csv (en-tete = template)
hdr = open(os.path.join(ROOT, "skills", "scoring-prospects", "templates",
                        "tableau-recap.csv"), encoding="utf-8").read().strip().splitlines()[0]
def csv_cell(x):
    return str(x).replace(",", " ").replace("\n", " ") if x is not None else ""
with open(os.path.join(OUT, "tableau-recap.csv"), "w", encoding="utf-8") as f:
    f.write(hdr + "\n")
    for r in sorted(scored, key=lambda x: -x["score"]):
        lh = r.get("lh") or {}
        f.write(",".join(csv_cell(x) for x in [
            r["nom"], r["bucket"], r["tier"], r["score"], r["valeur"], r["proba"],
            r["rue"], r["cp"], r["ville"], r["tel"], r["website"], r["cuisine"],
            r["note"], r["avis"], lh.get("perf"), lh.get("seo"), lh.get("a11y"),
            lh.get("bp"), lh.get("lcp"), lh.get("cls"), r.get("age"),
            r["gmb"] if r["gmb"] is not None else 50,
            "non mesuré", "non détecté",
            "oui" if (DEGRADE or (not r.get("lh") and r["bucket"] != "pas-de-site")) else "non",
            "oui" if r["partiel"] else "non", r["drapeau"], "", ""]) + "\n")

# --- Sync restaurants.yml : preserve header+_modele + tunnel/notes/override ---
yml_path = os.path.join(PROS, "restaurants.yml")
raw = open(yml_path, encoding="utf-8").read()
parsed = yaml.safe_load(raw) or {}
prev = {}
for e in parsed.get("restaurants", []):
    if e.get("id") and e["id"] != "_modele":
        prev[e["id"]] = e

# preamble verbatim = tout jusqu'a la fin du bloc _modele (avant 1er vrai id)
lines = raw.splitlines()
end = len(lines)
in_modele = False
for i, ln in enumerate(lines):
    if re.match(r"\s*-\s+id:\s*_modele", ln):
        in_modele = True
        continue
    if in_modele and re.match(r"\s*-\s+id:\s*(?!_modele)", ln):
        end = i
        break
preamble = "\n".join(lines[:end]).rstrip() + "\n"

def y(s):
    if s is None:
        return "null"
    return '"' + str(s).replace('"', "'") + '"'

def emit(r):
    p = prev.get(r["slug"], {})
    sc = p.get("scoring", {}) or {}
    ov = sc.get("mike_override")
    tn = p.get("tunnel", {}) or {}
    nm = p.get("notes_mike", "")
    site = r["website"] or ("aucun (présence " + r["agg"] + ")"
                            if r.get("agg") else "aucun")
    note = "null" if r["note"] is None else r["note"]
    avis = "null" if r["avis"] is None else r["avis"]
    gmb = "null" if r["gmb"] is None else r["gmb"]
    lhm = "null" if not r.get("lh") else r["lh"]["perf"]
    age = "null" if r.get("age") is None else r["age"]
    if ov is None:
        ov_s = "null"
    else:
        ov_s = ("{ score: " + str(ov.get("score"))
                + ", raison: " + y(ov.get("raison")) + " }")
    hist = tn.get("historique", []) or []
    hist_s = "[]" if not hist else yaml.safe_dump(
        hist, allow_unicode=True, default_flow_style=True).strip()
    return f"""
  - id: {r['slug']}

    identite:
      nom: {y(r['nom'])}
      adresse: {y(r['rue'] or 'inconnue')}
      cp: {y(r['cp'] or '28000')}
      ville: {y(r['ville'])}
      telephone: {y(r['tel'] or 'inconnu')}
      cuisine: {y(r['cuisine'] or 'inconnue')}
      site_actuel: {y(site)}

    scan:
      date_scan: {DATE}
      note_google: {note}
      nb_avis: {avis}
      gmb_completude: {gmb}
      lighthouse_mobile: {lhm}
      age_site_ans: {age}
      source_donnees: "osm+pagespeed+wayback"

    scoring:
      score: {r['score']}
      tier: {r['tier']}
      valeur: {r['valeur']}
      proba: {r['proba']}
      drapeau_rouge: {y(r['drapeau'])}
      mike_override: {ov_s}

    tunnel:
      statut: {tn.get('statut', 'a_qualifier')}
      historique: {hist_s}
      argument_qui_a_converti: {y(tn.get('argument_qui_a_converti'))}
      raison_perte: {y(tn.get('raison_perte'))}

    notes_mike: {y(nm) if nm else '""'}
"""

body = "".join(emit(r) for r in sorted(scored, key=lambda x: -x["score"]))
open(yml_path, "w", encoding="utf-8").write(preamble + body)

# --- restaurants.csv : vue plate vivante (en-tete existant) --------
csv_path = os.path.join(PROS, "restaurants.csv")
csv_hdr = open(csv_path, encoding="utf-8").read().strip().splitlines()[0]
with open(csv_path, "w", encoding="utf-8") as f:
    f.write(csv_hdr + "\n")
    for r in sorted(scored, key=lambda x: -x["score"]):
        f.write(",".join(csv_cell(x) for x in [
            r["slug"], r["nom"], r["ville"], r["cuisine"],
            r["website"] or "aucun", r["note"], r["avis"],
            r["gmb"] if r["gmb"] is not None else 50,
            r["lh"]["perf"] if r.get("lh") else "",
            r.get("age"), r["score"], r["tier"], r["valeur"], r["proba"],
            "a_qualifier", r["drapeau"], DATE, "", ""]) + "\n")

# --- Recap (1 tete par liste, JAMAIS de top global melange) ---
tiers = Counter(r["tier"] for r in scored)
log("="*60)
log(f"SCORING TERMINE — Chartres 5 km — {len(scored)} scores, {len(exc)} exclus")
log(f"  eatbu={n_e}  autre-site={n_a}  pas-de-site={n_s}")
log(f"  tiers: A={tiers['A']} B={tiers['B']} C={tiers['C']}")
log(f"  Places: {'OK' if PLACES_OK else 'INDISPONIBLE (defauts conformes)'}")
log("  Tete de chaque liste (selon le tri propre a la liste) :")
for nom_liste, L in (("eatbu", L_e), ("autre-site", L_a),
                     ("sans-site", L_s)):
    if L:
        t = L[0]
        log(f"   [{nom_liste}] {t['nom']} — valeur {t['valeur']}/100, "
            f"proba {t['proba']}/100, Tier {t['tier']}")
log("="*60)
print("DONE")
LOG.close()
