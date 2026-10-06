import json, os, math, statistics, datetime
NOW=datetime.datetime(2026,10,5,3,0,tzinfo=datetime.timezone.utc)   # snapshot time of the v4.3 pull; refresh.py overrides NOW and CACHE
CACHE='cache'
def load(kind,slug):
    p=os.path.join(CACHE,kind,f'{slug}.json')
    if not os.path.exists(p): return None
    try: return json.load(open(p))
    except Exception: return None
def days_since(ts):
    try: return (NOW-datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))).total_seconds()/86400
    except Exception: return 999
def item_info(slug):
    d=load('item',slug)
    return (d or {}).get('data') or {}
def price(slug, rank='max'):
    """rank: 'max' -> item maxRank if it has one; None -> ignore rank; int -> that rank"""
    info=item_info(slug)
    o=load('orders',slug)
    if o is None or not info: return {'status':'NOT FETCHED'}
    mr=info.get('maxRank')
    R = mr if rank=='max' else rank
    orders=o.get('data') or []
    def rank_ok(x):
        if R is None: return True
        return x.get('rank',0)==R
    sells=[x for x in orders if x['type']=='sell' and x.get('visible',True) and rank_ok(x) and x['user'].get('platform','pc')=='pc']
    buys=[x for x in orders if x['type']=='buy' and x.get('visible',True) and rank_ok(x)]
    online=[x for x in sells if x['user'].get('status') in ('ingame','online')]
    recent=[x for x in sells if x['user'].get('status') not in ('ingame','online') and days_since(x['user'].get('lastSeen',''))<=3]
    cred=sorted(online,key=lambda x:x['platinum'])
    basis='online sellers'
    if len(cred)<3:
        cred=sorted(online+recent,key=lambda x:x['platinum']); basis='online + seen<=3d'
    prices=[x['platinum'] for x in cred]
    # drop absurd outliers relative to cheapest-5 median (troll listings)
    st=load('stats',slug) or {}
    st=(st.get('payload') or {}).get('statistics_closed') or {}
    def rk(e):
        if R is None: return True
        return e.get('mod_rank',0)==R
    d90=[e for e in st.get('90days',[]) if rk(e)]
    h48=[e for e in st.get('48hours',[]) if rk(e)]
    vol90=sum(e['volume'] for e in d90); vol48=sum(e['volume'] for e in h48)
    def wmed(es,key):
        pts=sorted((e[key],e['volume']) for e in es if e.get(key) is not None)
        tot=sum(v for _,v in pts)
        if not tot: return None
        acc=0
        for p,v in pts:
            acc+=v
            if acc>=tot/2: return p
    med90=wmed(d90,'median'); 
    d30=[e for e in d90 if days_since(e['datetime'])<=30]
    med30=wmed(d30,'median')
    wa90=round(sum(e['wa_price']*e['volume'] for e in d90)/vol90,1) if vol90 else None
    res={'slug':slug,'name':info.get('i18n',{}).get('en',{}).get('name',slug),'rank':R,'maxRank':mr,
         'sellers_online':len(online),'sellers_credible':len(prices),'basis':basis,
         'median90':med90,'median30':med30,'wa90':wa90,'vol90':vol90,'vol48h':vol48,
         'best_buy':max([x['platinum'] for x in buys if x['user'].get('status') in ('ingame','online')],default=None),
         'tradable':info.get('tradable',True)}
    if not prices:
        # fall back to stats only if there is trade history
        res['status']='NO CREDIBLE SELL ORDERS'+(' (stats only)' if med30 or med90 else ' - MARKET DATA UNAVAILABLE')
        ref=med30 or med90
        if ref:
            res.update(floor=None,realistic=ref,conservative=math.ceil(ref*1.25))
        return res
    floor=prices[0]
    top=prices[:5]
    # realistic: median of the cheapest 3-5 credible sellers
    realistic=statistics.median(top) if len(top)>=3 else statistics.mean(top)
    # conservative: higher of realistic, 5th-cheapest seller and 30d traded median, each capped at 2x realistic
    # (thin books often have troll listings), plus a 10% liquidity/convenience allowance
    # thin books: asks far above where the item actually trades are not representative.
    # Bound Realistic by max(Floor, 1.5 x traded median [30d, else 90d]) when trade history exists.
    ref_med=med30 or med90
    if ref_med and vol90>=1:
        realistic=min(realistic, max(floor, 1.5*ref_med))
    p5=prices[min(4,len(prices)-1)]
    cap=2*realistic
    ref=max(realistic,min(p5,cap),min(med30 or 0,cap))
    cons=math.ceil(ref*1.10)
    res.update(floor=floor,realistic=round(realistic,1),conservative=cons,spread=(floor-res['best_buy']) if res['best_buy'] else None,
               status='OK' if len(prices)>=3 else 'THIN')
    return res
if __name__=='__main__':
    import sys
    for s in sys.argv[1:]: print(json.dumps(price(s)))
