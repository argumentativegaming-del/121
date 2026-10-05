# Phase 3 v4.2 FINAL frame builds.
# Shard codes (live Archon Shard options, wiki 2026-10-05). Prefix "T:" = Tauforged (x1.5).
#   Crimson: CS Strength(+10%) CD Duration(+10%) CM Melee Crit Dmg(+25%) CP Primary Status(+25%) CC2 Secondary Crit Chance(+25%)
#   Amber:   AC Casting Speed(+25%) AE Energy orb eff(+50%) AH Health orb eff(+100%) ASP Energy on spawn(+30%) AP Parkour(+15%)
#   Azure:   ZH Health(+150) ZS Shield(+150) ZE Energy max(+50) ZA Armor(+150) ZR Health regen(+5/s)
#   Emerald: ETOX Toxin status dmg(+30%) ETH Toxin heal ECO Corrosion ability dmg(+10%) ECS Corrosion max stacks(+2)
#   Topaz:   TBH Blast-kill health TBS Blast-kill shields THC Secondary CC on Heat kill TRA Radiation ability dmg(+10%)
#   Violet:  VEA Electricity ability dmg(+10%) VPE Primary Electricity dmg VMC Melee crit dmg (x2 above 500 energy) VEQ Equilibrium
# Each build: role, helm=(ability, replaced) or ('NO HELMINTH', reason), aura, exilus, mods (8), arcanes (2), shards (5),
# focus, comp, cond (conditional stat sources), surv (survivability architecture), bp (breakpoints/targets), live (LIVE TEST items), notes
B = {}
def b(frame, **k): B[frame] = k

b('Ash Prime', role='Blade Storm finisher assassin; Shadow Clones crit melee scaling via Ability Combo; Melee Crescendo via finishers',
  helm=('Roar', 'Shuriken'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Rolling Guard','Rising Storm'],
  arcanes=['Molt Augmented','Arcane Avenger'], shards=['T:CS','CS','T:CM','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Growing Power +25% Str on weapon status','Molt Augmented up to +60% Str','Roar (subsumed) +30% x Str damage'],
  surv='Umbral health+armor set, Rolling Guard status cleanse/i-frames, Smoke Screen invisibility, Teleport repositioning',
  bp='No hard Str cap; Roar scales with Str. Duration only affects Smoke Screen/Roar uptime.',
  notes='Rising Storm: Blade Storm adds Melee Combo to sustain Shadow Clones scaling.')
b('Atlas Prime', role='Petrify/Rumblers tank and Landslide brawler (Ability Combo scaling)',
  helm=('Nourish', 'Tectonics'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Rubble Heap'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','ZA','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Nourish (subsumed) energy multiplier and Viral on weapons','Rubble Heap free Landslide above 1400 Rubble'],
  surv='Passive rubble armor overguard, Umbral health/armor, Petrify stone CC, Arcane Reaper armor/regen',
  bp='Rubble Heap threshold 1400 Rubble; Petrify/Rumblers scale on Str.')
b('Banshee Prime', role='U44 Banshee: Sonar weak-point damage multiplier support + Sonic Boom armor strip + Sound Quake blast nuke',
  helm=('Roar', 'Silence'), aura='Corrosive Projection', exilus='Power Drift',
  mods=['Umbral Intensify','Transient Fortitude','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Resonance'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','T:CS','CD','AC','ZH'], focus='Zenurik', comp='Helios Prime',
  cond=['Sonar weak points count for Acuity/Incarnon charging','Resonance chains Sonar on weak-spot kills'],
  surv='Low-armor caster: Sound Quake brief invulnerability, Silence replaced (stun aura loss accepted), reliance on Zenurik + Energize and team support',
  bp='Sonar multiplier 5x base at rank 3, scales with Str; Sonic Boom 70% armor reduction; prioritize Str > Range > Duration.',
  notes='Silence subsumed out because Roar stacks with Sonar; Savage Silence therefore unused (collection only).')
b('Baruuk Prime', role='Desert Wind exalted melee with Serene Storm restraint DR; Reactive Storm status',
  helm=('Roar', 'Elude'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Streamline','Rolling Guard','Reactive Storm'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','T:CM','ZA','ZH'], focus='Naramon', comp='Panzer Vulpaphyla',
  cond=['Restraint (passive) damage reduction up to 50%+','Reactive Storm converts Desert Wind to elemental by Desert Wind status'],
  surv='Restraint DR, Umbral set, Lull sleep CC, Rolling Guard', bp='Range affects Lull and Desert Wind waves; Str drives Desert Wind damage.')
b('Caliban Prime', role='Sentient Wrath armor-strip CC + Lethal Progeny summoner',
  helm=('Molt', 'Razor Gyre'), aura='Corrosive Projection', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Augur Reach','Streamline','Primed Flow'],
  arcanes=['Arcane Camisado','Molt Augmented'], shards=['T:CS','CS','ZA','ZH','AC'], focus='Unairu', comp='Panzer Vulpaphyla',
  cond=['Arcane Camisado: minion attacks up to +60% Str next cast','Sentient adaptation passive'],
  surv='Adaptive resistance passive + Adaptation-style Sentient passive, Umbral set, Molt (subsumed) decoy+speed',
  bp='Sentient Wrath armor strip scales with Str; Range for Wrath radius.', notes='Razor Mortar augment not used (Razor Gyre replaced).')
b('Chroma Prime', role='Vex Armor damage/armor self-buff weapon platform',
  helm=('Nourish', 'Spectral Scream'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Guardian Armor'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','T:CS','ZA','ZH','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Vex Armor Scorn/Fury stacks from damage taken/dealt','Elemental Ward element (Heat=health/armor? set by emissive)'],
  surv='Vex Armor armor multiplier, Elemental Ward (choose Heat/Cold), Umbral set',
  bp='Vex Armor Fury/Scorn cap scale with Str; Duration for uptime.')
b('Citrine Prime', role='Crystallize/Prismatic Gem support and Fractured Blast status farmer',
  helm=('NO HELMINTH', 'Kit complete; all four abilities used'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Prismatic Companion'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AH'], focus='Vazarin', comp='Panzer Vulpaphyla',
  cond=['Passive health regen grows with health orbs (Amber Health orb shard)'],
  surv='Passive regen, Preserving Shell, Umbral set', bp='Prismatic Gem damage/status scale with Str; Duration for gem uptime.')
b('Cyte-09', role='Neutralizer weak-point sniper; Resupply ammo/energy; Evade invisibility',
  helm=('Roar', 'Seek'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Rolling Guard'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','T:CP','ZA','AC'], focus='Madurai', comp='Helios Prime',
  cond=['Passive: weak point kills +1% weak point CC up to 300%','Roar (subsumed)'],
  surv='Evade invisibility, Umbral set, Rolling Guard', bp='Neutralizer damage is exalted; Str for Roar; no hard cap.',
  notes='No live augments for Cyte-09.')
b('Dagath', role='Wyrd Scythes/Doom slash-status reaper; Rakhali\'s Cavalry mount',
  helm=('Roar', "Rakhali's Cavalry"), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Spectral Spirit'],
  arcanes=['Molt Augmented','Arcane Energize'], shards=['T:CS','CS','CD','ZH','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Doom transfers damage', 'Wyrd Scythes slash procs'], surv='Passive revive, Umbral set', bp='Str for Doom/Scythes; Duration for Doom.',
  notes="Roar replaces Rakhali's Cavalry so Grave Spirit (Spectral Spirit augment) is retained.")
b('Dante', role='Dark/Light Verse tome caster: Tragedy armor strip + Final Verse nukes; Noctua exalted scanner',
  helm=('Nourish', 'Light Verse'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Noctua Swarm'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Helios Prime',
  cond=['Passive: +50% status chance on fully scanned targets'], surv='Overguard from Verses, Umbral set',
  bp='Tragedy armor strip and Final Verse scale with Str.',
  live=['Light Verse replaced by Nourish: confirm Verse combos still reach Tragedy/Wordwarden via Dark Verse + Final Verse -> LIVE TEST REQUIRED'],
  notes='Noctua kept as additional Exalted; no Secondary replacement (ruling unchanged).')
b('Ember Prime', role='Inferno/Fireball heat CC nuker with Immolation DR',
  helm=('Roar', 'Fire Blast'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Exothermic'],
  arcanes=['Arcane Hot Shot','Molt Augmented'], shards=['T:CS','THC','THC','ZA','AC'], focus='Madurai', comp='Dethcube Prime',
  cond=['Arcane Hot Shot: weapon CC from ability heat procs','Topaz Secondary CC on heat kill x2'], surv='Immolation DR, Umbral set',
  bp='Immolation DR scales with Str; Inferno range.')
b('Equinox Prime', role='Maim damage storage nuke / Pacify DR support',
  helm=('Roar', 'Rest & Rage'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Transient Fortitude','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Peaceful Provocation'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','T:CS','CS','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Roar (subsumed)'], surv='Pacify mode DR when needed; Umbral Vitality', bp='Maim stores damage; Str/Range priority.',
  notes='Roar replaces Rest & Rage (Pacify & Provoke covers DR); Metamorphosis retained for form swap.')
b('Excalibur Umbra', role='Exalted Umbra Blade waves/melee with Radial Howl CC',
  helm=('Roar', 'Radial Howl'), aura='Growing Power', exilus="Warrior's Rest",
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Chromatic Blade'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','T:CM','ZA','AC'], focus='Naramon', comp='Adarza Kavat',
  cond=['Passive: +10% damage & attack speed with swords','Chromatic Blade: emissive element on Exalted Blade'],
  surv='Umbral set (native Umbra polarities), Exalted Blade blocking', bp='Exalted Blade waves scale with Str/Range.',
  notes="Warrior's Rest is Umbra's Exilus augment (live).")
b('Follie', role='Shadowgraph/Plein Air ink caster; Enkaus alt-fire Inkblot synergy',
  helm=('Roar', 'Forced Perspective'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Augur Secrets'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Inkblot passive: 50% slow, 20% orb drop chance'], surv='Self Portrait DR (own, uncapped), Umbral set', bp='Str for ink damage; no augments exist.',
  notes='No live Follie augments.')
b('Frost Prime', role='Snow Globe defense anchor + Freeze/Ice Wave cold CC',
  helm=('Rebuild Shields', 'Freeze'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Icy Avalanche'],
  arcanes=['Arcane Ice Storm','Molt Augmented'], shards=['T:CS','CS','ZA','ZS','AC'], focus='Vazarin', comp='Wyrm Prime',
  cond=['Arcane Ice Storm: Str/Dur stacks on freeze'], surv='Snow Globe, Icy Avalanche overguard, Umbral set', bp='Globe health scales with Str.',
  notes='Freeze replaced; Freeze Force augment unused.')
b('Gara Prime', role='Splinter Storm DR + Mass Vitrify; Shattered Lash exalted (Ability Combo)',
  helm=('Roar', 'Spectrorage'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Mending Splinters'],
  arcanes=['Molt Augmented','Arcane Reaper'], shards=['T:CS','CS','ZA','ZH','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Splinter Storm DR up to 90%'], surv='Splinter Storm DR, Mending Splinters heal, Umbral set', bp='Splinter Storm DR caps at 90% via Str.')
b('Garuda Prime', role='Blood Altar/Bloodletting sustain with Garuda Talons melee',
  helm=('Roar', 'Dread Mirror'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Blood Forge'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','T:CM','ZH','AH'], focus='Naramon', comp='Panzer Vulpaphyla',
  cond=['Passive: up to +100% damage from kills'], surv='Blood Altar lifesteal, Bloodletting energy, Umbral set', bp='Str for Altar heal.',
  notes='Blood Forge augments Bloodletting (kept). Dread Mirror replaced; Dread Ward unused.')
b('Gauss Prime', role='Redline battery speed/fire-rate; Thermal Sunder cold/heat; Acceltra/Akarius sprint reload bonus',
  helm=('Roar', 'Kinetic Plating'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Thermal Transfer'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','ZA','ZS','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Battery level drives Redline and shield recharge'], surv='Shield recharge passive, Umbral set', bp='Str for Redline fire-rate; Kinetic Plating dropped.')
b('Grendel Prime', role='Feast/Nourish support; Pulverize ball DR; Regurgitate',
  helm=('Rebuild Shields', 'Regurgitate'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Hearty Nourishment'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','ZA','ZH','AC'], focus='Vazarin', comp='Panzer Vulpaphyla',
  cond=['Nourish energy multiplier (native, full strength)'], surv='Huge health pool, Hearty Nourishment overguard, Umbral set',
  bp='Nourish multiplier scales with Str.')
b('Gyre Prime', role='Rotorswell crit-boost electric caster; Cathode Grace',
  helm=('Roar', 'Arcsphere'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Coil Recharge'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','VEA','VEA','ZS','AC'], focus='Zenurik', comp='Diriga',
  cond=['Passive electric crit chance','Violet electricity ability dmg x2'], surv='Shield gating + Umbral set', bp='Str for Rotorswell crit.')
b('Harrow Prime', role='Thurible energy support + Covenant crit buff',
  helm=('NO HELMINTH', 'All four abilities core to support loop'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Warding Thurible'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Vazarin', comp='Helios Prime',
  cond=['Thurible headshot energy'], surv='Penance lifesteal, Covenant, Warding Thurible', bp='Covenant crit scales with Str.')
b('Hildryn Prime', role='Shield-tank: Haven/Pillage/Aegis Storm; Balefire Charger',
  helm=('Roar', 'Aegis Storm'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Redirection','Augur Accord','Primed Continuity','Stretch','Augur Reach','Umbral Vitality','Blazing Pillage'],
  arcanes=['Arcane Expertise','Molt Augmented'], shards=['T:CS','CS','ZS','ZS','ZS'], focus='Vazarin', comp='Wyrm Prime',
  cond=['Arcane Expertise: Str applies to max shields'], surv='Massive shields, Pillage shield restore, Haven', bp='Shields = energy; no Efficiency/Flow (no energy).')
b('Hydroid Prime', role='Tentacle Swarm CC + Plunder corrosive armor strip',
  helm=('Roar', 'Tidal Surge'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Pilfering Swarm'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','ECO','ZA','AC'], focus='Zenurik', comp='Smeeta Kavat',
  cond=['Plunder corrosive procs (Emerald corrosion ability dmg)'], surv='Umbral set, Plunder armor gain', bp='Str for Tentacle damage/Plunder.')
b('Inaros Prime', role='Scarab Shell/health tank; Desiccation lifesteal',
  helm=('Roar', 'Sandstorm'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Negation Armor'],
  arcanes=['Arcane Reaper','Arcane Bellicose'], shards=['T:CS','ZH','ZH','ZA','ZA'], focus='Vazarin', comp='Panzer Vulpaphyla',
  cond=['Arcane Bellicose: +6% Str per 250 max health (cap 72%)'], surv='No shields; huge health, Scarab Shell armor, Negation Armor', bp='Bellicose cap at 3000 max health.')
b('Ivara Prime', role='Prowl stealth / Artemis Bow exalted; Navigator',
  helm=('Roar', 'Navigator'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Infiltrate'],
  arcanes=['Arcane Crepuscular','Arcane Avenger'], shards=['T:CS','CS','CD','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Arcane Crepuscular +30% Str / x3 final CD while invisible'], surv='Prowl invisibility, Umbral set', bp='Str for Artemis Bow damage.')
b('Jade', role='Light\'s Judgment/Ophanim Eyes judgment debuff caster; Glory exalted; two Aura slots',
  helm=('Roar', 'Symphony of Mercy'), aura='Growing Power', aura2='Corrosive Projection', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline',"Jade's Judgment"],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Helios Prime',
  cond=['Judgments +50% enemy damage vulnerability'], surv='Umbral set, flight', bp='Str for judgment/Glory.')
b('Khora Prime', role='Strangledome CC + Whipclaw exalted (Ability Combo); Venari exalted companion',
  helm=('Roar', 'Ensnare'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Accumulating Whipclaw'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CM','ZA','AC'], focus='Madurai', comp='Smeeta Kavat',
  cond=['Accumulating Whipclaw stacking damage'], surv='Venari heal mode, Umbral set', bp='Str for Whipclaw.')
b('Koumei', role='Omikuji luck dice / Bunraku status caster',
  helm=('Roar', 'Kumihimo'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline',"Omikuji's Fortune"],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Smeeta Kavat',
  cond=['Passive weapon random status 60s cycle'], surv='Omamori charms, Umbral set', bp='Str for Bunraku.',
  notes='Kumihimo replaced; Kumihimo Loading unused.')
b('Kullervo', role='Wrathful Advance crit melee teleport; Storm of Ukko',
  helm=('Roar', 'Collective Curse'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Wrath of Ukko'],
  arcanes=['Arcane Reaper','Arcane Fury'], shards=['T:CS','T:CM','CM','ZH','ZA'], focus='Naramon', comp='Adarza Kavat',
  cond=['Passive heavy attack efficiency/wind-up'], surv='No shields; health/armor, Recompense heal', bp='Str for Wrathful Advance crit.')
b('Lavos Prime', role='Cooldown elemental alchemist; Catalyze/Vial Rush',
  helm=('Roar', 'Ophidian Bite'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Augur Reach','Transient Fortitude','Valence Formation'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','ZA','ZH','ZH'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['No energy: cooldown based; Efficiency irrelevant'], surv='Passive status immunity on cast, Umbral set', bp='Str for Catalyze/Vial; no Efficiency mods (no energy).')
b('Limbo Prime', role='Cataclysm/Stasis rift control',
  helm=('Roar', 'Banish'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Cataclysmic Continuum'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','CD','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Rift plane immunity'], surv='Rift plane invulnerability', bp='Cataclysm range/duration.')
b('Loki Prime', role='Invisibility/Radial Disarm stealth support',
  helm=('Roar', 'Switch Teleport'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Irradiating Disarm'],
  arcanes=['Arcane Crepuscular','Arcane Energize'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Huras Kubrow',
  cond=['Arcane Crepuscular while invisible'], surv='Invisibility, Disarm', bp='Range for Radial Disarm.')
b('Mag Prime', role='Magnetize/Polarize shield strip and Crush; Fracturing Crush armor strip',
  helm=('Roar', 'Pull'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Transient Fortitude','Primed Continuity','Stretch','Primed Flow','Streamline','Umbral Vitality','Fracturing Crush'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','T:CS','CS','ZS','AC'], focus='Zenurik', comp='Diriga',
  cond=['Polarize shields'], surv='Polarize overshield regen, shield gating', bp='Fracturing Crush armor strip scales with Str.')
b('Mesa Prime', role='Peacemaker (Regulators) exalted gunslinger; Shatter Shield DR',
  helm=('Roar', 'Ballistic Battery'), aura='Growing Power', exilus="Mesa's Waltz",
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Rolling Guard'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','T:CC2','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Shooting Gallery damage buff'], surv='Shatter Shield 95% ranged DR, Umbral set', bp='Shatter Shield DR cap; Str for Peacemaker.')
b('Mirage Prime', role='Eclipse damage + Hall of Mirrors clones',
  helm=('Nourish', 'Sleight of Hand'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Total Eclipse'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Eclipse light/dark mode','Nourish (subsumed) energy + Viral'], surv='Eclipse DR (dark), Umbral set', bp='Eclipse damage/DR scale with Str.',
  notes='Nourish chosen over Roar: subsumed damage buffs (Roar/Eclipse/Chyrinka Pillar) carry a 1-damage-buff-per-Warframe limit; Mirage already has native Eclipse.')
b('Narin', role='Ice-blade caster: Neote/Naraemagi Ice generation into Nurinarim sword dance',
  helm=('Roar', 'Hakchum'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Augur Secrets'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Passive: Sangodae cold pickups add Cold to primary/secondary'], surv='Umbral set, mobility during dance', bp='Nurinarim slash 20k at max Str scaling.',
  live=['Hakchum replaced: Hakchum is a listed Ice source but Nurinarim cannot gain Ice during the dance; confirm Neote+Naraemagi alone sustain Ice -> LIVE TEST REQUIRED'],
  notes='Nurinarim ruling: cast ability, no Melee replacement (Prisma Skana retained). No live Narin augments.')
b('Nekros Prime', role='Desecrate loot + Shadows of the Dead army',
  helm=('Roar', 'Soul Punch'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Shield of Shadows'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Vazarin', comp='Smeeta Kavat',
  cond=['Shield of Shadows DR per shadow'], surv='Shield of Shadows, Umbral set', bp='Shadows damage scales with Str.')
b('Nezha Prime', role='Warding Halo invulnerability + Divine Spears CC',
  helm=('Roar', 'Fire Walker'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Divine Retribution'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','ZA','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Warding Halo health scales with armor'], surv='Warding Halo, Umbral set', bp='Halo scales with armor+Str.')
b('Nidus Prime', role='Virulence/Larva mutation stack infested caster',
  helm=('Roar', 'Parasitic Link'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Larva Burst'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','ZH','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Mutation stacks'], surv='No shields; Undying passive, Ravenous', bp='Virulence/Larva Str/Range.')
b('Nokko', role='Mushroom caster: Stinkbrain/Brightbonnet pulses, Reroot',
  helm=('Roar', 'Sporespring'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Reroot Rampage'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Arbucep shots empower Stinkbrain/Brightbonnet'], surv='Sprodling revive passive, Umbral set', bp='Str for mushroom pulses.')
b('Nova Prime', role='Molecular Prime slow/speed + Antimatter Drop',
  helm=('Roar', 'Null Star'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Molecular Fission'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Molecular Prime damage doubling'], surv='Shield gating, Wormhole escape', bp='Str: slow (negative Str = speed); this build is slow/damage.')
b('Nyx Prime', role='Current Nyx: Psychic Bolts defense strip, Chaos radiation, Absorb weapon buff',
  helm=('Roar', 'Mind Control'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Pacifying Bolts'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','TRA','ZA','AC'], focus='Zenurik', comp='Helios Prime',
  cond=['Chaos applies 10 Radiation statuses (Topaz radiation ability dmg)'], surv='Absorb invulnerability, armor steal from Bolts, Umbral set',
  bp='Psychic Bolts 100% defense strip at 125% Str (met).')
b('Oberon Prime', role='Reworked Oberon: Smite/Reckoning armor strip, Renewal armor buff, Hallowed Ground',
  helm=('NO HELMINTH', 'All four reworked abilities synergize (Hallowed Ground radiation feeds Reckoning)'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Hallowed Reckoning'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','ZA','ZA','AC'], focus='Vazarin', comp='Panzer Vulpaphyla',
  cond=['Reckoning armor gain up to +1000','Righteous Negation charges from health orbs'], surv='Renewal armor (x2 to allies), Reckoning armor, Umbral set',
  bp='Reckoning removes enemy armor fully at 167% Str; Renewal armor buff caps at 200% Str.')
b('Octavia Prime', role='Mallet/Resonator damage + Metronome/Amp buffs; Helminth: Resonator is her donated ability (not Mallet)',
  helm=('NO HELMINTH', 'Kit loop requires all four'), aura='Growing Power', exilus='Conductor',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Partitioned Mallet'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Amp energy passive'], surv='Metronome invisibility/armor, Umbral Vitality', bp='Duration for Mallet/Resonator.')
b('Oraxia', role='Webbed Embrace / Widow\'s Brood spider caster; Silken Stride',
  helm=('Roar', "Mercy's Kiss"), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline',"Brood's Oversurge"],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Panzer Vulpaphyla',
  cond=["Predator's Lurk invisibility on wall latch"], surv='Invisibility passive, Umbral set', bp='Str for Brood.')
b('Protea Prime', role='Dispensary/Blaze Artillery support with Temporal Anchor rewind; RESOLVED: Roar replaces Grenade Fan',
  helm=('Roar', 'Grenade Fan'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Temporal Artillery'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Passive: every 4th cast +100% Str'], surv='Temporal Anchor rewind, Dispensary, Umbral set',
  bp='Temporal Artillery requires Temporal Anchor (kept) and Blaze Artillery (kept).',
  notes='v4 resolution: Roar moved from Temporal Anchor to Grenade Fan; Temporal Artillery now valid.')
b('Qorvex', role='Radiation pillar/wall tank: Chyrinka Pillar, Containment Wall, Crucible Blast',
  helm=('Roar', 'Disometric Guard'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Wrecking Wall'],
  arcanes=['Arcane Universal Fallout','Molt Augmented'], shards=['T:CS','TRA','TRA','ZA','AC'], focus='Vazarin', comp='Panzer Vulpaphyla',
  cond=['Passive +3 weapon Punch Through','Radiation ability damage (Topaz x2)'], surv='875 armor, Umbral Fiber, walls', bp='Str for Crucible/Pillar.')
b('Revenant Prime', role='Mesmer Skin invulnerability + Reave/Danse Macabre',
  helm=('Roar', 'Enthrall'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Mesmer Shield'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Mesmer Skin charges'], surv='Mesmer Skin charges, Reave shield gain', bp='Mesmer charges scale with Str.')
b('Rhino Prime', role='Iron Skin tank + native Roar damage buff',
  helm=('Nourish', 'Rhino Charge'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Reinforcing Stomp'],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','ZA','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Native Roar (full strength)','Nourish energy multiplier (subsumed)'], surv='Iron Skin scales with armor, Umbral set', bp='Iron Skin Str/armor.')
b('Saryn Prime', role='Spores/Miasma status nuker; Molt',
  helm=('Roar', 'Toxic Lash'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Venom Dose'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','ETOX','ECO','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Toxin/Corrosive procs (Emerald)'], surv='Molt decoy/speed, Umbral set', bp='Spores damage growth with Str.')
b('Sevagoth Prime', role='Reap/Sow death harvest; Gloom slow/lifesteal; Exalted Shadow form',
  helm=('Roar', 'Sow'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Shadow Haze'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Death Harvest gauge fills Exalted Shadow'], surv='Gloom lifesteal, shadow revive, Umbral set', bp='Gloom slow/lifesteal Str.')
b('Sirius & Orion', role='Twin constellation frames (one inventory item, two separately modded bodies); Sirius config here',
  helm=('Roar', 'Coronal Ejection'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Augur Secrets'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Zenurik', comp='Adarza Kavat',
  cond=['Swap grants +45% efficiency next 2 casts'], surv='Secondary Son invulnerable ally, Umbral set', bp='Str for Jade Stars/Astral Shell.',
  live=['Helminth: only Primary Son can receive the cyst; confirm Coronal Ejection replacement -> LIVE TEST REQUIRED','Reactor: Orion is an Exalted Warframe; one Reactor assumed -> LIVE TEST REQUIRED'],
  notes='No live S&O augments.')
b('Styanax Prime', role='Axios Javelin/Final Stand nuker; Tharros Strike shield/armor strip; Afentis Prime signature',
  helm=('Roar', 'Rally Point'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Tharros Lethality'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','ZS','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Passive crit chance from shields, doubled for spearguns'], surv='Large shields, Umbral set', bp='Str for Final Stand.')
b('Temple', role='Backbeat rhythm caster: Pyrotechnics/Overdrive/Ripper\'s Wail; Lizzie exalted guitar (Primary replacement)',
  helm=('NO HELMINTH', 'Backbeat synergy requires native kit'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Rhythm Guard'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Madurai', comp='Dethcube Prime',
  cond=['Backbeat +50% efficiency when on-beat'], surv='Rhythm Guard, Umbral set', bp='Str for Lizzie/Pyrotechnics.')
b('Titania Prime', role='Permanent Razorwing: Dex Pixia + Diwata exalted; Tribute buffs',
  helm=('Roar', 'Spellbind'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Razorwing Blitz'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','CD','ZA','ZA'], focus='Madurai', comp='Adarza Kavat',
  cond=['Tribute buffs','Razorflies'], surv='Small hitbox in Razorwing, Umbral set', bp='Duration/Efficiency for Razorwing drain; Str for Razorflies.')
b('Trinity Prime', role='Energy Vampire/Blessing support',
  helm=('Roar', 'Well of Life'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline',"Champion's Blessing"],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Vazarin', comp='Helios Prime',
  cond=['Blessing DR'], surv='Blessing DR, Link', bp='Blessing DR cap with Str.')
b('Uriel', role='Demon summoner: Infernalis/Remedium/Demonium, Brimstone',
  helm=('NO HELMINTH', 'Demon kit requires all abilities'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Infernum'],
  arcanes=['Arcane Camisado','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Madurai', comp='Panzer Vulpaphyla',
  cond=['Arcane Camisado minion Str stacks'], surv='Remedium heal, Umbral set', bp='Str for demons.')
b('Valkyr Prime', role='Hysteria invulnerable Talons melee; Warcry',
  helm=('Roar', 'Paralysis'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Eternal War'],
  arcanes=['Arcane Reaper','Arcane Fury'], shards=['T:CS','T:CM','CM','ZA','ZA'], focus='Naramon', comp='Adarza Kavat',
  cond=['Warcry attack speed + armor'], surv='Hysteria invulnerability, 1000 armor, Umbral set', bp='Hysteria drain: Efficiency/Duration.')
b('Vauban Prime', role='Bastille/Vortex CC + Photon Strike',
  helm=('Roar', 'Tesla Nervos'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Enduring Bastille'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Bastille armor strip'], surv='CC-based', bp='Bastille armor strip per second scales with Str.')
b('Volt Prime', role='Discharge/Electric Shield caster + Speed',
  helm=('Roar', 'Shock'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Primed Continuity','Stretch','Augur Reach','Primed Flow','Streamline','Umbral Vitality','Capacitance'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','VEA','VEA','ZS','AC'], focus='Zenurik', comp='Diriga',
  cond=['Static Discharge passive','Electricity ability dmg (Violet x2)'], surv='Capacitance shields, Electric Shield', bp='Str for Discharge.')
b('Voruna Prime', role='Lycath\'s Hunt/Fangs of Raksh hunter; Perigale/Sarofang signatures',
  helm=('Roar', 'Shroud of Dynar'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline',"Ulfrun's Endurance"],
  arcanes=['Arcane Reaper','Molt Augmented'], shards=['T:CS','CS','T:CM','ZA','AC'], focus='Naramon', comp='Adarza Kavat',
  cond=['Passive orb drops'], surv='Ulfrun health, Umbral set', bp='Str for Fangs.', notes='Prey of Dynar unused (Shroud replaced).')
b('Wisp Prime', role='Reservoir support + Breach Surge/Sol Gate',
  helm=('Roar', 'Wil-O-Wisp'), aura='Growing Power', exilus='Fused Reservoir',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Critical Surge'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Reservoir motes'], surv='Haste/vitality motes', bp='Breach Surge sparks scale with Str.')
b('Wukong Prime', role='Celestial Twin + Primal Fury Iron Staff exalted; Defy',
  helm=('Roar', 'Cloud Walker'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Primed Flow','Streamline','Stretch','Primal Rage'],
  arcanes=['Arcane Reaper','Arcane Fury'], shards=['T:CS','T:CM','CM','ZA','ZH'], focus='Naramon', comp='Adarza Kavat',
  cond=['Primal Rage crit on kill'], surv='Passive death avoidance, Defy, Umbral set', bp='Iron Staff crit via Primal Rage.')
b('Xaku Prime', role='The Vast Untime damage amp/CC; Grasp of Lohk (no replacement)',
  helm=('Roar', "Xata's Whisper"), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Untime Rift'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZH','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['25% evasion passive'], surv='Passive evasion, Umbral set', bp='Untime damage amp with Str.')
b('Yareli Prime', role='Merulina/Aquablades mobile caster; Kompressa Prime signature',
  helm=('Roar', 'Sea Snares'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Merulina Guardian'],
  arcanes=['Arcane Energize','Molt Augmented'], shards=['T:CS','CS','CD','ZS','AC'], focus='Zenurik', comp='Dethcube Prime',
  cond=['Merulina DR'], surv='Merulina DR, Umbral set', bp='Aquablades Str/Range.')
b('Zephyr Prime', role='Turbulence projectile deflection + Tornado; Jet Stream',
  helm=('Roar', 'Tail Wind'), aura='Growing Power', exilus='Power Drift',
  mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Jet Stream'],
  arcanes=['Arcane Avenger','Molt Augmented'], shards=['T:CS','CS','CD','ZA','AC'], focus='Madurai', comp='Adarza Kavat',
  cond=['Airborne bonuses'], surv='Turbulence ranged deflection, Umbral set', bp='Duration for Turbulence.')

# Separately moddable Exalted Warframe configs (count toward Exalted builds, NOT toward the 66 / 330)
EXALTED_FRAMES = {
 "Sevagoth Prime's Shadow": dict(aura='Steel Charge', exilus=None,
   mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Rolling Guard'],
   notes='Exalted Warframe (own mods/polarities); uses Shadow Claws Prime. No shards/arcanes slots.'),
 'Orion': dict(aura='Growing Power', exilus='Power Drift',
   mods=['Umbral Intensify','Umbral Vitality','Umbral Fiber','Primed Continuity','Stretch','Primed Flow','Streamline','Augur Secrets'],
   notes='Second body of Sirius & Orion; separately moddable per wiki. Arcane/shard sharing with Sirius: LIVE TEST REQUIRED.'),
}
