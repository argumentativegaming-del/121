import json, math, statistics, datetime, collections, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pricer import price, item_info, load, days_since
import meta
TS='2026-10-05 UTC (WFM pull 02:52-04:00)'
PLAT_USD=1000/23000
W=json.load(open('weapons_all.json'))
FR=json.load(open('warframes.json'))['Warframes']
items={i['slug']:i for i in json.load(open('wfm_items.json'))['data']}
byname={i['i18n']['en']['name'].lower():s for s,i in items.items()}
MODS=json.load(open('mods.json'))['Mods']; modbyn={v['Name'].lower():v for v in MODS.values()}
ARC=json.load(open('arcanes.json'))['Arcanes']; arcbyn={v['Name'].lower():v for v in ARC.values()}
rows=[l.strip().split('|') for l in open('alloc_new.txt') if l.strip()]
old={r[0]:r[1:] for r in (l.strip().split('|') for l in open('alloc_old.txt') if l.strip())}
INC=set()
for k,v in W.items():
    if v.get('IncarnonImage') or any('Incarnon' in str(a.get('AttackName','')) for a in v.get('Attacks',[])): INC.add(k)
COLS=['Category','Item','Assigned Frame(s)','Slot','Variant','Required Rank','Quantity','Acquisition Method','Tradeable?','Already Owned?','Priority',
 'Floor Platinum','Realistic Platinum','Conservative Platinum','Market Timestamp','Status','Notes','Source/Reasoning',
 'Market Slug','Credible Sellers','Online Sellers','Recent Median (30d)','90d Median','90d Weighted Avg','90d Volume','48h Volume','Best Online Buy','Buy/Sell Spread',
 'Signature status','Mechanical frame bonus','Incarnon?','Adapter required?','Adversary family?','Valence target','Element target','Rank 40?','Ephemera?','Catalyst?','Forma estimate',
 'Mod Category','Endo to Max','Credits to Max','R0 Realistic','Max via R0 copies (Realistic)','Counted in Player-Trade Total?']
proc=[]
def row(**k):
    r={c:None for c in COLS}; r.update(k); proc.append(r); return r
def mk(p):
    return {'Floor Platinum':p.get('floor'),'Realistic Platinum':p.get('realistic'),'Conservative Platinum':p.get('conservative'),
            'Market Timestamp':TS if p.get('status')!='NOT FETCHED' else None,'Status':p.get('status'),'Market Slug':p.get('slug'),
            'Credible Sellers':p.get('sellers_credible'),'Online Sellers':p.get('sellers_online'),'Recent Median (30d)':p.get('median30'),'90d Median':p.get('median90'),
            '90d Weighted Avg':p.get('wa90'),'90d Volume':p.get('vol90'),'48h Volume':p.get('vol48h'),'Best Online Buy':p.get('best_buy'),'Buy/Sell Spread':p.get('spread')}
def slug_for(name, parts=True):
    for c in [name+' set', name, name+' blueprint']:
        if c.lower() in byname: return byname[c.lower()]
    return None
# ---------------- Frames
for r in rows:
    f=r[0]; v=FR.get(f,{})
    prime=f.endswith('Prime')
    s=slug_for(f) if prime else None
    owned='YES' if f=='Cyte-09' else None
    if s:
        p=price(s,None); d=mk(p)
        row(Category='Warframe',Item=f,**{'Assigned Frame(s)':f,'Slot':'Warframe','Variant':'Prime','Quantity':1,'Acquisition Method':'Player trade (set)','Tradeable?':'Yes','Already Owned?':owned,'Priority':'Core',
            'Counted in Player-Trade Total?':'Yes','Source/Reasoning':'Best permanent version (Prime replaces Normal)','Notes':f"Helminth: {v.get('Subsumed') or FR.get(f.replace(' Prime',''),{}).get('Subsumed')}"},**d)
    else:
        how={'Excalibur Umbra':'Quest: The Sacrifice (slot + reactor included)','Cyte-09':'Already owned'}.get(f,'Farm / quest / vendor (account-bound)')
        row(Category='Warframe',Item=f,**{'Assigned Frame(s)':f,'Slot':'Warframe','Variant':'Umbra' if 'Umbra' in f else 'Base (no Prime)','Quantity':1,'Acquisition Method':how,'Tradeable?':'No','Already Owned?':owned,'Priority':'Core',
            'Status':'FARMABLE / ACCOUNT-BOUND','Counted in Player-Trade Total?':'No','Source/Reasoning':'No Prime exists in live data' if f!='Excalibur Umbra' else 'Doctrine: Umbra replaces Excalibur','Notes':f"Helminth: {v.get('Subsumed')}"})
# ---------------- Weapons
for r in rows:
    f=r[0]
    for i,(sl,wn) in enumerate(zip(['Primary','Secondary','Melee'],r[1:])):
        v=W.get(wn) or {}
        ch=meta.CHANGES.get((f,sl))
        oldw=old[f][i]
        reason=ch[2] if ch else ('Unchanged from v3 allocation')
        base=wn.replace(' (Primary)','').replace(' (Melee)','')
        sig=meta.SIG.get(base)
        sigtxt=('Signature - '+sig[0]) if sig and sig[0]==f else None
        bonus=sig[1] if sigtxt else None
        exalted = v.get('Class') in ('Exalted Weapon','Unique') or wn in ('Garuda Prime Talons','Razorflies')
        common={'Assigned Frame(s)':f,'Slot':sl,'Signature status':sigtxt or ('Exalted/Intrinsic' if exalted else 'Non-signature'),'Mechanical frame bonus':bonus,
                'Source/Reasoning':reason,'Notes':(f'v3: {oldw}' if oldw!=wn else None)}
        if exalted:
            row(Category='Exalted / Intrinsic',Item=wn,**common,**{'Quantity':1,'Acquisition Method':'Comes with frame','Tradeable?':'No','Status':'INCLUDED WITH FRAME','Counted in Player-Trade Total?':'No','Catalyst?':'No (frame Reactor)'})
            continue
        if wn=='Vinquibus (Melee)':
            row(Category='Weapon',Item=wn,**common,**{'Quantity':0,'Acquisition Method':'Same item as Vinquibus (Primary)','Tradeable?':'No','Status':'COVERED BY VINQUIBUS','Counted in Player-Trade Total?':'No','Catalyst?':'Shared'})
            continue
        INNATE={'Innodem','Praedos','Ruvox','Phenmor','Onos','Felarx','Laetum'}
        innate=wn in INNATE
        isinc=wn in INC or innate
        incf={'Incarnon?':('Yes (innate)' if innate else 'Yes (Genesis)') if isinc else 'No','Adapter required?':'Incarnon Genesis (farm: Steel Path Circuit)' if isinc and not innate else None,'Forma estimate':4 if isinc else 3}
        if wn.startswith(('Kuva ','Tenet ')):
            continue  # handled in adversary section
        s=slug_for(base)
        if s:
            p=price(s,None); d=mk(p)
            bp=s.endswith('_blueprint')
            row(Category='Weapon',Item=base,**common,**incf,**{'Variant':'Prime' if 'Prime' in base else ('Vandal/Wraith/Prisma' if any(x in base for x in ['Vandal','Wraith','Prisma']) else 'Standard'),
                'Quantity':1,'Acquisition Method':'Player trade (blueprint; craft resources farmable)' if bp else 'Player trade','Tradeable?':'Yes','Priority':'Core','Catalyst?':'Yes','Counted in Player-Trade Total?':'Yes'},**d)
        else:
            row(Category='Weapon',Item=base,**common,**incf,**{'Variant':'Standard','Quantity':1,'Acquisition Method':'Farm / vendor / Dojo / quest','Tradeable?':'No','Priority':'Core','Catalyst?':'Yes','Status':'FARMABLE / ACCOUNT-BOUND','Counted in Player-Trade Total?':'No'})
# archgun signature extras
for wn,f in [('Larkspur Prime','Hildryn Prime'),('Mandonel','Qorvex'),('Arbucep','Nokko')]:
    s=slug_for(wn); sig=meta.SIG[wn]
    base={'Assigned Frame(s)':f,'Slot':'Archgun','Signature status':'Signature - '+f,'Mechanical frame bonus':sig[1],'Priority':'Optional (signature extra)','Quantity':1,'Source/Reasoning':'Signature archgun; not an ordinary slot. Uses free Archweapon slots (4 starter).'}
    if s:
        p=price(s,None); row(Category='Archgun',Item=wn,**base,**{'Acquisition Method':'Player trade','Tradeable?':'Yes','Counted in Player-Trade Total?':'Optional'},**mk(p))
    else:
        row(Category='Archgun',Item=wn,**base,**{'Acquisition Method':'Farm / vendor','Tradeable?':'No','Status':'FARMABLE / ACCOUNT-BOUND','Counted in Player-Trade Total?':'No'})
# ---------------- Adversary
for r in rows:
    f=r[0]
    for sl,wn in zip(['Primary','Secondary','Melee'],r[1:]):
        if not wn.startswith(('Kuva ','Tenet ')): continue
        slug=wn.lower().replace(' ','_'); el=meta.ELEMENT[wn]
        a=(load('auctions',slug) or {}).get('payload',{}).get('auctions',[])
        cred=[x for x in a if x.get('visible') and not x.get('closed') and x.get('is_direct_sell') and x.get('buyout_price') and days_since(x['owner'].get('last_seen',''))<=7]
        def pick(cond):
            return sorted(x['buyout_price'] for x in cred if cond(x['item']))
        exact=pick(lambda it: it.get('element')==el and it.get('damage',0)>=58)
        anyhi=pick(lambda it: it.get('damage',0)>=58)
        elany=pick(lambda it: it.get('element')==el)
        eph=pick(lambda it: it.get('element')==el and it.get('damage',0)>=58 and it.get('having_ephemera'))
        use,basis=(exact,'target element, >=58% valence') if len(exact)>=1 else ((elany,'target element, any valence (fuse to 60% by farming)') if elany else (anyhi,'any element >=58%'))
        d={}
        if use:
            top=use[:3]; real=statistics.median(top)
            d={'Floor Platinum':use[0],'Realistic Platinum':round(real,1),'Conservative Platinum':math.ceil(max(real,use[min(2,len(use)-1)])*1.10),'Status':('OK' if len(use)>=3 else 'THIN')+' - '+basis,'Market Timestamp':TS,'Credible Sellers':len(use)}
        else: d={'Status':'MARKET DATA UNAVAILABLE'}
        row(Category='Adversary Weapon',Item=wn,**{'Assigned Frame(s)':f,'Slot':sl,'Variant':'Kuva' if wn.startswith('Kuva') else 'Tenet','Quantity':1,'Acquisition Method':'WFM Lich/Sister auction (direct buyout)','Tradeable?':'Yes (auction)','Priority':'Core',
            'Adversary family?':'Kuva Lich' if wn.startswith('Kuva') else 'Sister of Parvos','Valence target':'60%','Element target':el.title(),'Rank 40?':'Yes (5 Forma/Rank-ups; farm)','Ephemera?':'Not required' + (f' (cheapest w/ ephemera: {eph[0]}p)' if eph else ''),
            'Catalyst?':'Pre-installed','Forma estimate':5+3,'Counted in Player-Trade Total?':'Yes','Market Slug':slug,'Source/Reasoning':'Existing v3 selection kept; Coda not substituted per doctrine','Notes':f"{len(a)} auctions total; {len(cred)} direct-sell w/ owner seen <=7d; >=58%/any element floor: {anyhi[0] if anyhi else 'n/a'}"},**d)
# ---------------- Mods
EXCL_MOD={'equilibrium_steam_pinnacle_pack','cephalon_suda_augment_mod','steel_meridian_augment_mod','the_perrin_sequence_augment_mod','new_loka_augment_mod','arbiters_of_hexis_augment_mod','red_veil_augment_mod','grendel_systems_locator','grendel_chassis_locator','grendel_neuroptics_locator'}
RAR={'Common':1,'Uncommon':2,'Rare':3,'Legendary':4,'Riven':4,'Amalgam':3,'Peculiar':3}
def modcat(i,wm):
    t=set(i['tags']); ty=(wm or {}).get('Type','')
    nm=i['i18n']['en']['name']
    if 'pvp' in t: return 'Conclave (PvP)'
    if nm.startswith('Primed '): pre='Primed '
    elif nm.startswith('Galvanized '): pre='Galvanized '
    elif nm.startswith('Archon '): pre='Archon '
    elif nm.startswith('Umbral ') or nm.startswith('Sacrificial '): pre='Umbral/Sacrificial '
    elif 'augment' in t or (wm or {}).get('IsAbilityAugment') or (wm or {}).get('IsWeaponAugment'): pre='Augment '
    elif 'aura' in t: pre=''
    elif 'stance' in t: pre=''
    else: pre=''
    if 'aura' in t: return 'Aura'
    if 'stance' in t: return 'Stance'
    if 'syndicate' in t and 'augment' in t: return 'Syndicate Weapon Augment'
    if (wm or {}).get('Polarity')=='Umbra' or 'Corrupted' in str(wm.get('Rarity') if wm else ''): pass
    base=ty or next((x for x in ['warframe','primary','secondary','melee','shotgun','rifle','sentinel','kubrow','kavat','archwing','archgun','archmelee','necramech','railjack','k_drive','parazon'] if x in t),'Other')
    return (pre+base).strip()
for s,i in sorted(items.items()):
    t=set(i['tags'])
    if 'mod' not in t or 'riven_mod' in t or 'veiled_riven' in t or s in EXCL_MOD: continue
    nm=i['i18n']['en']['name']; wm=modbyn.get(nm.lower())
    if wm and wm.get('IsFlawed'): continue
    info=item_info(s); mr=info.get('maxRank') if info else (wm or {}).get('MaxRank')
    p=price(s,'max'); d=mk(p)
    p0=price(s,0) if mr else {}
    rar=(wm or {}).get('Rarity') or info.get('rarity','').title() if info else 'Common'
    m=RAR.get(str(rar).title(),2)
    endo=10*m*(2**mr-1) if mr else 0
    cat=modcat(i,wm)
    row(Category='Mod',Item=nm,**{'Variant':cat,'Required Rank':mr,'Quantity':1,'Acquisition Method':'Player trade (max rank)','Tradeable?':'Yes','Priority':'Collection' if cat!='Conclave (PvP)' else 'Collection (PvP)',
        'Mod Category':cat,'Endo to Max':endo,'Credits to Max':round(endo*48.3) if endo else 0,'R0 Realistic':p0.get('realistic'),'Counted in Player-Trade Total?':'Yes' if cat!='Conclave (PvP)' else 'PvP subtotal',
        'Source/Reasoning':'Every current tradeable mod at MAX RANK (WFM catalogue, rivens/locators excluded)'},**d)
# wiki-tradeable mods absent from WFM
for v in MODS.values():
    if v.get('Tradable') and not v.get('IsFlawed') and not v.get('_IgnoreEntry') and 'riven' not in v['Name'].lower() and 'fusion core' not in v['Name'].lower() and v['Name']!='Legendary Core' and 'Pinnacle Pack' not in v['Name']:
        if v['Name'].lower() not in byname:
            row(Category='Mod',Item=v['Name'],**{'Variant':v.get('Type'),'Required Rank':v.get('MaxRank'),'Quantity':1,'Acquisition Method':'Player trade (in-game only)','Tradeable?':'Yes (wiki)','Status':'MARKET DATA UNAVAILABLE','Mod Category':v.get('Type'),'Counted in Player-Trade Total?':'No (no data)','Source/Reasoning':'Wiki lists as tradeable; no Warframe.Market listing'})
REQ_ARC_V3=['Molt Augmented','Arcane Energize','Arcane Grace','Arcane Guardian','Arcane Fury','Arcane Strike','Arcane Aegis','Arcane Avenger','Arcane Precision','Arcane Velocity','Molt Efficiency','Molt Reconstruct','Arcane Blessing','Melee Crescendo']
REQ_ARC_V4=['Primary Merciless','Primary Deadhead','Primary Dexterity','Secondary Merciless','Secondary Deadhead','Secondary Dexterity','Melee Influence','Melee Animosity','Melee Duplicate','Melee Exposure','Melee Vortex']
# ---------------- Companions (v3 list)
COMP=[('Panzer Vulpaphyla',None),('Nautilus Prime','nautilus_prime_set'),('Wyrm Prime','wyrm_prime_set'),('Dethcube Prime','dethcube_prime_set'),('Diriga',None),('Adarza Kavat','adarza_kavat_imprint'),('Smeeta Kavat','smeeta_kavat_imprint'),('Shade Prime','shade_prime_set'),('Huras Kubrow',None),('Sahasa Kubrow',None),('Helios Prime','helios_prime_set'),('Taxon',None),('Helminth Charger',None)]
for nm,s in COMP:
    if s and 'imprint' not in s:
        p=price(s,None); row(Category='Companion',Item=nm,**{'Slot':'Companion','Variant':'Prime sentinel','Quantity':1,'Acquisition Method':'Player trade (set)','Tradeable?':'Yes','Priority':'Core','Catalyst?':'Reactor','Counted in Player-Trade Total?':'Yes','Source/Reasoning':'v3 companion list','Notes':'Sentinel weapon not specified in v3 - OPEN'},**mk(p))
    else:
        row(Category='Companion',Item=nm,**{'Slot':'Companion','Variant':'Beast/Sentinel','Quantity':1,'Acquisition Method':'Breed / incubate / vendor (imprint optional trade)' if s else 'Farm / vendor / incubate','Tradeable?':'Imprint only' if s else 'No','Priority':'Core','Status':'FARMABLE / ACCOUNT-BOUND','Counted in Player-Trade Total?':'No','Market Slug':s,'Source/Reasoning':'v3 companion list'})
# ---------------- Arcanes
for s,i in sorted(items.items()):
    if 'arcane_enhancement' not in i['tags']: continue
    nm=i['i18n']['en']['name']; wa=arcbyn.get(nm.lower()) or {}
    info=item_info(s); mr=(info or {}).get('maxRank', wa.get('MaxRank'))
    p=price(s,'max'); d=mk(p)
    p0=price(s,0) if mr else {}
    copies=(mr+1)*(mr+2)//2 if mr else 1
    via=round(p0['realistic']*copies,1) if p0.get('realistic') else None
    real=d['Realistic Platinum']
    note=None
    if via is not None and (real is None or via<real):
        note=f'Cheaper via {copies}x R0 ({via}p realistic) than buying max rank'
    row(Category='Arcane',Item=nm,**{'Variant':wa.get('Type') or ','.join(x for x in i['tags'] if x not in ('arcane_enhancement',)),'Required Rank':mr,'Quantity':1,'Acquisition Method':'Player trade (max rank)','Tradeable?':'Yes',
        'R0 Realistic':p0.get('realistic'),'Max via R0 copies (Realistic)':via,
        'Counted in Player-Trade Total?':'Yes' if nm in REQ_ARC_V3+REQ_ARC_V4 else 'Collection (optional)','Priority':'Required (v3 build list)' if nm in REQ_ARC_V3 else ('Required (v4 weapon-arcane baseline)' if nm in REQ_ARC_V4 else 'Collection (optional)'),'Notes':note,
        'Source/Reasoning':'Arcanes share across items like mods (one max-rank copy covers every build).'},**d)
json.dump(proc,open('proc.json','w'))
print(len(proc), collections.Counter(r['Category'] for r in proc))
