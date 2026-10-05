import urllib.request, time, os, json
H={'User-Agent':'wf-procurement-research/1.0','Platform':'pc','Language':'en'}
def get(url,path):
    if os.path.exists(path): return
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30) as r: open(path,'wb').write(r.read())
            time.sleep(0.8); return
        except Exception as e: time.sleep(2**a)
    print('FAIL',url)
for s in ['innodem_blueprint','phenmor_blueprint','praedos_blueprint','felarx_blueprint','laetum_blueprint']:
    get(f'https://api.warframe.market/v2/item/{s}',f'cache/item/{s}.json')
    get(f'https://api.warframe.market/v2/orders/item/{s}',f'cache/orders/{s}.json')
    get(f'https://api.warframe.market/v1/items/{s}/statistics',f'cache/stats/{s}.json')
for w,t in [('kuva_hek','lich'),('kuva_nukor','lich'),('kuva_sobek','lich'),('kuva_bramma','lich'),('kuva_ogris','lich'),('kuva_twin_stubbas','lich'),('tenet_plinx','sister'),('tenet_diplos','sister'),('tenet_detron','sister'),('tenet_arca_plasmor','sister'),('tenet_cycron','sister'),('tenet_spirex','sister')]:
    get(f'https://api.warframe.market/v1/auctions/search?type={t}&weapon_url_name={w}&sort_by=price_asc',f'cache/auctions/{w}.json')
print('DONE')
