#!/usr/bin/env python
# -*- coding: utf-8 -*-
# run_zpr — Moteur d'analyse de Zone de Prospection Rentable (ZPR), Etapes 1 & 2.
#
# Fidele a la Strategie Operationnelle "Definition de la ZPR" :
#   - Etape 1 : taux de rotation tau_R = (mutations annuelles moy. / logements) x 100,
#               SEUIL DE VIABILITE = 4,0 % (en dessous : ne JAMAIS prospecter).
#   - Etape 2 : gisement DPE (passoires F/G), signal pre-marche (DPE recents),
#               sociodemo INSEE/Filosofi (proprietaires occupants, revenu, 60 ans+ = les "3D").
#   - Proscription : garages/box exclus du numerateur (honoraires trop faibles).
#
# Comparaison MULTI-VILLES : classe les communes candidates pour decider OU s'implanter.
#
# SOURCES OPEN DATA (aucune cle requise) :
#   - DVF (mutations)    : https://files.data.gouv.fr/geo-dvf/latest/csv/{annee}/communes/{dep}/{insee}.csv
#   - DPE (ADEME)        : https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines
#   - Communes (meta)    : https://geo.api.gouv.fr/communes/{insee}
#   - Logements + sociodemo : INSEE "Dossier complet" -> a RENSEIGNER a la main dans zones.yml
#                             (le denominateur officiel ne s'expose pas en API keyless ;
#                              a defaut on derive une ESTIMATION explicitement taggee).
#
# DISCIPLINE (cf prospects/run_scoring.py) : jamais de chiffre invente. Une donnee
# manquante reste manquante (verdict "INDETERMINE"), une estimation est taggee [ESTIME].
# Reutilise les caches valides. LOCAL : zones.yml versionne, cache/ gitignore.
import csv, io, json, os, re, time, datetime, unicodedata, subprocess, sys, statistics
from concurrent.futures import ThreadPoolExecutor

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, "cache")
DATE = os.environ.get("ZPR_CAMPAGNE", datetime.date.today().isoformat())
OUT = os.path.join(ROOT, DATE)
ZONES_YML = os.path.join(ROOT, "zones.yml")
UA = "MB-Studio-ZPR/1.0 (contact: kroostiyummy@gmail.com)"

# --- Parametres methode (SOURCE DE VERITE = la Strategie ZPR) ---------------
SEUIL_ROTATION = 4.0                     # % : seuil critique de rentabilite
NB_ANNEES = int(os.environ.get("ZPR_ANNEES", "5"))      # fenetre DVF (annees pleines)
TAILLE_MENAGE = 2.2                      # INSEE ~2,2 pers/menage (fallback ESTIME only)
VOLUMETRIE_MIN, VOLUMETRIE_MAX = 1500, 3000             # boites aux lettres cibles
MICRO_ZONE = (300, 500)                  # portes par micro-secteur (Etape 2)
DPE_DATASET = os.environ.get("ZPR_DPE_DATASET", "dpe-v2-logements-existants")
JOURS_PRE_MARCHE = 90                    # DPE recents = signal pre-annonce

RESIDENTIEL = {"Maison", "Appartement"}  # numerateur rotation : logements seulement
VENTES = {"Vente", "Vente en l'état futur d'achèvement"}  # vraies mutations marche

# === Infrastructure (idiome run_scoring.py) ================================
def log(m):
    line = f"{datetime.datetime.now():%H:%M:%S} {m}"
    if _LOG:
        _LOG.write(line + "\n"); _LOG.flush()
    print(line, flush=True)
_LOG = None

def curl(args, timeout=90):
    try:
        r = subprocess.run(["curl", "-s", "--max-time", str(timeout)] + args,
                           capture_output=True, timeout=timeout + 15)
        return (r.stdout or b"").decode("utf-8", errors="replace")
    except Exception as e:
        log(f"curl err: {e}")
        return ""

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn")

def dep_from_insee(insee):
    """Departement DVF a partir du code commune (gere Corse 2A/2B et DOM 97x/98x)."""
    insee = str(insee).strip().upper()
    if insee[:2] in ("2A", "2B"):
        return insee[:2]
    if insee[:2] in ("97", "98"):
        return insee[:3]
    return insee[:2]

# === CALCULS PURS (importables -> testables hors-ligne, cf tests/) =========
def parse_dvf_csv(text):
    """Parse un CSV geo-dvf commune/annee -> liste de lignes-dict utiles.
    geo-dvf est en virgule ; on laisse csv sniffer le delimiteur par securite."""
    text = text.lstrip("﻿")
    if not text.strip():
        return []
    sample = text[:4096]
    delim = ";" if sample.count(";") > sample.count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def compte_mutations(rows):
    """Compte les VRAIES mutations residentielles sur un jeu de lignes DVF.
    - dedup par id_mutation (une mutation = plusieurs lignes possibles) ;
    - une mutation compte si elle vend >=1 Maison/Appartement ;
    - garages/box ('Dependance', locaux) JAMAIS comptes (proscription methode) ;
    - collecte type dominant + surfaces/pieces pour le segment de biens."""
    par_mut = {}                          # id_mutation -> {residentiel, types, surfaces, pieces}
    for r in rows:
        idm = r.get("id_mutation") or r.get("id")
        nat = (r.get("nature_mutation") or "").strip()
        typ = (r.get("type_local") or "").strip()
        if not idm:
            continue
        m = par_mut.setdefault(idm, {"resid": False, "vente": nat in VENTES,
                                     "types": [], "surf": [], "pieces": []})
        m["vente"] = m["vente"] or nat in VENTES
        if typ in RESIDENTIEL:
            m["resid"] = True
            m["types"].append(typ)
            try:
                s = float((r.get("surface_reelle_bati") or "").replace(",", "."))
                if s > 0:
                    m["surf"].append((typ, s))
            except ValueError:
                pass
            try:
                p = int(float(r.get("nombre_pieces_principales") or 0))
                if p > 0:
                    m["pieces"].append((typ, p))
            except ValueError:
                pass
    retenues = [m for m in par_mut.values() if m["resid"] and m["vente"]]
    types, surfs, pieces = [], [], []
    for m in retenues:
        types += m["types"]; surfs += m["surf"]; pieces += m["pieces"]
    return {"n_mutations": len(retenues), "types": types,
            "surfaces": surfs, "pieces": pieces}


def segment_dominant(types, surfaces, pieces):
    """Libelle du segment dominant facon tableau ZPR : 'Maison < 90 m²',
    'Appartement T1-T2', etc. Renvoie None si donnees insuffisantes."""
    if not types:
        return None
    from collections import Counter
    dom = Counter(types).most_common(1)[0][0]
    if dom == "Maison":
        ss = [s for t, s in surfaces if t == "Maison"]
        if not ss:
            return "Maison"
        med = statistics.median(ss)
        seuil = "< 90 m²" if med < 90 else ("90-130 m²" if med <= 130 else "> 130 m²")
        return f"Maison {seuil}"
    if dom == "Appartement":
        pp = [p for t, p in pieces if t == "Appartement"]
        if not pp:
            return "Appartement"
        med = statistics.median(pp)
        lib = "T1-T2" if med <= 2 else ("T3" if med == 3 else "T4+")
        return f"Appartement {lib}"
    return dom


def taux_rotation(mutations_an, nb_logements):
    """tau_R = (mutations annuelles moyennes / nombre de logements) x 100.
    None si le denominateur est inconnu (jamais de division inventee)."""
    if not nb_logements:
        return None
    return round(mutations_an / nb_logements * 100, 2)


def verdict_rotation(taux):
    """Verdict binaire de la methode : seuil critique 4,0 %."""
    if taux is None:
        return "INDÉTERMINÉ"
    return "GO" if taux >= SEUIL_ROTATION else "NO-GO"


def part(n, total):
    return round(n / total * 100, 1) if total else None


def score_opportunite(taux, part_fg, part_proprio, part_senior, dpe_recents):
    """Score 0-100 pour CLASSER les zones GO entre elles (le verdict, lui,
    reste binaire sur tau_R). Pondere les leviers de la methode :
      - rotation (le marche bouge)            40 %
      - proprietaires occupants (mandats)     20 %
      - 60 ans+ (succession, mobilite = 3D)   15 %
      - gisement passoires F/G                15 %
      - DPE recents = signal pre-marche       10 %
    Les composantes manquantes sont neutralisees (0,5) pour rester honnete."""
    def n(x, lo, hi):
        if x is None:
            return 0.5
        return max(0.0, min(1.0, (x - lo) / (hi - lo)))
    s = (0.40 * n(taux, 4.0, 12.0)
         + 0.20 * n(part_proprio, 40.0, 75.0)
         + 0.15 * n(part_senior, 15.0, 35.0)
         + 0.15 * n(part_fg, 5.0, 25.0)
         + 0.10 * (1.0 if (dpe_recents or 0) > 0 else 0.5))
    return round(s * 100)


# === I/O reseau (cache TTL) ================================================
def _cache_get(path, ttl_days):
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < ttl_days * 86400:
        try:
            return open(path, encoding="utf-8").read()
        except Exception:
            return None
    return None


def fetch_commune_meta(insee):
    """geo.api.gouv.fr : nom, population, codes postaux, centre. Cache 30j."""
    cf = os.path.join(CACHE, "geo", f"{insee}.json")
    data = _cache_get(cf, 30)
    if data is None:
        data = curl(["-H", f"User-Agent: {UA}",
                     f"https://geo.api.gouv.fr/communes/{insee}"
                     "?fields=nom,code,codesPostaux,population,centre,codeDepartement"], 20)
        open(cf, "w", encoding="utf-8").write(data or "{}")
        time.sleep(0.2)
    try:
        return json.loads(data or "{}")
    except Exception:
        return {}


def fetch_dvf_annee(insee, annee):
    """CSV geo-dvf d'une commune pour une annee. Cache 90j (donnee figee).
    Renvoie (rows, dispo) : dispo=False si fichier absent (annee non publiee)."""
    cf = os.path.join(CACHE, "dvf", f"{insee}-{annee}.csv")
    data = _cache_get(cf, 90)
    if data is None:
        dep = dep_from_insee(insee)
        url = (f"https://files.data.gouv.fr/geo-dvf/latest/csv/{annee}"
               f"/communes/{dep}/{insee}.csv")
        data = curl(["-L", "-H", f"User-Agent: {UA}", url], 60)
        # 404 -> page HTML/erreur courte ; on ne cache que des CSV plausibles
        if data and ("id_mutation" in data[:2000] or data.count(",") > 5):
            open(cf, "w", encoding="utf-8").write(data)
        else:
            open(cf, "w", encoding="utf-8").write("")   # cache le "vide" pour ne pas reessayer
            data = ""
        time.sleep(0.2)
    rows = parse_dvf_csv(data)
    return rows, bool(rows)


def _dpe_total(insee, extra=""):
    """Nombre de DPE matchant un filtre (size=0 -> champ 'total'). None si echec."""
    qs = f'code_insee_ban:"{insee}"' + (f" AND {extra}" if extra else "")
    url = (f"https://data.ademe.fr/data-fair/api/v1/datasets/{DPE_DATASET}/lines"
           f"?size=0&qs={qs}")
    out = curl(["-G", "https://data.ademe.fr/data-fair/api/v1/datasets/"
                f"{DPE_DATASET}/lines",
                "-H", f"User-Agent: {UA}",
                "--data-urlencode", "size=0",
                "--data-urlencode", f"qs={qs}"], 30)
    try:
        return json.loads(out or "{}").get("total")
    except Exception:
        return None


def fetch_dpe(insee):
    """ADEME : total DPE, passoires F/G, et DPE recents (signal pre-marche).
    Cache 7j (base vivante). Tout None si API indisponible."""
    cf = os.path.join(CACHE, "dpe", f"{insee}.json")
    data = _cache_get(cf, 7)
    if data is not None:
        try:
            return json.loads(data)
        except Exception:
            pass
    depuis = (datetime.date.today()
              - datetime.timedelta(days=JOURS_PRE_MARCHE)).isoformat()
    d = {
        "total": _dpe_total(insee),
        "passoires_fg": _dpe_total(insee, '(etiquette_dpe:"F" OR etiquette_dpe:"G")'),
        "recents": _dpe_total(insee, f"date_etablissement_dpe:[{depuis} TO *]"),
        "date_collecte": DATE, "fenetre_jours": JOURS_PRE_MARCHE,
    }
    json.dump(d, open(cf, "w", encoding="utf-8"))
    return d


# === PIPELINE ==============================================================
def charger_zones():
    """Lit zones.yml ; renvoie (preamble, entrees, prev_par_code).
    Preserve l'en-tete + _modele + les champs saisis a la main (insee_filosofi, notes)."""
    raw = open(ZONES_YML, encoding="utf-8").read()
    parsed = yaml.safe_load(raw) or {}
    entrees = [e for e in parsed.get("villes", [])
               if e.get("code_insee") and e.get("code_insee") != "_modele"]
    prev = {str(e["code_insee"]): e for e in entrees}
    return entrees, prev


def analyser(insee, prev):
    insee = str(insee)
    meta = fetch_commune_meta(insee)
    nom = meta.get("nom") or prev.get("identite", {}).get("nom") or insee
    population = meta.get("population")
    dep = meta.get("codeDepartement") or dep_from_insee(insee)
    log(f"  {insee} {nom} — DVF {NB_ANNEES} ans + DPE...")

    # --- DVF : mutations residentielles sur la fenetre d'annees publiees ---
    cur = datetime.date.today().year
    annees_ok, total_mut = [], 0
    types, surfs, pieces = [], [], []
    for an in range(cur - 1, cur - 1 - (NB_ANNEES + 2), -1):   # marge : DVF publie avec retard
        if len(annees_ok) >= NB_ANNEES:
            break
        rows, dispo = fetch_dvf_annee(insee, an)
        if not dispo:
            continue
        c = compte_mutations(rows)
        total_mut += c["n_mutations"]
        types += c["types"]; surfs += c["surfaces"]; pieces += c["pieces"]
        annees_ok.append(an)
    mut_an = round(total_mut / len(annees_ok), 1) if annees_ok else None
    segment = segment_dominant(types, surfs, pieces)

    # --- Denominateur : nb logements (manuel INSEE > sinon ESTIME tagge) ----
    filo = (prev.get("insee_filosofi") or {})
    nb_log = filo.get("nb_logements")
    log_src = "INSEE (saisi)"
    if not nb_log:
        if population:
            nb_log = round(population / TAILLE_MENAGE)
            log_src = "[ESTIMÉ] population/2,2 — à remplacer par INSEE Dossier complet"
        else:
            log_src = "MANQUANT — renseigner insee_filosofi.nb_logements"

    taux = taux_rotation(mut_an, nb_log) if mut_an is not None else None
    verdict = verdict_rotation(taux)

    # --- DPE (gisement passoires + signal pre-marche) ----------------------
    dpe = fetch_dpe(insee)
    part_fg = part(dpe.get("passoires_fg"), dpe.get("total")) \
        if dpe.get("passoires_fg") is not None and dpe.get("total") else None

    # --- Sociodemo (saisie INSEE/Filosofi) ---------------------------------
    part_proprio = filo.get("part_proprietaires_occ")
    revenu = filo.get("revenu_median")
    part_senior = filo.get("part_60_ans_plus")

    score = score_opportunite(taux, part_fg, part_proprio, part_senior,
                              dpe.get("recents"))

    # --- Volumetrie / micro-zonage (Etape 2) -------------------------------
    if not nb_log:
        volum = "logements inconnus"
    elif nb_log > VOLUMETRIE_MAX:
        n_micro = -(-nb_log // MICRO_ZONE[1])     # ceil
        volum = (f"{nb_log} logements > {VOLUMETRIE_MAX} : segmenter en "
                 f"~{n_micro} micro-zones de {MICRO_ZONE[0]}-{MICRO_ZONE[1]} portes")
    elif nb_log < VOLUMETRIE_MIN:
        volum = f"{nb_log} logements < {VOLUMETRIE_MIN} : zone un peu maigre, élargir"
    else:
        volum = f"{nb_log} logements : volumétrie idéale ({VOLUMETRIE_MIN}-{VOLUMETRIE_MAX})"

    # confiance = part des briques observees
    obs = sum(x is not None for x in
              [mut_an, filo.get("nb_logements"), part_fg, part_proprio,
               part_senior, revenu])
    confidence = round(100 * obs / 6)

    return {
        "code_insee": insee, "nom": nom, "departement": dep,
        "population": population,
        "nb_logements": nb_log, "nb_logements_source": log_src,
        "annees_dvf": annees_ok, "mut_an_moy": mut_an, "total_mutations": total_mut,
        "segment": segment,
        "taux_rotation": taux, "verdict": verdict,
        "dpe_total": dpe.get("total"), "dpe_fg": dpe.get("passoires_fg"),
        "dpe_part_fg": part_fg, "dpe_recents": dpe.get("recents"),
        "part_proprietaires_occ": part_proprio, "revenu_median": revenu,
        "part_60_ans_plus": part_senior,
        "score_opportunite": score, "confidence": confidence,
        "volumetrie": volum,
    }


# === RENDU (YAML source de verite + CSV plat + comparatif markdown) ========
def yq(s):
    if s is None:
        return "null"
    if isinstance(s, (int, float)):
        return str(s)
    return '"' + str(s).replace('"', "'") + '"'


def ecrire_zones_yml(resultats, prev):
    """Reecrit zones.yml en preservant l'en-tete + _modele + champs manuels."""
    raw = open(ZONES_YML, encoding="utf-8").read()
    lines = raw.splitlines()
    end = len(lines)
    in_modele = False
    for i, ln in enumerate(lines):
        if re.match(r"\s*-\s+code_insee:\s*_modele", ln) or \
           re.match(r'\s*-\s+code_insee:\s*"?_modele', ln):
            in_modele = True
            continue
        if in_modele and re.match(r'\s*-\s+code_insee:\s*"?(?!_modele)', ln):
            end = i
            break
    preamble = "\n".join(lines[:end]).rstrip() + "\n"

    body = ""
    for r in resultats:
        p = prev.get(r["code_insee"], {})
        filo = p.get("insee_filosofi") or {}
        notes = p.get("notes", "")
        body += f"""
  - code_insee: "{r['code_insee']}"

    identite:
      nom: {yq(r['nom'])}
      departement: {yq(r['departement'])}
      population: {yq(r['population'])}

    insee_filosofi:                 # SAISI A LA MAIN depuis INSEE "Dossier complet"
      nb_logements: {yq(filo.get('nb_logements'))}
      part_proprietaires_occ: {yq(filo.get('part_proprietaires_occ'))}
      revenu_median: {yq(filo.get('revenu_median'))}
      part_60_ans_plus: {yq(filo.get('part_60_ans_plus'))}

    scan:                           # AUTO — regenere par run_zpr.py
      date_scan: {DATE}
      annees_dvf: {yq(', '.join(map(str, r['annees_dvf'])) or None)}
      total_mutations: {yq(r['total_mutations'])}
      mutations_an_moy: {yq(r['mut_an_moy'])}
      segment_dominant: {yq(r['segment'])}
      nb_logements_utilise: {yq(r['nb_logements'])}
      nb_logements_source: {yq(r['nb_logements_source'])}
      dpe_total: {yq(r['dpe_total'])}
      dpe_passoires_fg: {yq(r['dpe_fg'])}
      dpe_part_fg_pct: {yq(r['dpe_part_fg'])}
      dpe_recents_90j: {yq(r['dpe_recents'])}

    scoring:
      taux_rotation_pct: {yq(r['taux_rotation'])}
      seuil_viabilite_pct: {SEUIL_ROTATION}
      verdict: {yq(r['verdict'])}
      score_opportunite: {yq(r['score_opportunite'])}
      confidence: {yq(r['confidence'])}
      volumetrie: {yq(r['volumetrie'])}

    notes: {yq(notes) if notes else '""'}
"""
    open(ZONES_YML, "w", encoding="utf-8").write(preamble + body)


def ecrire_csv(resultats):
    hdr = ("code_insee,nom,departement,population,nb_logements,nb_log_source,"
           "annees_dvf,total_mutations,mutations_an_moy,segment_dominant,"
           "taux_rotation_pct,seuil_pct,verdict,dpe_total,dpe_passoires_fg,"
           "dpe_part_fg_pct,dpe_recents_90j,part_proprietaires_occ,revenu_median,"
           "part_60_ans_plus,score_opportunite,confidence")

    def cell(x):
        return str(x).replace(",", " ").replace("\n", " ") if x is not None else ""
    with open(os.path.join(OUT, "zones.csv"), "w", encoding="utf-8") as f:
        f.write(hdr + "\n")
        for r in resultats:
            f.write(",".join(cell(x) for x in [
                r["code_insee"], r["nom"], r["departement"], r["population"],
                r["nb_logements"], r["nb_logements_source"],
                " ".join(map(str, r["annees_dvf"])), r["total_mutations"],
                r["mut_an_moy"], r["segment"], r["taux_rotation"], SEUIL_ROTATION,
                r["verdict"], r["dpe_total"], r["dpe_fg"], r["dpe_part_fg"],
                r["dpe_recents"], r["part_proprietaires_occ"], r["revenu_median"],
                r["part_60_ans_plus"], r["score_opportunite"], r["confidence"]]) + "\n")


def fiche(r):
    ico = {"GO": "✅", "NO-GO": "⛔", "INDÉTERMINÉ": "❔"}[r["verdict"]]
    seg = r["segment"] or "segment indéterminé"
    taux = "—" if r["taux_rotation"] is None else f"{r['taux_rotation']} %"
    L = [f"### {ico} {r['nom']} ({r['code_insee']}) — rotation {taux}", "",
         f"**Verdict :** {r['verdict']} (seuil de viabilité {SEUIL_ROTATION} %) · "
         f"**Score opportunité :** {r['score_opportunite']}/100 · "
         f"**Confiance :** {r['confidence']}/100",
         f"**Marché (DVF {', '.join(map(str, r['annees_dvf'])) or 'n/d'}) :** "
         f"{r['total_mutations']} mutations résidentielles → "
         f"{r['mut_an_moy'] if r['mut_an_moy'] is not None else '?'}/an · "
         f"segment dominant **{seg}**",
         f"**Dénominateur :** {r['nb_logements'] or '?'} logements "
         f"_({r['nb_logements_source']})_",
         f"**Volumétrie :** {r['volumetrie']}"]
    if r["dpe_total"]:
        fg = f"{r['dpe_part_fg']} %" if r["dpe_part_fg"] is not None else "?"
        L.append(f"**Gisement DPE :** {r['dpe_total']} DPE · passoires F/G "
                 f"{r['dpe_fg'] or '?'} ({fg}) · {r['dpe_recents'] or 0} DPE "
                 f"récents (<{JOURS_PRE_MARCHE}j = signal pré-marché)")
    socio = []
    if r["part_proprietaires_occ"] is not None:
        socio.append(f"{r['part_proprietaires_occ']} % propriétaires occupants")
    if r["part_60_ans_plus"] is not None:
        socio.append(f"{r['part_60_ans_plus']} % de 60 ans+ (signal 3D)")
    if r["revenu_median"] is not None:
        socio.append(f"revenu médian {r['revenu_median']} €")
    if socio:
        L.append("**Sociodémo INSEE/Filosofi :** " + " · ".join(socio))
    if r["verdict"] == "NO-GO":
        L.append(f"> ⛔ Sous le seuil {SEUIL_ROTATION} % : **ne pas prospecter** "
                 "(présence commerciale non rentabilisable).")
    if r["verdict"] == "INDÉTERMINÉ":
        L.append("> ❔ Taux non calculable — renseigne `insee_filosofi.nb_logements` "
                 "(INSEE Dossier complet) puis relance.")
    if r["confidence"] < 60:
        L.append("> ℹ️ Confiance faible (données INSEE/DPE incomplètes) — à compléter.")
    return "\n".join(L) + "\n\n---\n\n"


def ecrire_comparatif(resultats):
    go = [r for r in resultats if r["verdict"] == "GO"]
    rang = sorted(resultats, key=lambda r: (
        {"GO": 0, "INDÉTERMINÉ": 1, "NO-GO": 2}[r["verdict"]],
        -(r["score_opportunite"] or 0)))
    md = [f"# Comparatif ZPR multi-villes — {DATE}",
          "",
          f"Décider **où s'implanter** : taux de rotation vs seuil de viabilité "
          f"**{SEUIL_ROTATION} %** (Étape 1), enrichi du gisement DPE et de la "
          f"sociodémo (Étape 2). Fenêtre DVF : {NB_ANNEES} dernières années publiées.",
          "",
          f"**{len(go)}/{len(resultats)} communes au-dessus du seuil.** "
          "Le verdict est binaire sur la rotation ; le score d'opportunité ne sert "
          "qu'à classer les communes GO entre elles.",
          "",
          "## Tableau de décision",
          "",
          "| # | Commune | Rotation | Verdict | Segment dominant | F/G | Score | Conf. |",
          "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rang, 1):
        taux = "—" if r["taux_rotation"] is None else f"{r['taux_rotation']} %"
        ico = {"GO": "✅", "NO-GO": "⛔", "INDÉTERMINÉ": "❔"}[r["verdict"]]
        fg = f"{r['dpe_part_fg']} %" if r["dpe_part_fg"] is not None else "—"
        md.append(f"| {i} | **{r['nom']}** ({r['code_insee']}) | {taux} | "
                  f"{ico} {r['verdict']} | {r['segment'] or '—'} | {fg} | "
                  f"{r['score_opportunite']} | {r['confidence']} |")
    md += ["",
           f"> Moyenne nationale ≈ 2,5 %. Seuil critique de rentabilité = "
           f"**{SEUIL_ROTATION} %** : en dessous, on ne prospecte jamais.",
           "",
           "## Fiches détaillées", ""]
    for r in rang:
        md.append(fiche(r))
    md += ["## Rappel conformité (Étape 5 / RGPD-Bloctel)", "",
           "- Dès le **11 août 2026**, démarchage téléphonique non sollicité "
           "interdit sans consentement explicite ou contrat en cours.",
           "- Privilégier l'inbound et la recommandation ; emailing = consentement RGPD ; "
           "SMS ultra-local sur base opt-in.",
           "- Exclusions méthode déjà appliquées : garages/box hors numérateur. "
           "Copropriétés dégradées : à écarter manuellement (non détectable en DVF).",
           ""]
    text = "\n".join(md)
    open(os.path.join(OUT, "comparatif-villes.md"), "w",
         encoding="utf-8").write(text)
    # version txt brute
    txt = re.sub(r"[*`#|]", "", text)
    open(os.path.join(OUT, "comparatif-villes.txt"), "w",
         encoding="utf-8").write(txt)


def main():
    global _LOG
    os.makedirs(OUT, exist_ok=True)
    for d in ("geo", "dvf", "dpe"):
        os.makedirs(os.path.join(CACHE, d), exist_ok=True)
    _LOG = open(os.path.join(OUT, "_run.log"), "w", encoding="utf-8")

    entrees, prev = charger_zones()
    log(f"ZPR — {len(entrees)} communes candidates — campagne {DATE}")
    if not entrees:
        log("Aucune commune dans zones.yml (section 'villes'). Stop.")
        return

    resultats = []
    for e in entrees:
        resultats.append(analyser(e["code_insee"], prev.get(str(e["code_insee"]), {})))

    ecrire_zones_yml(resultats, prev)
    ecrire_csv(resultats)
    ecrire_comparatif(resultats)

    go = [r for r in resultats if r["verdict"] == "GO"]
    log("=" * 60)
    log(f"TERMINE — {len(resultats)} communes, {len(go)} au-dessus du seuil "
        f"{SEUIL_ROTATION} %")
    for r in sorted(resultats, key=lambda x: -(x["score_opportunite"] or 0)):
        log(f"  {r['verdict']:>11s} | {r['nom'][:24]:24s} | "
            f"rot {str(r['taux_rotation']):>6s}% | score {r['score_opportunite']:>3d} "
            f"| conf {r['confidence']:>3d}")
    log("=" * 60)
    print("DONE")
    _LOG.close()


if __name__ == "__main__":
    main()
