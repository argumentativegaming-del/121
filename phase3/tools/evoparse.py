import re,glob,json
def clean(s):
    s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\[\[File:[^\]]+\]\]','',s)
    s=re.sub(r"\{\{(?:D|M|Stat|A|Weapon|WF|Resource|Faction|E)\|([^}|]+)[^}]*\}\}",r'\1',s)
    s=re.sub(r'\[\[(?:[^|\]]+\|)?([^\]]+)\]\]',r'\1',s); s=s.replace("'''",'')
    return s.strip()
out={}
for f in glob.glob('evo/*.txt'):
    n=f[4:-4].replace('_',' ')
    t=open(f).read()
    m=re.search(r'===\s*Evolutions\s*===(.*?)(\n==[^=]|\Z)',t,re.S)
    body=m.group(1) if m else t
    heads=[(mm.start(),'EVO'+mm.group(1)) for mm in re.finditer(r'EVO\s*(\d)',body)]
    tiers={}
    for mm in re.finditer(r"white-space: ?nowrap;[^|]*\|\s*'''(.+?)'''(.*?)(?=\n\|-|\n\|\})",body,re.S):
        tier=[h for p,h in heads if p<mm.start()]
        if not tier: continue
        eff=[clean(x) for x in re.findall(r'^\*\s*(.+)$',mm.group(2),re.M)]
        tiers.setdefault(tier[-1],[]).append({'perk':clean(mm.group(1)),'effect':'; '.join(eff)[:240]})
    pc=re.search(r'Cavalero for \{\{pc\|(\d+)\}\}',t)
    out[n]={'tiers':tiers,'cavalero_plat':int(pc.group(1)) if pc else None}
json.dump(out,open('evolutions.json','w'),indent=1)
for n,o in sorted(out.items()): print(f"{n:14s}",{k:len(v) for k,v in sorted(o['tiers'].items())},o['cavalero_plat'])
