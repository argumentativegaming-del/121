"""Build validation + stat/capacity engine for Phase 3 v4.2 frame builds (live wiki data 2026-10-05)."""
import json, re, math, importlib
import builds_data as BD
MODS = {v['Name'].lower(): v for v in json.load(open('mods.json'))['Mods'].values() if not v.get('IsFlawed')}
ARC = {v['Name'].lower(): v for v in json.load(open('arcanes.json'))['Arcanes'].values()}
FR = json.load(open('warframes.json'))['Warframes']
ROWS = [l.strip().split('|') for l in open('alloc_new.txt') if l.strip()]
SUBS = {v.get('Subsumed') for v in FR.values() if v.get('Subsumed')}
NATIVE = {'Empower','Infested Mobility',"Master's Summons",'Rebuild Shields','Perspicacity','Energized Munitions','Marked For Death',
          'Expedite Suffering','Parasitic Armor','Hideous Resistance','Voracious Metastasis','Sickening Pulse','Golden Instinct'}
HELM_POOL = SUBS | NATIVE
FAMILIES = [{'Flow','Primed Flow','Archon Flow'},{'Continuity','Primed Continuity','Archon Continuity'},{'Intensify','Archon Intensify','Umbral Intensify'},
            {'Vitality','Archon Vitality','Umbral Vitality'},{'Stretch','Archon Stretch'},{'Redirection','Primed Redirection'},{'Steel Fiber','Umbral Fiber'},
            {'Vigor','Primed Vigor'},{'Sure Footed','Primed Sure Footed'}]
SHARD = {'CS':('Crimson','Ability Strength',10),'CD':('Crimson','Ability Duration',10),'CM':('Crimson','Melee Critical Damage',25),'CP':('Crimson','Primary Status Chance',25),
         'CC2':('Crimson','Secondary Critical Chance',25),'AC':('Amber','Casting Speed',25),'AE':('Amber','Energy Orb Effectiveness',50),'AH':('Amber','Health Orb Effectiveness',100),
         'ASP':('Amber','Energy on Spawn',30),'AP':('Amber','Parkour Velocity',15),'ZH':('Azure','Health',150),'ZS':('Azure','Shield Capacity',150),'ZE':('Azure','Energy Max',50),
         'ZA':('Azure','Armor',150),'ZR':('Azure','Health Regen/s',5),'ETOX':('Emerald','Toxin Status Damage',30),'ETH':('Emerald','Toxin Status Heal',2),
         'ECO':('Emerald','Ability Damage vs Corrosion',10),'ECS':('Emerald','Corrosion Max Stacks',2),'TBH':('Topaz','Blast-kill Max Health',1),'TBS':('Topaz','Blast-kill Shield Regen',5),
         'THC':('Topaz','Secondary Crit Chance on Heat kill',1),'TRA':('Topaz','Ability Damage vs Radiation',10),'VEA':('Violet','Ability Damage vs Electricity',10),
         'VPE':('Violet','Primary Electricity Damage',30),'VMC':('Violet','Melee Crit Damage (x2 >500 energy)',25),'VEQ':('Violet','Health/Energy orb conversion',20)}
NO_SHIELD = {'Inaros Prime','Kullervo','Nidus Prime'}; NO_ENERGY = {'Hildryn Prime','Lavos Prime'}
STATRE = re.compile(r'([+-]\d+(?:\.\d+)?)% Ability (Strength|Duration|Range|Efficiency)(?! for your)')
def mod(n): return MODS.get(n.lower())
def stats(mods, shards, frame):
    s = {'Strength':100.0,'Duration':100.0,'Range':100.0,'Efficiency':100.0}
    umb = sum(1 for m in mods if m.startswith('Umbral '))
    for m in mods:
        v = mod(m)
        if not v: continue
        for val, st in STATRE.findall(v.get('Description') or ''):
            val = float(val)
            if m == 'Umbral Intensify': val *= {1:1,2:1.25,3:1.75}[umb]
            s[st] += val
    for c in shards:
        tau = c.startswith('T:'); code = c[2:] if tau else c
        if code in ('CS','CD'): s['Strength' if code=='CS' else 'Duration'] += SHARD[code][2]*(1.5 if tau else 1)
    s['Efficiency'] = min(s['Efficiency'], 175.0)
    return {k: round(v,1) for k,v in s.items()}
def drain(v):
    return (v.get('BaseDrain') or 0) + (v.get('MaxRank') or 0)
POLMAP = {'Madurai':'Madurai','Vazarin':'Vazarin','Naramon':'Naramon','Zenurik':'Zenurik','Unairu':'Unairu','Penjaga':'Penjaga','Umbra':'Umbra'}
def capacity(frame, aura, exilus, mods):
    fd = FR.get(frame, {})
    pols = [p for p in (fd.get('Polarities') or []) if p != 'Aura']
    ap = fd.get('AuraPolarity'); ap = ap[0] if isinstance(ap, list) else ap
    av = mod(aura) if aura else None
    cap = 60
    if av:
        a = abs(av.get('BaseDrain') or 0) + (av.get('MaxRank') or 0)
        cap += a*2 if (ap in ('Aura', av.get('Polarity'))) else math.floor(a*0.75) if ap else a
    items = [(mod(m), m) for m in mods + ([exilus] if exilus else [])]
    items = [(v, m) for v, m in items if v]
    free = list(pols)
    cost = 0; unmatched = []
    for v, m in sorted(items, key=lambda x: -drain(x[0])):
        d = drain(v); p = v.get('Polarity')
        if p in free or (p != 'Umbra' and 'Umbra' in free and m.startswith('Umbral')):
            free.remove(p if p in free else 'Umbra'); cost += math.ceil(d/2)
        elif p == 'Umbra' and 'Umbra' in free:
            free.remove('Umbra'); cost += math.ceil(d/2)
        else:
            unmatched.append((d, m)); cost += d
    forma = 0
    for d, m in sorted(unmatched, reverse=True):
        if cost <= cap: break
        cost -= d - math.ceil(d/2); forma += 1
    return dict(capacity=cap, cost=cost, fits=cost <= cap, forma=forma, innate=pols)
def augment_target(v):
    m = re.match(r'\s*([^:]+?) Augment\s*:', v.get('Description') or '')
    return m.group(1).strip() if m else None
def validate(frame, bd):
    errs = []; warns = []
    fd = FR.get(frame, {}); abil = fd.get('Abilities') or []
    base = frame.replace(' Prime', '')
    mods = bd['mods']
    if len(mods) != 8: errs.append(f'{len(mods)} mods (need 8)')
    if len(set(mods)) != len(mods): errs.append('duplicate mod')
    for m in mods:
        v = mod(m)
        if not v: errs.append(f'unknown mod {m}'); continue
        t = v.get('Type')
        if t not in ('Warframe', base, frame, 'Excalibur Umbra', 'Excalibur') : errs.append(f'{m} type {t} not usable on {frame}')
        if t == 'Aura': errs.append(f'{m} is an Aura')
    allm = mods + [bd.get('exilus')] if bd.get('exilus') else list(mods)
    for fam in FAMILIES:
        hit = [m for m in allm if m in fam]
        if len(hit) > 1: errs.append(f'incompatible family {hit}')
    for m in allm:
        v = mod(m) or {}
        for inc in v.get('Incompatible') or []:
            if inc in allm: errs.append(f'{m} incompatible with {inc}')
    for key in ('aura','aura2'):
        a = bd.get(key)
        if a:
            v = mod(a)
            if not v or v.get('Type') != 'Aura': errs.append(f'{key} {a} not an Aura')
    if frame == 'Jade' and not bd.get('aura2'): errs.append('Jade has two Aura slots')
    ex = bd.get('exilus')
    if ex:
        v = mod(ex)
        if not v or not v.get('IsExilus'): errs.append(f'exilus {ex} not Exilus-eligible')
        elif v.get('Type') not in ('Warframe', base, frame, 'Excalibur Umbra'): errs.append(f'exilus {ex} wrong frame')
    h, rep = bd['helm']
    if h != 'NO HELMINTH':
        if h not in HELM_POOL: errs.append(f'Helminth {h} not in pool')
        if rep not in abil: errs.append(f'replaced {rep} not an ability of {frame}')
        if h in abil: errs.append(f'{h} is native to {frame}')
    augs = []
    for m in allm:
        v = mod(m) or {}
        if v.get('Type') in (base, frame, 'Excalibur Umbra'):
            tgt = augment_target(v); augs.append(m)
            if tgt and h != 'NO HELMINTH' and tgt == rep: errs.append(f'augment {m} targets replaced ability {rep}')
            if tgt and tgt not in abil and tgt != 'Passive': warns.append(f'augment {m} targets "{tgt}" not in live ability list')
            if m == 'Temporal Artillery' and ('Temporal Anchor' == rep or 'Blaze Artillery' == rep): errs.append('Temporal Artillery requires Temporal Anchor and Blaze Artillery')
    ar = bd['arcanes']
    if len(ar) != 2 or len(set(ar)) != 2: errs.append('need 2 distinct arcanes')
    for a in ar:
        v = ARC.get(a.lower())
        if not v or v.get('Type') != 'Warframe': errs.append(f'arcane {a} not a Warframe arcane')
    sh = bd['shards']
    if len(sh) != 5: errs.append(f'{len(sh)} shards')
    for c in sh:
        code = c[2:] if c.startswith('T:') else c
        if code not in SHARD: errs.append(f'bad shard {c}')
        if code == 'ZS' and frame in NO_SHIELD: errs.append('shield shard on shieldless frame')
        if code == 'ZE' and frame in NO_ENERGY: errs.append('energy shard on energyless frame')
    if bd['focus'] not in ('Madurai','Vazarin','Naramon','Unairu','Zenurik'): errs.append('bad focus')
    if frame in NO_ENERGY and any(m in ('Primed Flow','Flow','Streamline','Fleeting Expertise','Archon Flow') for m in allm): errs.append('energy mod on energyless frame')
    return errs, warns, augs
def run():
    importlib.reload(BD)
    out = {}
    for r in ROWS:
        f = r[0]; bd = BD.B.get(f)
        if not bd: out[f] = {'errs':['NO BUILD']}; continue
        e, w, augs = validate(f, bd)
        out[f] = dict(errs=e, warns=w, augs=augs, stats=stats(bd['mods']+([bd['exilus']] if bd.get('exilus') else []), bd['shards'], f),
                      cap=capacity(f, bd.get('aura'), bd.get('exilus'), bd['mods']))
    return out
if __name__ == '__main__':
    o = run(); n = 0
    for f, r in o.items():
        if r['errs'] or r.get('warns') or not r.get('cap',{}).get('fits',True):
            n += 1; print(f, '| ERR', r['errs'], '| WARN', r.get('warns'), '| cap', r.get('cap'))
    print('frames with issues:', n, '/', len(o))
