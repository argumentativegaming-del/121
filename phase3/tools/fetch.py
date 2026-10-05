import json, os, time, urllib.request, sys
it=json.load(open('wfm_items.json'))['data']
want=[]
excl={'relic','scene','fish','skin','emote','imprint','ayatan_sculpture','gem','key','consumable','riven_mod','veiled_riven','tome','misc','k_drive'}
for i in it:
    t=set(i['tags'])
    if t & excl: continue
    if 'component' in t or 'blueprint' in t: continue
    if t & {'mod','arcane_enhancement','set','weapon','warframe','sentinel','kubrow','kavat','hound','moa','companion','archwing','necramech','pet','lens'}:
        want.append(i['slug'])
print(len(want), flush=True)
def get(url, path):
    if os.path.exists(path): return
    for a in range(6):
        try:
            req=urllib.request.Request(url, headers={'User-Agent':'wf-procurement-research/1.0','Platform':'pc','Language':'en'})
            with urllib.request.urlopen(req, timeout=30) as r: data=r.read()
            open(path,'wb').write(data); time.sleep(0.36); return
        except Exception as e:
            code=getattr(e,'code',None)
            if code==404: open(path,'w').write('{"error":404}'); return
            time.sleep(2**a)
    print('FAIL',url,flush=True)
for n,s in enumerate(want):
    get(f'https://api.warframe.market/v2/item/{s}', f'cache/item/{s}.json')
    get(f'https://api.warframe.market/v2/orders/item/{s}', f'cache/orders/{s}.json')
    get(f'https://api.warframe.market/v1/items/{s}/statistics', f'cache/stats/{s}.json')
    if n%100==0: print(n, time.strftime('%H:%M:%S'), flush=True)
print('DONE', flush=True)
