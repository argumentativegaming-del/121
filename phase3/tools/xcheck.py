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
unpriced=[m for m in req if 'UNAVAILABLE' in str(pm[m.lower()]['Status'])]
chk('Build-required mod pricing', dict(st), not unpriced, f'{sum(1 for m in req if pm[m.lower()]["Status"]=="OK")} market-priced; ACCOUNT-BOUND (earned, 0p) = '+', '.join(sorted(m for m in req if pm[m.lower()]['Status']=='ACCOUNT-BOUND'))+f'; unpriced = {len(unpriced)}')
_ARCH=set(json.load(open('archived_list.json')))
arch=sorted(m for m in req if m in _ARCH)
chk('Archived (unobtainable) mods in final builds', len(arch), not arch, ', '.join(arch) or 'wiki {{Archived}} list checked against every build-required mod')
_MD=json.load(open('mods.json'))['Mods']
_alts={k:[i for i in (v.get('Incompatible') or []) if i in req] for k,v in _MD.items() if v.get('Tradable') is False and not v.get('IsFlawed')}
for k,v in _MD.items():
    base=k.replace('Primed ','').replace('Amalgam ','').replace('Umbral ','')
    if v.get('Tradable') is False and not v.get('IsFlawed') and base!=k and base in req: _alts.setdefault(k,[]).append(base)
unruled=sorted(k for k,v in _alts.items() if v and k not in X.ACCOUNT_BOUND_RULINGS)
restore_missing=sorted(k for k,(a,r,w) in X.ACCOUNT_BOUND_RULINGS.items() if r.startswith('RESTORE') and k not in req)
chk('Account-bound alternatives ruled on mechanics (no procurement substitution)', f'{len(unruled)} unruled / {len(restore_missing)} RESTORE rulings not in builds', not unruled and not restore_missing,
    '; '.join(f'{k}: {r}' for k,(a,r,w) in X.ACCOUNT_BOUND_RULINGS.items()))
bad_out=[r['frame'] for r in W if r['arcane']=='Secondary Outburst']
bad_anim=[r['frame'] for r in W if r['arcane']=='Melee Animosity' and r['template'] not in ('HEAVY_ATTACK',)]
chk('Outburst on combo builds / Animosity without heavy build', f'{len(bad_out)} / {len(bad_anim)}', not bad_out and not bad_anim)
cw={k:X.validate_comp_weapon(k) for k in X.COMP_WEAPON_BUILD}
chk('Companion weapon builds', f'{sum(1 for v in cw.values() if not v[0])}/{len(cw)} valid', all(not v[0] for v in cw.values()), '; '.join(f'{k}: {"VALID" if not v[0] else v[0]}' for k,v in cw.items()))
_dk=next(k for k in cw if k.startswith('Deconstructor'))
_users=sorted(f for f,b in B.items() if b['comp']=='Helios Prime')
chk('Deconstructor Prime config', 'VALID' if not cw[_dk][0] else 'INVALID', not cw[_dk][0] and len(_users)==7, f'{" | ".join(X.COMP_WEAPON_BUILD[_dk][0])}; {" + ".join(cw[_dk][1])}; {cw[_dk][2]["Deconstructor Prime"][0]} Forma {cw[_dk][2]["Deconstructor Prime"][1]}/60; serves {len(_users)}: {", ".join(_users)}')
import capcheck as _C
ps=[r for r in W if 'Primed Shred' in r['mods']]
psok=[r for r in ps if r['capacity'] and r['capacity'][1]<=r['capacity'][2] and _C.drain('Primed Shred')==16]
chk('Primed Shred weapon capacity checks', f'{len(psok)}/{len(ps)} PASS', len(ps)==5 and len(psok)==5, '; '.join(f"{r['weapon']}: {r['forma']}" for r in ps)+' (Primed Shred max-rank drain 16)')
capbad=[r['weapon'] for r in W if not r['capacity'] or r['capacity'][1]>r['capacity'][2]]
chk('Weapon capacity / Forma (all configs)', f'{len(W)-len(capbad)}/{len(W)} fit', not capbad, 'exact max-rank drain with computed Forma; melee excludes stance capacity (upper bound)')
live=[(f,l) for f,b in B.items() for l in (b.get('live') or [])]
chk('LIVE TEST REQUIRED', len(live), True, '; '.join(f'{f}: {l}' for f,l in live))
json.dump(dict(ok=ok, rows=R), open('xcheck.json','w'), indent=1)
for r in R: print(f'{r[2]:4s} | {r[0]}: {r[1]} {("- "+r[3]) if r[3] else ""}'[:400])
print('ALL PASS' if ok else 'FAILURES PRESENT')
