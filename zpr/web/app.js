/* app.js — Interface (clics, affichage). Toute la logique de calcul est dans
 * zpr-core.js, la récupération de données dans zpr-data.js. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (html != null) e.innerHTML = html;
    return e;
  }
  function num(v) { v = parseFloat(String(v).replace(',', '.')); return isNaN(v) ? null : v; }
  function fmt(n) { return n == null ? '—' : Number(n).toLocaleString('fr-FR'); }

  // ===================== Onglets =====================
  document.querySelectorAll('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('actif'); });
      document.querySelectorAll('.panel').forEach(function (x) { x.classList.remove('actif'); });
      t.classList.add('actif');
      $('#panel-' + t.dataset.tab).classList.add('actif');
    });
  });

  /* ============================================================
   *  ONGLET 1 — OÙ PROSPECTER ? (ZPR)
   * ============================================================ */
  var zprRoot = $('#zpr-rows');

  function zprAddRow(d) {
    d = d || {};
    var card = el('div', { class: 'ville-carte' });
    card.innerHTML =
      '<div class="ville-tete"><strong class="vnom">' + (d.nom || 'Nouvelle ville') + '</strong>' +
      '<button class="btn fantome mini sup">🗑 retirer</button></div>' +
      '<div class="grille">' +
      '  <div><label>Ville</label><input class="f-nom" placeholder="ex. Rouen" value="' + (d.nom || '') + '"></div>' +
      '  <div><label>Code INSEE</label><input class="f-insee" placeholder="ex. 76540" value="' + (d.insee || '') + '"></div>' +
      '  <div><label>Nombre de logements</label><input class="f-log" type="number" placeholder="INSEE" value="' + (d.log != null ? d.log : '') + '"></div>' +
      '  <div><label>Ventes / an (résidentiel)</label><input class="f-mut" type="number" placeholder="DVF" value="' + (d.mut != null ? d.mut : '') + '"></div>' +
      '  <div><label>% propriétaires occ. <span class="opt">(opt.)</span></label><input class="f-prop" type="number" value="' + (d.prop != null ? d.prop : '') + '"></div>' +
      '  <div><label>% de 60 ans + <span class="opt">(opt.)</span></label><input class="f-senior" type="number" value="' + (d.senior != null ? d.senior : '') + '"></div>' +
      '  <div><label>% passoires F/G <span class="opt">(opt.)</span></label><input class="f-fg" type="number" value="' + (d.fg != null ? d.fg : '') + '"></div>' +
      '  <div><label>DPE récents 90j <span class="opt">(opt.)</span></label><input class="f-rec" type="number" value="' + (d.rec != null ? d.rec : '') + '"></div>' +
      '</div>' +
      '<div class="barre"><button class="btn doux mini auto">⚡ Récupérer les chiffres</button>' +
      '<a class="btn fantome mini" href="https://app.dvf.etalab.gouv.fr/" target="_blank" rel="noopener">Carte DVF (ventes)</a>' +
      '<a class="btn fantome mini" href="https://www.insee.fr/fr/statistiques?debut=0&theme=1&categorie=3" target="_blank" rel="noopener">INSEE (logements)</a></div>' +
      '<div class="statut"></div>';
    zprRoot.appendChild(card);
    $('.sup', card).addEventListener('click', function () { card.remove(); });
    $('.f-nom', card).addEventListener('change', function () { $('.vnom', card).textContent = this.value || 'Nouvelle ville'; });
    $('.auto', card).addEventListener('click', function () { zprAuto(card); });
    return card;
  }

  async function zprAuto(card) {
    var st = $('.statut', card);
    var insee = $('.f-insee', card).value.trim();
    var nom = $('.f-nom', card).value.trim();
    try {
      if (!insee && nom) {
        st.textContent = 'Recherche du code INSEE…';
        var matches = await ZPRDATA.searchCommune(nom);
        if (matches && matches.length) {
          insee = matches[0].code;
          $('.f-insee', card).value = insee;
          $('.f-nom', card).value = matches[0].nom; $('.vnom', card).textContent = matches[0].nom;
        }
      }
      if (!insee) { st.textContent = '⚠️ Indique le nom ou le code INSEE de la ville.'; return; }
      st.textContent = 'Récupération des données publiques…';
      try {
        var c = await ZPRDATA.fetchCommune(insee);
        if (c && c.nom && !$('.f-nom', card).value) { $('.f-nom', card).value = c.nom; $('.vnom', card).textContent = c.nom; }
      } catch (e) { /* population non bloquante */ }
      // DVF (ventes/an) — via relais si le direct est bloqué. Peut être un peu long.
      try {
        st.textContent = 'Lecture des ventes (DVF), patiente (~10-30 s)…';
        var rot = await ZPRDATA.fetchRotationDVF(insee, 5, function (an, ok) {
          st.textContent = 'Lecture des ventes ' + an + (ok === null ? ' …' : (ok ? ' ✓' : ' (rien)'));
        });
        if (rot.mut_an != null) $('.f-mut', card).value = rot.mut_an;
        if (rot.segment) card.dataset.segment = rot.segment;
        st.textContent = rot.mut_an != null
          ? '✅ Ventes : ' + rot.mut_an + '/an (moyenne ' + rot.annees.join(', ') + ')' +
            (rot.segment ? ' · segment ' + rot.segment : '')
          : 'ℹ️ Aucune vente trouvée pour cette commune sur la période.';
      } catch (e) {
        st.innerHTML = '⚠️ Récupération des ventes indisponible pour le moment. ' +
          'Ouvre la <a href="https://app.dvf.etalab.gouv.fr/" target="_blank" rel="noopener">carte DVF</a>, ' +
          'compte les ventes de maisons/appartements sur 1 an et saisis le nombre dans « Ventes / an ».';
      }
      // DPE
      try {
        var dpe = await ZPRDATA.fetchDPE(insee);
        if (dpe.total) {
          var pfg = ZPR.part(dpe.passoires_fg, dpe.total);
          if (pfg != null) $('.f-fg', card).value = pfg;
          if (dpe.recents != null) $('.f-rec', card).value = dpe.recents;
        }
      } catch (e) { /* DPE optionnel */ }
    } catch (e) {
      st.textContent = '⚠️ ' + e.message + ' — saisis les chiffres à la main.';
    }
  }

  function zprReadRow(card) {
    return {
      nom: $('.f-nom', card).value.trim() || $('.f-insee', card).value.trim() || 'Ville',
      insee: $('.f-insee', card).value.trim(),
      log: num($('.f-log', card).value),
      mut: num($('.f-mut', card).value),
      prop: num($('.f-prop', card).value),
      senior: num($('.f-senior', card).value),
      fg: num($('.f-fg', card).value),
      rec: num($('.f-rec', card).value),
      segment: card.dataset.segment || null
    };
  }

  function zprCompute() {
    var cards = zprRoot.querySelectorAll('.ville-carte');
    if (!cards.length) { $('#zpr-results').innerHTML = '<div class="carte info">Ajoute au moins une ville.</div>'; return; }
    var res = [];
    cards.forEach(function (card) {
      var r = zprReadRow(card);
      r.taux = ZPR.tauxRotation(r.mut, r.log);
      r.verdict = ZPR.verdictRotation(r.taux);
      r.score = ZPR.scoreOpportunite(r.taux, r.fg, r.prop, r.senior, r.rec);
      res.push(r);
    });
    var ordre = { 'GO': 0, 'INDÉTERMINÉ': 1, 'NO-GO': 2 };
    res.sort(function (a, b) { return (ordre[a.verdict] - ordre[b.verdict]) || (b.score - a.score); });

    var go = res.filter(function (r) { return r.verdict === 'GO'; }).length;
    var html = '<div class="carte"><h2>Classement de décision</h2>' +
      '<p class="aide"><strong>' + go + '/' + res.length + '</strong> ville(s) au-dessus du seuil de ' +
      ZPR.SEUIL_ROTATION + ' % (moyenne nationale ≈ 2,5 %). Le verdict est binaire sur la rotation&nbsp;; ' +
      'le score ne sert qu\'à classer les villes « GO » entre elles.</p>' +
      '<table><thead><tr><th>#</th><th>Ville</th><th>Rotation</th><th>Verdict</th>' +
      '<th>Segment</th><th>F/G</th><th>Score</th></tr></thead><tbody>';
    res.forEach(function (r, i) {
      var cls = r.verdict === 'GO' ? 'go' : (r.verdict === 'NO-GO' ? 'nogo' : '');
      var b = r.verdict === 'GO' ? 'b-go' : (r.verdict === 'NO-GO' ? 'b-nogo' : 'b-ind');
      html += '<tr class="' + cls + '"><td>' + (i + 1) + '</td><td><strong>' + r.nom + '</strong>' +
        (r.insee ? ' <span style="color:#8a94a6">(' + r.insee + ')</span>' : '') + '</td>' +
        '<td>' + (r.taux == null ? '—' : r.taux + ' %') + '</td>' +
        '<td><span class="badge ' + b + '">' + r.verdict + '</span></td>' +
        '<td>' + (r.segment || '—') + '</td>' +
        '<td>' + (r.fg == null ? '—' : r.fg + ' %') + '</td>' +
        '<td>' + r.score + '</td></tr>';
      if (r.verdict === 'INDÉTERMINÉ')
        html += '<tr><td></td><td colspan="6" class="statut">❔ Renseigne « logements » et « ventes/an » pour calculer la rotation.</td></tr>';
    });
    html += '</tbody></table>' +
      '<p class="aide" style="margin-top:10px">⛔ Sous 4 % : ne pas prospecter (présence non rentabilisable). ' +
      'Garages/box exclus du calcul. Copropriétés dégradées&nbsp;: à écarter à la main.</p></div>';
    $('#zpr-results').innerHTML = html;
  }

  $('#zpr-add').addEventListener('click', function () { zprAddRow(); });
  $('#zpr-calc').addEventListener('click', zprCompute);
  $('#zpr-demo').addEventListener('click', function () {
    zprRoot.innerHTML = '';
    // ⚠️ Chiffres d'ILLUSTRATION (pour montrer la mécanique), pas des données réelles.
    [{ nom: 'Rouen (démo)', insee: '76540', log: 75000, mut: 8850, prop: 38, senior: 24, fg: 14, rec: 60, segment: 'Maison < 90 m²' },
     { nom: 'Bordeaux (démo)', insee: '33063', log: 145000, mut: 14790, prop: 33, senior: 21, fg: 11, rec: 90, segment: 'Maison < 90 m²' },
     { nom: 'Chartres (démo)', insee: '28085', log: 14000, mut: 520, prop: 45, senior: 27, fg: 18, rec: 8, segment: 'Appartement T3' }
    ].forEach(function (d) { var c = zprAddRow(d); if (d.segment) c.dataset.segment = d.segment; });
    $('#zpr-results').innerHTML = '<div class="carte info">▶︎ Données d\'illustration chargées (chiffres fictifs). ' +
      'Clique « Calculer le classement » pour voir le résultat, puis remplace par tes vrais chiffres.</div>';
  });
  zprAddRow();   // une ville vide au démarrage

  /* ============================================================
   *  ONGLET 2 — OÙ J'EN SUIS ? (tunnel)
   * ============================================================ */
  var tRoot = $('#t-rows');
  var SOURCES = ['terrain', 'pige', 'warm_list', 'recommandation', 'inbound'];
  var STATUTS = ['contact', 'qualifie', 'estimation', 'mandat', 'perdu'];

  function tAddRow(d) {
    d = d || {};
    var card = el('div', { class: 'ville-carte' });
    function opts(arr, sel) { return arr.map(function (o) { return '<option' + (o === sel ? ' selected' : '') + '>' + o + '</option>'; }).join(''); }
    card.innerHTML =
      '<div class="ville-tete"><strong>' + (d.nom || 'Prospect') + '</strong>' +
      '<button class="btn fantome mini sup">🗑 retirer</button></div>' +
      '<div class="grille">' +
      '  <div><label>Nom / adresse</label><input class="p-nom" value="' + (d.nom || '') + '"></div>' +
      '  <div><label>Source</label><select class="p-src">' + opts(SOURCES, d.source) + '</select></div>' +
      '  <div><label>Statut</label><select class="p-stat">' + opts(STATUTS, d.statut || 'contact') + '</select></div>' +
      '  <div><label>Stade atteint si perdu</label><select class="p-stade">' + opts(['contact', 'qualifie', 'estimation'], d.stade_atteint) + '</select></div>' +
      '  <div><label>Honoraires estimés (€)</label><input class="p-hono" type="number" value="' + (d.honoraires_estimes != null ? d.honoraires_estimes : '') + '"></div>' +
      '  <div><label>Consentement RGPD</label><select class="p-rgpd"><option value="non"' + (d.consentement_rgpd ? '' : ' selected') + '>non</option><option value="oui"' + (d.consentement_rgpd ? ' selected' : '') + '>oui</option></select></div>' +
      '</div>';
    tRoot.appendChild(card);
    $('.sup', card).addEventListener('click', function () { card.remove(); tCompute(); });
    return card;
  }

  function tReadProspects() {
    var out = [];
    tRoot.querySelectorAll('.ville-carte').forEach(function (card) {
      out.push({
        id: ($('.p-nom', card).value || 'p').toLowerCase().replace(/\s+/g, '-'),
        nom: $('.p-nom', card).value,
        source: $('.p-src', card).value,
        statut: $('.p-stat', card).value,
        stade_atteint: $('.p-stade', card).value,
        honoraires_estimes: num($('.p-hono', card).value),
        consentement_rgpd: $('.p-rgpd', card).value === 'oui'
      });
    });
    return out;
  }

  function tReadObjectif() {
    return {
      ca_cible: num($('#o-ca').value), mandats_cibles: num($('#o-mandats').value),
      horizon_mois: num($('#o-horizon').value), date_debut: $('#o-debut').value,
      honoraires_moyens: num($('#o-hono').value),
      ratio_cible: { contact: 30, qualifie: 5, estimation: 2, mandat: 1 }
    };
  }

  function pct(x) { return x == null ? '—' : (Math.round(x * 1000) / 10) + ' %'; }

  function tCompute() {
    var obj = tReadObjectif();
    var pros = tReadProspects();
    var counts = ZPR.etatFunnel(pros);
    var tr = ZPR.tauxConversion(counts);
    var tc = ZPR.ratioCibleTaux(obj.ratio_cible);
    var hmA = ZPR.honorairesMoyens(obj); var hm = hmA[0];
    var caR = ZPR.caRealise(pros, hm);
    var caP = ZPR.caPondere(counts, obj.ratio_cible, hm);
    var ref = new Date();
    var proj = ZPR.projection(obj, counts, ref);
    var vol = ZPR.volumeRequis(obj, counts, tr, ref);
    var risque = ZPR.controleConformite(pros, ref);
    var maxc = Math.max(counts.contact, 1);

    var h = '<div class="carte"><h2>Tableau de bord</h2>';
    // KPI
    h += '<div class="kpi">' +
      '<div class="b"><div class="v">' + counts.mandat + (obj.mandats_cibles ? ' / ' + obj.mandats_cibles : '') + '</div><div class="l">Mandats signés</div></div>' +
      '<div class="b"><div class="v">' + fmt(caR) + ' €</div><div class="l">CA signé' + (obj.ca_cible ? ' / ' + fmt(obj.ca_cible) + ' €' : '') + '</div></div>' +
      '<div class="b"><div class="v">' + (caP == null ? '—' : fmt(caP) + ' €') + '</div><div class="l">CA pondéré du pipeline</div></div>' +
      (proj ? '<div class="b"><div class="v ' + (proj.on_track ? 'ok' : 'warn') + '">' + proj.projete_echeance + '</div><div class="l">Mandats projetés à l\'échéance</div></div>' : '') +
      '</div>';
    // Entonnoir
    h += '<h2 style="margin-top:14px">Entonnoir (cible 30 → 5 → 2 → 1)</h2><div class="funnel">';
    [['contact', 'Contacts', null], ['qualifie', 'Qualifiés', 'qualifie/contact'],
     ['estimation', 'Estimations', 'estimation/qualifie'], ['mandat', 'Mandats', 'mandat/estimation']]
      .forEach(function (s) {
        var w = Math.round(counts[s[0]] / maxc * 480);
        var taux = s[2] ? ' · réel ' + pct(tr[s[2]]) + ' (cible ' + pct(tc[s[2]]) + ')' : '';
        h += '<div class="row"><div class="lab">' + s[1] + taux + '</div>' +
          '<div class="bar" style="width:' + w + 'px"></div><div class="val">' + counts[s[0]] + '</div></div>';
      });
    h += '</div>';
    // Projection + volume
    if (proj) {
      var etat = proj.on_track ? '<span class="ok">✅ sur la trajectoire</span>' : '<span class="warn">⚠️ sous la trajectoire</span>';
      h += '<p class="aide">' + proj.mandats_signes + ' mandat(s) en ' + proj.mois_ecoules + ' mois → ' +
        proj.rate_mandats_mois + ' mandat/mois · projeté ' + proj.projete_echeance +
        ' (cible ' + proj.cible + ', écart ' + (proj.ecart >= 0 ? '+' : '') + proj.ecart + ') — ' + etat + '</p>';
    }
    if (vol) {
      h += '<div class="info">🚜 Pour signer les <strong>' + vol.mandats_restants + ' mandats restants</strong>' +
        (vol.semaines_restantes != null ? ' d\'ici l\'échéance (' + vol.semaines_restantes + ' semaines)' : '') +
        ', base de taux : <em>' + vol.base_taux + '</em> :<br>' +
        '<strong>' + fmt(vol.contacts_a_produire) + ' contacts</strong> → ' + fmt(vol.qualifs_a_produire) +
        ' qualifiés → ' + fmt(vol.estimations_a_produire) + ' estimations' +
        (vol.contacts_par_semaine ? '<br>Cadence : <strong>~' + vol.contacts_par_semaine + ' contacts/semaine</strong> (≈ 2 h de prospection/jour).' :
          '<br>⏰ Échéance atteinte/dépassée : recale la date de début ou l\'horizon.') + '</div>';
    }
    // Conformité
    if (ref >= new Date('2026-08-11')) {
      h += risque.length
        ? '<div class="alerte" style="margin-top:10px">⚠️ ' + risque.length + ' prospect(s) à risque si appel à froid (ni consentement, ni contrat) : ' +
          risque.slice(0, 15).join(', ') + '. → privilégie l\'inbound / la recommandation, ou obtiens le consentement.</div>'
        : '<div class="info" style="margin-top:10px">✅ Aucun prospect en infraction d\'appel à froid.</div>';
    } else {
      h += '<p class="aide">Bascule Bloctel du 11/08/2026 pas encore atteinte — anticipe en bâtissant le consentement dès maintenant.</p>';
    }
    h += '</div>';
    $('#t-dashboard').innerHTML = h;
  }

  // Recalcule à chaque changement (sans réécrire les champs -> pas de perte de focus).
  ['input', 'change'].forEach(function (ev) {
    $('#panel-tunnel').addEventListener(ev, function (e) {
      if (e.target.closest('#t-rows') || e.target.closest('.carte')) tCompute();
    });
  });
  $('#t-add').addEventListener('click', function () { tAddRow(); tCompute(); });
  $('#t-demo').addEventListener('click', function () {
    tRoot.innerHTML = '';
    [{ nom: 'M. Dupont — 12 rue des Lilas', source: 'terrain', statut: 'estimation', honoraires_estimes: 9500, consentement_rgpd: true },
     { nom: 'Succession Martin — 4 place du Marché', source: 'recommandation', statut: 'mandat', honoraires_estimes: 11000, consentement_rgpd: true },
     { nom: 'Annonce PAP — 7 av. Jean Moulin', source: 'pige', statut: 'qualifie', consentement_rgpd: false }
    ].forEach(tAddRow);
    tCompute();
  });
  tAddRow(); tCompute();   // un prospect vide + tableau de bord au démarrage
})();
