#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Self-test HORS-LIGNE du tunnel : valide la logique d'entonnoir, les taux de
# conversion, la projection et les garde-fous conformite sur des cas synthetiques.
#
#   python zpr/tunnel/tests/run_tests.py
import datetime, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import run_tunnel as t

_ok = _ko = 0


def check(label, cond):
    global _ok, _ko
    if cond:
        _ok += 1; print(f"  ok   {label}")
    else:
        _ko += 1; print(f"  FAIL {label}")


# 30 contacts, 5 qualifies, 2 estimations, 1 mandat -> pile le ratio cible.
def mk(n, stade, **kw):
    out = []
    for i in range(n):
        p = {"id": f"{stade}-{i}", "statut": stade}
        p.update(kw); out.append(p)
    return out


PROS = (mk(25, "contact") + mk(3, "qualifie") + mk(1, "estimation")
        + mk(1, "mandat", honoraires_estimes=12000, consentement_rgpd=True))
# cumulatif attendu : contact 30, qualifie 5, estimation 2, mandat 1
OBJ = {"ca_cible": 100000, "mandats_cibles": 10, "horizon_mois": 6,
       "date_debut": "2026-01-01", "honoraires_moyens": 10000,
       "ratio_cible": {"contact": 30, "qualifie": 5, "estimation": 2, "mandat": 1}}


def test_funnel():
    c = t.etat_funnel(PROS)
    check("entonnoir cumulatif 30/5/2/1",
          c == {"contact": 30, "qualifie": 5, "estimation": 2, "mandat": 1})


def test_taux():
    c = t.etat_funnel(PROS)
    tr = t.taux_conversion(c)
    tc = t.ratio_cible_taux(OBJ["ratio_cible"])
    check("taux reels == taux cibles sur ce jeu calibre",
          tr["mandat/contact"] == tc["mandat/contact"] and
          tr["estimation/qualifie"] == tc["estimation/qualifie"])
    check("taux global contact->mandat ~ 0.0333", tr["mandat/contact"] == 0.0333)


def test_perdu_stade():
    perdu = {"id": "x", "statut": "perdu", "stade_atteint": "estimation"}
    check("perdu compte jusqu'a son stade atteint",
          t.stade_max(perdu) == "estimation")
    check("perdu sans stade -> contact",
          t.stade_max({"id": "y", "statut": "perdu"}) == "contact")


def test_ca():
    hm, hypo = t.honoraires_moyens(OBJ)
    check("honoraires moyens lus", hm == 10000 and hypo is False)
    check("honoraires deduits si absent",
          t.honoraires_moyens({"ca_cible": 100000, "mandats_cibles": 10})
          == (10000, True))
    check("CA signe = honoraires du mandat", t.ca_realise(PROS, hm) == 12000)


def test_projection_et_volume():
    ref = datetime.date(2026, 4, 1)            # 3 mois ecoules, 1 mandat
    c = t.etat_funnel(PROS)
    proj = t.projection(OBJ, c, ref)
    check("run-rate ~0.34 mandat/mois", round(proj["rate_mandats_mois"], 2) == 0.34)
    check("projete a 6 mois ~2 mandats", proj["projete_echeance"] == 2.0)
    check("sous la trajectoire (cible 10)", proj["on_track"] is False)
    vol = t.volume_requis(OBJ, c, t.taux_conversion(c), ref)
    check("9 mandats restants", vol["mandats_restants"] == 9)
    # 9 mandats / (1/30) = 270 contacts
    check("270 contacts a produire", vol["contacts_a_produire"] == 270)
    check("cadence hebdo calculee", vol["contacts_par_semaine"] is not None)


def test_conformite():
    froid = [{"id": "a", "nom": "A", "source": "pige", "statut": "contact",
              "consentement_rgpd": False}]
    apres = datetime.date(2026, 9, 1)
    avant = datetime.date(2026, 6, 1)
    check("appel a froid signale apres le 11/08/2026",
          t.controle_conformite(froid, apres) == ["A"])
    check("rien signale avant la bascule",
          t.controle_conformite(froid, avant) == [])
    consenti = [{"id": "b", "nom": "B", "source": "pige", "statut": "contact",
                 "consentement_rgpd": True}]
    check("consentement -> non signale",
          t.controle_conformite(consenti, apres) == [])


def main():
    print("== Self-test tunnel de prospection (hors-ligne) ==")
    for fn in (test_funnel, test_taux, test_perdu_stade, test_ca,
               test_projection_et_volume, test_conformite):
        print(f"\n{fn.__name__}:")
        fn()
    print(f"\n{_ok} ok, {_ko} fail")
    sys.exit(1 if _ko else 0)


if __name__ == "__main__":
    main()
