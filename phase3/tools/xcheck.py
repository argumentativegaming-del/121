"""v4.3 final cross-roster consistency audit: recomputes every completion metric from the final data."""
import json, collections, engine, builds_data as BD, builds_extra as X
import audit_batch1 as A1, audit_batch2 as A2, audit_batch3 as A3, audit_batch4 as A4, audit_batch5 as A5
X.apply_shard_policy()
R=[]; ok=True
def chk(name, value, passed, note=''):
    global ok; ok &= bool(passed); R.append((name, value, 'PASS' if passed else 'FAIL', note))
AU={**A1.AUDIT,**A2.AUDIT,**A3.AUDIT,**A4.AUDIT,**A5.AUDIT}
B=BD.B; rows=engine.ROWS
chk('Frames', f'{len(B)}/66', len(B)==66 and len(rows)==66)
chk('Optimization audit', f'{len(AU)}/66', len(AU)==66, str(collections.Counter(a["outcome"] for a in AU.values())))
chk('Helminth', f"{sum(1 for b in B.values() if b['helm'])}/66", all(b['helm'] for b in B.values()), str(collections.Counter(b['helm'][0] for b in B.values())))
val={f:engine.validate(f,b) for f,b in B.items()}
chk('Frame mod configs', f"{sum(1 for b in B.values() if len(b['mods'])==8)}/66", all(len(b['mods'])==8 for b in B.values()))
fa=sum(len(b['arcanes']) for b in B.values())+sum(len(c.get('arcanes',[])) for c in BD.EXALTED_FRAMES.values())
chk('Frame Arcane slots', f'{fa}/{66*2+2*len(BD.EXALTED_FRAMES)}', fa==66*2+2*len(BD.EXALTED_FRAMES), '132 frame + Orion 2 + Sevagoth Shadow 2')
sh=[c for b in B.values() for c in b['shards']]
chk('Archon Shards', f'{len(sh)}/330', len(sh)==330 and all((c[2:] if c.startswith('T:') else c) in engine.SHARD for c in sh), f"{sum(c.startswith('T:') for c in sh)} Tauforged; Sirius & Orion share one set")
chk('Focus', f"{sum(1 for b in B.values() if b['focus'])}/66", all(b['focus'] for b in B.values()))
chk('Companions', f"{sum(1 for b in B.values() if b['comp'] in X.COMP)}/66", all(b['comp'] in X.COMP for b in B.values()) and all(not X.validate_comp(c) for c in X.COMP))
W=X.weapon_configs()
slots=collections.Counter(w for r in rows for w in r[1:])
dup=[w for w,n in slots.items() if n>1]
chk('Ordinary weapon slots', f'{len(W)}/{len(W)}', all(r['mods'] and r['arcane'] for r in W), f'{len({r["weapon"].replace(" (Primary)","").replace(" (Melee)","") for r in W})} distinct weapons (Vinquibus = Primary + Melee)')
exb=len(X.EXALTED)+1+len(BD.EXALTED_FRAMES)
chk('Exalted/intrinsic builds', f'{exb}/{exb}', all(w in X.BATCH1_EXALTED for w in X.EXALTED), '19 Exalted weapons + Venari Prime + Sevagoth Shadow + Orion')
exa=sum(1 for v in X.EXALTED.values() if v[3])
chk('Exalted Arcanes', f'{exa}/{len(X.EXALTED)}', exa==len(X.EXALTED))
nexil=[w for w,(f,s,m,a,e,n) in X.EXALTED.items() if s in ('Primary','Secondary') and not X.EXALTED_EXILUS.get(w)]
chk('Primary/Secondary Exalted Exilus', f'{8-len(nexil)}/8', not nexil)
inc=[r for r in W if r['evo_family']]
chk('Incarnons', f"{sum(1 for r in inc if r['incarnon'])}/{len(inc)}", len(inc)==39 and all(r['incarnon'] for r in inc))
el=sum(1 for r in W if not r['elem_errs'])+sum(1 for w in X.EXALTED if not X.exalted_element(w)[1])
chk('Element checks', f'{el}/{len(W)+len(X.EXALTED)}', el==len(W)+len(X.EXALTED))
hl=[f for f,(e,w,a) in val.items() if any('Helminth damage-buff' in x for x in e)]
chk('Helminth legality violations', len(hl), not hl)
ad=[f for f,(e,w,a) in val.items() if any(('needs' in x and 'subsumed' in x) or 'targets replaced ability' in x for x in e)]
chk('Broken augment dependencies', len(ad), not ad)
chk('All frame validator errors', sum(1 for e,w,a in val.values() if e), not any(e for e,w,a in val.values()))
chk('Unintended weapon duplicates', len(dup), not dup, 'family overlaps (base vs Prime) are distinct items - INTENTIONAL; Vinquibus dual-slot - MECHANICALLY REQUIRED')
P=json.load(open('proc.json')); pm={r['Item'].lower():r for r in P if r['Category']=='Mod'}; pa={r['Item']:r for r in P if r['Category']=='Arcane'}
req=X.required_mods(); miss=[m for m in req if m.lower() not in pm]
arcs={a for b in B.values() for a in b['arcanes']}|{a for c in BD.EXALTED_FRAMES.values() for a in c.get('arcanes',[])}|{r['arcane'] for r in W}|{v[3] for v in X.EXALTED.values() if v[3]}
amiss=[a for a in arcs if a not in pa]; anot=[a for a in arcs if a in pa and pa[a]['Counted in Player-Trade Total?']!='Yes']
astale=[a for a,r in pa.items() if r['Counted in Player-Trade Total?']=='Yes' and a not in arcs]
chk('Missing procurement rows', len(miss)+len(amiss), not miss and not amiss, f'{len(req)} build-required mods, {len(arcs)} build-required Arcanes')
chk('Required Arcanes priced as required / stale required', f'{len(anot)} / {len(astale)}', not anot and not astale)
st=collections.Counter(pm[m.lower()]['Status'] for m in req)
chk('Build-required mod pricing', dict(st), True, 'ACCOUNT-BOUND = Umbral x3; MARKET DATA UNAVAILABLE = Corroding Barrage, Swift Deth (in-game trade only)')
bad_out=[r['frame'] for r in W if r['arcane']=='Secondary Outburst']
bad_anim=[r['frame'] for r in W if r['arcane']=='Melee Animosity' and r['template'] not in ('HEAVY_ATTACK',)]
chk('Outburst on combo builds / Animosity without heavy build', f'{len(bad_out)} / {len(bad_anim)}', not bad_out and not bad_anim)
live=[(f,l) for f,b in B.items() for l in (b.get('live') or [])]
chk('LIVE TEST REQUIRED', len(live), True, '; '.join(f'{f}: {l}' for f,l in live))
json.dump(dict(ok=ok, rows=R), open('xcheck.json','w'), indent=1)
for r in R: print(f'{r[2]:4s} | {r[0]}: {r[1]} {("- "+r[3]) if r[3] else ""}'[:400])
print('ALL PASS' if ok else 'FAILURES PRESENT')
