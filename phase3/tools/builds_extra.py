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
def template(slot, cls, arcane=None):
    if slot=='Melee' and arcane=='Melee Influence': return 'MELEE_INFLUENCE', MELEE_INFLUENCE
    if slot=='Melee': return 'MELEE_CRIT', MELEE_CRIT
    if slot=='Primary' and cls in ('Shotgun',): return 'SHOTGUN', SHOTGUN
    if slot=='Secondary': return 'PISTOL_CRIT', PISTOL_CRIT
    return 'RIFLE_CRIT', RIFLE_CRIT
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
AUDITED_FRAMES = {'Ash Prime','Atlas Prime','Banshee Prime','Baruuk Prime','Caliban Prime','Chroma Prime','Citrine Prime',
                  'Cyte-09','Dagath','Dante','Ember Prime','Equinox Prime','Excalibur Umbra','Follie','Frost Prime','Gara Prime','Garuda Prime','Gauss Prime','Grendel Prime'}
def weapon_configs():
    rows=[]
    for r in engine.ROWS:
        f=r[0]
        for slot,w in zip(['Primary','Secondary','Melee'],r[1:]):
            cls,v=wclass(w)
            if cls=='Exalted Weapon' or w in ('Razorflies','Garuda Prime Talons'): continue
            if w=='Vinquibus (Melee)': cls='Bayonet'
            cc,sc=norm_attack(v) if v else (0,0)
            kind='crit' if cc>=0.24 else ('status' if sc>=0.28 else ('crit' if cc>=sc else 'status'))
            ov0=WEAPON_OVERRIDE.get((f,slot),{})
            arc0=ov0.get('arcane') or weapon_arcane(slot,cls,w,f,ov0.get('kind') or kind)
            tname,tmods=template(slot,cls,arc0)
            fam=evo_family(w.replace(' (Primary)','').replace(' (Melee)',''))
            inc=[]
            if fam: inc=evo_pick(fam,kind)
            ov=WEAPON_OVERRIDE.get((f,slot),{})
            if ov.get('kind'): kind=ov['kind']
            if ov.get('incarnon'): inc=ov['incarnon']
            rows.append(dict(audited=f in AUDITED_FRAMES, why=ov.get('why',''), frame=f,slot=slot,weapon=w,cls=cls,cc=cc,sc=sc,kind=kind,template=tname,mods=tmods,
                             arcane=arc0,element=('Adversary innate element (see Adversary sheet) + ' if w.startswith(('Kuva ','Tenet ')) else '')+TEMPLATE_ELEMENT[tname],incarnon=inc,evo_family=fam,
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
