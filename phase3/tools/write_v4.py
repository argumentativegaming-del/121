import json, math, collections, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.workbook.properties import CalcProperties
import meta
from build import COLS, rows, old, W, FR, INC, TS, PLAT_USD, REQ_ARC_V3, REQ_ARC_V4
proc=json.load(open('proc.json'))
wb=openpyxl.load_workbook('v3.xlsx')
H=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F3A5F'); B=Font(bold=True)
CH=PatternFill('solid',fgColor='FFF2CC')
def hdr(ws,r=1):
    for c in ws[r]: c.font=H; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
def newsheet(name,header,data,widths=None,idx=None):
    if name in wb.sheetnames: del wb[name]
    ws=wb.create_sheet(name,idx); ws.append(header); hdr(ws)
    for d in data: ws.append(list(d))
    ws.freeze_panes='B2'; ws.auto_filter.ref=ws.dimensions
    for i,h in enumerate(header,1): ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(h,min(40,max(10,len(str(h))+2)))
    return ws
# ---- Procurement Master
pm=newsheet('Procurement Master',COLS,[[r[c] for c in COLS] for r in proc],{'Item':30,'Assigned Frame(s)':18,'Notes':50,'Source/Reasoning':60,'Status':30,'Acquisition Method':30})
N=len(proc)+1; L={c:get_column_letter(i+1) for i,c in enumerate(COLS)}
def rng(c): return f"'Procurement Master'!${L[c]}$2:${L[c]}${N}"
# ---- static computations (snapshot)
def S(cat,flag,col): return sum((r[col] or 0) for r in proc if r['Category']==cat and r['Counted in Player-Trade Total?']==flag)
ws_count=sum(1 for r in proc if r['Category'] in ('Weapon','Adversary Weapon') and r['Quantity']==1)
cat_count=sum(1 for r in proc if r['Category']=='Weapon' and r['Quantity']==1 and not str(r.get('Catalyst?')).startswith('Pre-installed'))
quest_slot=sum(1 for r in proc if r['Category']=='Weapon' and r['Quantity']==1 and str(r.get('Catalyst?')).startswith('Pre-installed (quest'))
import build as _b
COMP_SLOTS=len(_b.USED_COMP)+sum(1 for c in _b.USED_COMP if c in ('Dethcube Prime','Helios Prime','Wyrm Prime','Diriga','Nautilus Prime','Shade Prime','Taxon'))
# ---- Economic Model (replace)
idx=wb.sheetnames.index('Economic Model'); del wb['Economic Model']
ms=wb.create_sheet('Economic Model',idx)
for c,wd in zip('ABCDEFGH',[60,16,16,16,16,16,16,60]): ms.column_dimensions[c].width=wd
def add(vals,bold=False):
    ms.append(vals)
    if bold:
        for c in ms[ms.max_row]: c.font=B
    return ms.max_row
add(['PHASE 3 ECONOMIC MODEL v4 - NORMALIZED ROSTER, LIVE WARFRAME.MARKET PRICING'],True); ms['A1'].font=Font(bold=True,size=14)
add([f'Market: Warframe.Market PC, {TS}. Floor = cheapest credible (online, else seen <=3d) sell order at the required rank; Realistic = median of cheapest 3-5 credible, bounded by max(Floor, 1.5x traded median) when trade history exists; Conservative = max(Realistic, 5th seller, 30d traded median; capped 2x Realistic) x1.10. Adversary: direct-buyout auctions, owner seen <=7d.'])
add([f'Benchmark: 23,000p = $1,000 (5 x 4,600p @ $199.99). 1p = ${PLAT_USD:.5f}. Cells are live formulas over Procurement Master.'])
add([])
add(['1. PLAYER-TRADE ACQUISITION','Floor','Realistic','Conservative','Rows counted','Rows w/o sell orders','Rows no data','Scope'],True)
cats=[('Prime frame acquisition','Warframe','51 Prime sets; 15 base/quest frames are account-bound (0p)'),
      ('Weapon acquisition (ordinary, tradeable)','Weapon','Prime sets, Vandal/Wraith/Prisma, Zariman/Entrati blueprints'),
      ('Adversary acquisition (Kuva/Tenet)','Adversary Weapon','12 weapons, target element, >=58% valence'),
      ('Max-rank mod acquisition (PvE, every tradeable mod)','Mod','All WFM mods ex Rivens/Flawed/locators; Conclave reported separately'),
      ('Max-rank Arcane acquisition (required)','Arcane','v3 14 required + v4 11 weapon-arcane baseline'),
      ('Companions (Prime sentinel sets)','Companion','v3 companion list; beasts/base sentinels farmed')]
r0=ms.max_row+1
for lab,cat,scope in cats:
    f=lambda col: f'=SUMIFS({rng(col)},{rng("Category")},"{cat}",{rng("Counted in Player-Trade Total?")},"Yes")'
    add([lab,f('Floor Platinum'),f('Realistic Platinum'),f('Conservative Platinum'),
         f'=COUNTIFS({rng("Category")},"{cat}",{rng("Counted in Player-Trade Total?")},"Yes")',
         f'=COUNTIFS({rng("Category")},"{cat}",{rng("Counted in Player-Trade Total?")},"Yes",{rng("Floor Platinum")},"")',
         f'=COUNTIFS({rng("Category")},"{cat}",{rng("Status")},"*UNAVAILABLE*")',scope])
PT=add(['PLAYER-TRADE TOTAL',f'=SUM(B{r0}:B{ms.max_row})',f'=SUM(C{r0}:C{ms.max_row})',f'=SUM(D{r0}:D{ms.max_row})'],True)
add(['   Rows without credible sell orders contribute Realistic/Conservative from the traded median when one exists (Floor blank); otherwise 0 and marked MARKET DATA UNAVAILABLE.'])
add([])
add(['SEPARATE / OPTIONAL TRADE LINES (not in totals)','Floor','Realistic','Conservative'],True)
def f2(cat,flag,col): return f'=SUMIFS({rng(col)},{rng("Category")},"{cat}",{rng("Counted in Player-Trade Total?")},"{flag}")'
add(['Conclave/PvP-only mods (max rank)']+[f2('Mod','PvP subtotal',c) for c in ('Floor Platinum','Realistic Platinum','Conservative Platinum')])
add(['Remaining Arcane collection (all other tradeable Arcanes, max rank)']+[f2('Arcane','Collection (optional)',c) for c in ('Floor Platinum','Realistic Platinum','Conservative Platinum')])
add(['Signature archguns (Larkspur Prime; Mandonel/Arbucep farmed)']+[f2('Archgun','Optional',c) for c in ('Floor Platinum','Realistic Platinum','Conservative Platinum')])
add(['Signature extras for Exalted-replaced/shared slots (Reconifex, Cobra & Crane Prime; Skiajati/Wrath farmed)']+[f2('Signature Extra','Optional',c) for c in ('Floor Platinum','Realistic Platinum','Conservative Platinum')])
add(['Upcoming / not live (Brysko, Corecracker, Rain & Shine, Hound, Sentient shotgun, Tigris Incarnon)','EXCLUDED','EXCLUDED','EXCLUDED'])
add([])
add(['2. FIXED / DIRECT INFRASTRUCTURE','Count','Unit Pt','Gross Pt','Free slots','Net Pt','','Basis'],True)
ia=ms.max_row+1
add(['Warframe slots',66,20,'=B{0}*C{0}'.format(ia),5,'=(B{0}-E{0})*C{0}'.format(ia),'','Free: 3 starter, Excalibur Umbra (Sacrifice), Nora\'s Mix'])
add(['Weapon slots (2 per 12p)',ws_count,6,'=CEILING(B{0}/2,1)*12'.format(ia+1),23+quest_slot,'=CEILING((B{0}-E{0})/2,1)*12'.format(ia+1),'',f'{ws_count} slot-taking weapons (Exalted/intrinsic excluded; Vinquibus counted once). Free: 11 starter + 12 junction/quest + {quest_slot} weapons that bring their own slot (Grimoire, Nataruk) (other quest weapons such as Thornbak, Broken War, Skiajati and Rumblejack must be sold to free theirs)'])
add(['Companion slots (2 per 12p)',COMP_SLOTS,6,'=CEILING(B{0}/2,1)*12'.format(ia+2),10,'=MAX(0,CEILING((B{0}-E{0})/2,1)*12)'.format(ia+2),'',f'{COMP_SLOTS} = 8 assigned companions + 4 bundled sentinel weapons (v4.3 final builds); 10 starter'])
ib=ms.max_row
FI=add(['FIXED INFRASTRUCTURE TOTAL','','',f'=SUM(D{ia}:D{ib})','',f'=SUM(F{ia}:F{ib})'],True)
add([])
add(['3. OPTIONAL CONVENIENCE (plat shortcut for farmable items)','Count','Unit Pt','Pt','','','','Basis'],True)
oa=ms.max_row+1
add(['Orokin Reactors',65,20,f'=B{oa}*C{oa}','','','','66 frames minus Excalibur Umbra (pre-installed). Sirius & Orion counted once for Sirius; Orion\'s Reactor is pre-installed (wiki). Verified v4.3 XR against every frame page.'])
add(['Orokin Catalysts',cat_count,20,f'=B{oa+1}*C{oa+1}','','','',f'{cat_count} ordinary non-adversary weapons (Kuva/Tenet pre-installed; Grimoire/Nataruk quest pre-installed; Exalted use frame Reactor)'])
add(['Incarnon Genesis via Cavalero (plat, one-time each)',32,120,f'=B{oa+2}*C{oa+2}','','','','wiki (U39): rotation adapters purchasable for 120p incl. install resources (U39). Otherwise farm Steel Path Circuit'])
OC=add(['OPTIONAL CONVENIENCE TOTAL','','',f'=SUM(D{oa}:D{oa+2})'],True)
add([])
add(['4. RECONSTRUCTION TOTALS','Floor Pt','Realistic Pt','Conservative Pt','USD Floor','USD Realistic','USD Conservative'],True)
def tot(lab,extra):
    i=ms.max_row+1
    add([lab,f'=B{PT}+{extra}',f'=C{PT}+{extra}',f'=D{PT}+{extra}',f'=B{i}*{PLAT_USD}',f'=C{i}*{PLAT_USD}',f'=D{i}*{PLAT_USD}'])
    return i
T1=tot('TOTAL RECONSTRUCTION (trade + fixed infra net of free slots)',f'F{FI}')
T2=tot('TOTAL RECONSTRUCTION (trade + fixed infra gross, v3 method)',f'D{FI}')
T3=tot('TOTAL incl. optional Reactors/Catalysts (gross)',f'D{FI}+D{OC}')
add([])
add(['5. COMPARISON vs ~$1,000 / ~23,000p','Floor','Realistic','Conservative'],True)
c1=add(['Net reconstruction / 23,000p',f'=B{T1}/23000',f'=C{T1}/23000',f'=D{T1}/23000'])
c2=add(['Gross + potatoes / 23,000p',f'=B{T3}/23000',f'=C{T3}/23000',f'=D{T3}/23000'])
add(['Interpretation: see 7. MODEL NOTES. Account-purchase risk (ban/recovery/ToS) is NOT priced here and must be assessed separately.'])
add([])
add(['6. FARMABLE SAVINGS / ACCOUNT-BOUND (not plat)','Value','','','','','','Note'],True)
add(['Mods bought at R0 instead of max (realistic plat)',f'=SUMIFS({rng("R0 Realistic")},{rng("Category")},"Mod",{rng("Counted in Player-Trade Total?")},"Yes")','','','','','','Requires the Endo/credits below; R0 not on market for some mods'])
add(['  Endo needed to max every PvE mod yourself',f'=SUMIFS({rng("Endo to Max")},{rng("Category")},"Mod",{rng("Counted in Player-Trade Total?")},"Yes")'])
add(['  Credits needed to max every PvE mod yourself',f'=SUMIFS({rng("Credits to Max")},{rng("Category")},"Mod",{rng("Counted in Player-Trade Total?")},"Yes")'])
add(['Arcanes via R0 copies (sum where available, required set)',f'=SUMIFS({rng("Max via R0 copies (Realistic)")},{rng("Category")},"Arcane",{rng("Counted in Player-Trade Total?")},"Yes")'])
add(['Non-tradeable frames/weapons/companions (farm/quest/vendor/Dojo)',f'=COUNTIFS({rng("Status")},"FARMABLE*")','','','','','','items; 0p by definition'])
add(['Incarnon Genesis adapters (Steel Path Circuit)',f'=COUNTIFS({rng("Adapter required?")},"Incarnon*")','','','','','','adapters'])
add(['Build-required mods: account-bound / earned (0p, see EARNED REQUIREMENTS)',f'=COUNTIFS({rng("Category")},"Mod",{rng("Priority")},"ACCOUNT-BOUND*")','','','','','','Umbral x3 (The Sacrifice), Primed Shred (Daily Tribute), Amalgam Organ Shatter (Thermia Fractures)'])
add(['Build-required mods with NO market price (excluded from totals)',f'=COUNTIFS({rng("Category")},"Mod",{rng("Priority")},"BUILD REQUIRED*",{rng("Status")},"*UNAVAILABLE*")','','','','','','Must be 0 for FINAL; any such row would be acquired by farm / private trade outside these totals'])
add(['Archon Shards (account-bound)',330,'','','','','','66 frames x 5; v3 shard plan covers only 230'])
add([])
add(['Official Platinum pack',4600,199.99,'','','','','Current undiscounted USD price (v3)'])
add(['$1,000 benchmark packs',5,4600,'=B{0}*C{0}'.format(ms.max_row+1),'','','','Five 4,600p packs = 23,000p for $999.95'])
add([])
add(['7. MODEL NOTES'],True)
for t in ['Mods are ~70% of the player-trade total. Buying every PvE mod already at max rank is the most expensive acquisition route; buying R0 copies and ranking them yourself (section 6) removes most of that premium at the cost of Endo/credits.',
          'Many collection mods (common drops, syndicate offerings, Nightwave/Cephalon Simaris items) are farmable at no plat cost; the max-rank trade total is an upper-bound valuation of the mandate, not a recommended spend plan.',
          'Conservative mod pricing is wide because many max-rank books are thin (few sellers). Use Realistic for decisions; Conservative is an allowance.',
          'Prime frames/weapons are priced as complete sets; buying parts or cracking relics is cheaper but slower.',
          'Account purchase comparison: the $1,000 / 23,000p benchmark should be compared to the portion of THIS procurement universe a candidate account already satisfies (equivalency audit), not to its raw inventory. Purchase risk is separate.',
          'Platinum totals exclude Forma, Archon Shards, Focus, Helminth, Incarnon Genesis, Endo and credits (all farmable/account-bound).',
          'Platinum totals EXCLUDE any unpriced private-trade acquisition: a build-required row with Status MARKET DATA UNAVAILABLE contributes 0p (count in section 6; v4.3 FINAL has none - Corroding Barrage and Swift Deth were archived mods, replaced by Rousing Plunder and Assault Mode, both priced). Earned account-bound build requirements (Umbral x3, Primed Shred, Amalgam Organ Shatter) are 0p by definition - see EARNED REQUIREMENTS.']:
    add(['  - '+t])
for row_ in ms.iter_rows(min_row=5):
    for c in row_[1:7]:
        if isinstance(c.value,str) and c.value.startswith('='): c.number_format='#,##0'
for r in (T1,T2,T3):
    for col in 'EFG': ms[f'{col}{r}'].number_format='$#,##0'
for r in (c1,c2):
    for col in 'BCD': ms[f'{col}{r}'].number_format='0.00"x"'
# ---- Corrections log, allocation, roster, open items
v3c=[('Mods sheet','Savage Silence listed as Ash augment','Mod data: Savage Silence is the Banshee Silence augment.','Reassigned to Banshee.','None (collection buys every mod).'),
     ('Mods sheet','Repelling Bastille (Vauban)','Mod data: no such mod exists live; the Bastille augment is Enduring Bastille.','Replaced with Enduring Bastille.','None (collection).'),
     ('Archon Shards','230 planned shards','66 frames x 5 slots = 330.','100 shards unplanned; flagged.','Account-bound; no plat effect.'),
     ('Companion slots','7 pairs (14 slots) x 12p, zero free','13 companions + 7 sentinel robotic weapons = 20 companion slots; 10 starter slots.','Gross 10 pairs (120p); net 5 pairs (60p).','Infrastructure recalculated.'),
     ('Arcanes','14 Warframe + Melee Crescendo only','183 ordinary weapons have arcane slots but no weapon arcanes were specified.','Added a v4 weapon-arcane baseline (11 Arcanes) as required.','Required Arcane total increases.'),
     ('Summary counts','Adversary targets 11 / Incarnon 18 / weapons 176','Normalized: adversary 12, Incarnon 39 (32 Genesis + 7 innate), 183 slot weapons + 14 Exalted/intrinsic.','Summary updated.','Slots, Catalysts, Elemental Vice (12) recalculated.')]
newsheet('Corrections Log',['Area','OLD ASSUMPTION','CURRENT EVIDENCE','CORRECTION','DOWNSTREAM EFFECT'],list(meta.CORRECTIONS)+v3c,{'OLD ASSUMPTION':40,'CURRENT EVIDENCE':70,'CORRECTION':55,'DOWNSTREAM EFFECT':45},idx=1)
al=[[r[0]]+r[1:]+old[r[0]]+['; '.join(sl for sl,a,b in zip(['Primary','Secondary','Melee'],r[1:],old[r[0]]) if a!=b) or '-'] for r in rows]
wa=newsheet('Weapon Allocation v4',['Frame','Primary','Secondary','Melee','v3 Primary','v3 Secondary','v3 Melee','Changed slots'],al,{'Frame':18,'Primary':24,'Secondary':24,'Melee':24,'v3 Primary':20,'v3 Secondary':20,'v3 Melee':20,'Changed slots':24},idx=2)
for i,r in enumerate(rows,2):
    for j in range(3):
        if r[1+j]!=old[r[0]][j]: wa.cell(i,2+j).fill=CH
ro=[]
for r in rows:
    f=r[0]; v=FR.get(f,{}); b=FR.get(f.replace(' Prime',''),{})
    ro.append([f,'Prime' if f.endswith('Prime') else ('Umbra' if 'Umbra' in f else 'Base (no Prime)'),v.get('Introduced'),', '.join(v.get('Abilities') or []),(v.get('Passive') or '').replace('\n',' ')[:300],v.get('Subsumed') or b.get('Subsumed'),', '.join(k for k,s in meta.SIG.items() if s[0]==f)])
newsheet('Roster v4 (live)',['Frame','Version','Introduced','Abilities (live)','Passive (live)','Helminth ability (live)','Signature weapons (live)'],ro,{'Abilities (live)':55,'Passive (live)':70,'Signature weapons (live)':40},idx=3)
oi=[('Protea','RESOLVED v4.3 B4: Roar over Grenade Fan + Temporal Artillery + Temporal Erosion','No action'),
    ('Dante','Noctua ruled additional Exalted (no Secondary replacement); Noctua build kept for Wordwarden','OPTIONAL preference only: in-game check if a Secondary replacement is ever wanted (not a LIVE TEST)'),
    ('Sirius & Orion','RESOLVED v4.3 B5 (wiki): Orion comes with a pre-installed Orokin Reactor; one Reactor per S&O is correct','No action'),
    ('Banshee (TIME-SENSITIVE, not in baseline)','Wiki: every player logging in 23 Sep - 7 Oct 2026 receives a free base Banshee (pre-installed Reactor + its own Warframe slot; U44 rework gift). Base Banshee is the Helminth donor for Silence, which Ash Prime subsumes (the only Silence build).','PREFERRED USE: feed her to the Helminth as Ash\'s Silence donor - this also frees the slot she arrived with. Her pre-installed Reactor is consumed with her (non-transferable) and does NOT reduce the 65-Reactor procurement count. Opportunity only: the model keeps baseline economics unless the claim is confirmed.'),
    ('Signature preference','v4.1 allocated uncontested no-bonus signatures (Temple Riot-848, Mirage Akzani, S&O Pride)','Revert to Athodai / Prisma Twin Gremlins / Caustacyst if preferred; counts unchanged'),
    ('Builds','RESOLVED v4.2/v4.3: per-frame aura/exilus/mods/Arcanes/shards/focus/companion builds for all 66 frames (FRAME BUILDS, optimization-audited 66/66)','No action'),
    ('Archon Shards','RESOLVED v4.2/v4.3: all 330 shard positions assigned (see ARCHON SHARD ASSIGNMENTS)','No action'),
    ('Sentinel weapons','Resolved v4.1: default weapons bundled (Verglas Prime, Prime Laser Rifle, Deth Machine Rifle Prime, Burst Laser Prime, Deconstructor Prime, Vulklok, Artax)','Change only if non-default sentinel weapons are wanted'),
    ('Brysko','Tracked in Upcoming (Not Live); excluded from live cost','Integrate on release: frame, Corecracker ruling, Rain & Shine, Hound, Sentient shotgun'),
    ('Tigris Incarnon','Announced Incarnon adapter (Nekros Tigris Prime) not live','Add Genesis row on release'),
    ('Adversary elements','RESOLVED v4.3: progenitor elements included in the element-order validator (203/203 configs valid)','No action'),
    ('Variant families','Vectis/Prime, Trumna/Prime, Dual Keres/Prime, Epitaph/Prime, Cedo/Prime, Pyrana/Prime, Ohma/Prisma Ohma','Distinct items; optional further uniqueness pass'),
    ('Account purchase','No candidate account inventory supplied','Provide export for the equivalency audit')]
newsheet('Open Items',['Area','Issue','Action'],oi,{'Issue':80,'Action':70},idx=4)
import subprocess; subprocess.run(['python3','recon.py'],capture_output=True)
rec=json.load(open('recon.json'))
rs=newsheet('Live Content Reconciliation',['LIVE ITEM','Release (frames in that update)','Slot','Class','Association','PRESENT IN WORKBOOK?','CURRENT ASSIGNMENT','PROCUREMENT ROW?','ACTION REQUIRED'],rec,
   {'LIVE ITEM':26,'Release (frames in that update)':34,'Association':36,'CURRENT ASSIGNMENT':34,'PROCUREMENT ROW?':46,'ACTION REQUIRED':80},idx=2)
up=[[r['Item'],r['Variant'],r['Assigned Frame(s)'],r['Notes'],r['Status']] for r in proc if r['Category']=='Upcoming (Not Live)']
newsheet('Upcoming (Not Live)',['Item','Type','Frame','Notes','Status'],up,{'Item':28,'Type':34,'Notes':70,'Status':36},idx=3)
# ---- Update existing sheets
ws=wb['Weapons']; ws.delete_rows(2,ws.max_row)
ws.cell(1,8,'v4 Signature status'); ws.cell(1,9,'Mechanical frame bonus'); ws.cell(1,10,'Incarnon?'); ws.cell(1,11,'v3 value'); hdr(ws)
for r in proc:
    if r['Category'] in ('Weapon','Adversary Weapon','Exalted / Intrinsic','Archgun'):
        ws.append([r['Item'],r['Slot'],r['Category'],r['Acquisition Method'],r['Assigned Frame(s)'],r['Source/Reasoning'],r['Status'],r['Signature status'],r['Mechanical frame bonus'],r['Incarnon?'],r['Notes']])
ws=wb['Adversary']; ws.delete_rows(2,ws.max_row)
for i,h in enumerate(['Assigned Frame','Element target','Floor Pt','Realistic Pt','Conservative Pt','Market status'],6): ws.cell(1,i,h)
hdr(ws)
for r in proc:
    if r['Category']=='Adversary Weapon':
        ws.append([r['Item'],r['Variant'],'60% (>=58% priced)','Rank 40 (5 Forma) + Elemental Vice',r['Status'],r['Assigned Frame(s)'],r['Element target'],r['Floor Platinum'],r['Realistic Platinum'],r['Conservative Platinum'],r['Notes']])
ws=wb['Incarnon Genesis']; ws.delete_rows(2,ws.max_row); ws.cell(1,5,'Weapon (final variant)'); ws.cell(1,6,'Frame'); hdr(ws)
for r in proc:
    if r['Category']=='Weapon' and r['Incarnon?'] and r['Incarnon?'].startswith('Yes'):
        innate='innate' in r['Incarnon?']
        ws.append([r['Item'].replace(' Prime','') if not innate else r['Item'],'Innate Incarnon (no adapter)' if innate else 'Steel Path Circuit / Cavalero rotation','Native evolution' if innate else 'Install on assigned final variant','INNATE' if innate else 'Need',r['Item'],r['Assigned Frame(s)']])
ws=wb['Arcanes']
for i,h in enumerate(['Floor Pt','Realistic Pt','Conservative Pt','Via R0 copies Pt','Market status'],7): ws.cell(1,i,h)
hdr(ws)
pa={r['Item']:r for r in proc if r['Category']=='Arcane'}
for row_ in ws.iter_rows(min_row=2):
    r=pa.get(row_[0].value)
    if r:
        for i,k in enumerate(['Floor Platinum','Realistic Platinum','Conservative Platinum','Max via R0 copies (Realistic)','Status'],7): ws.cell(row_[0].row,i,r[k])
for nm in REQ_ARC_V4:
    r=pa.get(nm,{})
    ws.append([nm,nm.split()[0],'Rank 5','Tradeable','v4 weapon-arcane baseline','Need',r.get('Floor Platinum'),r.get('Realistic Platinum'),r.get('Conservative Platinum'),r.get('Max via R0 copies (Realistic)'),r.get('Status')])
ws=wb['Mods']
for i,h in enumerate(['Max Rank','Floor Pt','Realistic Pt','Conservative Pt','Market status'],8): ws.cell(1,i,h)
hdr(ws)
pmod={r['Item']:r for r in proc if r['Category']=='Mod'}
for row_ in ws.iter_rows(min_row=2):
    nm=row_[1].value
    if nm=='Savage Silence': ws.cell(row_[0].row,6,'Banshee (v4 fix: was Ash)')
    if nm=='Repelling Bastille': ws.cell(row_[0].row,2,'Enduring Bastille'); ws.cell(row_[0].row,6,'Vauban (v4 fix: Repelling Bastille does not exist)'); nm='Enduring Bastille'
    r=pmod.get(nm)
    if r:
        for i,k in enumerate(['Required Rank','Floor Platinum','Realistic Platinum','Conservative Platinum','Status'],8): ws.cell(row_[0].row,i,r[k])
ws.append(['Collection mandate (v4)',f'{sum(1 for r in proc if r["Category"]=="Mod")} mods priced at max rank','MAX RANK','See Procurement Master','','Full list incl. category, Endo/credit relevance',''])
ws=wb['Companions']
for i,h in enumerate(['Floor Pt','Realistic Pt','Conservative Pt','Market status'],5): ws.cell(1,i,h)
hdr(ws)
pc={r['Item']:r for r in proc if r['Category']=='Companion'}
for row_ in ws.iter_rows(min_row=2):
    r=pc.get(row_[0].value)
    if r:
        for i,k in enumerate(['Floor Platinum','Realistic Platinum','Conservative Platinum','Status'],5): ws.cell(row_[0].row,i,r[k])
ws=wb['Archon Shards']; ws.append(['TOTAL PLANNED',230,'','','v4: 66 frames x 5 = 330 slots; 100 unplanned','OPEN'])
ws=wb['Account Infrastructure']
for row_ in ws.iter_rows(min_row=2):
    if row_[0].value=='Orokin Catalysts': ws.cell(row_[0].row,2,f'{cat_count} ordinary non-adversary weapons (v4.3: Grimoire/Nataruk pre-installed)')
    if row_[0].value=='Elemental Vice': ws.cell(row_[0].row,2,'12 baseline (v4: 12 adversary weapons)')
    if row_[0].value=='Orokin Reactors': ws.cell(row_[0].row,2,'65 (66 frames minus Umbra)')
ws=wb['Normalization Log']
for (f,sl),(o,n,why) in meta.CHANGES.items(): ws.append([f'{f}: {o} -> {n} ({sl})',why,'FINAL (v4)'])
ws=wb['Frames']
for row_ in ws.iter_rows(min_row=2):
    f=row_[0].value; r=next((x for x in proc if x['Category']=='Warframe' and x['Item']==f),None)
    if r: ws.cell(row_[0].row,6,f"v4: {r['Status']}; R={r['Realistic Platinum']}p")
    if f=='Protea Prime': ws.cell(row_[0].row,5,'v4: Roar/Temporal Artillery conflict - see Open Items')
    if f=='Narin': ws.cell(row_[0].row,5,'v4: Nurinarim = cast ability, no Melee replacement; Prisma Skana')
    if f=='Nokko': ws.cell(row_[0].row,5,'v4: Sporothrix / Ocucor / Mios; Arbucep signature archgun')
    if f=='Dante': ws.cell(row_[0].row,5,'v4: Phenmor / Onos / Ruvox; Noctua additional Exalted')
ws=wb['Phase 3 Summary']
upd={'Named weapon rows':(ws_count,f'{ws_count} slot-taking + 14 Exalted/intrinsic (v4 normalized)'),'Incarnon adapters':(32,'32 Genesis + 7 innate (v4)'),
     'Adversary targets':(12,'v4'),'Arcane families':(25,'14 v3 + 11 v4 weapon baseline'),'Exact duplicate weapon names':(0,'v4 logical audit: 0 exact'),'Incarnon Genesis targets':(32,'v4 live audit')}
for row_ in ws.iter_rows(min_row=1):
    m=row_[3].value
    if m in upd: ws.cell(row_[0].row,5,upd[m][0]); ws.cell(row_[0].row,6,upd[m][1])
    if m=='Gross storage Pt': ws.cell(row_[0].row,5,f"='Economic Model'!D{FI}"); ws.cell(row_[0].row,6,'Gross fixed infrastructure (v4)')
    if m=='Gross potato shortcut Pt': ws.cell(row_[0].row,5,f"='Economic Model'!D{OC}")
    if m=='Gross fixed shortcut Pt': ws.cell(row_[0].row,5,f"='Economic Model'!D{FI}+'Economic Model'!D{OC}")
    if m=='$1k official-store benchmark Pt': ws.cell(row_[0].row,5,23000)
ws.append([]); ws.append(['','','','Realistic total reconstruction Pt (v4)',f"='Economic Model'!C{T1}",'Trade + net fixed infrastructure'])
ws['A1']='WARFRAME PERMANENT ACCOUNT - PHASE 3 PROCUREMENT MASTER v4 (normalized + live-priced)'
src=wb['Sources']; src.append(['Warframe Wiki data modules (Warframes/Weapons/Mods/Arcane data)','https://wiki.warframe.com/w/Module:Weapons/data','Live roster, slots, Incarnon, signatures, mod tradeability (pulled 2026-10-05)']); src.append(['Warframe.Market API v2/v1','https://api.warframe.market','Live orders, 90d statistics, lich/sister auctions (PC)'])
wb.calculation=CalcProperties(fullCalcOnLoad=True)
wb.save('Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx'); print('saved', wb.sheetnames)
