/* zpr-data.js — Récupération des données publiques DEPUIS LE NAVIGATEUR.
 * (DVF, DPE/ADEME, communes geo.api). Optionnel : si un service bloque l'accès
 * direct (CORS) ou est lent, l'interface bascule sur la saisie manuelle.
 * Aucune clé, aucune installation. */
(function (global) {
  'use strict';

  function depFromInsee(insee) {
    insee = String(insee).toUpperCase();
    var p2 = insee.slice(0, 2);
    if (p2 === '2A' || p2 === '2B') return p2;
    if (p2 === '97' || p2 === '98') return insee.slice(0, 3);
    return p2;
  }

  // Parse CSV (gère guillemets et délimiteur , ou ;).
  function parseCSV(text) {
    text = text.replace(/^﻿/, '');
    var lines = text.split(/\r\n|\n/).filter(function (l) { return l.length; });
    if (!lines.length) return [];
    var delim = (lines[0].split(';').length > lines[0].split(',').length) ? ';' : ',';
    function split(line) {
      var out = [], cur = '', q = false;
      for (var i = 0; i < line.length; i++) {
        var ch = line[i];
        if (q) {
          if (ch === '"') { if (line[i + 1] === '"') { cur += '"'; i++; } else q = false; }
          else cur += ch;
        } else {
          if (ch === '"') q = true;
          else if (ch === delim) { out.push(cur); cur = ''; }
          else cur += ch;
        }
      }
      out.push(cur); return out;
    }
    var hdr = split(lines[0]); var rows = [];
    for (var i = 1; i < lines.length; i++) {
      var f = split(lines[i]); var o = {};
      for (var j = 0; j < hdr.length; j++) o[hdr[j]] = f[j];
      rows.push(o);
    }
    return rows;
  }

  async function fetchCommune(insee) {
    var r = await fetch('https://geo.api.gouv.fr/communes/' + insee +
      '?fields=nom,code,population,codesPostaux,codeDepartement');
    if (!r.ok) throw new Error('geo ' + r.status);
    return r.json();
  }

  async function searchCommune(nom) {
    var r = await fetch('https://geo.api.gouv.fr/communes?nom=' +
      encodeURIComponent(nom) +
      '&fields=nom,code,population,codeDepartement&boost=population&limit=7');
    if (!r.ok) throw new Error('geo ' + r.status);
    return r.json();
  }

  // Certains fichiers publics (DVF) ne sont pas accessibles en direct depuis un
  // navigateur (protection « CORS »). On tente le direct, puis un « relais »
  // public qui, lui, est autorisé. Données 100 % publiques (open data) -> OK.
  var RELAIS = [
    function (u) { return 'https://corsproxy.io/?url=' + encodeURIComponent(u); },
    function (u) { return 'https://api.allorigins.win/raw?url=' + encodeURIComponent(u); }
  ];
  // Renvoie {status, text}. status 404 = absent (à ignorer), throw = inaccessible.
  async function fetchText(url) {
    try {
      var r = await fetch(url);
      if (r.status === 404) return { status: 404, text: '' };
      if (r.ok) return { status: 200, text: await r.text() };
    } catch (e) { /* CORS/réseau -> on tente les relais */ }
    for (var i = 0; i < RELAIS.length; i++) {
      try {
        var r2 = await fetch(RELAIS[i](url));
        if (r2.ok) { var t = await r2.text(); if (t && t.length) return { status: 200, text: t }; }
      } catch (e2) { /* relais suivant */ }
    }
    throw new Error('inaccessible');
  }
  async function fetchJSON(url) {
    var res = await fetchText(url);
    try { return JSON.parse(res.text); } catch (e) { throw new Error('réponse illisible'); }
  }

  // Télécharge + compte les mutations résidentielles sur N années (geo-dvf).
  // onProgress(année, dispo) pour le retour visuel.
  async function fetchRotationDVF(insee, nbAnnees, onProgress) {
    var dep = depFromInsee(insee);
    var cur = new Date().getFullYear();
    var anneesOk = [], total = 0, types = [], surf = [], pieces = [];
    var erreurDure = null;
    for (var an = cur - 1; an > cur - 1 - (nbAnnees + 2) && anneesOk.length < nbAnnees; an--) {
      var url = 'https://files.data.gouv.fr/geo-dvf/latest/csv/' + an +
        '/communes/' + dep + '/' + insee + '.csv';
      var res;
      try {
        if (onProgress) onProgress(an, null);     // "en cours"
        res = await fetchText(url);
      } catch (e) { erreurDure = e; break; }       // ni direct ni relais -> on arrête
      if (res.status === 404 || !res.text) { if (onProgress) onProgress(an, false); continue; }
      var rows = parseCSV(res.text);
      // Garde-fou : ignore une page d'erreur renvoyée par un relais (pas du DVF).
      if (!rows.length || !('id_mutation' in rows[0])) { if (onProgress) onProgress(an, false); continue; }
      var c = ZPR.compteMutations(rows);
      total += c.n_mutations; types = types.concat(c.types);
      surf = surf.concat(c.surfaces); pieces = pieces.concat(c.pieces);
      anneesOk.push(an);
      if (onProgress) onProgress(an, true);
    }
    if (!anneesOk.length && erreurDure) throw erreurDure;   // déclenche le message manuel
    var mutAn = anneesOk.length ? Math.round(total / anneesOk.length * 10) / 10 : null;
    return {
      annees: anneesOk, total: total, mut_an: mutAn,
      segment: ZPR.segmentDominant(types, surf, pieces)
    };
  }

  async function dpeTotal(insee, extra) {
    var qs = 'code_insee_ban:"' + insee + '"' + (extra ? (' AND ' + extra) : '');
    var url = 'https://data.ademe.fr/data-fair/api/v1/datasets/' +
      'dpe-v2-logements-existants/lines?size=0&qs=' + encodeURIComponent(qs);
    var j = await fetchJSON(url);
    return j.total;
  }

  async function fetchDPE(insee) {
    var depuis = new Date(Date.now() - 90 * 86400000).toISOString().slice(0, 10);
    var total = await dpeTotal(insee, '');
    var fg = await dpeTotal(insee, '(etiquette_dpe:"F" OR etiquette_dpe:"G")');
    var recents = await dpeTotal(insee, 'date_etablissement_dpe:[' + depuis + ' TO *]');
    return { total: total, passoires_fg: fg, recents: recents };
  }

  global.ZPRDATA = {
    depFromInsee: depFromInsee, parseCSV: parseCSV, fetchCommune: fetchCommune,
    searchCommune: searchCommune, fetchRotationDVF: fetchRotationDVF, fetchDPE: fetchDPE
  };
})(window);
