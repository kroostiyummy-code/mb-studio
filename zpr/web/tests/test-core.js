/* Self-test Node du cœur de calcul de la page web (mêmes cas que les pipelines
 * Python). Lance :  node zpr/web/tests/test-core.js  */
var Z = require('../zpr-core.js');
var ok = 0, ko = 0;
function check(label, cond) {
  if (cond) { ok++; console.log('  ok   ' + label); }
  else { ko++; console.log('  FAIL ' + label); }
}

// --- ZPR ---
var rows = [
  { id_mutation: '1', nature_mutation: 'Vente', type_local: 'Maison', surface_reelle_bati: '82', nombre_pieces_principales: '4' },
  { id_mutation: '2', nature_mutation: 'Vente', type_local: 'Maison', surface_reelle_bati: '95', nombre_pieces_principales: '5' },
  { id_mutation: '2', nature_mutation: 'Vente', type_local: 'Dépendance', surface_reelle_bati: '18' },
  { id_mutation: '3', nature_mutation: 'Vente', type_local: 'Dépendance', surface_reelle_bati: '14' },
  { id_mutation: '4', nature_mutation: 'Vente', type_local: 'Appartement', surface_reelle_bati: '44', nombre_pieces_principales: '2' },
  { id_mutation: '5', nature_mutation: 'Donation', type_local: 'Maison', surface_reelle_bati: '110', nombre_pieces_principales: '5' },
  { id_mutation: '7', nature_mutation: 'Vente', type_local: 'Maison', surface_reelle_bati: '78', nombre_pieces_principales: '3' }
];
var c = Z.compteMutations(rows);
check('4 mutations résidentielles (dédup + exclusions)', c.n_mutations === 4);
check('segment = Maison < 90 m²', Z.segmentDominant(c.types, c.surfaces, c.pieces) === 'Maison < 90 m²');
check('τ_R arrondi', Z.tauxRotation(40, 1000) === 4.0);
check('denominateur inconnu -> null', Z.tauxRotation(40, null) === null);
check('verdict GO au seuil', Z.verdictRotation(4.0) === 'GO');
check('verdict NO-GO sous seuil', Z.verdictRotation(3.99) === 'NO-GO');
check('verdict INDÉTERMINÉ si null', Z.verdictRotation(null) === 'INDÉTERMINÉ');
check('part F/G', Z.part(50, 200) === 25.0);
var s1 = Z.scoreOpportunite(8, 15, 60, 25, 5);
check('score dans [0,100]', s1 >= 0 && s1 <= 100);
check('score neutre ~50 quand tout manque',
  Z.scoreOpportunite(null, null, null, null, null) >= 45 && Z.scoreOpportunite(null, null, null, null, null) <= 55);

// --- Tunnel ---
function mk(n, stade, extra) { var a = []; for (var i = 0; i < n; i++) { var p = { id: stade + i, statut: stade }; if (extra) Object.assign(p, extra); a.push(p); } return a; }
var PROS = mk(25, 'contact').concat(mk(3, 'qualifie'), mk(1, 'estimation'),
  mk(1, 'mandat', { honoraires_estimes: 12000, consentement_rgpd: true }));
var OBJ = { ca_cible: 100000, mandats_cibles: 10, horizon_mois: 6, date_debut: '2026-01-01', honoraires_moyens: 10000, ratio_cible: { contact: 30, qualifie: 5, estimation: 2, mandat: 1 } };
var counts = Z.etatFunnel(PROS);
check('entonnoir 30/5/2/1', counts.contact === 30 && counts.qualifie === 5 && counts.estimation === 2 && counts.mandat === 1);
var tr = Z.tauxConversion(counts);
check('taux global contact->mandat 0.0333', tr['mandat/contact'] === 0.0333);
check('perdu compte jusqu\'à stade_atteint', Z.stadeMax({ statut: 'perdu', stade_atteint: 'estimation' }) === 'estimation');
check('honoraires moyens lus', Z.honorairesMoyens(OBJ)[0] === 10000 && Z.honorairesMoyens(OBJ)[1] === false);
check('CA signé = honoraires du mandat', Z.caRealise(PROS, 10000) === 12000);
var ref = new Date('2026-04-01');
var proj = Z.projection(OBJ, counts, ref);
check('run-rate ~0.34/mois', Math.round(proj.rate_mandats_mois * 100) / 100 === 0.34);
check('projeté à 6 mois ~2', proj.projete_echeance === 2.0);
check('sous la trajectoire', proj.on_track === false);
var vol = Z.volumeRequis(OBJ, counts, tr, ref);
check('9 mandats restants', vol.mandats_restants === 9);
check('270 contacts à produire', vol.contacts_a_produire === 270);
var froid = [{ id: 'a', nom: 'A', source: 'pige', statut: 'contact', consentement_rgpd: false }];
check('appel à froid signalé après 11/08/2026', JSON.stringify(Z.controleConformite(froid, new Date('2026-09-01'))) === '["A"]');
check('rien signalé avant la bascule', Z.controleConformite(froid, new Date('2026-06-01')).length === 0);

console.log('\n' + ok + ' ok, ' + ko + ' fail');
process.exit(ko ? 1 : 0);
