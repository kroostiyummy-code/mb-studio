/* zpr-core.js — Cœur de calcul PARTAGÉ (ZPR + tunnel), sans dépendance.
 * Mêmes formules que les pipelines Python (run_zpr.py / tunnel/run_tunnel.py).
 * Fonctionne dans le navigateur (window.ZPR) ET sous Node (module.exports),
 * pour pouvoir tester la logique hors-ligne. Aucune ligne de commande requise
 * côté utilisateur : ce fichier est chargé par index.html. */
(function (global) {
  'use strict';

  // ===================== ZPR (Étapes 1 & 2) =====================
  var SEUIL_ROTATION = 4.0;                       // % : seuil critique de rentabilité
  var RESIDENTIEL = { 'Maison': 1, 'Appartement': 1 };
  var VENTES = { 'Vente': 1, "Vente en l'état futur d'achèvement": 1 };

  function median(arr) {
    if (!arr.length) return null;
    var a = arr.slice().sort(function (x, y) { return x - y; });
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  }

  // Compte les VRAIES mutations résidentielles (dédup par id, garages/box exclus).
  function compteMutations(rows) {
    var parMut = {};
    rows.forEach(function (r) {
      var idm = r.id_mutation || r.id;
      if (!idm) return;
      var nat = (r.nature_mutation || '').trim();
      var typ = (r.type_local || '').trim();
      var m = parMut[idm] || (parMut[idm] = { resid: false, vente: false, types: [], surf: [], pieces: [] });
      if (VENTES[nat]) m.vente = true;
      if (RESIDENTIEL[typ]) {
        m.resid = true; m.types.push(typ);
        var s = parseFloat(String(r.surface_reelle_bati || '').replace(',', '.'));
        if (s > 0) m.surf.push([typ, s]);
        var p = parseInt(r.nombre_pieces_principales || 0, 10);
        if (p > 0) m.pieces.push([typ, p]);
      }
    });
    var retenues = Object.keys(parMut).map(function (k) { return parMut[k]; })
      .filter(function (m) { return m.resid && m.vente; });
    var types = [], surf = [], pieces = [];
    retenues.forEach(function (m) {
      types = types.concat(m.types); surf = surf.concat(m.surf); pieces = pieces.concat(m.pieces);
    });
    return { n_mutations: retenues.length, types: types, surfaces: surf, pieces: pieces };
  }

  function segmentDominant(types, surfaces, pieces) {
    if (!types.length) return null;
    var c = {}; types.forEach(function (t) { c[t] = (c[t] || 0) + 1; });
    var dom = Object.keys(c).reduce(function (a, b) { return c[b] > c[a] ? b : a; });
    if (dom === 'Maison') {
      var ss = surfaces.filter(function (x) { return x[0] === 'Maison'; }).map(function (x) { return x[1]; });
      if (!ss.length) return 'Maison';
      var med = median(ss);
      return 'Maison ' + (med < 90 ? '< 90 m²' : (med <= 130 ? '90-130 m²' : '> 130 m²'));
    }
    if (dom === 'Appartement') {
      var pp = pieces.filter(function (x) { return x[0] === 'Appartement'; }).map(function (x) { return x[1]; });
      if (!pp.length) return 'Appartement';
      var med2 = median(pp);
      return 'Appartement ' + (med2 <= 2 ? 'T1-T2' : (med2 === 3 ? 'T3' : 'T4+'));
    }
    return dom;
  }

  function tauxRotation(mutAn, nbLog) {
    if (!nbLog || mutAn === null || mutAn === undefined) return null;
    return Math.round(mutAn / nbLog * 100 * 100) / 100;
  }
  function verdictRotation(t) {
    if (t === null || t === undefined) return 'INDÉTERMINÉ';
    return t >= SEUIL_ROTATION ? 'GO' : 'NO-GO';
  }
  function part(n, total) {
    if (n === null || n === undefined || !total) return null;
    return Math.round(n / total * 100 * 10) / 10;
  }
  function scoreOpportunite(taux, partFG, partProprio, partSenior, dpeRecents) {
    function n(x, lo, hi) {
      if (x === null || x === undefined) return 0.5;
      return Math.max(0, Math.min(1, (x - lo) / (hi - lo)));
    }
    var s = 0.40 * n(taux, 4, 12) + 0.20 * n(partProprio, 40, 75)
      + 0.15 * n(partSenior, 15, 35) + 0.15 * n(partFG, 5, 25)
      + 0.10 * ((dpeRecents || 0) > 0 ? 1 : 0.5);
    return Math.round(s * 100);
  }

  // ===================== TUNNEL (Étapes 4 & 5) =====================
  var STAGES = ['contact', 'qualifie', 'estimation', 'mandat'];

  function stadeMax(p) {
    var st = (p.statut || '').trim().toLowerCase();
    if (STAGES.indexOf(st) >= 0) return st;
    if (st === 'perdu') {
      var sa = (p.stade_atteint || 'contact').trim().toLowerCase();
      return STAGES.indexOf(sa) >= 0 ? sa : 'contact';
    }
    return 'contact';
  }
  function etatFunnel(prospects) {
    var counts = { contact: 0, qualifie: 0, estimation: 0, mandat: 0 };
    prospects.forEach(function (p) {
      var smi = STAGES.indexOf(stadeMax(p));
      STAGES.forEach(function (s, i) { if (i <= smi) counts[s]++; });
    });
    return counts;
  }
  function r4(a, b) { return a ? Math.round(b / a * 10000) / 10000 : null; }
  function tauxConversion(c) {
    return {
      'qualifie/contact': r4(c.contact, c.qualifie),
      'estimation/qualifie': r4(c.qualifie, c.estimation),
      'mandat/estimation': r4(c.estimation, c.mandat),
      'mandat/contact': r4(c.contact, c.mandat)
    };
  }
  function ratioCibleTaux(ratio) {
    var c = ratio.contact, q = ratio.qualifie, e = ratio.estimation, m = ratio.mandat;
    return {
      'qualifie/contact': c ? Math.round(q / c * 10000) / 10000 : null,
      'estimation/qualifie': q ? Math.round(e / q * 10000) / 10000 : null,
      'mandat/estimation': e ? Math.round(m / e * 10000) / 10000 : null,
      'mandat/contact': c ? Math.round(m / c * 10000) / 10000 : null
    };
  }
  function honorairesMoyens(obj) {
    if (obj.honoraires_moyens) return [Number(obj.honoraires_moyens), false];
    if (obj.ca_cible && obj.mandats_cibles) return [Math.round(obj.ca_cible / obj.mandats_cibles), true];
    return [null, true];
  }
  function caRealise(prospects, hm) {
    var t = 0;
    prospects.forEach(function (p) {
      if (stadeMax(p) === 'mandat' && (p.statut || '').toLowerCase() === 'mandat')
        t += Number(p.honoraires_estimes || hm || 0);
    });
    return Math.round(t);
  }
  function caPondere(counts, ratio, hm) {
    if (!hm) return null;
    var t = ratioCibleTaux(ratio);
    var pM = {
      contact: t['mandat/contact'],
      qualifie: (t['estimation/qualifie'] || 0) * (t['mandat/estimation'] || 0),
      estimation: t['mandat/estimation'], mandat: 1
    };
    var exact = {};
    STAGES.forEach(function (s, i) { var nxt = STAGES[i + 1]; exact[s] = counts[s] - (nxt ? counts[nxt] : 0); });
    var val = STAGES.reduce(function (acc, s) { return acc + exact[s] * (pM[s] || 0); }, 0);
    return Math.round(val * hm);
  }
  function semainesRestantes(obj, dateRef) {
    if (!obj.date_debut || !obj.horizon_mois) return null;
    var d0 = new Date(obj.date_debut);
    var fin = new Date(d0.getTime() + Math.round(obj.horizon_mois * 30.44) * 86400000);
    return Math.round(Math.max(0, (fin - dateRef) / 86400000) / 7 * 10) / 10;
  }
  function projection(obj, counts, dateRef) {
    if (!obj.date_debut || !obj.horizon_mois) return null;
    var d0 = new Date(obj.date_debut);
    var moisEcoules = Math.max((dateRef - d0) / 86400000, 1) / 30.44;
    var signes = counts.mandat || 0;
    var rate = signes / moisEcoules;
    var projete = Math.round(rate * obj.horizon_mois * 10) / 10;
    var cible = obj.mandats_cibles;
    return {
      mois_ecoules: Math.round(moisEcoules * 10) / 10, mandats_signes: signes,
      rate_mandats_mois: Math.round(rate * 100) / 100, projete_echeance: projete,
      cible: cible, ecart: (cible != null ? Math.round((projete - cible) * 10) / 10 : null),
      on_track: (cible != null ? projete >= cible : null)
    };
  }
  function volumeRequis(obj, counts, tauxReels, dateRef) {
    var cible = obj.mandats_cibles; if (cible == null) return null;
    var ratio = obj.ratio_cible || {}; var restant = Math.max(0, cible - (counts.mandat || 0));
    var tc = ratioCibleTaux(ratio);
    var assez = (counts.contact || 0) >= (ratio.contact || 30);
    function eff(k) { return (assez ? tauxReels[k] : null) || tc[k]; }
    var rmc = eff('mandat/contact') || tc['mandat/contact'];
    var req = eff('estimation/qualifie') || tc['estimation/qualifie'];
    var rme = eff('mandat/estimation') || tc['mandat/estimation'];
    var contacts = rmc ? Math.round(restant / rmc) : null;
    var qualifs = (rme && req) ? Math.round(restant / (rme * req)) : null;
    var estims = rme ? Math.round(restant / rme) : null;
    var sem = semainesRestantes(obj, dateRef);
    var parSem = (contacts && sem) ? Math.round(contacts / sem * 10) / 10 : null;
    return {
      mandats_restants: restant, contacts_a_produire: contacts,
      qualifs_a_produire: qualifs, estimations_a_produire: estims,
      semaines_restantes: sem, contacts_par_semaine: parSem,
      base_taux: assez ? 'réels' : 'cibles (échantillon < 30 contacts)'
    };
  }
  function controleConformite(prospects, dateRef) {
    var bascule = new Date('2026-08-11'); var risque = [];
    prospects.forEach(function (p) {
      var consent = !!p.consentement_rgpd; var contrat = stadeMax(p) === 'mandat';
      var src = (p.source || '').toLowerCase(); var froid = (src === 'pige' || src === 'terrain' || src === '');
      if (dateRef >= bascule && froid && !consent && !contrat) risque.push(p.nom || p.id || '?');
    });
    return risque;
  }

  var API = {
    SEUIL_ROTATION: SEUIL_ROTATION, STAGES: STAGES, median: median,
    compteMutations: compteMutations, segmentDominant: segmentDominant,
    tauxRotation: tauxRotation, verdictRotation: verdictRotation, part: part,
    scoreOpportunite: scoreOpportunite, stadeMax: stadeMax, etatFunnel: etatFunnel,
    tauxConversion: tauxConversion, ratioCibleTaux: ratioCibleTaux,
    honorairesMoyens: honorairesMoyens, caRealise: caRealise, caPondere: caPondere,
    semainesRestantes: semainesRestantes, projection: projection,
    volumeRequis: volumeRequis, controleConformite: controleConformite
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  global.ZPR = API;
})(typeof window !== 'undefined' ? window : globalThis);
