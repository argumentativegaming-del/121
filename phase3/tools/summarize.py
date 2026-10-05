import json, math
p=json.load(open('proc.json'))
def S(cat,flag,col): return sum((r[col] or 0) for r in p if r['Category']==cat and r['Counted in Player-Trade Total?']==flag)
C=('Floor Platinum','Realistic Platinum','Conservative Platinum')
out={}
for lab,cat in [('Frames','Warframe'),('Weapons','Weapon'),('Adversary','Adversary Weapon'),('Mods','Mod'),('Arcanes(req)','Arcane'),('Companions','Companion')]:
    out[lab]=[S(cat,'Yes',c) for c in C]
    n=sum(1 for r in p if r['Category']==cat and r['Counted in Player-Trade Total?']=='Yes')
    nf=sum(1 for r in p if r['Category']==cat and r['Counted in Player-Trade Total?']=='Yes' and r['Floor Platinum'] is None)
    nd=sum(1 for r in p if r['Category']==cat and 'UNAVAILABLE' in str(r['Status']))
    nnf=sum(1 for r in p if r['Category']==cat and r['Status']=='NOT FETCHED')
    print(f"{lab:12s} n={n:4d} nofloor={nf:3d} nodata={nd:3d} notfetched={nnf:4d} F={out[lab][0]:9,.0f} R={out[lab][1]:9,.0f} C={out[lab][2]:9,.0f}")
T=[sum(v[i] for v in out.values()) for i in range(3)]
print('PLAYER TRADE',[f'{x:,.0f}' for x in T])
for lab,cat,flag in [('PvP mods','Mod','PvP subtotal'),('Arcane collection rest','Arcane','Collection (optional)'),('Archguns','Archgun','Optional')]:
    print(lab,[f'{S(cat,flag,c):,.0f}' for c in C])
ws=sum(1 for r in p if r['Category'] in ('Weapon','Adversary Weapon') and r['Quantity']==1)
cat=sum(1 for r in p if r['Category']=='Weapon' and r['Quantity']==1)
fg=66*20+math.ceil(ws/2)*12+math.ceil(20/2)*12; fn=61*20+math.ceil((ws-23)/2)*12+math.ceil(10/2)*12
oc=65*20+cat*20
print('slots',ws,'cat',cat,'FI gross',fg,'net',fn,'opt',oc)
u=1000/23000
for lab,add in [('net',fn),('gross',fg),('gross+pot',fg+oc)]:
    print(lab,[f'{x+add:,.0f}p ${(x+add)*u:,.0f} ({(x+add)/23000:.2f}x)' for x in T])
print('mods R0',sum((r['R0 Realistic'] or 0) for r in p if r['Category']=='Mod' and r['Counted in Player-Trade Total?']=='Yes'),
 'endo',sum((r['Endo to Max'] or 0) for r in p if r['Category']=='Mod' and r['Counted in Player-Trade Total?']=='Yes'))
