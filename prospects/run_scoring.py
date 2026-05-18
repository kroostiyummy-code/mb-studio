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
import math
from concurrent.futures import ThreadPoolExecutor
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROS = os.path.join(ROOT, "prospects")
CACHE = os.path.join(PROS, "cache")
# Campagne = date du scan (les donnees viennent du cache du 2026-05-17).
# Recalcul de score depuis le cache => on garde le meme snapshot, pas de re-scan.
# Surchargable : MB_CAMPAGNE=YYYY-MM-DD pour un nouveau scan date.
DATE = os.environ.get("MB_CAMPAGNE", "2026-05-17")
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

# === ETAPE 6 — Scoring Couche 1 (scoring-formula.md, SOURCE DE VERITE) ===
# Refonte decision Mike 2026-05-18. Baremes deterministes (recalcul cache OK).

# Charge l'etat precedent de restaurants.yml : override + couche2 + tunnel/notes
# DOIVENT survivre au recalcul (jamais ecrases par l'outil).
COUCHE2_COLS = ["cta_appel", "cta_itineraire", "cta_resa", "menu_facile",
                "photos_exploitables", "instagram_actif", "repond_avis",
                "ecart_concurrentiel", "angle_approche", "commentaire_manuel"]
yml_path = os.path.join(PROS, "restaurants.yml")
raw = open(yml_path, encoding="utf-8").read()
parsed = yaml.safe_load(raw) or {}
PREV = {e["id"]: e for e in parsed.get("restaurants", [])
        if e.get("id") and e["id"] != "_modele"}

# --- Normalisation [verbatim] ---
def clip(x):
    return min(max(x, 0.0), 1.0)

def inv_score(x, good, poor):
    return clip((good - x) / (good - poor))

def log_cap(n, cap):
    return clip(math.log(1 + n) / math.log(1 + cap))

def rating_norm(r):
    return clip((r - 4.0) / 0.7)

SAAS = ("wixsite.", "wix.com", "sitew.", "grubkit.", "jimdo.", "jimdofree.",
        "wordpress.com", "business.site", "godaddysites.", "weebly.",
        "webnode.", "e-monsite.", "site123.", "strikingly.", "mozello.",
        "myshopify.", "wixsite", "pages.dev", "github.io")

# === ETAPE 5bis — DOM fetch leger (conversion + seo + contact), cache ===
os.makedirs(os.path.join(CACHE, "dom"), exist_ok=True)
CTA_KW = ("reserver", "commander", "reservation", "order", "booking", "resa")

def dom_fetch(r):
    """Homepage + /robots.txt + /sitemap.xml. Cache 30j. Sites only."""
    cf = os.path.join(CACHE, "dom", f"{r['slug']}.json")
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 30 * 86400:
        try:
            return json.load(open(cf, encoding="utf-8"))
        except Exception:
            pass
    url = r["website"]
    sp = urllib.parse.urlsplit(url if "://" in url else "http://" + url)
    origin = f"{sp.scheme or 'http'}://{sp.netloc}"
    html = curl(["-L", "--max-filesize", "2000000", "-H", f"User-Agent: {UA}",
                 url], 15)[:500000]
    d = {"fetched": False}
    if not html or len(html) < 80:
        json.dump(d, open(cf, "w", encoding="utf-8"))
        return d
    robots = curl(["-L", "-H", f"User-Agent: {UA}",
                   origin + "/robots.txt"], 10)
    sm = curl(["-L", "-I", "-H", f"User-Agent: {UA}",
               origin + "/sitemap.xml"], 10)
    low = strip_accents(html).lower()
    txt = strip_accents(re.sub(r"<[^>]+>", " ", html)).lower()
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
    md = re.search(r'<meta[^>]+name=["\']description["\'][^>]*'
                   r'content=["\'](.*?)["\']', html, re.I | re.S)
    h1 = ""
    mh = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if mh:
        h1 = strip_accents(re.sub(r"<[^>]+>", " ", mh.group(1))).lower()
    cuis = strip_accents((r["cuisine"] or "")).lower().split(";")[0]
    robots_low = (robots or "").lower()
    blanket = bool(re.search(r"(?mi)^\s*disallow:\s*/\s*$", robots_low)
                   and "user-agent: *" in robots_low)
    sitemap_ok = ("200" in (sm or "").split("\n")[0]
                  or "sitemap:" in robots_low)
    robots_fetched = bool(robots)
    conv = {
        "tel": bool(re.search(r'href=["\']?tel:', html, re.I)),
        "map": bool(re.search(r"(maps\.google|google\.[a-z.]+/maps|"
                              r"goo\.gl/maps|openstreetmap\.org)", low)),
        "cta": any(k in txt for k in CTA_KW),
        "menu": bool(re.search(r'href=["\'][^"\']*(menu|carte)', low)
                     or re.search(r">[^<]*\b(menu|la carte)\b[^<]*<", txt)),
        "addr": bool(re.search(r"\b28\d{3}\b", txt)
                     or ("chartres" in txt and re.search(
                         r"\b(rue|avenue|boulevard|place|impasse)\b", txt))),
        "hours": bool("horaire" in txt or "ouvert" in txt or re.search(
            r"(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)[^<]{0,40}"
            r"\d{1,2}\s?[h:]", txt)),
    }
    seo = {
        "title": 10 <= len(title) <= 65,
        "meta": bool(md) and 50 <= len(md.group(1).strip()) <= 160,
        "h1": bool(mh),
        "canonical": bool(re.search(r'rel=["\']canonical["\']', html, re.I)),
        "indexable": not re.search(r'name=["\']robots["\'][^>]*noindex',
                                   html, re.I) and not blanket,
        "sitemap": sitemap_ok,
        "schema": bool(re.search(r"(localbusiness|\"@type\"\s*:\s*\""
                                 r"?restaurant|schema.org/restaurant)", low)),
        "geo": ("chartres" in strip_accents(title).lower()
                or "chartres" in h1
                or (cuis and (cuis in strip_accents(title).lower()
                              or cuis in h1))),
    }
    d = {"fetched": True, "conv": conv, "seo": seo,
         "robots_fetched": robots_fetched,
         "email": bool(re.search(r'href=["\']?mailto:', html, re.I)),
         "social": bool(re.search(r"(instagram\.com|facebook\.com)", low)),
         "date": DATE}
    json.dump(d, open(cf, "w", encoding="utf-8"))
    return d

sites_dom = ([] if os.environ.get("MB_NO_DOM") else
             [r for r in restos if r["bucket"] in ("eatbu", "autre-site")
              and r["website"]])
log(f"ETAPE 5bis: DOM fetch sur {len(sites_dom)} sites (cache 30j)...")
with ThreadPoolExecutor(max_workers=5) as ex:
    for r, dd in zip(sites_dom, ex.map(dom_fetch, sites_dom)):
        r["dom"] = dd
for r in restos:
    r.setdefault("dom", None)
log("ETAPE 5bis: DOM termine")

# === ETAPE 6 — Scoring architecture normalisee (scoring-formula.md) ===
# Refonte Mike 2026-05-18 (Rapport_classement). Confidence + tiers A/B/C/D.
WV = {"presence": 25, "perf": 20, "conv": 20, "seo": 15, "lpg": 10, "rep": 10}
WP = {"bp": 35, "sw": 20, "con": 15, "tm": 15, "ind": 10, "cx": 5}
WTOT = sum(WV.values()) + sum(WP.values())          # 200

def presence_class(r):
    b = r["bucket"]
    if b == "pas-de-site":
        return ("agg", 0.90) if r.get("agg") else ("aucun", 1.00)
    if b == "eatbu":
        return ("eatbu", 0.80)
    host = strip_accents(r["website"]).lower()
    if any(s in host for s in SAAS):
        return ("saas", 0.65)
    return ("propre", 0.35)

def score_one(r):
    b = r["bucket"]
    lh = r.get("lh")
    dom = r.get("dom")
    perf = lh["perf"] if lh else None
    seo_s = lh["seo"] if lh else None
    note, avis = r["note"], r["avis"]
    obs = {}                                        # composante -> observee?
    pcls, presence_gap = presence_class(r)
    obs["presence"] = True
    # business_proof
    if note is not None and avis is not None:
        business_proof = 0.55 * rating_norm(note) + 0.45 * log_cap(avis, 300)
        obs["bp"] = True
    else:
        business_proof = 0.50
        obs["bp"] = False
    # performance_gap
    if b == "pas-de-site":
        performance_gap = 0.60
        obs["perf"] = True
    elif perf is not None:
        performance_gap = inv_score(perf, 85, 40)
        obs["perf"] = True
    else:
        performance_gap = 0.50
        obs["perf"] = False
    # conversion_gap
    if b == "pas-de-site":
        conversion_gap = 0.90
        obs["conv"] = True
    elif dom and dom.get("fetched"):
        c = dom["conv"]
        present = (0.20 * c["tel"] + 0.15 * c["map"] + 0.25 * c["cta"]
                   + 0.20 * c["menu"] + 0.10 * c["addr"] + 0.10 * c["hours"])
        conversion_gap = clip(1 - present)
        obs["conv"] = True
    else:
        conversion_gap = 0.50
        obs["conv"] = False
    # seo_gap
    if b == "pas-de-site":
        seo_gap = 0.90
        obs["seo"] = True
    elif dom and dom.get("fetched") and seo_s is not None:
        s = dom["seo"]
        seo_checks = sum(1 for v in s.values() if v) / len(s)
        seo_gap = 0.60 * (1 - seo_checks) + 0.40 * inv_score(seo_s, 85, 50)
        obs["seo"] = bool(dom.get("robots_fetched"))   # sous-signal manquant -> non observe
    else:
        seo_gap = 0.50
        obs["seo"] = False
    # local_profile_gap : signaux Places non persistes -> partiellement aveugle
    places_ok = (note is not None or avis is not None or r["gmb"] is not None)
    pc = [1 if r["website"] else 0, 1 if r["tel"] else 0,
          0, 0,                                     # hours/photos non recuperables
          1 if note is not None else 0,
          1 if avis is not None else 0]
    if places_ok:
        local_profile_gap = clip(1 - sum(pc) / len(pc))
    else:
        local_profile_gap = 0.50
    obs["lpg"] = False                              # signaux Places incomplets (honnete)
    # digital_deficit + reputation_misalignment
    digital_deficit = (presence_gap + performance_gap + conversion_gap) / 3
    reputation_misalignment = business_proof * digital_deficit
    obs["rep"] = obs["bp"] and obs["perf"] and obs["conv"]
    V = (WV["presence"] * presence_gap + WV["perf"] * performance_gap
         + WV["conv"] * conversion_gap + WV["seo"] * seo_gap
         + WV["lpg"] * local_profile_gap + WV["rep"] * reputation_misalignment)
    # switchability
    if pcls == "aucun":
        switchability, obs["sw"] = 1.00, True
    elif pcls == "agg":
        switchability, obs["sw"] = 0.90, True
    elif pcls == "eatbu":
        switchability, obs["sw"] = 0.85, True
    elif pcls == "saas":
        switchability, obs["sw"] = 0.75, True
    elif perf is not None:
        switchability = 0.55 if perf < 60 else 0.20
        obs["sw"] = True
    else:
        switchability, obs["sw"] = 0.50, False
    # contactability
    phone_known = 1.0 if r["tel"] else 0.0
    if dom and dom.get("fetched"):
        email_t = 1.0 if dom.get("email") else 0.5
        social_t = 1.0 if dom.get("social") else 0.5
        obs["con"] = True
    else:
        email_t = social_t = 0.5
        obs["con"] = bool(r["tel"])
    contactability = 0.50 * phone_known + 0.25 * email_t + 0.25 * social_t
    # timing
    age = r.get("age")
    if age is not None and age < 0.5:
        timing = 0.15
    elif b == "pas-de-site":
        timing = 0.80
    elif b == "eatbu":
        timing = 0.65
    else:
        timing = 0.50
    obs["tm"] = True
    # independence / complexity : observables seulement si site a inspecter
    if b == "pas-de-site":
        independence = complexity = 0.50
        obs["ind"] = obs["cx"] = False
    else:
        independence = complexity = 1.00
        obs["ind"] = obs["cx"] = True
    P = (WP["bp"] * business_proof + WP["sw"] * switchability
         + WP["con"] * contactability + WP["tm"] * timing
         + WP["ind"] * independence + WP["cx"] * complexity)
    final = 0.55 * V + 0.45 * P
    obs_w = (sum(WV[k] for k in WV if obs.get(k))
             + sum(WP[k] for k in WP if obs.get(k)))
    confidence = round(100 * obs_w / WTOT)
    r["_comp"] = {"presence_gap": round(presence_gap, 3),
                  "performance_gap": round(performance_gap, 3),
                  "conversion_gap": round(conversion_gap, 3),
                  "seo_gap": round(seo_gap, 3),
                  "local_profile_gap": round(local_profile_gap, 3),
                  "business_proof": round(business_proof, 3),
                  "switchability": switchability, "timing": timing,
                  "reputation_misalignment": round(reputation_misalignment, 3)}
    return (round(V, 1), round(P, 1), round(final, 1), confidence, pcls)

scored = [r for r in restos
          if r["bucket"] in ("eatbu", "autre-site", "pas-de-site")]
for r in scored:
    V, P, final, conf, pcls = score_one(r)
    r["valeur"] = round(V)
    r["proba"] = round(P)
    r["valeur_f"] = V
    r["proba_f"] = P
    r["confidence"] = conf
    r["presence_cls"] = pcls
    ov = (PREV.get(r["slug"], {}).get("scoring", {}) or {}).get("mike_override")
    if ov and ov.get("score") is not None:
        r["score"] = ov["score"]
        r["override"] = ov
    else:
        r["score"] = round(final)
        r["override"] = None
    r["score_f"] = final
    s = r["score"]
    if s >= 75 and conf >= 60:
        r["tier"] = "A"
    elif s >= 65:
        r["tier"] = "B"
    elif s >= 55:
        r["tier"] = "C"
    else:
        r["tier"] = "D"
    cp = r["_comp"]
    note, avis = r["note"], r["avis"]
    if cp["presence_gap"] >= 0.80 and r.get("override") is None and (
            avis or 0) >= 50:
        lbl = {"aucun": "aucun site à lui", "agg": f"juste une page {r.get('agg')}",
               "eatbu": "site eatbu loué"}.get(pcls, "présence web faible")
        r["pourquoi"] = (f"{note if note is not None else '?'}/"
                         f"{avis if avis is not None else '?'} avis mais {lbl}")
    elif cp["performance_gap"] >= 0.7 and r["bucket"] != "pas-de-site":
        r["pourquoi"] = (f"site lent (perf "
                         f"{r['lh']['perf'] if r.get('lh') else '?'}/100)")
    elif cp["conversion_gap"] >= 0.7 and r["bucket"] != "pas-de-site":
        r["pourquoi"] = ("site sans appel à l'action clair (ni réservation, "
                         "ni menu, ni tel visible)")
    elif cp["seo_gap"] >= 0.7 and r["bucket"] != "pas-de-site":
        r["pourquoi"] = "site mal référencé localement (SEO faible)"
    else:
        r["pourquoi"] = "présence numérique en dessous de ce qu'on livre"
    fl = "aucun"
    age = r.get("age")
    if age is not None and age < 0.5:
        fl = ("Site très récent (<6 mois) : vient d'investir. "
              "Ne pas visiter avant 12 mois.")
    elif note is not None and note < 3.5:
        fl = "Note Google basse : sujet sensible, ne pas aborder frontalement."
    if conf < 50:
        fl = (fl + " · " if fl != "aucun" else "") + \
            "Confiance faible (données incomplètes) — à vérifier sur place."
    r["drapeau"] = fl
    r["partiel"] = conf < 60
    pc2 = (PREV.get(r["slug"], {}) or {}).get("couche2", {}) or {}
    r["couche2"] = {c: pc2.get(c, "") for c in COUCHE2_COLS}
log(f"ETAPE 6: {len(scored)} restos scores (archi normalisee 2026-05-18)")

# === ETAPE 7 — Sync restaurants.yml + 5 vues =======================
# Decision Mike 2026-05-18 : scoring 2 couches + CLASSEMENT GLOBAL.
# Remplace la decision 2026-05-17 « jamais de classement global » :
# Vue 1 = classement global par score_final (radar principal),
# Vues 2/3/4 = filtres par categorie, Vue 5 = quick wins.
CRITERES = {
 "global": {
   "def": "TOUS les restos scorables de l'agglo, toutes catégories "
          "confondues (eatbu, site perso, sans site).",
   "angle": "Le radar principal : qui attaquer en premier, indépendamment "
            "de la catégorie. La vue à ouvrir en premier.",
   "tri": "par **score final décroissant** (valeur 55 % + probabilité 45 %).",
 },
 "eatbu": {
   "def": "Site hébergé sur **eatbu.com** — adresse louée, modèle mutualisé "
          "identique à des milliers de restos. Le patron ne possède ni le "
          "site, ni vraiment son adresse. **C'est le CŒUR DE CIBLE de "
          "MB Studio.**",
   "angle": "**Liste de travail stratégique de 1er rang — à travailler EN "
            "PARALLÈLE du classement global**, même si le score objectif y "
            "est plus bas. Mécanique normale et assumée : un eatbu a moins "
            "de déficit brut qu'un sans-site, donc un score plus bas — le "
            "scoring reste volontairement objectif, on ne le truque pas. "
            "Mais ici le **pitch est le plus fort** : « vous louez votre "
            "site, il est lent, il n'est pas à vous » ; et c'est la "
            "**transformation la plus visible à raconter** (avant/après "
            "spectaculaire, futur ambassadeur).",
   "tri": "par **score final décroissant**. ⚠️ Sur CETTE liste, ne juge "
          "pas au score seul : il est structurellement plus bas qu'un "
          "sans-site — c'est une liste de pitch, pas un classement de "
          "valeur brute.",
 },
 "autre-site": {
   "def": "A déjà **son propre site** (autre qu'eatbu, pas une page de "
          "plateforme). Le patron a déjà investi.",
   "angle": "Plus dur à convaincre. Ne pas critiquer frontalement : "
            "s'appuyer sur des **chiffres mesurés** (vitesse, SEO) et le gain "
            "concret visible.",
   "tri": "par **score final décroissant**.",
 },
 "pas-de-site": {
   "def": "**Aucun site à lui** : rien, ou seulement une page agrégateur / "
          "livraison / réseau social.",
   "angle": "**Valeur maximale** : on part de zéro, tout est gain. Beaucoup "
            "d'avis Google = resto établi, capable d'investir 490 €.",
   "tri": "par **score final décroissant**.",
 },
 "quickwins": {
   "def": "La **bande « Priorité semaine »** : le top ~10 du classement "
          "global, hors confiance faible. Ta liste d'attaque immédiate.",
   "angle": "Ce sont les cibles à voir cette semaine : meilleur score final "
            "ET confiance suffisante. Commence strictement par ici, dans "
            "l'ordre.",
   "tri": "par **score final décroissant, puis confiance décroissante**.",
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

def lighthouse_str(r):
    lh = r.get("lh")
    if lh:
        return (f"performance {lh['perf']}/100 · SEO {lh['seo']}/100 · "
                f"accessibilité {lh['a11y']}/100 · charge en "
                f"{float(lh['lcp']):.1f} s")
    if r["bucket"] == "pas-de-site":
        return "— (pas de site à mesurer)"
    return "non mesuré (site injoignable au test)"

def fiche(r, n):
    cu = r["cuisine"] or "cuisine non précisée"
    note = "note non mesurée" if r["note"] is None else f"{r['note']}"
    avis = "?" if r["avis"] is None else r["avis"]
    ov = " _(score corrigé à la main par Mike)_" if r.get("override") else ""
    adr = ", ".join(p for p in [r["rue"],
                                " ".join(x for x in [r["cp"], r["ville"]] if x)]
                     if p) or "adresse inconnue"
    L = [f"### {n}. {r['nom']} — {cu} — ⭐ {note} / {avis} avis", "",
         f"**Adresse :** {adr} · "
         f"**Téléphone :** {r['tel'] or 'inconnu'}",
         f"**Présence web :** {presence_web(r)}",
         f"**Lighthouse :** {lighthouse_str(r)}",
         f"**Ce qu'on peut apporter :** {r['valeur']}/100  ·  "
         f"**Probabilité qu'il accepte :** {r['proba']}/100",
         f"**Score final :** {r['score']}/100 · **Confiance : "
         f"{r['confidence']}/100** · **Tier {r['tier']}**{ov}",
         f"**Pourquoi lui :** {r['pourquoi']}",
         f"**Action :** {r['bande']}"]
    if r["partiel"]:
        L.append("> ℹ️ Note/avis/fiche Google non mesurés — sous-score "
                 "« probabilité » approximatif.")
    if DEGRADE or (not r.get("lh") and r["bucket"] in ("eatbu", "autre-site")):
        L.append("> ⚠️ Vitesse non mesurée — sous-score « valeur » approximatif.")
    if r["drapeau"] != "aucun":
        L.append(f"> 🚩 {r['drapeau']}")
    L += ["", "---", ""]
    return "\n".join(L) + "\n"

def entete(view_key, titre, n):
    c = CRITERES[view_key]
    return (f"# {titre}\n\n"
            f"**Chartres — rayon 5 km — {DATE}** · {n} restaurants\n\n"
            f"## 📋 Critères de cette liste\n\n"
            f"- **Ce qui définit cette liste :** {c['def']}\n\n"
            f"- **Angle stratégique (pourquoi / comment pitcher) :** "
            f"{c['angle']}\n\n"
            f"- **Tri de cette liste :** {c['tri']}\n\n---\n\n")

def md_to_txt(md):
    out = []
    for ln in md.splitlines():
        s = re.sub(r"^#{1,6}\s*", "", ln).replace("**", "").replace("`", "")
        s = re.sub(r"^>\s?", "  ", s)
        out.append("-" * 60 if s.strip() == "---" else s)
    return "\n".join(out)

def ecrire_vue(rows, base, titre, view_key):
    md = entete(view_key, titre, len(rows))
    for i, r in enumerate(rows, 1):
        md += fiche(r, i)
    open(os.path.join(OUT, base + ".md"), "w", encoding="utf-8").write(md)
    open(os.path.join(OUT, base + ".txt"), "w",
         encoding="utf-8").write(md_to_txt(md))

# nettoyage anciens noms de fichiers (formats anterieurs)
for old in ("prospects-avec-site-eatbu.md", "prospects-avec-site-autre.md",
            "prospects-sans-site.md"):
    op = os.path.join(OUT, old)
    if os.path.exists(op):
        os.remove(op)

def tri_score(x):                                   # final ↓ puis confidence ↓
    return (-x["score"], -x["confidence"], -x["valeur"])

classement = sorted(scored, key=tri_score)
# Bandes d'action par RANG global (decision Mike) :
# top ~10 = semaine, ~15 suivants = mois, reste = reserve ;
# confidence < 50 ecrase en « A surveiller ».
for i, r in enumerate(classement, 1):
    if r["confidence"] < 50:
        r["bande"] = "À surveiller (confiance faible)"
    elif i <= 10:
        r["bande"] = "Priorité semaine"
    elif i <= 25:
        r["bande"] = "Priorité mois"
    else:
        r["bande"] = "Réserve"
L_e = [r for r in classement if r["bucket"] == "eatbu"]
L_a = [r for r in classement if r["bucket"] == "autre-site"]
L_s = [r for r in classement if r["bucket"] == "pas-de-site"]
qw = [r for r in classement if r["bande"] == "Priorité semaine"]
n_e, n_a, n_s = len(L_e), len(L_a), len(L_s)

ecrire_vue(classement, "classement-global",
           "Classement global — toutes catégories", "global")
ecrire_vue(L_e, "liste-eatbu", "Filtre — site eatbu (loué)", "eatbu")
ecrire_vue(L_a, "liste-autre-site", "Filtre — site perso existant",
           "autre-site")
ecrire_vue(L_s, "liste-sans-site", "Filtre — sans site à eux", "pas-de-site")
ecrire_vue(qw, "quick-wins", "Priorité semaine — top à attaquer",
           "quickwins")

exc = [r for r in restos if r["bucket"].startswith("exclu")]
with open(os.path.join(OUT, "prospects-exclus.md"), "w",
          encoding="utf-8") as f:
    f.write(f"# Prospects exclus — Chartres, {DATE}\n\n{len(exc)} exclus.\n\n")
    for r in sorted(exc, key=lambda x: x["nom"].lower()):
        raison = ("Chaîne nationale (pas la main sur son site)"
                  if r["bucket"] == "exclu-chaine"
                  else "Site custom moderne (Lighthouse ≥85, rien à apporter)")
        f.write(f"- **{r['nom']}** — {raison}\n")

def csv_cell(x):
    return str(x).replace(",", " ").replace("\n", " ") if x is not None else ""

# tableau-recap.csv (campagne — en-tete = template, compat)
hdr = open(os.path.join(ROOT, "skills", "scoring-prospects", "templates",
           "tableau-recap.csv"), encoding="utf-8").read().strip(
           ).splitlines()[0]
with open(os.path.join(OUT, "tableau-recap.csv"), "w",
          encoding="utf-8") as f:
    f.write(hdr + "\n")
    for r in classement:
        lh = r.get("lh") or {}
        f.write(",".join(csv_cell(x) for x in [
            r["nom"], r["bucket"], r["tier"], r["score"], r["valeur"],
            r["proba"], r["rue"], r["cp"], r["ville"], r["tel"],
            r["website"], r["cuisine"], r["note"], r["avis"],
            lh.get("perf"), lh.get("seo"), lh.get("a11y"), lh.get("bp"),
            lh.get("lcp"), lh.get("cls"), r.get("age"),
            r["gmb"] if r["gmb"] is not None else "",
            "non mesuré", "non détecté",
            "oui" if (DEGRADE or (not r.get("lh")
                      and r["bucket"] != "pas-de-site")) else "non",
            "oui" if r["partiel"] else "non", r["drapeau"], "", ""]) + "\n")

# --- Sync restaurants.yml : preserve header+_modele + tunnel/notes/c2 ---
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
    p = PREV.get(r["slug"], {})
    tn = p.get("tunnel", {}) or {}
    nm = p.get("notes_mike", "")
    ov = r.get("override")
    site = r["website"] or ("aucun (présence " + r["agg"] + ")"
                            if r.get("agg") else "aucun")
    note = "null" if r["note"] is None else r["note"]
    avis = "null" if r["avis"] is None else r["avis"]
    gmb = "null" if r["gmb"] is None else r["gmb"]
    lhm = "null" if not r.get("lh") else r["lh"]["perf"]
    age = "null" if r.get("age") is None else r["age"]
    ov_s = ("null" if not ov else "{ score: " + str(ov.get("score"))
            + ", raison: " + y(ov.get("raison")) + " }")
    hist = tn.get("historique", []) or []
    hist_s = "[]" if not hist else yaml.safe_dump(
        hist, allow_unicode=True, default_flow_style=True).strip()
    c2 = r["couche2"]
    def c2v(k):
        return y(c2[k]) if c2[k] else '""'
    c2_s = "\n".join(f"      {k}: {c2v(k)}" for k in COUCHE2_COLS)
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
      source_donnees: "osm+pagespeed+wayback+places"

    scoring:
      valeur_apportable: {r['valeur']}
      proba_acceptation: {r['proba']}
      score_final: {r['score']}
      confidence: {r['confidence']}
      tier: {r['tier']}
      bande_action: {y(r['bande'])}
      pourquoi_lui: {y(r['pourquoi'])}
      drapeau_rouge: {y(r['drapeau'])}
      score: {r['score']}
      valeur: {r['valeur']}
      proba: {r['proba']}
      mike_override: {ov_s}

    couche2:                          # rempli A LA MAIN, jamais auto-calcule
{c2_s}

    tunnel:
      statut: {tn.get('statut', 'a_qualifier')}
      historique: {hist_s}
      argument_qui_a_converti: {y(tn.get('argument_qui_a_converti'))}
      raison_perte: {y(tn.get('raison_perte'))}

    notes_mike: {y(nm) if nm else '""'}
"""

body = "".join(emit(r) for r in classement)
open(yml_path, "w", encoding="utf-8").write(preamble + body)

# --- restaurants.csv : vue plate vivante (Couche 1 + Couche 2 vide) ---
csv_path = os.path.join(PROS, "restaurants.csv")
CSV_HDR = ("id,nom,ville,cuisine,site_actuel,note_google,nb_avis,"
           "gmb_completude,lighthouse_mobile,age_site_ans,valeur_apportable,"
           "proba_acceptation,score_final,confidence,tier,bande_action,"
           "pourquoi_lui,statut,drapeau_rouge,date_scan,"
           "argument_qui_a_converti,raison_perte," + ",".join(COUCHE2_COLS))
with open(csv_path, "w", encoding="utf-8") as f:
    f.write(CSV_HDR + "\n")
    for r in classement:
        tn = (PREV.get(r["slug"], {}) or {}).get("tunnel", {}) or {}
        f.write(",".join(csv_cell(x) for x in [
            r["slug"], r["nom"], r["ville"], r["cuisine"],
            r["website"] or ("agrégateur:" + r["agg"] if r.get("agg")
                             else "aucun"),
            r["note"], r["avis"],
            r["gmb"] if r["gmb"] is not None else "",
            r["lh"]["perf"] if r.get("lh") else "",
            r.get("age"), r["valeur"], r["proba"], r["score"],
            r["confidence"], r["tier"], r["bande"], r["pourquoi"],
            tn.get("statut", "a_qualifier"), r["drapeau"], DATE,
            tn.get("argument_qui_a_converti"), tn.get("raison_perte")]
            + [r["couche2"][c] for c in COUCHE2_COLS]) + "\n")

# --- Recap (classement global autorise depuis 2026-05-18) ---
tc = Counter(r["tier"] for r in scored)
import statistics as _st
sfs = [r["score"] for r in scored]
log("="*60)
log(f"SCORING TERMINE — Chartres 5 km — {len(scored)} scores, "
    f"{len(exc)} exclus")
log(f"  eatbu={n_e}  autre-site={n_a}  pas-de-site={n_s}  "
    f"semaine={len(qw)}")
log(f"  tiers: A={tc['A']} B={tc['B']} C={tc['C']} D={tc['D']}")
log(f"  score_final: min={min(sfs)} max={max(sfs)} "
    f"med={int(_st.median(sfs))} moy={_st.mean(sfs):.1f}")
log(f"  Places: {'OK' if PLACES_OK else 'INDISPONIBLE'}  "
    f"DOM fetched={sum(1 for r in scored if (r.get('dom') or {}).get('fetched'))}")
log("  TOP 15 classement global (final · conf · tier) :")
for i, r in enumerate(classement[:15], 1):
    log(f"   {i:2d}. {r['nom'][:30]:30s} {r['score']:.0f}/100 "
        f"conf {r['confidence']:>3d} {r['tier']} [{r['bucket']}]")
log("="*60)
print("DONE")
LOG.close()
