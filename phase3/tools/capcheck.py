"""Weapon capacity / Forma validator: max-rank drain, innate polarities, optimal Forma placement (exact)."""
import json, itertools, math
MODS=json.load(open('mods.json'))['Mods']
_W=json.load(open('weapons_all.json')); _W=_W.get('Weapons',_W)
def rh(x): return int(math.floor(x+0.5))
def drain(m): v=MODS[m]; return v['BaseDrain']+v['MaxRank']
def cost(m,slotpol):
    d=drain(m); p=MODS[m].get('Polarity')
    if not slotpol: return d
    if slotpol==p: return rh(d/2)
    return rh(d*1.25)
def capacity(w, rank40=False):
    return (40 if rank40 else 30)*2          # Orokin Catalyst (pre-installed on Kuva/Tenet)
def min_forma(w, mods, exilus=None, rank40=False):
    """Return (forma_needed, drain_after, capacity, detail) for the cheapest legal polarity layout."""
    cap=capacity(w,rank40); inn=list(_W[w].get('Polarities') or [])
    best=None
    slots=inn+[None]*(len(mods)-len(inn))
    for perm in set(itertools.permutations(range(len(mods)), len(inn))):
        # perm[i] = index of the mod placed in innate slot i
        layout=[None]*len(mods)
        for i,mi in enumerate(perm): layout[mi]=inn[i]
        base=[cost(m,layout[i]) for i,m in enumerate(mods)]
        sav=sorted((b-cost(m,MODS[m].get('Polarity')) for b,m in zip(base,mods)), reverse=True)
        tot=sum(base)
        if exilus: tot+=cost(exilus,_W[w].get('ExilusPolarity'))
        for k in range(len(mods)+1):
            t=tot-sum(sav[:k])
            if t<=cap:
                if best is None or k<best[0] or (k==best[0] and t<best[1]): best=(k,t)
                break
    return best[0], best[1], cap, f'innate {inn or "none"}; max-rank drain {sum(drain(m) for m in mods)+(drain(exilus) if exilus else 0)} unpolarized'
