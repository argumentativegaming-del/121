"""Companion configs, Exalted builds, weapon configurations, shard policy for v4.2 FINAL."""
import json, re
import engine, builds_data as BD
W = json.load(open('weapons_all.json'))
EVO = json.load(open('evolutions.json'))

# ---------------- Companion configurations (one config per companion; shared by every frame that uses it)
COMP = {
 'Adarza Kavat': dict(weapon='Adarza Claws', role='Crit support: Cat\'s Eye crit buff; Tenacious Bond final crit multiplier', mods=["Cat's Eye",'Reflect','Primed Animal Instinct','Primed Pack Leader','Link Fiber','Link Vitality','Tenacious Bond','Vicious Bond','Hastened Deflection','Enhanced Vitality']),
 'Panzer Vulpaphyla': dict(weapon='Panzer Claws', role='Viral priming (Viral Quills), Martyr Symbiosis revive, status spread', mods=['Viral Quills','Panzer Devolution','Martyr Symbiosis','Primed Pack Leader','Primed Animal Instinct','Link Fiber','Link Vitality','Contagious Bond','Vicious Bond','Hastened Deflection']),
 'Smeeta Kavat': dict(weapon='Smeeta Claws', role='Loot/energy economy: Charm buffs; Duplex Bond clones on energy spent', mods=['Charm','Mischief','Primed Animal Instinct','Primed Pack Leader','Link Fiber','Link Vitality','Enhanced Vitality','Duplex Bond','Tenacious Bond','Loyal Retriever']),
 'Huras Kubrow': dict(weapon='Huras Claws', role='Stealth: Stalk shares invisibility; Covert Bond', mods=['Stalk','Hunt','Primed Animal Instinct','Primed Pack Leader','Link Fiber','Link Vitality','Covert Bond','Tenacious Bond','Hastened Deflection','Enhanced Vitality']),
 'Dethcube Prime': dict(weapon='Deth Machine Rifle Prime', role='Energy economy: Energy Generator; Mystic Bond free casts', mods=['Energy Generator','Vaporize','Swift Deth','Primed Regen','Guardian','Vacuum','Link Fiber','Link Redirection','Mystic Bond','Manifold Bond']),
 'Helios Prime': dict(weapon='Deconstructor Prime', role='Scanning (codex/Investigator), Detect Vulnerability weak points', mods=['Investigator','Detect Vulnerability','Targeting Receptor','Primed Regen','Guardian','Vacuum','Link Fiber','Link Redirection','Mystic Bond','Manifold Bond']),
 'Wyrm Prime': dict(weapon='Prime Laser Rifle', role='Defensive: Negate status cleanse, Crowd Dispersion; Reinforced Bond', mods=['Negate','Crowd Dispersion','Primed Regen','Guardian','Vacuum','Link Fiber','Link Redirection','Metal Fiber','Reinforced Bond','Manifold Bond']),
 'Diriga': dict(weapon='Vulklok', role='Electric priming (Arc Coil / Electro Pulse) for electricity casters', mods=['Arc Coil','Electro Pulse','Calculated Shot','Primed Regen','Guardian','Vacuum','Link Fiber','Link Redirection','Mystic Bond','Manifold Bond']),
}
COMP_TYPES = {'Adarza Kavat':{'Adarza Kavat','Kavat'},'Panzer Vulpaphyla':{'Panzer Vulpaphyla','Vulpaphyla'},'Smeeta Kavat':{'Smeeta Kavat','Kavat'},'Huras Kubrow':{'Huras Kubrow','Kubrow'},
              'Dethcube Prime':{'Dethcube','Sentinel','Robotic'},'Helios Prime':{'Helios','Sentinel','Robotic'},'Wyrm Prime':{'Wyrm','Sentinel','Robotic'},'Diriga':{'Diriga','Sentinel','Robotic'}}
BEAST = {'Adarza Kavat','Panzer Vulpaphyla','Smeeta Kavat','Huras Kubrow'}
def validate_comp(c):
    errs=[]; cfg=COMP[c]
    for m in cfg['mods']:
        v=engine.mod(m)
        if not v: errs.append('unknown '+m); continue
        t=v.get('Type'); ok=COMP_TYPES[c]|{'Companion'}|({'Beast'} if c in BEAST else {'Robotic','Sentinel'})
        if t not in ok: errs.append(f'{m} type {t} not usable on {c}')
    if len(set(cfg['mods']))!=len(cfg['mods']): errs.append('dup')
    return errs
# Companion weapon builds
COMP_WEAPON_BUILD = {
 'Beast claws (Adarza/Panzer/Smeeta/Huras)': (['Bite','Maul','Bell Ringer','Hunter Synergy','Sepsis Claws','Shocking Claws','Venom Teeth','Precision Conditioning'], {'Claws'}),
 'Sentinel rifles (Deth Machine Rifle Prime, Deconstructor Prime*, Prime Laser Rifle, Vulklok)': (['Serration','Split Chamber','Point Strike','Vital Sense','Hellfire','Malignant Force','High Voltage','Galvanized Aptitude'], {'Rifle','Primary'}),
}

# ---------------- Exalted / separately moddable builds
# v4.3: element mods ordered so combinations are correct (Cold before Toxin = Viral; unpaired Electricity after a completed pair)
MELEE_CRIT = ['Primed Pressure Point','Blood Rush','Weeping Wounds','Organ Shatter','Berserker Fury','Condition Overload','North Wind','Virulent Scourge']
MELEE_INFLUENCE = ['Primed Pressure Point','Blood Rush','Weeping Wounds','Organ Shatter','Condition Overload','North Wind','Virulent Scourge','Voltaic Strike']
# v4.3: pseudo-Exalted melee (Landslide/Shattered Lash/Whipclaw) do not benefit from Attack Speed -> Berserker Fury replaced by Gladiator Might
PSEUDO_MELEE = ['Primed Pressure Point','Blood Rush','Weeping Wounds','Organ Shatter','Gladiator Might','Condition Overload','North Wind','Virulent Scourge']
# Shadow Clones (Blade Storm): 5% base crit / 1.2x / 5% status -> relative crit/status mods are near-useless; finisher-damage stack instead
SHADOW_CLONES = ['Covert Lethality','Finishing Touch','Primed Pressure Point','Organ Shatter','Gladiator Might','Condition Overload','North Wind','Virulent Scourge']
RIFLE_CRIT = ['Serration','Galvanized Chamber','Point Strike','Vital Sense','Hammer Shot','Galvanized Aptitude','Primed Cryo Rounds','Malignant Force']
PISTOL_CRIT = ['Hornet Strike','Galvanized Diffusion','Primed Pistol Gambit','Primed Target Cracker','Galvanized Crosshairs','Galvanized Shot','Deep Freeze','Pathogen Rounds']
SHOTGUN = ['Primed Point Blank','Galvanized Hell','Primed Ravage','Critical Deceleration','Galvanized Savvy','Chilling Grasp','Toxic Barrage','Primed Charged Shell']
NEUTRALIZER = ['Primary Acuity','Serration','Galvanized Scope','Bladed Rounds','Vital Sense','Hammer Shot','Primed Cryo Rounds','Malignant Force']
TEMPLATE_ELEMENT = {'RIFLE_CRIT':'Viral (Primed Cryo Rounds -> Malignant Force)','PISTOL_CRIT':'Viral (Deep Freeze -> Pathogen Rounds)','SHOTGUN':'Viral + Electricity (Chilling Grasp -> Toxic Barrage, then Primed Charged Shell unpaired)',
                    'MELEE_CRIT':'Viral (North Wind -> Virulent Scourge)','MELEE_INFLUENCE':'Viral + Electricity (North Wind -> Virulent Scourge, Voltaic Strike unpaired: required to trigger Melee Influence)','PSEUDO_MELEE':'Viral','SHADOW_CLONES':'Viral'}
# v4.3 Batch 3: status templates (weapons with base crit < 15% and status-led stats get no crit mods)
RIFLE_STATUS = ['Serration','Galvanized Chamber','Vigilante Armaments','Galvanized Aptitude','Primed Shred','Rime Rounds','Malignant Force','High Voltage']
PISTOL_STATUS = ['Hornet Strike','Augur Pact','Galvanized Diffusion','Lethal Torrent','Galvanized Shot','Frostbite','Pistol Pestilence','Jolt']
SHOTGUN_STATUS = ['Primed Point Blank','Vicious Spread','Galvanized Hell','Galvanized Savvy','Shotgun Barrage','Frigid Blast','Toxic Barrage','Primed Charged Shell']
# ---------------- Element-order engine (v4.3 Batch 3 automated check)
# Mod elements combine in slot order; an innate element merges into the same element already added by a mod,
# otherwise it is appended after all mod elements. Elements then pair sequentially.
_ELTAG = {'DT_FREEZE':'Cold','DT_POISON':'Toxin','DT_FIRE':'Heat','DT_ELECTRICITY':'Electricity'}
_COMBO = {frozenset(('Cold','Toxin')):'Viral',frozenset(('Electricity','Toxin')):'Corrosive',frozenset(('Heat','Toxin')):'Gas',
          frozenset(('Cold','Electricity')):'Magnetic',frozenset(('Heat','Electricity')):'Radiation',frozenset(('Cold','Heat')):'Blast'}
_COMBINED = set(_COMBO.values())
def mod_element(m):
    d=(engine.mod(m) or {}).get('Description') or ''
    import re as _re
    for t in _re.findall(r'<(DT_[A-Z]+)_COLOR>', d):
        if t in _ELTAG and _re.search(r'\+\d+%\s*<'+t, d): return _ELTAG[t]
    return None
def innate_elements(w):
    v=W.get(w) or W.get(w+' (Primary)') or {}
    dmg=((v.get('Attacks') or [{}])[0].get('Damage') or {})
    els=[k for k in dmg if k in ('Cold','Toxin','Heat','Electricity') or k in _COMBINED]
    import meta as _meta
    pe=_meta.ELEMENT.get(w)
    if pe: els.append(pe.capitalize())
    return els
def combine(mods, innate=()):
    seq=[]
    for m in mods:
        e=mod_element(m)
        if e and e not in seq: seq.append(e)
    fixed=[e for e in innate if e in _COMBINED]
    for e in innate:
        if e not in _COMBINED and e not in seq: seq.append(e)
    out=[]; i=0
    while i < len(seq):
        if i+1 < len(seq): out.append(_COMBO[frozenset((seq[i],seq[i+1]))]); i+=2
        else: out.append(seq[i]); i+=1
    for e in fixed:
        if e not in out: out.append(e)
    return out
ARC_ELEM = {'Melee Influence':'Electricity','Primary Frostbite':'Cold','Primary Blight':'Toxin','Melee Vortex':'Magnetic','Primary Obstruct':'Magnetic','Secondary Irradiate':'Radiation'}
def element_check(mods, innate, arcane=None, target=None):
    res=combine(mods, innate); errs=[]
    if arcane in ARC_ELEM and ARC_ELEM[arcane] not in res: errs.append(f'{arcane} needs a {ARC_ELEM[arcane]} element (got {" + ".join(res)})')
    for t in (target or []):
        if t not in res: errs.append(f'target element {t} not produced')
    return res, errs
EXALTED = {
 'Neutralizer':('Cyte-09','Primary',NEUTRALIZER,'Primary Deadhead','Viral','Weak-point sniper: Primary Acuity (+350% weak point dmg/crit; ricochets trigger on weak point hits), Galvanized Scope/Bladed Rounds (enabled on Exalteds in U38.5). Exilus: Hush. Primary Deadhead on weak point kills'),
 'Artemis Bow Prime':('Ivara Prime','Primary',RIFLE_CRIT,'Primary Deadhead','Viral+Heat','Charged multi-arrow; bow uses rifle mods'),
 'Lizzie':('Temple','Primary',RIFLE_CRIT,'Primary Merciless','Viral+Heat','Exalted guitar (Primary replacement)'),
 'Balefire Charger Prime':('Hildryn Prime','Secondary',PISTOL_CRIT,'Secondary Merciless','Viral+Heat','Shield-fed exalted'),
 'Regulators Prime':('Mesa Prime','Secondary',PISTOL_CRIT,'Secondary Deadhead','Viral+Heat','Peacemaker exalted (project Melee credit)'),
 'Dex Pixia Prime':('Titania Prime','Secondary',PISTOL_CRIT,'Secondary Merciless','Viral+Heat','Razorwing pistols'),
 'Glory':('Jade','Secondary',PISTOL_CRIT,'Secondary Merciless','Viral+Heat','Additional Exalted'),
 'Noctua':('Dante','Secondary',PISTOL_CRIT,'Secondary Encumber','Viral','Subsumed over by Roar; build persists because Wordwarden inherits Noctua mods and can trigger Secondary Encumber (wiki). Galvanized Shot scales incorrectly on Wordwarden (bug noted on wiki).'),
 'Desert Wind Prime':('Baruuk Prime','Melee',MELEE_CRIT,None,'Viral+Heat (Reactive Storm overrides)','Exalted fists'),
 'Exalted Umbra Blade':('Excalibur Umbra','Melee',MELEE_INFLUENCE,None,'Chromatic Blade Electricity (emissive) + Viral','Exalted Blade; Slash Dash inherits these mods and the Arcane'),
 'Garuda Prime Talons':('Garuda Prime','Melee',PSEUDO_MELEE,None,'Viral+Heat','Normal-ish weapon, no heavy attacks/Exilus'),
 'Shadow Claws Prime':('Sevagoth Prime','Melee',MELEE_CRIT,None,'Viral+Heat','Exalted Shadow claws'),
 'Valkyr Prime Talons':('Valkyr Prime','Melee',MELEE_CRIT,None,'Viral+Heat','Hysteria talons'),
 'Iron Staff Prime':('Wukong Prime','Melee',MELEE_CRIT,None,'Viral+Heat','Primal Fury staff'),
 'Diwata Prime':('Titania Prime','Melee',MELEE_CRIT,None,'Viral+Heat','Razorwing sword'),
 'Shadow Clones Prime':('Ash Prime','Melee',SHADOW_CLONES,'Melee Crescendo','Viral+Heat','Blade Storm finishers; flat crit from Smoke Shadow/Crepuscular; Crescendo on finisher kills'),
 'Landslide Fists Prime':('Atlas Prime','Melee',PSEUDO_MELEE,None,'Viral+Heat','U38.5 Exalted (Ability Combo)'),
 'Shattered Lash Prime':('Gara Prime','Melee',PSEUDO_MELEE,None,'Viral+Heat','U38.5 Exalted (Ability Combo)'),
 'Whipclaw Prime':('Khora Prime','Melee',PSEUDO_MELEE,None,'Viral+Heat','U38.5 Exalted (Ability Combo)'),
}
EXALTED_ARCANE = {'Desert Wind Prime': 'Melee Duplicate', 'Exalted Umbra Blade': 'Melee Duplicate', 'Garuda Prime Talons': 'Melee Duplicate', 'Shadow Claws Prime': 'Melee Duplicate', 'Valkyr Prime Talons': 'Melee Duplicate', 'Iron Staff Prime': 'Melee Duplicate', 'Diwata Prime': 'Melee Duplicate', 'Landslide Fists Prime': 'Melee Duplicate', 'Shattered Lash Prime': 'Melee Duplicate', 'Whipclaw Prime': 'Melee Duplicate', 'Regulators Prime': 'Secondary Merciless', 'Balefire Charger Prime': 'Secondary Merciless', 'Dex Pixia Prime': 'Secondary Merciless', 'Glory': 'Secondary Merciless', 'Noctua': 'Secondary Merciless'}
BATCH1_EXALTED = {'Shadow Clones Prime','Landslide Fists Prime','Desert Wind Prime','Neutralizer','Noctua','Exalted Umbra Blade','Shattered Lash Prime','Garuda Prime Talons'}
EXALTED_ARCANE['Exalted Umbra Blade']='Melee Influence'; EXALTED_ARCANE['Noctua']='Secondary Encumber'
for _w,_a in EXALTED_ARCANE.items():
    _f,_slot,_mods,_old,_el,_n=EXALTED[_w]
    EXALTED[_w]=(_f,_slot,_mods,_a,_el,_n+('' if _w in BATCH1_EXALTED else ' [Arcane provisional - re-review in frame batch]'))
# ---------------- v4.3 Batch 3 Exalted audit (U38.5: Arcane on all Exalteds; Exilus on Primary/Secondary Exalteds)
_B3_EXALTED = {
 'Artemis Bow Prime': (['Serration','Galvanized Chamber','Point Strike','Vital Sense','Galvanized Scope','Hammer Shot','Primed Cryo Rounds','Malignant Force'],'Primary Deadhead','Terminal Velocity',
     'Concentrated Arrow: single arrow +25% base crit, +50% crit and 7m explosion on weak points; Galvanized Scope (aimed weak-point crit) replaces Galvanized Aptitude; Prowl headshot bonus + Crepuscular x3 final crit'),
 'Balefire Charger Prime': (['Hornet Strike','Augur Pact','Galvanized Diffusion','Lethal Torrent','Galvanized Shot','Deep Freeze','Pathogen Rounds','Primed Convulsion'],'Secondary Merciless','Lethal Momentum',
     '5% crit / 1.5x / 10% status: crit template was dead weight -> flat damage + multishot; base 1500 (charged) scales with Str; Viral + innate Electricity; Blazing Pillage Heat procs feed Galvanized Shot'),
 'Regulators Prime': (['Hornet Strike','Galvanized Diffusion','Primed Pistol Gambit','Primed Target Cracker','Lethal Torrent','Galvanized Shot','Deep Freeze','Pathogen Rounds'],'Secondary Merciless','Suppress',
     'Peacemaker auto-targets (no aiming) -> Galvanized Crosshairs dead, Lethal Torrent instead; Galvanized buffs persist across recasts (wiki); Suppress is the only Exilus with effect (wiki); Crimson Tau Secondary Crit shard applies'),
 'Glory': (['Hornet Strike','Galvanized Diffusion','Primed Pistol Gambit','Primed Target Cracker','Lethal Torrent','Galvanized Shot','Deep Freeze','Pathogen Rounds'],'Secondary Merciless','Lethal Momentum',
     'Primary fire 10% Judgment chance per shot -> fire rate (Lethal Torrent) over aimed weak-point Crosshairs; Viral + innate Heat; alt-fire detonates Judgments'),
 'Whipclaw Prime': (['Primed Pressure Point','Blood Rush','Primed Reach','Organ Shatter','Gladiator Might','Condition Overload','North Wind','Virulent Scourge'],'Melee Duplicate',None,
     'Primed Reach extends the explosion radius past the 10m Range cap (wiki); no Attack Speed benefit (Gladiator Might); no Exilus slot; Ensnare subsumed -> Roar multiplies every Whipclaw'),
}
for _w,(_m,_a,_x,_n) in _B3_EXALTED.items():
    _f,_slot,_old,_oa,_el,_on=EXALTED[_w]
    EXALTED[_w]=(_f,_slot,_m,_a,_el,_n)
    EXALTED_ARCANE[_w]=_a
BATCH1_EXALTED |= set(_B3_EXALTED)
EXALTED_EXILUS = {'Neutralizer':'Hush', **{w:x for w,(m,a,x,n) in _B3_EXALTED.items() if x}}
VENARI_AUDITED = 'B3: Venari Prime config audited - Primed Pack Leader/Link mods for survival, Vicious/Contagious Bond for Viral spread; Venari Bodyguard not taken (Khora build slot goes to Accumulating Whipclaw)'
def exalted_element(w):
    f,slot,mods,a,e,n = EXALTED[w]
    res,errs = element_check(mods, innate_elements(w), a)
    return ' + '.join(res) + (' [ELEMENT ERROR: '+'; '.join(errs)+']' if errs else ''), errs
VENARI = ['Primed Pack Leader','Primed Animal Instinct','Link Fiber','Link Vitality','Enhanced Vitality','Vicious Bond','Contagious Bond','Hastened Deflection']
def validate_mods(mods, allowed):
    errs=[]
    for m in mods:
        v=engine.mod(m)
        if not v: errs.append('unknown '+m)
        elif v.get('Type') not in allowed: errs.append(f'{m} type {v.get("Type")}')
    if len(set(mods))!=len(mods): errs.append('dup')
    return errs
SLOT_TYPES = {'Primary':{'Rifle','Primary','Sniper','Bow','Assault Rifle'},'Secondary':{'Pistol','Secondary'},'Melee':{'Melee'},'Shotgun':{'Shotgun','Primary'}}

# ---------------- Weapon configurations
def wclass(w):
    v=W.get(w) or W.get(w+' (Primary)') or {}
    return v.get('Class') or '?', v
def norm_attack(v):
    a=(v.get('Attacks') or [{}])[0]
    return a.get('CritChance') or 0, a.get('StatusChance') or 0
def template(slot, cls, arcane=None, kind=None, cc=1.0, incarnon=False):
    if slot=='Melee' and arcane=='Melee Influence': return 'MELEE_INFLUENCE', MELEE_INFLUENCE
    if slot=='Melee': return 'MELEE_CRIT', MELEE_CRIT
    status = kind=='status' and cc < 0.15 and not incarnon   # v4.3 B3: crit mods are dead weight below 15% base crit (Incarnon forms excluded: form/evolutions change the crit profile)
    if slot=='Primary' and cls in ('Shotgun',): return ('SHOTGUN_STATUS', SHOTGUN_STATUS) if status else ('SHOTGUN', SHOTGUN)
    if slot=='Secondary': return ('PISTOL_STATUS', PISTOL_STATUS) if status else ('PISTOL_CRIT', PISTOL_CRIT)
    return ('RIFLE_STATUS', RIFLE_STATUS) if status else ('RIFLE_CRIT', RIFLE_CRIT)
ARC_RULE = {}
def weapon_arcane(slot, cls, w, frame, kind):
    if slot=='Primary':
        if cls in ('Sniper Rifle','Bow','Crossbow') : return 'Primary Deadhead'
        if cls=='Shotgun': return 'Shotgun Vendetta'
        if 'Kuva' in w or 'Tenet' in w: return 'Primary Merciless'
        return 'Primary Merciless'
    if slot=='Secondary':
        if frame in ('Ash Prime','Excalibur Umbra','Valkyr Prime','Wukong Prime','Garuda Prime','Kullervo','Baruuk Prime','Voruna Prime'): return 'Secondary Outburst'
        if kind=='status': return 'Secondary Encumber'
        return 'Secondary Merciless'
    if slot=='Melee':
        if frame=='Ash Prime': return 'Melee Crescendo'
        if kind=='status': return 'Melee Influence'
        if cls in ('Heavy Blade','Heavy Scythe','Hammer','Scythe') : return 'Melee Animosity'
        return 'Melee Duplicate'
def element(kind, w, frame):
    if w.startswith(('Kuva ','Tenet ')): return 'Adversary innate element (see Adversary sheet) + Viral'
    if kind=='status': return 'Corrosive + Viral (status priority, Condition Overload/Galvanized scaling)'
    return 'Viral + Heat (Steel Path generalist; swap Heat->Corrosive vs armored Grineer)'
def evo_family(w):
    base=w.replace(' Prime','').replace(' Vandal','').replace(' Wraith','').replace('Prisma ','')
    for k in EVO:
        if k==base: return k
    return None
def evo_pick(fam, kind):
    tiers=EVO[fam]['tiers']; picks=[]
    for t in sorted(tiers):
        opts=tiers[t]
        if t=='EVO1' or not opts: continue
        def score(o):
            e=(o['perk']+' '+o['effect']).lower(); s=0
            if kind=='crit': s+= 3*('critical' in e) + 2*('multishot' in e) + 1*('damage' in e) - 1*('status' in e and 'critical' not in e)
            else: s+= 3*('status' in e) + 2*('multishot' in e) + 1*('damage' in e)
            s+= 0.5*('incarnon form' in e and 'damage' in e)
            s-= 1*('reload' in e and t!='EVO3') ; s-= 1.5*('ammo' in e and 'damage' not in e)
            return s
        best=max(opts,key=score); picks.append(f"{t}: {best['perk']}")
    return picks
WEAPON_OVERRIDE = {
 ('Ash Prime','Secondary'): dict(arcane='Secondary Merciless', why='Outburst consumes Melee Combo, which Ash does not build on normal melee'),
 ('Ash Prime','Melee'): dict(arcane='Melee Crescendo', incarnon=['EVO2: Bladed Harmony','EVO3: Blade Twister','EVO4: Protracted Execution','EVO5: Stunning Brutality'], why='Teleport-finisher loop: finisher damage, combo on finisher, finisher stun'),
 ('Atlas Prime','Secondary'): dict(incarnon=['EVO2: Hoplite Virtue','EVO3: Moonrise Velocity','EVO4: Elemental Balance'], why='Paladin Virtue needs >700 max energy; Atlas reaches ~613'),
 ('Banshee Prime','Primary'): dict(kind='crit', arcane='Primary Deadhead', incarnon=['EVO2: Riddled Target','EVO3: Marksman\'s Hand','EVO4: Critical Parallel'], why='Sonar spots are weak points (Deadhead); Flensing Spikes redundant with Sonic Boom full strip'),
 ('Banshee Prime','Secondary'): dict(arcane='Secondary Deadhead', why='Sonar weak points'),
 ('Baruuk Prime','Primary'): dict(incarnon=['EVO2: Deadly Pace','EVO3: Swift Deliverance','EVO4: Vicious Promise'], why='Baruuk Prime sprint 1.2 activates Deadly Pace (+80% fire rate); bow projectile speed; first-shot crit'),
 ('Caliban Prime','Melee'): dict(arcane='Melee Duplicate', why='Venato signature boosts combo-count chance on normal attacks, not heavy attacks'),
 ('Chroma Prime','Secondary'): dict(incarnon=['EVO2: Reified Bane','EVO3: Exact Penance','EVO4: Survivor\'s Edge'], why='Haven Foray needs Overshields (Chroma has none); always-on perks'),
}
WEAPON_OVERRIDE.update({
 ('Cyte-09','Secondary'): dict(arcane='Secondary Deadhead', incarnon=['EVO2: Hoplite Virtue','EVO3: Lex Talionis','EVO4: Critical Parallel'], why='Weak-point frame; Trusty Sidearm needs a channeled ability (none)'),
 ('Dagath','Primary'): dict(kind='crit', why='Grave Spirit adds +50% x Str crit damage to all weapons'),
 ('Dagath','Secondary'): dict(incarnon=['EVO2: Mauler\'s Magazine','EVO3: Rapid Reinforcement','EVO4: Fatal Affliction'], why='Reload-from-empty crit damage (satisfiable); Doom Viral + weapon statuses feed Fatal Affliction'),
 ('Dante','Primary'): dict(kind='status', incarnon=['EVO2: Rapid Wrath','EVO3: Retribution\'s Vessel','EVO4: Elemental Excess','EVO5: Devouring Attrition'], why='Dante +50% status on scanned targets and Pageflight vulnerability favour status; Devouring Attrition rewards non-crit hits'),
 ('Dante','Secondary'): dict(incarnon=['EVO2: Rapid Wrath','EVO3: Rapid Reinforcement','EVO4: Lethal Lance','EVO5: Impaler\'s Ferocity'], why='Lethal Lance (punch through on kill) satisfies Impaler\'s Ferocity (punch-through hits +200%)'),
 ('Dante','Melee'): dict(incarnon=['EVO2: Lethal Impetus','EVO3: Adept Reflexes','EVO4: Swift Transmute','EVO5: Vulnerability Serum'], why='Status-oriented Dante; impaled +35% flat status'),
 ('Ember Prime','Secondary'): dict(kind='crit', arcane='Secondary Merciless', why='7% crit x5 multiplier + flat crit from Arcane Hot Shot and Topaz heat-kill shards; Heat element target'),
 ('Equinox Prime','Primary'): dict(incarnon=['EVO2: Forceful Finality','EVO3: Extended Volley','EVO4: Fatal Affliction'], why='Fortress Salvo needs >450 armor (not reached); Maim slash procs + weapon statuses'),
 ('Equinox Prime','Secondary'): dict(incarnon=['EVO2: Carnage Reign','EVO3: Evolved Autoloader','EVO4: Neurotoxin'], why='Ready Retaliation documented as not working; Commodore +20% on 5% base is weak'),
 ('Excalibur Umbra','Primary'): dict(incarnon=['EVO2: Munitions Grit','EVO3: Void\'s Guidance','EVO4: Critical Parallel'], why='Daring Reverie needs a channeled ability'),
 ('Excalibur Umbra','Secondary'): dict(incarnon=['EVO2: Deathtrap Trigger','EVO3: Awakened Readiness','EVO4: Commodore\'s Fortune'], why='Lone Gun needs no Primary equipped (Umbra carries Braton Prime)'),
 ('Follie','Primary'): dict(why='Signature: alt-fire applies Inkblot; siphons ammo from ability Inkblot - keep Enkaus alt-fire in the loop'),
 ('Frost Prime','Primary'): dict(arcane='Primary Frostbite', why='Cold beam on a Cold-stacking frame: crit damage/multishot per Cold status'),
 ('Frost Prime','Secondary'): dict(arcane='Secondary Shiver', why='Frost stacks Cold statuses (Ice Wave/Globe/Avalanche); +45% damage per Cold status'),
 ('Frost Prime','Melee'): dict(arcane='Melee Animosity', incarnon=['EVO2: Master\'s Shatter','EVO3: Kinetic Harmony','EVO4: Mounting Avalanche'], why='Cold-target combo perks satisfied by Frost; heavy-attack hammer'),
 ('Gara Prime','Melee'): dict(arcane='Melee Animosity', why='Volnus Prime signature +100% radial slam -> heavy slam build'),
 ('Garuda Prime','Secondary'): dict(incarnon=['EVO2: Fatal Affliction','EVO3: Rapid Reinforcement','EVO4: Critical Parallel'], why='Stalker\'s Vendetta needs Dread and Hate equipped'),
 ('Gauss Prime','Secondary'): dict(arcane='Secondary Merciless', why='Explosive kill-chaining under Redline'),
 ('Gauss Prime','Melee'): dict(incarnon=['EVO2: Whirling Flurry','EVO3: Adept Reflexes','EVO4: Swift Transmute','EVO5: Kinetic Harmony'], why='Attack speed + heavy wind-up'),
})
# ---------------- v4.3 Batch 3 (Gyre -> Mesa) weapon audit
HEAVY_ATTACK = ['Primed Pressure Point','Killing Blow','Blood Rush','Organ Shatter','Galvanized Reflex','Condition Overload','North Wind','Virulent Scourge']
HEAVY_KULLERVO = ['Primed Pressure Point','Killing Blow','Blood Rush','Organ Shatter','Primed Reach','Condition Overload','North Wind','Virulent Scourge']
WEAPON_OVERRIDE.update({
 ('Frost Prime','Primary'): dict(arcane='Primary Frostbite', tname='RIFLE_COLD', target=['Cold'],
     mods=['Serration','Galvanized Chamber','Vigilante Armaments','Galvanized Aptitude','Primed Shred','Primed Cryo Rounds','Rime Rounds','Hammer Shot'],
     why='SYSTEMIC FIX (B3 element validator): Primary Frostbite triggers on Cold status, but the Viral template consumed Glaxion Vandal\'s Cold; pure Cold kept. Batch 2 decision unchanged'),
 ('Gyre Prime','Primary'): dict(kind='crit', why='Cathode Grace adds +50% x Str weapon crit chance (additive with Point Strike); innate Electricity left unpaired after Viral feeds the passive (+10% ability crit per Electricity stack)'),
 ('Gyre Prime','Secondary'): dict(kind='crit', arcane='Secondary Merciless', incarnon=['EVO2: Paladin Virtue','EVO3: Swift Deliverance','EVO4: Critical Parallel'],
     why='Haven Foray needs Overshields (Gyre has no source); Paladin Virtue +75 base unconditional and its >700 energy crit bonus is met (285 x 2.85 Primed Flow = 812); Cathode Grace makes crit the scaling axis'),
 ('Gyre Prime','Melee'): dict(why='Melee Influence spreads Electricity (Voltaic Strike unpaired) -> Gyre passive ability-crit stacks'),
 ('Harrow Prime','Primary'): dict(arcane='Primary Deadhead', tname='RIFLE_COVENANT',
     mods=['Serration','Galvanized Chamber','Vital Sense','Hammer Shot','Galvanized Aptitude','Rime Rounds','Malignant Force','High Voltage'],
     why='Covenant adds up to +200% FLAT crit on weak points (Condemn exposes heads): crit-damage mods pay off on a 10% base; Deadhead on weak-point kills'),
 ('Harrow Prime','Secondary'): dict(arcane='Secondary Deadhead', why='Knell signature (+1 magazine), headshot weapon; Covenant weak-point crit'),
 ('Hildryn Prime','Primary'): dict(incarnon=["EVO2: Hunter's Mantra",'EVO3: Resonant Restore',"EVO4: Survivor's Edge"],
     why="EVO2 taken for base damage only: Hunter's Mantra conditional needs an ENERGY-draining channel (Haven drains shields - inactive); Hoplite Virtue needs personal shield break (rare on ~4000 shields)"),
 ('Inaros Prime','Melee'): dict(arcane='Melee Crescendo', why='Desiccation blind + Sandstorm knockdown -> finisher loop (passive heals 20% per finisher kill); Crescendo stacks combo on finisher kills'),
 ('Ivara Prime','Secondary'): dict(kind='crit', arcane='Secondary Deadhead', why='Prowl +40% x Str headshot damage and Crepuscular x3 final crit: weak-point crit sidearm'),
 ('Jade','Secondary'): dict(kind='crit', arcane='Secondary Merciless', why='Cantare 18% crit: crit template; Judgments +50% vulnerability'),
 ('Khora Prime','Secondary'): dict(arcane='Secondary Deadhead', why='Hystrix Prime signature: 8% instant reload on headshot -> headshot/weak-point play'),
 ('Khora Prime','Melee'): dict(arcane='Melee Animosity', tname='HEAVY_ATTACK', mods=HEAVY_ATTACK,
     why='Dual Keres Prime signature: +20% Heavy Attack Efficiency -> heavy-attack build (Galvanized Reflex); Whipclaw remains the primary damage'),
 ('Koumei','Secondary'): dict(kind='crit', incarnon=['EVO2: Swift Conclusion','EVO3: Swift Deliverance',"EVO4: Survivor's Edge"],
     why="Sage's Resolve needs a channeled ability (Koumei has none); Deathtrap Trigger only lasts 4s after swapping from Primary (bugged as permanent in Arsenal)"),
 ('Kullervo','Primary'): dict(arcane='Primary Dexterity', why='Melee-centric frame: melee kills fuel +60% primary damage stacks and +7.5s combo (Rauta signature +7s combo duration)'),
 ('Kullervo','Secondary'): dict(arcane='Secondary Dexterity', why='Secondary Outburst would consume the combo Kullervo banks for Wrathful Advance heavy attacks'),
 ('Kullervo','Melee'): dict(tname='HEAVY_KULLERVO', mods=HEAVY_KULLERVO,
     why='Wrathful Advance = heavy attack with +200% x Str flat final crit; passive +75% heavy efficiency/+100% wind-up -> Berserker Fury/Weeping Wounds dead; Collective Curse spreads the hit'),
 ('Mesa Prime','Secondary'): dict(kind='status', arcane='Secondary Encumber', tname='PISTOL_STATUS', mods=PISTOL_STATUS,
     why='Akjagara Prime 32% status, Slash-weighted burst; Mesa passive +15% fire rate dual-wield. Regulators carry the crit role'),
})
# ---------------- v4.3 Batch 4 (Mirage -> Rhino) weapon audit + explicit threshold reviews for earlier audited frames
MIRAGE_BOW = ['Serration','Split Chamber','Vigilante Armaments','Point Strike','Vital Sense','Hammer Shot','Primed Cryo Rounds','Malignant Force']
MIRAGE_PISTOL = ['Hornet Strike','Barrel Diffusion','Lethal Torrent','Primed Pistol Gambit','Primed Target Cracker','Augur Pact','Deep Freeze','Pathogen Rounds']
NARIN_BOW = ['Serration','Galvanized Chamber','Point Strike','Vital Sense','Galvanized Aptitude','Hammer Shot','Primed Cryo Rounds','Rime Rounds']
NARIN_PISTOL = ['Hornet Strike','Galvanized Diffusion','Primed Pistol Gambit','Primed Target Cracker','Galvanized Shot','Lethal Torrent','Deep Freeze','Frostbite']
WEAPON_OVERRIDE.update({
 # --- threshold reviews (documentation; builds unchanged)
 ('Citrine Prime','Secondary'): dict(why='THRESHOLD REVIEW: Catabolyst 11% crit; Prismatic Gem adds +100% x Str status chance -> status build confirmed'),
 ('Follie','Secondary'): dict(why='THRESHOLD REVIEW: Staticor 14% crit, AoE charged orbs; no flat-crit source on Follie -> status build confirmed'),
 ('Hydroid Prime','Secondary'): dict(why='THRESHOLD REVIEW: Pox 1% crit, Toxin AoE -> status build confirmed'),
 ('Inaros Prime','Secondary'): dict(why='THRESHOLD REVIEW: Zymos 5% crit; no flat-crit source on Inaros -> status build confirmed'),
 ('Lavos Prime','Secondary'): dict(why='THRESHOLD REVIEW: Cyanex 8% crit; Valence Formation adds a guaranteed-status element -> status build confirmed'),
 ('Mag Prime','Secondary'): dict(why='THRESHOLD REVIEW: Mara Detron 8% crit / 1.5x -> status build confirmed'),
 ('Equinox Prime','Secondary'): dict(incarnon=['EVO2: Carnage Reign','EVO3: Evolved Autoloader','EVO4: Neurotoxin'],
     why='THRESHOLD REVIEW (B4): Incarnon Form 11% crit / 43% status -> status template now matches the Batch 2 status perks (Neurotoxin)'),
 ('Dante','Secondary'): dict(kind='crit', incarnon=['EVO2: Rapid Wrath','EVO3: Rapid Reinforcement','EVO4: Lethal Lance',"EVO5: Impaler's Ferocity"],
     why="THRESHOLD REVIEW (B4): Incarnon Form 14% crit / 18% status - neither axis strong; locked Batch 2 crit build kept (Primed Pistol Gambit -> ~40%); damage comes from the punch-through perks (Lethal Lance -> Impaler's Ferocity)"),
 # --- Batch 4
 ('Mirage Prime','Primary'): dict(tname='MIRAGE_CLONE_SAFE', mods=MIRAGE_BOW, why='Hall of Mirrors clones copy modded stats but NOT Galvanized mods or Arcanes (wiki) -> static Split Chamber/Vigilante instead of Galvanized; Kuva Bramma Heat progenitor'),
 ('Mirage Prime','Secondary'): dict(tname='MIRAGE_CLONE_SAFE', mods=MIRAGE_PISTOL, why='Clone-safe: Barrel Diffusion/Lethal Torrent/Augur Pact instead of Galvanized Diffusion/Crosshairs/Shot (not inherited by clones)'),
 ('Narin','Primary'): dict(arcane='Primary Frostbite', tname='COLD_PURE', mods=NARIN_BOW, target=['Cold'],
     why='Nunchasa innate Cold kept pure: weapon Cold procs feed Naraemagi absorption, Sangodae drops (1%/Cold stack) and freeze for Nurinarim explosions; Primary Frostbite on Cold'),
 ('Narin','Secondary'): dict(arcane='Secondary Shiver', tname='COLD_PURE', mods=NARIN_PISTOL, target=['Cold'], why='Aksondol innate Cold kept pure (same loop); Secondary Shiver +45% per Cold status'),
 ('Narin','Melee'): dict(incarnon=['EVO2: Wartime Nerve','EVO3: Orokin Reach',"EVO4: Survivor's Edge"], why="Guardian's Promise needs Overshields - Narin generates Overguard, not Overshields -> Wartime Nerve"),
 ('Nekros Prime','Primary'): dict(why='THRESHOLD REVIEW: Tigris Prime 10% crit, Slash-weighted double barrel -> status/Slash build confirmed. Announced Tigris Incarnon is NOT live (Upcoming ledger) - no evolutions assigned'),
 ('Nezha Prime','Primary'): dict(tname='TOXIN_DR', mods=['Serration','Galvanized Chamber','Vigilante Armaments','Galvanized Aptitude','Primed Shred','Malignant Force','Infected Clip','Hammer Shot'], target=['Toxin'],
     why='Divine Retribution: speared explosions scale x1.5 per remaining Slash/Toxin/Heat status -> raw Toxin (not Viral); Chakram/Fire Walker supply Heat'),
 ('Nezha Prime','Secondary'): dict(tname='TOXIN_DR', mods=['Hornet Strike','Augur Pact','Galvanized Diffusion','Lethal Torrent','Galvanized Shot','Pistol Pestilence','Pathogen Rounds','Stunning Speed'], target=['Toxin'],
     why='Zakti Prime 42% status AoE -> raw Toxin for Divine Retribution'),
 ('Nokko','Primary'): dict(why='THRESHOLD REVIEW: Sporothrix 1% crit / 53% status -> status build confirmed'),
 ('Nokko','Secondary'): dict(kind='crit', arcane='Secondary Merciless', why='Ocucor 16% crit beam with innate Radiation: crit template + Merciless (status Arcane on crit mods was a mismatch)'),
 ('Nova Prime','Primary'): dict(incarnon=['EVO2: Fortifying Bloodshed','EVO3: Kinetic Battle','EVO4: Zeroed In'], why='Fortress Salvo needs >450 armor (Nova 135) -> Fortifying Bloodshed (+100 overshield on Slash kill)'),
 ('Nyx Prime','Secondary'): dict(why='THRESHOLD REVIEW: Hikou Prime 6% crit; Nyx passive (+40% crit per confused enemy) is additive to the crit MULTIPLIER, so 6% base stays low -> status confirmed'),
 ('Oberon Prime','Secondary'): dict(incarnon=['EVO2: Feigned Retreat',"EVO3: Void's Guidance","EVO4: Commodore's Fortune"], why="King's Gambit sets body-shot crit to x0 - Oberon is not a weak-point frame -> Feigned Retreat"),
 ('Protea Prime','Secondary'): dict(why='THRESHOLD REVIEW: Velox Prime 14% crit, 32% status (signature +40% ammo efficiency) -> status confirmed'),
 ('Qorvex','Primary'): dict(kind='status', tname='SHOTGUN_STATUS', mods=SHOTGUN_STATUS, incarnon=['EVO2: Attuned Accuracy','EVO3: Dual-Mode','EVO4: Racking Wrath','EVO5: Devastating Attrition'],
     why='INCARNON OVERRIDE: Devastating Attrition = 50% chance of +2000% on NON-critical hits -> crit mods lower damage; Racking Wrath (-10% crit, +20% status); Incarnon Form innate Radiation feeds the Crucible/Pillar chain'),
 ('Qorvex','Secondary'): dict(incarnon=['EVO2: Infused Shots','EVO3: Extended Volley','EVO4: Rain of Lead'], why='Speeding Bullet needs sprint speed >=1.2 (not met) -> Infused Shots (per 50 energy spent); Incarnon Form 24% / 3.2x crit'),
 ('Revenant Prime','Primary'): dict(why='Signature Phantasma Prime has INNATE Radiation, which turns thralls back to enemies (wiki) - documented conflict; avoid sweeping thralls with the beam'),
 ('Revenant Prime','Secondary'): dict(kind='status', tname='PISTOL_STATUS_NO_ELEC', mods=['Hornet Strike','Augur Pact','Galvanized Diffusion','Lethal Torrent','Galvanized Shot','Frostbite','Pistol Pestilence','Stunning Speed'],
     why='Tenet Cycron 40% status beam; Jolt removed because Electricity + innate Heat = Radiation (un-thralls Enthrall targets) -> Viral + Heat'),
 ('Revenant Prime','Melee'): dict(why='Signature Tatsu Prime has INNATE Radiation (+4 Soul Swarm charges) - documented thrall conflict'),
 ('Rhino Prime','Primary'): dict(incarnon=['EVO2: Crimson Overture','EVO3: Rapid Reinforcement',"EVO4: Survivor's Edge"], why="Hunter's Mantra needs a channeled ability (Rhino has none) -> Crimson Overture; Incarnon Form 24% / 3x crit -> crit"),
})
AUDITED_FRAMES = {'Ash Prime','Atlas Prime','Banshee Prime','Baruuk Prime','Caliban Prime','Chroma Prime','Citrine Prime',
                  'Cyte-09','Dagath','Dante','Ember Prime','Equinox Prime','Excalibur Umbra','Follie','Frost Prime','Gara Prime','Garuda Prime','Gauss Prime','Grendel Prime',
                  'Mirage Prime','Narin','Nekros Prime','Nezha Prime','Nidus Prime','Nokko','Nova Prime','Nyx Prime','Oberon Prime','Octavia Prime','Oraxia','Protea Prime','Qorvex','Revenant Prime','Rhino Prime',
                  'Gyre Prime','Harrow Prime','Hildryn Prime','Hydroid Prime','Inaros Prime','Ivara Prime','Jade','Khora Prime','Koumei','Kullervo','Lavos Prime','Limbo Prime','Loki Prime','Mag Prime','Mesa Prime'}
def weapon_configs():
    rows=[]
    for r in engine.ROWS:
        f=r[0]
        for slot,w in zip(['Primary','Secondary','Melee'],r[1:]):
            cls,v=wclass(w)
            if cls=='Exalted Weapon' or w in ('Razorflies','Garuda Prime Talons'): continue
            if w=='Vinquibus (Melee)': cls='Bayonet'
            cc,sc=norm_attack(v) if v else (0,0)
            # v4.3 B4: Incarnon weapons are classified on their Incarnon Form (the Steel Path mode), base stats kept for display
            form=[a for a in (v.get('Attacks') or []) if a.get('AttackName','').startswith('Incarnon Form')] if v else []
            ccx,scx=(form[0].get('CritChance') or 0, form[0].get('StatusChance') or 0) if form else (cc,sc)
            kind='crit' if ccx>=0.24 else ('status' if scx>=0.28 else ('crit' if ccx>=scx else 'status'))
            ov=WEAPON_OVERRIDE.get((f,slot),{})
            if ov.get('kind'): kind=ov['kind']
            arc0=ov.get('arcane') or weapon_arcane(slot,cls,w,f,kind)
            fam=evo_family(w.replace(' (Primary)','').replace(' (Melee)',''))
            tname,tmods=template(slot,cls,arc0,kind,ccx,False)
            flag=[]
            if form: flag.append(f'Incarnon Form {ccx:.0%} crit / {scx:.0%} status (base {cc:.0%}/{sc:.0%})')
            if slot!='Melee' and kind=='status' and ccx<0.15: flag.append('THRESHOLD FLAG: <15% crit -> status template proposed; needs weapon-specific review')
            review=('AUDITED: '+ov['why']) if (ov.get('why') and f in AUDITED_FRAMES) else ('AUDITED: no weapon/frame mechanic overrides the default' if f in AUDITED_FRAMES else ('REVIEW PENDING' if flag else 'PENDING'))
            if ov.get('mods'): tname,tmods=ov.get('tname','CUSTOM'),ov['mods']
            inc=[]
            if fam: inc=evo_pick(fam,kind)
            if ov.get('incarnon'): inc=ov['incarnon']
            res,eerr=element_check(tmods, innate_elements(w.replace(' (Primary)','').replace(' (Melee)','')), arc0, ov.get('target'))
            rows.append(dict(audited=f in AUDITED_FRAMES, why=ov.get('why',''), flag='; '.join(flag), review=review, frame=f,slot=slot,weapon=w,cls=cls,cc=cc,sc=sc,ccx=ccx,kind=kind,template=tname,mods=tmods,
                             arcane=arc0,element=' + '.join(res) + (' [ELEMENT ERROR: '+'; '.join(eerr)+']' if eerr else ''),elem_errs=eerr,exilus=ov.get('exilus'),incarnon=inc,evo_family=fam,
                             forma='5 Forma to Rank 40 + ~3 polarization' if w.startswith(('Kuva ','Tenet ')) else ('~4 (Incarnon)' if fam else '~3')))
    return rows

# ---------------- Shard policy (deliberate Tauforged allocation)
# Tau Crimson Strength kept only where Strength is the build's primary scaling stat without a met cap.
NORMAL_STR = {'Nyx Prime':'Psychic Bolts cap 125% met without Tau','Oberon Prime':'200% Renewal cap met without Tau','Limbo Prime':'Range/Duration build',
              'Loki Prime':'Range/Duration build','Octavia Prime':'Duration-driven','Titania Prime':'Razorwing duration/efficiency build','Zephyr Prime':'Turbulence duration build',
              'Vauban Prime':'CC build','Harrow Prime':'support','Trinity Prime':'support','Wisp Prime':'support','Nekros Prime':'loot/support','Citrine Prime':'support',
              'Hildryn Prime':'shield-scaling via Expertise uses Str but shields from Azure','Lavos Prime':'cooldown build','Koumei':'luck caster'}
def apply_shard_policy():
    changed={}
    for f,b in BD.B.items():
        sh=list(b['shards'])
        if f in NORMAL_STR and 'T:CS' in sh:
            sh[sh.index('T:CS')]='CS'; changed[f]=NORMAL_STR[f]
        b['shards']=sh
    return changed
TAU_ASSUMPTION = ('Tauforged shards are FINITE. They are allocated deliberately: Tau Crimson Strength only on frames whose primary scaling stat is uncapped Strength; '
                  'Tau Melee Crit Damage on melee-centric frames; Tau Primary Status / Secondary Crit on weapon-reliant frames. All other positions use normal shards. '
                  'Ascent Fusion (3 normal -> 1 Tauforged) is the planned conversion route; acquisition is account-bound (Archon Hunts / Netracells / Archimedea).')
