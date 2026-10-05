import json, re
import meta
W=json.load(open('weapons_all.json'))
FR=json.load(open('warframes.json'))['Warframes']
proc=json.load(open('proc.json'))
rows=[l.strip().split('|') for l in open('alloc_new.txt') if l.strip()]
alloc={}
for r in rows:
    for sl,w in zip(['Primary','Secondary','Melee'],r[1:]): alloc.setdefault(w.replace(' (Primary)','').replace(' (Melee)',''),[]).append(f'{r[0]} {sl}')
byitem={}
for r in proc: byitem.setdefault(r['Item'],[]).append(r)
def vkey(v): return [int(x) for x in re.findall(r'\d+',str(v))]
REL={}
for k,v in FR.items():
    iv=str(v.get('Introduced'))
    if vkey(iv) and vkey(iv)[0]>=33 and k not in ('Stalker',"Sevagoth Prime's Shadow",'Sirius','Orion'): REL.setdefault(iv,[]).append(k)
def release_of(iv):
    fr=REL.get(str(iv),[])
    maj=str(iv).split('.')[0]
    return f"U{iv}" + (f" ({', '.join(fr)})" if fr else '')
items=[]
for k,v in W.items():
    iv=str(v.get('Introduced'))
    if not vkey(iv) or vkey(iv)[0]<33: continue
    items.append((k,v))
for k in ['Larkspur Prime']: items.append((k,W[k]))
extra=[('Grasp of Lohk','Xaku Prime','Ability weapon'),("Ulfrun's Descent",'Voruna Prime','Ability form'),('Nurinarim','Narin','Ability (Update 44)'),('Nautilus Prime',None,'Companion (U36.1, Sevagoth Prime Access)')]
out=[]
def assoc(k,v):
    base=k.replace(' (Primary)','').replace(' (Melee)','')
    if base in meta.SIG: return 'Signature - '+meta.SIG[base][0]
    if v.get('Class')=='Exalted Weapon': return 'Exalted - '+', '.join(v.get('Users') or [])
    t=v.get('Traits') or []
    if any('Coda' in x for x in t): return 'Technocyte Coda variant'
    if v.get('Slot')=='Beast': return 'Beast companion natural weapon'
    if v.get('Slot')=='Robotic': return 'Sentinel weapon'
    if 'Kuva Lich' in t or 'Tenet' in t: return 'Adversary variant'
    if 'Scaldra' in t: return 'Scaldra (1999) weapon'
    if 'Incarnon' in t or k=='Thalys': return 'Incarnon weapon'
    fr=REL.get(str(v.get('Introduced')),[])
    if 'Prime' in k and any(f.endswith('Prime') for f in fr): return 'Prime Access co-release: '+', '.join(f for f in fr if f.endswith('Prime'))
    return 'No frame association'
for k,v in sorted(items,key=lambda kv:(vkey(kv[1].get('Introduced')),kv[0])):
    base=k.replace(' (Primary)','').replace(' (Melee)','')
    a=assoc(k,v)
    rs=byitem.get(base) or byitem.get(k) or []
    al=alloc.get(k) or alloc.get(base) or []
    present='YES' if rs or al else 'NO'
    assign='; '.join(al) or '; '.join(f"{r['Assigned Frame(s)']} ({r['Slot']})" for r in rs if r['Assigned Frame(s)']) or '-'
    prow='; '.join(sorted({f"{r['Category']}: {r['Status']}" + (f" R={r['Realistic Platinum']}p" if r['Realistic Platinum'] else '') for r in rs})) or 'NO'
    if k.endswith('(Atmosphere)'):
        present='YES (mode)'; action=f"None - atmospheric mode of {k.replace(' (Atmosphere)','')} (same item)"
    elif k=='Thornbak': action='None for allocation. NOTE: The Teacher quest reward with its own free slot + Catalyst; that free slot (counted in the 23) stays occupied unless Thornbak is sold'
    elif present=='YES': action='None' if not k.startswith('Vinquibus (Melee)') else 'None (shared item with Vinquibus Primary)'
    elif a.startswith('Technocyte Coda'):
        b=k.replace('Dual Coda ','').replace('Coda ','')
        action=f"None - doctrine: no automatic Coda substitution (base {b} {'allocated to '+'; '.join(alloc[b]) if b in alloc else 'not allocated'})"
    elif a=='Beast companion natural weapon': action='None - built into beast companion, no slot/procurement'
    elif a=='Sentinel weapon': action='None - bundled with Prime sentinel (not in v3 list)' if k not in byitem else 'None'
    elif a=='Adversary variant':
        b=k.replace('Kuva ','').replace('Tenet ','')
        action=f"Optional upgrade only ({b} family: {'; '.join(alloc.get(b,[]) or alloc.get(b+' Vandal',[])) or 'not allocated'})"
    elif a.startswith('Prime Access co-release'):
        b=k.replace(' Prime','')
        action=f"None - no signature claim; base {b} {'allocated to '+'; '.join(alloc[b]) if b in alloc else 'not allocated'}" + (' -> consider Prime variant' if b in alloc else '')
    elif a=='Incarnon weapon': action='Unallocated Incarnon option (not required)'
    elif a.startswith('Signature'): action='REVIEW - signature not represented'
    elif a.startswith('Exalted') and any(u+' Prime' in [r[0] for r in rows] for u in (v.get('Users') or [])): action='None - roster uses the Prime frame; Prime version represented'
    elif a.startswith('Exalted'): action='REVIEW - Exalted not represented'
    else: action='Not required (no frame association; MR/collection only)'
    out.append([k,release_of(v.get('Introduced')),v.get('Slot'),v.get('Class'),a,present,assign,prow,action])
for k,f,typ in extra:
    rs=byitem.get(k,[])
    out.append([k,'-',typ,typ,('Intrinsic - '+f) if f else 'Companion',('YES' if rs else 'NO'),'; '.join(f"{r['Assigned Frame(s)']} ({r['Slot']})" for r in rs) or '-','; '.join(sorted({r['Category']+': '+str(r['Status']) for r in rs})) or 'NO','None' if rs else 'REVIEW'])
json.dump(out,open('recon.json','w'))
import collections
print(len(out), collections.Counter(r[5] for r in out))
for r in out:
    if r[8].startswith('REVIEW') or ('Signature' in r[4] or 'Exalted' in r[4]): print(' | '.join(str(x) for x in [r[0],r[1],r[4],r[5],r[6],r[7][:60],r[8]]))
