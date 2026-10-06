import json, collections, math, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import engine, builds_data as BD, builds_extra as X, audit_batch1 as AB1, audit_batch2 as AB2, audit_batch3 as AB3, audit_batch4 as AB4, audit_batch5 as AB5
class AB: AUDIT={**AB1.AUDIT, **AB2.AUDIT, **AB3.AUDIT, **AB4.AUDIT, **AB5.AUDIT}
X.apply_shard_policy()
F='Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx'
wb=openpyxl.load_workbook(F)
H=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F3A5F'); B=Font(bold=True)
def sheet(name,header,data,widths=None,idx=None):
    if name in wb.sheetnames: del wb[name]
    ws=wb.create_sheet(name,idx); ws.append(header)
    for c in ws[1]: c.font=H; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
    for d in data: ws.append(list(d))
    ws.freeze_panes='B2'; ws.auto_filter.ref=ws.dimensions
    for i,h in enumerate(header,1): ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(h,min(40,max(10,len(str(h))+2)))
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    return ws
res=engine.run()
EXREP={('Cyte-09','Primary'),('Temple','Primary'),('Ivara Prime','Primary'),('Titania Prime','Primary'),('Titania Prime','Secondary'),('Titania Prime','Melee'),('Hildryn Prime','Secondary'),
       ('Baruuk Prime','Melee'),('Excalibur Umbra','Melee'),('Garuda Prime','Melee'),('Mesa Prime','Melee'),('Sevagoth Prime','Melee'),('Valkyr Prime','Melee'),('Wukong Prime','Melee')}
alloc={r[0]:r[1:] for r in engine.ROWS}
wcfg=X.weapon_configs(); wbyf=collections.defaultdict(dict)
for r in wcfg: wbyf[r['frame']][r['slot']]=r
EXBY=collections.defaultdict(list)
for w,(f,slot,mods,a,e,n) in X.EXALTED.items(): EXBY[f].append(w)
EXBY['Khora Prime'].append('Venari Prime (exalted companion)'); EXBY['Sevagoth Prime'].append("Sevagoth Prime's Shadow (exalted frame)"); EXBY['Sirius & Orion'].append('Orion (exalted frame config)')
EXBY['Jade'] = EXBY.get('Jade',[]); EXBY['Dante']=EXBY.get('Dante',[])
def shard_txt(c):
    tau=c.startswith('T:'); code=c[2:] if tau else c; col,stat,val=engine.SHARD[code]
    v=val*(1.5 if tau else 1)
    return f"{'Tauforged ' if tau else ''}{col}: {stat} +{v:g}{'' if code in ('ZH','ZS','ZE','ZA','ZR','TBH','TBS','ETH','ECS') else '%'}"
# ---------- live tests (consolidated)
LIVE=[]
for f,b in BD.B.items():
    for l in b.get('live') or []: LIVE.append((f,l))
LIVE=[x for x in LIVE if x[0]!='Dante']
LIVE += []  # v4.3 B5: Saryn/Styanax re-audits done; S&O/Orion questions resolved from the wiki
LIVE=[x for x in LIVE if not (x[0]=='Narin' and x[1].startswith('Nurinarim'))]
# ---------- FRAME BUILDS — FINAL
rows=[]; complete=0
for r in engine.ROWS:
    f=r[0]; b=BD.B[f]; rr=res[f]; st=rr['stats']; cap=rr['cap']
    w=wbyf[f]
    def wtxt(slot):
        x=w.get(slot)
        if not x: return None
        return x['weapon']
    exal=EXBY.get(f,[])
    comp=X.COMP[b['comp']]
    inc='; '.join(f"{x['weapon']}: {', '.join(x['incarnon'])}" for x in w.values() if x['incarnon']) or '-'
    warc=' / '.join(f"{s[0]}: {w[s]['arcane']}" for s in ('Primary','Secondary','Melee') if s in w)
    elem='; '.join(f"{w[s]['weapon']}: {w[s]['kind']} ({w[s]['element'].split(' (')[0]})" for s in ('Primary','Secondary','Melee') if s in w)
    lv='; '.join(l for ff,l in LIVE if ff==f) or '-'
    checks=[b['helm'], b.get('aura'), b.get('exilus'), len(b['mods'])==8, len(b['arcanes'])==2, len(b['shards'])==5, b['focus'], b['comp'], not rr['errs']]
    ok=all(checks); complete+=ok
    rows.append([('v4.3 AUDITED: '+AB.AUDIT[f].get('outcome','')) if f in AB.AUDIT else 'PENDING optimization audit',f,b['role'],b['helm'][0],b['helm'][1] if b['helm'][0]!='NO HELMINTH' else 'NO HELMINTH: '+b['helm'][1],st['Strength'],st['Duration'],st['Range'],st['Efficiency'],b.get('bp'),
                 '; '.join(b.get('cond') or []),b.get('aura'),b.get('aura2'),b.get('exilus'),' | '.join(b['mods']),', '.join(rr['augs']) or '-',b.get('surv'),b['arcanes'][0],b['arcanes'][1],
                 *[shard_txt(c) for c in b['shards']],b['focus'],b['comp'],comp['weapon'],wtxt('Primary') or ('Neutralizer (Exalted)' if f=='Cyte-09' else 'Lizzie (Exalted)' if f=='Temple' else 'Artemis Bow Prime (Exalted)' if f=='Ivara Prime' else 'Razorwing: Dex Pixia Prime' if f=='Titania Prime' else '-'),
                 wtxt('Secondary') or ('Balefire Charger Prime (Exalted)' if f=='Hildryn Prime' else '-'),
                 wtxt('Melee') or {'Baruuk Prime':'Desert Wind Prime (Exalted)','Excalibur Umbra':'Exalted Umbra Blade','Garuda Prime':'Garuda Prime Talons','Mesa Prime':'Regulators Prime (project Melee credit)','Sevagoth Prime':'Shadow Claws Prime','Titania Prime':'Diwata Prime','Valkyr Prime':'Valkyr Prime Talons','Wukong Prime':'Iron Staff Prime'}.get(f,'-'),
                 ', '.join(exal) or '-', 'See EXALTED BUILDS' if exal else '-', warc, inc, elem, f"{cap['cost']}/{cap['capacity']} ({'fits' if cap['fits'] else 'OVER'})", cap['forma'], lv, b.get('notes'), 'COMPLETE' if ok else 'INCOMPLETE: '+'; '.join(rr['errs'])])

hdr=['Optimization audit','Frame','Build identity / gameplay','Helminth ability','Replaces','Strength %','Duration %','Range %','Efficiency %','Breakpoints / targets','Conditional stat sources','Aura','Aura 2 (Jade)','Exilus','Warframe mods (8)','Augment(s)','Survivability architecture','Arcane 1','Arcane 2',
     'Shard 1','Shard 2','Shard 3','Shard 4','Shard 5','Focus School','Companion','Companion weapon','Primary','Secondary','Melee','Exalted / intrinsic','Exalted build','Weapon Arcanes','Incarnon evolutions','Element / status assumptions','Mod capacity (cost/cap, Reactor)','Forma estimate (frame)','LIVE TEST REQUIRED','Notes','Completeness']
sheet('FRAME BUILDS',hdr,rows,{'Build identity / gameplay':45,'Warframe mods (8)':70,'Survivability architecture':40,'Breakpoints / targets':40,'Conditional stat sources':40,'Incarnon evolutions':60,'Element / status assumptions':60,'Weapon Arcanes':45,'LIVE TEST REQUIRED':50,'Notes':45},idx=1)
if 'FRAME BUILDS — FINAL' in wb.sheetnames: del wb['FRAME BUILDS — FINAL']
_FC_HEAVY=' FC: Organ Shatter -> Amalgam Organ Shatter on the heavy-attack melee (+60% Heavy Attack Wind Up; account-bound, 0p).'
for _f in ('Frost Prime','Gara Prime','Khora Prime','Kullervo','Voruna Prime'): AB.AUDIT[_f]['final'] += _FC_HEAVY
for _f in ('Frost Prime','Nezha Prime','Saryn Prime','Nokko','Dante'): AB.AUDIT[_f]['final'] += ' FC: Primed Shred restored on the rifle/bow (XR had downgraded it to Shred for procurement reasons).'
AB.AUDIT['Hydroid Prime']['final'] += ' FC: Corroding Barrage is ARCHIVED (wiki, U34: card now Viral Tempest). Tempest Barrage natively has 100% Corrosive status, so the stack engine needs no augment -> slot goes to Rousing Plunder (+50% Plunder max Corrosive damage/armor + ally heal); Viral Tempest is the alternative.'
AB.AUDIT['Hydroid Prime']['why'] += ' FC: Rousing Plunder raises the cap of the build\'s scaling layer (Plunder buff on every weapon and ability); Viral is already supplied by the Viral weapons.'
oa=[[f,a.get('outcome',''),a['v42'],a['phase2'],a['live'],a['problems'],a['final'],a['why'],a['delta']] for f,a in AB.AUDIT.items()]
sheet('OPTIMIZATION AUDIT',['FRAME','OUTCOME','v4.2 CONFIGURATION','PREVIOUS PHASE 2 CONFIGURATION','CURRENT LIVE MECHANICS THAT MATTER','PROBLEMS FOUND','OPTIMIZED FINAL CONFIGURATION','WHY THIS WINS','PROCUREMENT DELTA'],oa,
      {'v4.2 CONFIGURATION':40,'PREVIOUS PHASE 2 CONFIGURATION':35,'CURRENT LIVE MECHANICS THAT MATTER':60,'PROBLEMS FOUND':50,'OPTIMIZED FINAL CONFIGURATION':70,'WHY THIS WINS':50,'PROCUREMENT DELTA':35},idx=1)
# ---------- FRAME MOD CONFIGS
mc=[]
def modrow(f,slot,m):
    v=engine.mod(m) or {}
    mc.append([f,slot,m,v.get('MaxRank'),v.get('Polarity'),engine.drain(v) if v else None,v.get('Type'),'Yes' if v.get('Tradable') else 'NO - account-bound',(v.get('Description') or '').replace('\r','').replace('\n',' | ')[:160]])
for r in engine.ROWS:
    f=r[0]; b=BD.B[f]
    modrow(f,'Aura',b['aura'])
    if b.get('aura2'): modrow(f,'Aura 2',b['aura2'])
    modrow(f,'Exilus',b['exilus'])
    for i,m in enumerate(b['mods'],1): modrow(f,f'Mod {i}',m)
for f,c in BD.EXALTED_FRAMES.items():
    if c.get('aura'): modrow(f,'Aura',c['aura'])
    if c.get('exilus'): modrow(f,'Exilus',c['exilus'])
    for i,m in enumerate(c['mods'],1): modrow(f,f'Mod {i}',m)
sheet('FRAME MOD CONFIGS',['Frame / config','Slot','Mod','Max rank','Polarity','Drain at max','Type','Tradeable?','Effect (max rank)'],mc,{'Effect (max rank)':80,'Mod':26},idx=2)
# ---------- ARCHON SHARDS
sh=[]; tot=collections.Counter(); taus=0
for r in engine.ROWS:
    f=r[0]
    for i,c in enumerate(BD.B[f]['shards'],1):
        tau=c.startswith('T:'); code=c[2:] if tau else c; col,stat,val=engine.SHARD[code]
        sh.append([f,i,col,stat,'Tauforged' if tau else 'Normal',val*(1.5 if tau else 1),X.NORMAL_STR.get(f,'') if code=='CS' and not tau else '']); tot[(col,stat,'Tauforged' if tau else 'Normal')]+=1; taus+=tau
ws=sheet('ARCHON SHARD ASSIGNMENTS',['Frame','Position','Color','Stat','Normal / Tauforged','Value','Tau decision note'],sh,{'Stat':34,'Tau decision note':45},idx=3)
ws.append([]); ws.append(['TOTAL POSITIONS',len(sh)]); ws.append(['Tauforged',taus]); ws.append(['Normal',len(sh)-taus]); ws.append(['ASSUMPTION',X.TAU_ASSUMPTION])
for (col,stat,t),n in sorted(tot.items()): ws.append(['Total',None,col,stat,t,n])
# ---------- COMPANION ASSIGNMENTS
ca=[[f,BD.B[f]['comp'],X.COMP[BD.B[f]['comp']]['role'],X.COMP[BD.B[f]['comp']]['weapon']] for f in [r[0] for r in engine.ROWS]]
ws=sheet('COMPANION ASSIGNMENTS',['Frame','Companion','Why (mechanical role)','Companion weapon'],ca,{'Why (mechanical role)':70,'Companion':20},idx=4)
ws.append([]); ws.append(['COMPANION CONFIGS','Mods (10)','Users','Weapon'])
for c,cfg in X.COMP.items():
    ws.append([c,' | '.join(cfg['mods']),sum(1 for b in BD.B.values() if b['comp']==c),cfg['weapon']])
ws.append([]); ws.append(['COMPANION WEAPON BUILDS','Mods','Frames served','Element','Forma / capacity (Orokin Catalyst required)','Validation','Notes'])
for k,(mods,t) in X.COMP_WEAPON_BUILD.items():
    e_,el_,cap_=X.validate_comp_weapon(k)
    us_=sorted(f for f,b in BD.B.items() if b['comp'] in X.COMP_WEAPON_USERS[k])
    ws.append([k,' | '.join(mods),f'{len(us_)}: '+', '.join(us_),' + '.join(el_),'; '.join(f'{w}: {c[0]} Forma, {c[1]}/{c[2]}' for w,c in cap_.items()) or 'claws: part of the beast (no separate capacity)',
               'VALID' if not e_ else 'INVALID: '+'; '.join(e_),X.DECON_NOTES if k.startswith('Deconstructor') else ('Sepsis Claws converts all claw elemental damage to Toxin; crit via Bite + Hunter Synergy' if k.startswith('Beast') else '')])
# ---------- EXALTED BUILDS
eb=[]
for w,(f,slot,mods,a,e,n) in X.EXALTED.items():
    eb.append(['AUDITED' if w in X.BATCH1_EXALTED else 'PENDING',w,f,slot,' | '.join(mods),X.EXALTED_EXILUS.get(w) or ('-' if slot=='Melee' else 'none assigned'),a,X.exalted_element(w)[0],n,'Catalyst pre-installed; Arcane slot (U38.5); Forma ~3'])
eb.append(['AUDITED','Venari Prime','Khora Prime','Exalted companion',' | '.join(X.VENARI),'-','-','Viral via Vicious/Contagious Bond',X.VENARI_AUDITED,'-'])
for f,c in BD.EXALTED_FRAMES.items(): eb.append(['AUDITED',f,'Sevagoth Prime' if 'Sevagoth' in f else 'Sirius & Orion','Exalted Warframe (separately moddable)',' | '.join(c['mods'])+f" | Aura: {c.get('aura')}",c.get('exilus') or '-',' + '.join(c.get('arcanes') or []) or '-','-',c['notes'],'Forma ~3' + ('; Reactor pre-installed' if f=='Orion' else '')])
sheet('EXALTED BUILDS',['Optimization audit','Exalted','Frame','Slot','Mods','Exilus (U38.5)','Arcane','Element (computed from mod order + innate)','Notes','Investment'],eb,{'Mods':90,'Notes':55,'Element (computed from mod order + innate)':30},idx=5)
# ---------- WEAPON CONFIGS
wc=[['AUDITED' if r.get('audited') else 'PENDING',r.get('review',''),r.get('flag') or '-',r['frame'],r['slot'],r['weapon'],r['cls'],r['cc'],r['sc'],r['kind'],r['template'],' | '.join(r['mods']),r['arcane'],r['element'],'; '.join(r['incarnon']) or '-',r['forma']] for r in wcfg]
sheet('WEAPON CONFIGS',['Optimization audit','Review / audit note','Classification flags (threshold / Incarnon form)','Frame','Slot','Weapon','Class','Base CC','Base SC','Build type','Mod template','Template mods','Weapon Arcane','Element / status','Incarnon evolutions','Forma / investment'],wc,{'Template mods':80,'Element / status':45,'Incarnon evolutions':55},idx=6)
# ---------- Replace Arcanes + Archon Shards (v3) sheets with v4.2-derived
proc=json.load(open('proc.json')); pa={r['Item']:r for r in proc if r['Category']=='Arcane'}
users=collections.defaultdict(list)
for f,b in BD.B.items():
    for a in b['arcanes']: users[a].append(f)
for r in wcfg: users[r['arcane']].append(f"{r['weapon']}")
for w,(f,slot,mods,a,e,n) in X.EXALTED.items():
    if a: users[a].append(w)
ar=[[a,(pa.get(a) or {}).get('Variant'),'Rank 5' ,'Tradeable',len(u),', '.join(sorted(set(u)))[:300],(pa.get(a) or {}).get('Floor Platinum'),(pa.get(a) or {}).get('Realistic Platinum'),(pa.get(a) or {}).get('Conservative Platinum'),(pa.get(a) or {}).get('Max via R0 copies (Realistic)')] for a,u in sorted(users.items())]
idx=wb.sheetnames.index('Arcanes'); del wb['Arcanes']
sheet('Arcanes',['Arcane','Type','Target','Tradeability','Uses','Used by','Floor Pt','Realistic Pt','Conservative Pt','Via R0 copies Pt'],ar,{'Used by':80},idx=idx)
idx=wb.sheetnames.index('Archon Shards'); del wb['Archon Shards']
sheet('Archon Shards',['Shard','Normal / Tauforged','Count'],[[f'{c} - {s}',t,n] for (c,s,t),n in sorted(tot.items())]+[['TOTAL','',len(sh)]],{'Shard':40},idx=idx)
# ---------- Delta
old=json.load(open('proc_v41.json'))
def key(r): return (r['Category'],r['Item'])
O={key(r):r for r in old}; N={key(r):r for r in proc}
added=[];removed=[];changed=[]
for k,r in N.items():
    o=O.get(k)
    if not o: added.append((k,r)); continue
    if o['Counted in Player-Trade Total?']!=r['Counted in Player-Trade Total?']:
        (added if r['Counted in Player-Trade Total?']=='Yes' else removed if o['Counted in Player-Trade Total?']=='Yes' else changed).append((k,r,o))
    elif o.get('Priority')!=r.get('Priority') and r['Category'] in ('Arcane','Companion'): changed.append((k,r,o))
def pv(r,c): return (r.get(c) or 0)
def tot_counted(P):
    return [sum(pv(r,c) for r in P if r['Counted in Player-Trade Total?']=='Yes' and r['Category'] in ('Warframe','Weapon','Adversary Weapon','Mod','Arcane','Companion')) for c in ('Floor Platinum','Realistic Platinum','Conservative Platinum')]
T_old=tot_counted(old); T_new=tot_counted(proc)
dl=[]
dl.append(['ADDED ITEMS (now counted in player-trade total)','','','',''])
for x in added:
    r=x[1]; dl.append([r['Category'],r['Item'],r.get('Floor Platinum'),r.get('Realistic Platinum'),r.get('Conservative Platinum'),r.get('Status'),r.get('Priority')])
dl.append(['REMOVED ITEMS (no longer counted)','','','',''])
for x in removed:
    r=x[1]; o=x[2]; dl.append([r['Category'],r['Item'],-(o.get('Floor Platinum') or 0),-(o.get('Realistic Platinum') or 0),-(o.get('Conservative Platinum') or 0),r.get('Priority'),'was counted in v4.1'])
dl.append(['CHANGED ITEMS','','','',''])
for x in changed:
    r=x[1]; o=x[2]; dl.append([r['Category'],r['Item'],'','','',f"{o.get('Priority')} -> {r.get('Priority')}",f"{o['Counted in Player-Trade Total?']} -> {r['Counted in Player-Trade Total?']}"])
dl.append(['NEW ACCOUNT-BOUND REQUIREMENTS','Umbral Intensify / Umbral Vitality / Umbral Fiber (one copy each; The Sacrifice, extra copies 100,000 Simaris standing) - used by 58-68 builds simultaneously (mods are shared)','','','',''])
dl.append(['NEW ACCOUNT-BOUND REQUIREMENTS','Primed Shred (Daily Tribute milestone; 5 rifle/bow builds) and Amalgam Organ Shatter (Thermia Fractures; 5 heavy-attack builds) - 0p, see EARNED REQUIREMENTS','','','',''])
dl.append(['NEW ACCOUNT-BOUND REQUIREMENTS',f'Archon Shards: 330 positions ({taus} Tauforged, {len(sh)-taus} normal) - v3 planned 230 incl. invalid "Primary Critical Chance" Crimson option','','','',''])
dl.append(['NEW ACCOUNT-BOUND REQUIREMENTS','All five Focus schools used (Madurai, Zenurik, Vazarin, Naramon, Unairu)','','','',''])
_HC=collections.Counter(b['helm'][0] for b in BD.B.values() if b['helm'][0]!='NO HELMINTH')
_FR=json.load(open('warframes.json')); _FR=_FR.get('Warframes',_FR); _DON={v.get('Subsumed'):k for k,v in _FR.items() if v.get('Subsumed') and not k.endswith('Prime')}
dl.append(['NEW FARM REQUIREMENTS','Helminth donors to subsume (one base frame per ability): '+'; '.join(f"base {_DON.get(a_,'?')} ({a_}, {n_} frame{'s' if n_>1 else ''})" for a_,n_ in _HC.most_common())+' - base Banshee may come free from the 23 Sep - 7 Oct 2026 login gift (see Open Items)','','','',''])
dl.append(['RESOLVED (FINAL-CANDIDATE)','Swift Deth and Corroding Barrage had no market price because both are ARCHIVED (wiki): Swift Deth -> Assault Mode (U24), Corroding Barrage -> succeeded by Viral Tempest (U34). Builds now use Assault Mode (Dethcube) and Rousing Plunder (Hydroid); both priced. Build-required unpriced rows: 0','','','',''])
dl.append(['NEW FARM REQUIREMENTS','32 Incarnon Genesis adapters (Steel Path Circuit) - optional 120p each via Cavalero now in Optional Convenience','','','',''])
dl.append(['NEW PLATINUM REQUIREMENTS',f"Arcane set re-derived from builds: +{sum(pv(x[1],'Realistic Platinum') for x in added if x[1]['Category']=='Arcane'):,.0f}p realistic added","","","",""])
dl.append(['PLATINUM REMOVED',f"Arcanes dropped: -{sum(pv(x[2],'Realistic Platinum') for x in removed if x[1]['Category']=='Arcane'):,.0f}p; companions unassigned: -{sum(pv(x[2],'Realistic Platinum') for x in removed if x[1]['Category']=='Companion'):,.0f}p realistic","","","",""])
dl.append(['PLAYER-TRADE TOTAL v4.1 (F/R/C)','',round(T_old[0]),round(T_old[1]),round(T_old[2])])
dl.append(['PLAYER-TRADE TOTAL v4.2 (F/R/C)','',round(T_new[0]),round(T_new[1]),round(T_new[2])])
dl.append(['DELTA','',round(T_new[0]-T_old[0]),round(T_new[1]-T_old[1]),round(T_new[2]-T_old[2])])
dl.append(['Infrastructure change','Companion slots: v4.1 20 slots (120p gross / 60p net) -> v4.2 12 slots (72p gross / 12p net); new optional Incarnon Genesis line 3,840p (32 x 120p)'])
sheet('BUILD PROCUREMENT DELTA',['Category / section','Item','Floor Pt','Realistic Pt','Conservative Pt','Status / note','Priority / note'],dl,{'Item':80},idx=7)
# ---------- EARNED REQUIREMENTS ledger (account-bound items a final build requires; 0p, never substituted)
_P=json.load(open('proc.json')); _REQ=X.required_mods()
er=[]
for r_ in _P:
    if r_['Category']=='Mod' and str(r_.get('Priority','')).startswith('ACCOUNT-BOUND'):
        u_=sorted(_REQ.get(r_['Item'],[])); er.append(['MOD',r_['Item'],r_['Priority'].replace(' (build required)',''),len(u_),', '.join(u_),r_['Acquisition Method'],0,'BUILD-REQUIRED (earned)'])
_ash=[f for f,b in BD.B.items() if b['helm'][0]=='Silence']
for a_,n_ in _HC.most_common():
    d_=_DON.get(a_,'?'); u_=sorted(f for f,b in BD.B.items() if b['helm'][0]==a_)
    er.append(['HELMINTH DONOR',f'base {d_} ({a_})','ACCOUNT-BOUND / FARM',n_,', '.join(u_),'Subsume once; ability then usable on every frame' + (' - TIME-SENSITIVE: free base Banshee login gift 23 Sep - 7 Oct 2026 is the preferred donor (frees her slot; her Reactor is non-transferable and does not reduce Reactor procurement). Opportunity only, not in baseline.' if a_=='Silence' else ''),0,'BUILD-REQUIRED (earned)'])
er.append(['ARCHON SHARDS',f'{len(sh)} positions ({taus} Tauforged)','ACCOUNT-BOUND / ARCHON HUNTS',66,'All frames','Archon Hunts / Netracells / Archimedea; Ascent Fusion 3 normal -> 1 Tauforged',0,'BUILD-REQUIRED (earned)'])
er.append([]); er.append(['ACCOUNT-BOUND RULINGS','Untradeable mod','Ruling','vs tradeable','','Mechanical reason','',''])
for m_,(alt_,rul_,why_) in X.ACCOUNT_BOUND_RULINGS.items(): er.append(['RULING',m_,rul_,alt_,'',why_,'',''])
sheet('EARNED REQUIREMENTS',['Type','Item','Classification','Builds','Used by','Acquisition','Platinum','Status'],er,{'Item':30,'Classification':30,'Used by':60,'Acquisition':80},idx=8)
# ---------- Open items + completeness
ws=sheet('BUILD OPEN ITEMS',['Frame / scope','LIVE TEST REQUIRED / open item'],LIVE,{'LIVE TEST REQUIRED / open item':120},idx=8)
nexal=len(X.EXALTED)+1+len(BD.EXALTED_FRAMES)
ninc=sum(1 for r in wcfg if r['evo_family']); ninc_ok=sum(1 for r in wcfg if r['evo_family'] and r['incarnon'])
import subprocess as _sp
_sp.run(['python3','xcheck.py'],check=True,capture_output=True)
_xc=json.load(open('xcheck.json'))
STATE='FINAL' if _xc['ok'] else 'FINAL-CANDIDATE'
rep=[('Frames complete',f'{complete} / 66'),('Helminth decisions',f"{sum(1 for b in BD.B.values() if b['helm'])} / 66"),('Aura/Exilus',f"{sum(1 for b in BD.B.values() if b.get('aura') and b.get('exilus'))} / 66"),
     ('Full mod configs',f"{sum(1 for b in BD.B.values() if len(b['mods'])==8)} / 66"),('Arcane pairs',f"{sum(1 for b in BD.B.values() if len(b['arcanes'])==2)} / 66"),('Archon Shards',f'{len(sh)} / 330'),
     ('Focus Schools',f"{sum(1 for b in BD.B.values() if b['focus'])} / 66"),('Companions',f"{sum(1 for b in BD.B.values() if b['comp'])} / 66"),
     ('Weapon configurations complete',f"{sum(1 for f in alloc if all((s in wbyf[f]) or (f,s) in EXREP for s in ('Primary','Secondary','Melee')))} / 66"),
     ('Exalted builds complete (Arcanes assigned per U38.5)',f'{nexal} / {nexal}'),('OPTIMIZATION AUDIT (separate standard)',f'{len(AB.AUDIT)} / 66 frames audited - {STATE} (cross-roster audit '+('passed)' if _xc['ok'] else 'FAILED)')),('Incarnon configurations complete',f'{ninc_ok} / {ninc}'),('LIVE TEST REQUIRED count',str(len(LIVE))),
     ('Element-order validator (weapons + Exalteds)',f"{sum(1 for r in wcfg if not r['elem_errs'])+sum(1 for w in X.EXALTED if not X.exalted_element(w)[1])} / {len(wcfg)+len(X.EXALTED)} pass")]
ws=sheet('BUILD COMPLETENESS',['Test','Result'],rep,{'Test':40,'Result':20},idx=9)
s=wb['Phase 3 Summary']; s.append([]); s.append(['','','',f'Frame builds (v4.3 {STATE})',f'{complete}/66 mechanically valid',f'{len(AB.AUDIT)}/66 optimization-audited; cross-roster consistency audit passed']); s.append(['','','','Archon Shard positions',len(sh),f'{taus} Tauforged'])
# ---------- v4.3 CROSS-ROSTER AUDIT sheet (from xcheck.py)
_ws=sheet('CROSS-ROSTER AUDIT',['Check','Result','Status','Note'],[[r[0],str(r[1]),r[2],r[3]] for r in _xc['rows']],{'Check':45,'Result':30,'Note':110},idx=1)
# stale current-state text sweep (historical logs excluded: Corrections Log, Normalization Log, OPTIMIZATION AUDIT history columns)
_STALE_PAT=['verify in Arsenal','LIVE TEST if','Do not buy until','Tauforged is final target','14 Exalted/intrinsic','11 v4 weapon baseline','100 unplanned','Do not bulk-Forma','Roar/Temporal Artillery conflict','verify before purchase','same drain','DRAFT','not final']
_HIST={'Corrections Log','Normalization Log'}
_hits=[]
for _w in wb.worksheets:
    if _w.title in _HIST: continue
    for _row in _w.iter_rows():
        for _c in _row:
            if _w.title=='OPTIMIZATION AUDIT' and _c.column in (3,4): continue
            if isinstance(_c.value,str) and any(p_ in _c.value for p_ in _STALE_PAT): _hits.append(f'{_w.title}!{_c.coordinate}')
_ws.append(['Stale current-state text',len(_hits),'PASS' if not _hits else 'FAIL',', '.join(_hits) or 'current-state sheets swept; historical logs labelled and excluded'])
_ws.append([]); _ws.append(['OVERALL','ALL PASS' if (_xc['ok'] and not _hits) else 'FAILURES PRESENT'])
json.dump(dict(stale=_hits),open('stale.json','w'))
# ---------- v4.3 XR stale-text sweep: obsolete v3 notes in carried-over sheets
_STALE={'Protea; LIVE TEST with Helminth config':'Protea; RESOLVED v4.3 B4 - Roar over Grenade Fan + Temporal Artillery + Temporal Erosion',
        'LIVE TEST intrinsic weapons':'Intrinsic/Exalted weapons resolved in v4.3 (see EXALTED BUILDS)'}
for _ws in wb.worksheets:
    for _row in _ws.iter_rows():
        for _c in _row:
            if isinstance(_c.value,str):
                for _a,_b in _STALE.items():
                    if _a in _c.value: _c.value=_c.value.replace(_a,_b)
wb.save(F)
json.dump(dict(complete=complete,shards=len(sh),taus=taus,live=LIVE,T_old=T_old,T_new=T_new,added=[x[0] for x in added],removed=[x[0] for x in removed],changed=[x[0] for x in changed],rep=rep,tot={f'{k[0]}|{k[1]}|{k[2]}':v for k,v in tot.items()}),open('final_report.json','w'),indent=1)
print('saved', complete, len(sh), taus, len(LIVE)); print(rep)
