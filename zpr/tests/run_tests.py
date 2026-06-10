#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Self-test HORS-LIGNE du moteur ZPR : valide la LOGIQUE de calcul sur des
# fixtures synthetiques, sans toucher au reseau. C'est le garde-fou qui prouve
# que la formule tau_R, le dedup des mutations, les exclusions garages/box et le
# segment dominant se comportent comme la methode l'exige.
#
#   python zpr/tests/run_tests.py
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))            # importe run_zpr

import run_zpr as z

FIX = os.path.join(HERE, "fixtures")
_ok = 0
_ko = 0


def check(label, cond):
    global _ok, _ko
    if cond:
        _ok += 1
        print(f"  ok   {label}")
    else:
        _ko += 1
        print(f"  FAIL {label}")


def test_compte_mutations():
    rows = z.parse_dvf_csv(open(os.path.join(FIX, "dvf-sample.csv"),
                                encoding="utf-8").read())
    c = z.compte_mutations(rows)
    # Comptees : 2023-1 (Maison), 2023-2 (Maison+Dep -> 1 mutation), 2023-4 (Appt),
    #            2023-7 (Maison) = 4. Exclues : 2023-3 (garage seul),
    #            2023-5 (Donation), 2023-6 (local commercial).
    check("4 mutations residentielles (dedup + exclusions)", c["n_mutations"] == 4)
    check("garage/box seul NON compte", "2023-3" not in repr(c))
    check("3 Maisons + 1 Appartement dans les types",
          c["types"].count("Maison") == 3 and c["types"].count("Appartement") == 1)


def test_segment_dominant():
    rows = z.parse_dvf_csv(open(os.path.join(FIX, "dvf-sample.csv"),
                                encoding="utf-8").read())
    c = z.compte_mutations(rows)
    seg = z.segment_dominant(c["types"], c["surfaces"], c["pieces"])
    # Maisons retenues : 82, 95, 78 -> mediane 82 -> "< 90 m2"
    check("segment dominant = Maison < 90 m²", seg == "Maison < 90 m²")


def test_taux_et_verdict():
    # 4 mutations sur 1 an, 2000 logements -> 0,2 %/an... on calibre pour les deux cas.
    check("tau_R arrondi correct", z.taux_rotation(40, 1000) == 4.0)
    check("denominateur inconnu -> None", z.taux_rotation(40, None) is None)
    check("verdict GO au seuil", z.verdict_rotation(4.0) == "GO")
    check("verdict NO-GO sous le seuil", z.verdict_rotation(3.99) == "NO-GO")
    check("verdict INDETERMINE si None", z.verdict_rotation(None) == "INDÉTERMINÉ")


def test_score_borne_et_neutre():
    s = z.score_opportunite(8.0, 15.0, 60.0, 25.0, 5)
    check("score dans [0,100]", 0 <= s <= 100)
    # Tout manquant -> composantes neutralisees, score stable autour de 50.
    s_neutre = z.score_opportunite(None, None, None, None, None)
    check("score neutre ~50 quand tout manque", 45 <= s_neutre <= 55)
    # Plus de rotation => meilleur score.
    check("rotation plus forte => score >=",
          z.score_opportunite(12.0, 15.0, 60.0, 25.0, 5) >=
          z.score_opportunite(4.0, 15.0, 60.0, 25.0, 5))


def test_part_et_dep():
    check("part F/G", z.part(50, 200) == 25.0)
    check("part total 0 -> None", z.part(5, 0) is None)
    check("dep Corse 2A", z.dep_from_insee("2A004") == "2A")
    check("dep DOM 974", z.dep_from_insee("97411") == "974")
    check("dep metropole", z.dep_from_insee("28085") == "28")


def main():
    print("== Self-test moteur ZPR (hors-ligne) ==")
    for t in (test_compte_mutations, test_segment_dominant, test_taux_et_verdict,
              test_score_borne_et_neutre, test_part_et_dep):
        print(f"\n{t.__name__}:")
        t()
    print(f"\n{_ok} ok, {_ko} fail")
    sys.exit(1 if _ko else 0)


if __name__ == "__main__":
    main()
