#!/usr/bin/env python
# -*- coding: utf-8 -*-
# run_tunnel — Pilotage du tunnel de conversion immobilier (Etapes 4 & 5 ZPR).
#
# Branche le travail de prospection sur l'OBJECTIF CHIFFRE :
#   100 000 € de CA et 10 mandats exclusifs en 6 mois.
#
# Ratio de performance cible de la methode :
#   30 Contacts -> 5 Qualifies -> 2 Estimations -> 1 Mandat exclusif.
#
# Le moteur ZPR (zpr/run_zpr.py) dit OU prospecter ; ce tunnel dit OU TU EN ES
# et COMBIEN de contacts il reste a produire pour tenir l'objectif a l'echeance.
#
# SOURCE DE VERITE : pipeline.yml (objectif + prospects, saisis a la main).
# Sorties regenerees : {date}/tableau-de-bord.md + pipeline.csv.
# Discipline : aucun chiffre invente. Pas de honoraires => honoraires moyens
# (ca_cible / mandats_cibles) clairement signale comme hypothese.
import csv as _csv, datetime, os, re, sys
from collections import Counter

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
PIPELINE_YML = os.path.join(ROOT, "pipeline.yml")
DATE = os.environ.get("ZPR_CAMPAGNE", datetime.date.today().isoformat())
OUT = os.path.join(ROOT, DATE)

# Etapes de l'entonnoir, dans l'ordre. "perdu" = sorti du tunnel (hors etapes).
STAGES = ["contact", "qualifie", "estimation", "mandat"]
STAGE_LABEL = {"contact": "Contacts", "qualifie": "Qualifiés",
               "estimation": "Estimations", "mandat": "Mandats exclusifs"}


# === CALCULS PURS (importables -> testables hors-ligne) ====================
def stade_max(p):
    """Etape la plus avancee atteinte par un prospect.
    - statut dans STAGES -> ce stade ;
    - 'perdu' -> champ 'stade_atteint' si fourni, sinon 'contact' (prudent) ;
    - inconnu -> 'contact'."""
    st = (p.get("statut") or "").strip().lower()
    if st in STAGES:
        return st
    if st == "perdu":
        sa = (p.get("stade_atteint") or "contact").strip().lower()
        return sa if sa in STAGES else "contact"
    return "contact"


def etat_funnel(prospects):
    """Compte CUMULATIF par etape : combien ont atteint AU MOINS cette etape.
    Un mandat compte donc aussi dans contacts/qualifies/estimations."""
    idx = {s: i for i, s in enumerate(STAGES)}
    counts = {s: 0 for s in STAGES}
    for p in prospects:
        sm = idx[stade_max(p)]
        for s in STAGES:
            if idx[s] <= sm:
                counts[s] += 1
    return counts


def taux_conversion(counts):
    """Taux de passage entre etapes consecutives + taux global contact->mandat.
    4 decimales : le taux mandat/contact est petit (~0,033), arrondir trop tot
    fausse le calcul de volume en aval."""
    def r(a, b):
        return round(counts[b] / counts[a], 4) if counts.get(a) else None
    return {
        "qualifie/contact": r("contact", "qualifie"),
        "estimation/qualifie": r("qualifie", "estimation"),
        "mandat/estimation": r("estimation", "mandat"),
        "mandat/contact": r("contact", "mandat"),
    }


def ratio_cible_taux(ratio):
    """Convertit le ratio 30:5:2:1 en taux de conversion cibles."""
    c, q, e, m = (ratio.get("contact"), ratio.get("qualifie"),
                  ratio.get("estimation"), ratio.get("mandat"))
    return {
        "qualifie/contact": round(q / c, 4) if c else None,
        "estimation/qualifie": round(e / q, 4) if q else None,
        "mandat/estimation": round(m / e, 4) if e else None,
        "mandat/contact": round(m / c, 4) if c else None,
    }


def honoraires_moyens(objectif):
    hm = objectif.get("honoraires_moyens")
    if hm:
        return float(hm), False
    ca, n = objectif.get("ca_cible"), objectif.get("mandats_cibles")
    if ca and n:
        return round(ca / n), True              # True = hypothese (signaler)
    return None, True


def ca_realise(prospects, hm):
    """CA effectivement signe = somme des honoraires des mandats (hm a defaut)."""
    total = 0.0
    for p in prospects:
        if stade_max(p) == "mandat" and (p.get("statut") or "").lower() == "mandat":
            total += float(p.get("honoraires_estimes") or hm or 0)
    return round(total)


def ca_pondere(counts, ratio, hm):
    """CA prévisionnel pondéré du pipeline : chaque prospect en cours vaut sa
    proba de finir en mandat (taux cible depuis son etape) x honoraires moyens.
    Approxime via les taux cibles (30:5:2:1)."""
    if not hm:
        return None
    t = ratio_cible_taux(ratio)
    # proba mandat depuis chaque etape (produit des taux restants)
    p_mandat = {
        "contact": t["mandat/contact"],
        "qualifie": (t["estimation/qualifie"] or 0) * (t["mandat/estimation"] or 0),
        "estimation": t["mandat/estimation"],
        "mandat": 1.0,
    }
    # counts cumulatifs -> effectifs EXACTEMENT a chaque etape
    exact = {}
    for i, s in enumerate(STAGES):
        nxt = STAGES[i + 1] if i + 1 < len(STAGES) else None
        exact[s] = counts[s] - (counts[nxt] if nxt else 0)
    val = sum((exact[s]) * (p_mandat.get(s) or 0) for s in STAGES)
    return round(val * hm)


def semaines_restantes(objectif, date_ref):
    deb = objectif.get("date_debut")
    horizon = objectif.get("horizon_mois")
    if not deb or not horizon:
        return None
    d0 = datetime.date.fromisoformat(str(deb))
    fin = d0 + datetime.timedelta(days=round(horizon * 30.44))
    return round(max(0, (fin - date_ref).days) / 7, 1)


def projection(objectif, counts, date_ref):
    """Run-rate de mandats et projection a l'echeance. None si infos absentes."""
    deb = objectif.get("date_debut")
    horizon = objectif.get("horizon_mois")
    cible = objectif.get("mandats_cibles")
    if not (deb and horizon):
        return None
    d0 = datetime.date.fromisoformat(str(deb))
    mois_ecoules = max((date_ref - d0).days, 1) / 30.44
    signes = counts.get("mandat", 0)
    rate = signes / mois_ecoules                          # mandats / mois
    projete = round(rate * horizon, 1)
    return {
        "mois_ecoules": round(mois_ecoules, 1),
        "mandats_signes": signes,
        "rate_mandats_mois": round(rate, 2),
        "projete_echeance": projete,
        "cible": cible,
        "ecart": round((projete - cible), 1) if cible is not None else None,
        "on_track": (projete >= cible) if cible is not None else None,
    }


def volume_requis(objectif, counts, taux_reels, date_ref):
    """Combien de NOUVEAUX contacts/qualifs/estimations produire pour atteindre
    les mandats restants d'ici l'echeance, et a quelle cadence hebdomadaire.
    Utilise les taux REELS si dispo (>= seuil de donnees), sinon les taux cibles."""
    cible = objectif.get("mandats_cibles")
    ratio = objectif.get("ratio_cible", {})
    if cible is None:
        return None
    restant = max(0, cible - counts.get("mandat", 0))
    tc = ratio_cible_taux(ratio)
    # On ne fait confiance aux taux REELS qu'a partir d'un cycle complet (>=30
    # contacts, cf ratio 30:1). En dessous, l'echantillon est trop maigre pour
    # extrapoler -> on retombe sur les taux cibles de la methode.
    assez = counts.get("contact", 0) >= (ratio.get("contact") or 30)
    def eff(key):
        return (taux_reels.get(key) if assez else None) or tc.get(key)
    r_mc = eff("mandat/contact") or tc["mandat/contact"]
    r_eq = eff("estimation/qualifie") or tc["estimation/qualifie"]
    r_me = eff("mandat/estimation") or tc["mandat/estimation"]
    r_qc = eff("qualifie/contact") or tc["qualifie/contact"]
    contacts = round(restant / r_mc) if r_mc else None
    qualifs = round(restant / (r_me * r_eq)) if (r_me and r_eq) else None
    estims = round(restant / r_me) if r_me else None
    sem = semaines_restantes(objectif, date_ref)
    par_sem = round(contacts / sem, 1) if (contacts and sem) else None
    return {
        "mandats_restants": restant,
        "contacts_a_produire": contacts,
        "qualifs_a_produire": qualifs,
        "estimations_a_produire": estims,
        "semaines_restantes": sem,
        "contacts_par_semaine": par_sem,
        "base_taux": "réels" if assez else "cibles (échantillon < 30 contacts)",
    }


def controle_conformite(prospects, date_ref):
    """Garde-fou Bloctel/RGPD : a partir du 11/08/2026, demarchage telephonique
    non sollicite interdit sans consentement explicite ou contrat en cours.
    Renvoie la liste des prospects a risque si on les appelle a froid."""
    bascule = datetime.date(2026, 8, 11)
    risque = []
    for p in prospects:
        consent = bool(p.get("consentement_rgpd"))
        contrat = stade_max(p) == "mandat"
        src = (p.get("source") or "").lower()
        froid = src in ("pige", "terrain", "")        # canaux sortants a froid
        if date_ref >= bascule and froid and not consent and not contrat:
            risque.append(p.get("nom") or p.get("id") or "?")
    return risque


# === RENDU =================================================================
def charger():
    raw = open(PIPELINE_YML, encoding="utf-8").read()
    d = yaml.safe_load(raw) or {}
    obj = d.get("objectif", {}) or {}
    pros = [p for p in (d.get("prospects") or [])
            if p.get("id") and p.get("id") != "_modele"]
    return obj, pros


def _pct(x):
    return "—" if x is None else f"{round(x * 100, 1)} %"


def tableau_de_bord(obj, pros):
    counts = etat_funnel(pros)
    treel = taux_conversion(counts)
    tcible = ratio_cible_taux(obj.get("ratio_cible", {}))
    hm, hm_hypo = honoraires_moyens(obj)
    ca_r = ca_realise(pros, hm)
    ca_p = ca_pondere(counts, obj.get("ratio_cible", {}), hm)
    date_ref = datetime.date.fromisoformat(DATE)
    proj = projection(obj, counts, date_ref)
    vol = volume_requis(obj, counts, treel, date_ref)
    risque = controle_conformite(pros, date_ref)

    L = [f"# Tableau de bord — Tunnel de prospection — {DATE}", ""]

    # 1. Objectif
    ca_c = obj.get("ca_cible"); mc = obj.get("mandats_cibles")
    L += ["## 🎯 Objectif", "",
          f"- **Cible :** {ca_c or '?'} € de CA · {mc or '?'} mandats exclusifs "
          f"en {obj.get('horizon_mois', '?')} mois",
          f"- **Honoraires moyens / mandat :** {hm or '?'} €"
          + (" _(hypothèse ca_cible/mandats)_" if hm_hypo else ""),
          f"- **Début :** {obj.get('date_debut', '?')} · "
          f"**Semaines restantes :** {vol['semaines_restantes'] if vol else '?'}",
          ""]

    # 2. Entonnoir
    L += ["## 🔻 Entonnoir actuel vs cible (30 → 5 → 2 → 1)", "",
          "| Étape | Actuel | Taux réel | Taux cible |", "|---|---|---|---|"]
    keys = ["qualifie/contact", "estimation/qualifie", "mandat/estimation"]
    L.append(f"| {STAGE_LABEL['contact']} | {counts['contact']} | — | — |")
    for s, k in zip(["qualifie", "estimation", "mandat"], keys):
        L.append(f"| {STAGE_LABEL[s]} | {counts[s]} | {_pct(treel[k])} | "
                 f"{_pct(tcible[k])} |")
    L += ["",
          f"- **Taux global contact → mandat :** {_pct(treel['mandat/contact'])} "
          f"(cible {_pct(tcible['mandat/contact'])})", ""]

    # 3. Réalisé vs objectif
    L += ["## 💶 Chiffre d'affaires", "",
          f"- **CA signé (mandats fermes) :** {ca_r} €"
          + (f" / {ca_c} € → **{round(ca_r / ca_c * 100)} %**" if ca_c else ""),
          f"- **CA pondéré du pipeline en cours :** "
          f"{ca_p if ca_p is not None else '?'} € "
          "_(prospects × proba cible × honoraires)_", ""]

    # 4. Projection
    if proj:
        etat = ("✅ sur la trajectoire" if proj["on_track"]
                else "⚠️ sous la trajectoire")
        L += ["## 📈 Projection à l'échéance", "",
              f"- **{proj['mandats_signes']} mandats** signés en "
              f"{proj['mois_ecoules']} mois → "
              f"**{proj['rate_mandats_mois']} mandat/mois**",
              f"- **Projeté à l'échéance :** {proj['projete_echeance']} mandats "
              f"(cible {proj['cible']}) → écart **{proj['ecart']:+}** — {etat}", ""]

    # 5. Volume à produire
    if vol:
        L += ["## 🚜 Volume à produire pour tenir l'objectif", "",
              f"Pour signer les **{vol['mandats_restants']} mandats restants** "
              f"d'ici l'échéance (taux {vol['base_taux']}) :",
              f"- **{vol['contacts_a_produire']} contacts** "
              f"→ {vol['qualifs_a_produire']} qualifiés "
              f"→ {vol['estimations_a_produire']} estimations",
              (f"- **Cadence : ~{vol['contacts_par_semaine']} contacts / semaine** "
               f"sur {vol['semaines_restantes']} semaines"
               if vol["contacts_par_semaine"]
               else "- ⏰ **Échéance atteinte/dépassée** : recaler `date_debut` / "
                    "`horizon_mois` ou prolonger l'objectif."),
              "  _(la méthode prévoit ~2 h de prospection active / jour avant 11h)_",
              ""]

    # 6. Sources & signaux 3D
    src = Counter((p.get("source") or "inconnu").lower() for p in pros)
    d3 = Counter((p.get("signal_3d") or "aucun").lower() for p in pros
                 if (p.get("signal_3d") or "aucun").lower() != "aucun")
    L += ["## 🧭 Origine & signaux", "",
          "- **Sources :** "
          + (", ".join(f"{k} {v}" for k, v in src.most_common()) or "—"),
          "- **Signaux 3D (Divorce/Décès/Déménagement) :** "
          + (", ".join(f"{k} {v}" for k, v in d3.most_common()) or "aucun renseigné"),
          ""]

    # 7. Conformité
    L += ["## ⚖️ Conformité (Bloctel / RGPD)", ""]
    if date_ref >= datetime.date(2026, 8, 11):
        if risque:
            L += [f"- ⚠️ **{len(risque)} prospect(s) à risque** si appel à froid "
                  "(ni consentement, ni contrat) : " + ", ".join(risque[:15]),
                  "  → privilégier inbound / recommandation, ou obtenir le consentement."]
        else:
            L.append("- ✅ Aucun prospect en infraction d'appel à froid détecté.")
    else:
        L.append(f"- Bascule du 11/08/2026 pas encore atteinte au {DATE} — "
                 "anticiper en bâtissant le consentement dès maintenant.")
    L.append("")
    return "\n".join(L)


def ecrire_csv(pros, hm):
    hdr = ("id,nom,commune,source,statut,stade_atteint,segment,signal_3d,"
           "date_contact,date_mandat,honoraires_estimes,consentement_rgpd")

    def c(x):
        return str(x).replace(",", " ").replace("\n", " ") if x is not None else ""
    with open(os.path.join(OUT, "pipeline.csv"), "w", encoding="utf-8") as f:
        f.write(hdr + "\n")
        for p in pros:
            f.write(",".join(c(x) for x in [
                p.get("id"), p.get("nom"), p.get("commune"), p.get("source"),
                p.get("statut"), stade_max(p), p.get("segment"),
                p.get("signal_3d"), p.get("date_contact"), p.get("date_mandat"),
                p.get("honoraires_estimes"), p.get("consentement_rgpd")]) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    obj, pros = charger()
    hm, _ = honoraires_moyens(obj)
    md = tableau_de_bord(obj, pros)
    open(os.path.join(OUT, "tableau-de-bord.md"), "w", encoding="utf-8").write(md)
    open(os.path.join(OUT, "tableau-de-bord.txt"), "w",
         encoding="utf-8").write(re.sub(r"[*`#|]", "", md))
    ecrire_csv(pros, hm)
    counts = etat_funnel(pros)
    print(f"Tunnel — {len(pros)} prospects | "
          f"contacts {counts['contact']} · qualifiés {counts['qualifie']} · "
          f"estimations {counts['estimation']} · mandats {counts['mandat']}")
    print(f"Sorties: {OUT}/tableau-de-bord.md + pipeline.csv")


if __name__ == "__main__":
    main()
