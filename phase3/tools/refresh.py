#!/usr/bin/env python3
"""Phase 3 v4.3 FINAL - standing PRICE MAINTENANCE.

Refreshes Warframe.Market prices and economic totals ONLY. The build model (frames, Helminth, weapons,
build mods/Arcanes, shards, companions, Incarnons, infrastructure) is frozen: the script edits nothing
but price cells and refuses to save if any other cell differs.

  python3 refresh.py --mode light            # weekly
  python3 refresh.py --mode full             # monthly
  python3 refresh.py --mode light --dry-run --out /tmp/x.xlsx   # test without touching the workbook

Fetching is resumable: responses are cached under --cache (default $TMPDIR/wfm_refresh_<date>_<mode>),
so an interrupted run can simply be restarted.
"""
import argparse, json, os, sys, time, math, statistics, datetime, re, urllib.request, urllib.error
import openpyxl
from openpyxl.workbook.properties import CalcProperties

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pricer

WB_PATH = os.path.join(ROOT, 'Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx')
LOG_PATH = os.path.join(ROOT, 'market_refresh_log.json')
REPORT_DIR = os.path.join(ROOT, 'refresh_reports')
CATALOG = os.path.join(HERE, 'wfm_catalog_v43.json')
API = 'https://api.warframe.market'
HDR = {'User-Agent': 'wf-procurement-research/1.0', 'Platform': 'pc', 'Language': 'en', 'Crossplay': 'true'}

PRICED_CATS = {'Warframe', 'Weapon', 'Adversary Weapon', 'Mod', 'Arcane', 'Companion', 'Archgun', 'Signature Extra'}
TRADE_CATS = ('Warframe', 'Weapon', 'Adversary Weapon', 'Mod', 'Arcane', 'Companion')      # = Economic Model section 1
PRICED_FLAGS = {'Yes', 'Optional', 'Collection (optional)', 'PvP subtotal'}
NEVER_QUERY = ('ACCOUNT-BOUND', 'FARMABLE', 'INCLUDED WITH', 'COVERED BY', 'UPCOMING', 'DAILY TRIBUTE')
# Only these Procurement Master columns may change during price maintenance
PRICE_COLS = ['Floor Platinum', 'Realistic Platinum', 'Conservative Platinum', 'Market Timestamp', 'Status', 'Credible Sellers',
              'Online Sellers', 'Recent Median (30d)', '90d Median', '90d Weighted Avg', '90d Volume', '48h Volume', 'Best Online Buy',
              'Buy/Sell Spread', 'R0 Realistic', 'Max via R0 copies (Realistic)']
# Mirror sheets that repeat Procurement Master prices: sheet -> (name column, category, {mirror column: PM column})
MIRRORS = {
    'Companions': (1, 'Companion', {5: 'Floor Platinum', 6: 'Realistic Platinum', 7: 'Conservative Platinum', 8: 'Status'}),
    'Arcanes':    (1, 'Arcane', {7: 'Floor Platinum', 8: 'Realistic Platinum', 9: 'Conservative Platinum', 10: 'Max via R0 copies (Realistic)'}),
    'Mods':       (2, 'Mod', {9: 'Floor Platinum', 10: 'Realistic Platinum', 11: 'Conservative Platinum', 12: 'Status'}),
    'Adversary':  (1, 'Adversary Weapon', {8: 'Floor Platinum', 9: 'Realistic Platinum', 10: 'Conservative Platinum', 11: 'Status'}),
}
LIGHT_MIN_REALISTIC = 45          # "approximately 50p+"
LIGHT_MOD_PREFIX = ('Primed ', 'Archon ', 'Galvanized ')
MOVE_PCT, MOVE_ABS = 0.20, 25


# ---------------------------------------------------------------- fetching
def get_json(url, path, sleep=0.36):
    if os.path.exists(path):
        try: return json.load(open(path))
        except Exception: pass
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30) as r: data = r.read()
            open(path, 'wb').write(data); time.sleep(sleep); return json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code == 404: json.dump({'error': 404}, open(path, 'w')); return {'error': 404}
            time.sleep(2 ** a)
        except Exception:
            time.sleep(2 ** a)
    return None


def fetch_item(cache, slug, adversary=None):
    if adversary:
        t = 'lich' if adversary.startswith('Kuva') else 'sister'
        return get_json(f'{API}/v1/auctions/search?type={t}&weapon_url_name={slug}&sort_by=price_asc', os.path.join(cache, 'auctions', f'{slug}.json')) is not None
    o = get_json(f'{API}/v2/orders/item/{slug}', os.path.join(cache, 'orders', f'{slug}.json'))
    s = get_json(f'{API}/v1/items/{slug}/statistics', os.path.join(cache, 'stats', f'{slug}.json'))
    return o is not None and not o.get('error') and s is not None and not s.get('error')      # v2 bodies carry "error": null


# ---------------------------------------------------------------- pricing (v4.3 methodology, unchanged)
def price_adversary(cache, slug, element, now):
    a = (pricer.load('auctions', slug) or {}).get('payload', {}).get('auctions', [])
    cred = [x for x in a if x.get('visible') and not x.get('closed') and x.get('is_direct_sell') and x.get('buyout_price') and pricer.days_since(x['owner'].get('last_seen', '')) <= 7]
    pick = lambda c: sorted(x['buyout_price'] for x in cred if c(x['item']))
    exact = pick(lambda it: it.get('element') == element and it.get('damage', 0) >= 58)
    elany = pick(lambda it: it.get('element') == element)
    anyhi = pick(lambda it: it.get('damage', 0) >= 58)
    use, basis = (exact, 'target element, >=58% valence') if exact else ((elany, 'target element, any valence (fuse to 60% by farming)') if elany else (anyhi, 'any element >=58%'))
    if not use: return {'status': 'MARKET DATA UNAVAILABLE'}
    real = statistics.median(use[:3])
    return {'floor': use[0], 'realistic': round(real, 1), 'conservative': math.ceil(max(real, use[min(2, len(use) - 1)]) * 1.10),
            'sellers_credible': len(use), 'status': ('OK' if len(use) >= 3 else 'THIN') + ' - ' + basis}


def price_row(cache, r, now):
    cat, slug = r['Category'], r['Market Slug']
    if cat == 'Adversary Weapon': return price_adversary(cache, slug, str(r.get('Element target') or '').lower(), now), None   # auctions use lower-case elements
    rank = r.get('Required Rank') if cat in ('Mod', 'Arcane') else None
    rank = int(rank) if rank not in (None, '') else None
    os.makedirs(os.path.join(cache, 'item'), exist_ok=True)
    json.dump({'data': {'maxRank': rank, 'i18n': {'en': {'name': r['Item']}}, 'tradable': True}}, open(os.path.join(cache, 'item', f'{slug}.json'), 'w'))
    p = pricer.price(slug, rank)
    p0 = pricer.price(slug, 0) if rank else None
    return p, p0


def base_status(s):
    s = str(s or '')
    for pre in ('MARKET REFRESH UNAVAILABLE', 'ANOMALY HELD'):
        if s.startswith(pre): s = s.split('previous status: ', 1)[-1].rstrip(')')
    return s.replace('; VOLATILE', '')


def thin(s): return 'THIN' in str(s)


def decide(r, p, p0, ok_fetch, ts):
    """Apply the anti-churn rules. Returns (new price-column dict, event) where event in OK/THIN/HELD/UNAVAILABLE."""
    prev = {c: r.get(c) for c in PRICE_COLS + ['Notes']}
    pst = base_status(prev['Status'])
    keep = dict(prev)
    if not ok_fetch or p is None or p.get('status') in ('NOT FETCHED',) or 'UNAVAILABLE' in str(p.get('status')) or p.get('realistic') is None:
        keep['Status'] = f'MARKET REFRESH UNAVAILABLE ({ts}; previous verified value kept; previous status: {pst})'
        return keep, 'UNAVAILABLE'
    if str(p.get('status')).startswith('NO CREDIBLE SELL ORDERS'):
        # trade history only: do not invent a precise Realistic from it - keep the verified value, widen Conservative
        ref = p.get('realistic')
        keep['Conservative Platinum'] = max(prev['Conservative Platinum'] or 0, math.ceil((ref or 0) * 1.25)) or prev['Conservative Platinum']
        keep['Status'] = f'MARKET REFRESH UNAVAILABLE ({ts}; THIN MARKET - no credible sell orders, previous verified value kept; previous status: {pst})'
        keep['Recent Median (30d)'] = p.get('median30'); keep['90d Median'] = p.get('median90')
        return keep, 'UNAVAILABLE'
    new_real = p['realistic']; old_real = prev['Realistic Platinum']
    n = p.get('sellers_credible') or 0
    med = p.get('median30') or p.get('median90')
    if old_real and n < 3 and (new_real > 2 * old_real or new_real < 0.5 * old_real) and not (med and abs(new_real - med) <= 0.35 * med):
        keep['Status'] = f'ANOMALY HELD ({ts}; book shows {new_real}p from {n} seller(s), unsupported by trade history; previous status: {pst})'
        return keep, 'HELD'
    th = thin(p.get('status'))
    cons = p['conservative']          # v4.3 method already widens thin books (5th seller / 30d median, x1.10)
    st = str(p['status']).replace('THIN', 'THIN MARKET', 1)
    if old_real and abs(new_real - old_real) >= MOVE_PCT * old_real and abs(new_real - old_real) >= 5: st += '; VOLATILE'
    elif cons >= 1.8 * new_real: st += '; VOLATILE'
    out = dict(prev)
    out.update({'Floor Platinum': p.get('floor'), 'Realistic Platinum': new_real, 'Conservative Platinum': cons, 'Market Timestamp': ts, 'Status': st,
                'Credible Sellers': p.get('sellers_credible'), 'Online Sellers': p.get('sellers_online'), 'Recent Median (30d)': p.get('median30'),
                '90d Median': p.get('median90'), '90d Weighted Avg': p.get('wa90'), '90d Volume': p.get('vol90'), '48h Volume': p.get('vol48h'),
                'Best Online Buy': p.get('best_buy'), 'Buy/Sell Spread': p.get('spread')})
    if p0 is not None:
        out['R0 Realistic'] = p0.get('realistic')
        if r['Category'] == 'Arcane' and p0.get('realistic') and r.get('Required Rank'):
            mr = int(r['Required Rank']); copies = (mr + 1) * (mr + 2) // 2; via = round(p0['realistic'] * copies, 1)
            out['Max via R0 copies (Realistic)'] = via
            out['Notes'] = f'Cheaper via {copies}x R0 ({via}p realistic) than buying max rank' if via < new_real else None
    return out, 'THIN' if th else 'OK'


# ---------------------------------------------------------------- selection
def eligible(r):
    if r['Category'] not in PRICED_CATS or not r.get('Market Slug'): return False
    if r.get('Counted in Player-Trade Total?') not in PRICED_FLAGS: return False
    tag = f"{r.get('Priority') or ''} {r.get('Status') or ''}"
    return not any(x in tag.upper() for x in NEVER_QUERY)


def light(r):
    s = str(r.get('Status') or ''); real = r.get('Realistic Platinum') or 0
    if r['Category'] in ('Warframe', 'Weapon', 'Adversary Weapon', 'Companion', 'Archgun', 'Signature Extra'): return True
    if r['Category'] == 'Arcane' and r.get('Counted in Player-Trade Total?') == 'Yes': return True
    if real >= LIGHT_MIN_REALISTIC: return True
    if r['Category'] == 'Mod' and r['Item'].startswith(LIGHT_MOD_PREFIX): return True
    return any(x in s for x in ('THIN', 'VOLATILE', 'UNAVAILABLE', 'ANOMALY'))


# ---------------------------------------------------------------- totals
def totals(rows):
    t = [0.0, 0.0, 0.0]
    for r in rows:
        if r['Category'] in TRADE_CATS and r.get('Counted in Player-Trade Total?') == 'Yes':
            for i, c in enumerate(('Floor Platinum', 'Realistic Platinum', 'Conservative Platinum')): t[i] += float(r.get(c) or 0)
    return [round(x, 1) for x in t]


def infra_from_model(path):
    """Fixed infrastructure net/gross and optional convenience from the live formulas (pycel if available)."""
    try:
        from pycel import ExcelCompiler
        wb = openpyxl.load_workbook(path); ms = wb['Economic Model']; xc = ExcelCompiler(filename=path); out = {}
        for r in range(1, ms.max_row + 1):
            a = str(ms.cell(r, 1).value or '')
            if a == 'FIXED INFRASTRUCTURE TOTAL': out['infra_gross'] = xc.evaluate(f'Economic Model!D{r}'); out['infra_net'] = xc.evaluate(f'Economic Model!F{r}')
            if a == 'OPTIONAL CONVENIENCE TOTAL': out['optional'] = xc.evaluate(f'Economic Model!D{r}')
            if a == 'PLAYER-TRADE TOTAL': out['pt_formula'] = [xc.evaluate(f'Economic Model!{c}{r}') for c in 'BCD']
        return out
    except ImportError:
        return {}


# ---------------------------------------------------------------- content-audit sentinel
def content_audit(cache, pm_slugs):
    flags = []
    cat = get_json(f'{API}/v2/items', os.path.join(cache, 'catalog.json'), sleep=0.5)
    if not cat or 'data' not in cat: return ['catalog check failed (Warframe.Market /v2/items unavailable) - re-run later']
    snap = json.load(open(CATALOG))
    if cat.get('apiVersion') != snap.get('apiVersion'): flags.append(f"Warframe.Market API version {snap.get('apiVersion')} -> {cat.get('apiVersion')} (market-system change?)")
    rel = {'warframe', 'weapon', 'mod', 'arcane_enhancement', 'prime', 'set', 'sentinel', 'kavat', 'kubrow', 'companion'}
    live = {i['slug']: i for i in cat['data']}
    new = [i for s, i in live.items() if s not in snap['items'] and set(i.get('tags') or []) & rel and not set(i.get('tags') or []) & {'component', 'blueprint', 'relic', 'riven_mod', 'veiled_riven', 'scene', 'skin'}]
    if new: flags.append(f'{len(new)} new tradeable item(s) on Warframe.Market: ' + ', '.join(sorted(i['i18n']['en']['name'] for i in new)[:40]))
    gone = sorted(s for s in pm_slugs if s not in live)
    if gone: flags.append(f'{len(gone)} workbook market slug(s) no longer listed: ' + ', '.join(gone[:40]))
    return flags


# ---------------------------------------------------------------- workbook helpers
def read_pm(wb):
    ws = wb['Procurement Master']; hdr = [c.value for c in ws[1]]; col = {h: i + 1 for i, h in enumerate(hdr)}
    rows = []
    for i in range(2, ws.max_row + 1):
        r = {h: ws.cell(i, col[h]).value for h in hdr}; r['_row'] = i; rows.append(r)
    return ws, col, rows


def snapshot(wb, skip):
    return {(ws.title, c.coordinate): c.value for ws in wb.worksheets if ws.title not in skip for row in ws.iter_rows() for c in row
            if c.value is not None}


def log_sheet(wb, log):
    if 'MARKET REFRESH LOG' in wb.sheetnames: del wb['MARKET REFRESH LOG']
    ws = wb.create_sheet('MARKET REFRESH LOG', wb.sheetnames.index('Economic Model'))
    hdr = ['Date', 'Refresh type', 'Rows queried', 'Rows changed', 'Previous Floor total', 'New Floor total', 'Previous Realistic total', 'New Realistic total',
           'Previous Conservative total', 'New Conservative total', 'Largest individual increases', 'Largest individual decreases', 'Unavailable/failed lookups',
           'Notes', 'Total reconstruction net (F / R / C)', 'Build specification']
    ws.append(hdr)
    from openpyxl.styles import Font, PatternFill, Alignment
    for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F3A5F'); c.alignment = Alignment(wrap_text=True, vertical='top')
    for e in log:
        ws.append([e['date'], e['type'], e['queried'], e['changed'], e['prev'][0], e['new'][0], e['prev'][1], e['new'][1], e['prev'][2], e['new'][2],
                   e['inc'], e['dec'], e['unavailable'], e['notes'], ' / '.join(f'{x:,.1f}' for x in e['net']), e.get('spec', 'Phase 3 v4.3 FINAL')])
    for i, w in enumerate([18, 12, 10, 10, 12, 12, 12, 12, 12, 12, 60, 60, 50, 80, 30, 22], 1): ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes = 'C2'


def set_market_field(wb, ts, mode):
    s = wb['Phase 3 Summary']
    for row in s.iter_rows():
        if row[3].value == 'MARKET DATA REFRESHED': row[4].value = ts; row[5].value = f'{mode} refresh - see MARKET REFRESH LOG (build specification unchanged)'
    ms = wb['Economic Model']
    ms['A2'] = re.sub(r'^Market: Warframe\.Market PC, [^.]*\.', f'Market: Warframe.Market PC, refreshed {ts} ({mode}).', ms['A2'].value)


def fmt(x): return f'{x:,.1f}'.rstrip('0').rstrip('.') if isinstance(x, float) else f'{x:,}'


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['light', 'full'], required=True)
    ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--out'); ap.add_argument('--cache')
    ap.add_argument('--limit', type=int, help='testing: query at most N rows')
    ap.add_argument('--force', action='store_true', help='run a light refresh even right after a full one')
    a = ap.parse_args()
    now = datetime.datetime.now(datetime.timezone.utc); ts = now.strftime('%Y-%m-%d %H:%M UTC'); mode = a.mode.upper()
    log = json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else []
    if a.mode == 'light' and not a.force and log and log[-1]['type'] == 'FULL':
        last = datetime.datetime.strptime(log[-1]['date'], '%Y-%m-%d %H:%M UTC').replace(tzinfo=datetime.timezone.utc)
        if (now - last).days < 3: print(f'SKIPPED: FULL refresh ran {log[-1]["date"]}; light refresh not needed.'); return
    cache = a.cache or os.path.join(os.environ.get('TMPDIR', '/tmp'), f"wfm_refresh_{now:%Y%m%d}_{a.mode}")
    for k in ('orders', 'stats', 'auctions', 'item'): os.makedirs(os.path.join(cache, k), exist_ok=True)
    pricer.CACHE = cache; pricer.NOW = now

    wb = openpyxl.load_workbook(WB_PATH)
    ws, col, rows = read_pm(wb)
    allowed_pm = {col[c] for c in PRICE_COLS} | {col['Notes']}   # Notes: Arcane R0-copy note only
    before = snapshot(wb, {'MARKET REFRESH LOG'})
    prev_tot = totals(rows)
    infra = infra_from_model(WB_PATH) or {k: log[-1][k] for k in ('infra_net', 'infra_gross', 'optional') if log and k in log[-1]}

    sel = [r for r in rows if eligible(r) and (a.mode == 'full' or light(r))]
    if a.limit: sel = sel[:a.limit]
    print(f'{mode} refresh {ts}: {len(sel)} rows to query (cache {cache})', flush=True)
    events, changes, touched = {}, [], set()
    for n, r in enumerate(sel, 1):
        okf = fetch_item(cache, r['Market Slug'], r['Item'] if r['Category'] == 'Adversary Weapon' else None)
        try: p, p0 = price_row(cache, r, now)
        except Exception as e: p, p0, okf = None, None, False
        new, ev = decide(r, p, p0, okf, ts)
        events[r['_row']] = ev
        old3 = [r.get(c) for c in ('Floor Platinum', 'Realistic Platinum', 'Conservative Platinum')]
        new3 = [new.get(c) for c in ('Floor Platinum', 'Realistic Platinum', 'Conservative Platinum')]
        if old3 != new3: changes.append((r, old3, new3))
        newly_thin = thin(new['Status']) and not thin(r.get('Status')) and ev != 'UNAVAILABLE'
        r['_ev'] = ev; r['_newly_thin'] = newly_thin; r['_was_unavail'] = 'UNAVAILABLE' in str(r.get('Status'))
        for c in PRICE_COLS + (['Notes'] if r['Category'] == 'Arcane' else []):
            if new.get(c) != r.get(c):
                ws.cell(r['_row'], col[c], new.get(c)); touched.add(('Procurement Master', ws.cell(r['_row'], col[c]).coordinate))
            r[c] = new.get(c)
        if n % 100 == 0: print(f'  {n}/{len(sel)}', flush=True)

    # mirror sheets (same values as Procurement Master)
    pm_by = {(r['Category'], r['Item']): r for r in rows}
    for sh, (ncol, cat, m) in MIRRORS.items():
        if sh not in wb.sheetnames: continue
        w = wb[sh]
        for i in range(2, w.max_row + 1):
            r = pm_by.get((cat, w.cell(i, ncol).value))
            if not r: continue
            for mc, pc in m.items():
                if w.cell(i, mc).value != r.get(pc): w.cell(i, mc, r.get(pc)); touched.add((sh, w.cell(i, mc).coordinate))
    if 'Frames' in wb.sheetnames:
        w = wb['Frames']
        for i in range(2, w.max_row + 1):
            r = pm_by.get(('Warframe', w.cell(i, 1).value))
            if r and r.get('Market Slug'):
                v = f"v4: {base_status(r['Status']).split(';')[0]}; R={r['Realistic Platinum']}p"
                if w.cell(i, 6).value != v: w.cell(i, 6, v); touched.add(('Frames', w.cell(i, 6).coordinate))
    set_market_field(wb, ts, mode)
    for t in [('Economic Model', 'A2')] + [('Phase 3 Summary', c.coordinate) for row in wb['Phase 3 Summary'].iter_rows() if row[3].value == 'MARKET DATA REFRESHED' for c in row[4:6]]:
        touched.add(t)

    # FROZEN MODEL CHECK: every cell outside the price cells must be identical
    after = snapshot(wb, {'MARKET REFRESH LOG'})
    bad = [k for k in set(before) | set(after) if before.get(k) != after.get(k) and k not in touched]
    bad_pm = [k for k in touched if k[0] == 'Procurement Master' and openpyxl.utils.column_index_from_string(re.match(r'[A-Z]+', k[1]).group()) not in allowed_pm]
    if bad or bad_pm:
        print('FROZEN MODEL CHECK FAILED - nothing saved:', (bad + bad_pm)[:20]); sys.exit(2)

    new_tot = totals(rows)
    net = [new_tot[i] + (infra.get('infra_net') or 0) for i in range(3)]
    counted = [(r, o, nw) for r, o, nw in changes if r['Category'] in TRADE_CATS and r.get('Counted in Player-Trade Total?') == 'Yes']
    dR = lambda x: (x[2][1] or 0) - (x[1][1] or 0)
    inc = sorted([x for x in counted if dR(x) > 0], key=dR, reverse=True)[:10]
    dec = sorted([x for x in counted if dR(x) < 0], key=dR)[:10]
    unav = [r for r in sel if r['_ev'] == 'UNAVAILABLE']
    held = [r for r in sel if r['_ev'] == 'HELD']
    moves = [x for x in changes if x[1][1] and x[2][1] is not None and (abs(dR(x)) >= MOVE_PCT * x[1][1] or abs(dR(x)) >= MOVE_ABS)]
    nthin = [r for r in sel if r['_newly_thin']]
    nunav = [r for r in unav if not r['_was_unavail']]
    caf = content_audit(cache, {r['Market Slug'] for r in rows if r.get('Market Slug') and r['Category'] != 'Adversary Weapon'})   # adversary slugs are auction weapon names, not catalogue items
    lab = lambda x: f"{x[0]['Item']} ({x[0]['Category']}) {fmt(x[1][1] or 0)}->{fmt(x[2][1] or 0)}p ({dR(x):+,.1f})"
    notes = [f'{len(held)} anomalous quote(s) held at previous value' if held else '', f'{len(nthin)} newly THIN MARKET' if nthin else '',
             ('CONTENT AUDIT REQUIRED: ' + ' | '.join(caf)) if caf else 'No content change detected on Warframe.Market',
             'FROZEN MODEL CHECK: PASS (only price cells changed)', 'DRY RUN' if a.dry_run else '']
    entry = {'date': ts, 'type': mode, 'queried': len(sel), 'changed': len(changes), 'prev': prev_tot, 'new': new_tot, 'net': net,
             'infra_net': infra.get('infra_net'), 'infra_gross': infra.get('infra_gross'), 'optional': infra.get('optional'),
             'inc': '; '.join(lab(x) for x in inc), 'dec': '; '.join(lab(x) for x in dec),
             'unavailable': f'{len(unav)}: ' + ', '.join(r['Item'] for r in unav[:30]) if unav else '0', 'notes': '; '.join(x for x in notes if x),
             'spec': 'Phase 3 v4.3 FINAL'}
    log2 = log + [entry]
    log_sheet(wb, log2)
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    out = a.out or WB_PATH
    wb.save(out)
    chk = infra_from_model(out)
    if chk.get('pt_formula') and any(abs((chk['pt_formula'][i] or 0) - new_tot[i]) > 0.05 for i in range(3)):
        print('ECONOMIC MODEL RECALC MISMATCH', chk['pt_formula'], new_tot); sys.exit(3)
    if not a.dry_run:
        json.dump(log2, open(LOG_PATH, 'w'), indent=1)

    # ---------------- delta report
    d = lambda i: f"{fmt(prev_tot[i])} -> {fmt(new_tot[i])} ({new_tot[i] - prev_tot[i]:+,.1f})"
    L = [f'# Market refresh {ts} ({mode})', '', f'Market refresh date: {ts}', f'Refresh type: {mode}', f'Items checked: {len(sel)}', f'Items changed: {len(changes)}',
         '', 'Player trade (the only category price movement affects):', f'- Floor: {d(0)}', f'- Realistic: {d(1)}', f'- Conservative: {d(2)}',
         f"- Total reconstruction, net: {' / '.join(fmt(x) for x in net)} (fixed infrastructure {fmt(infra.get('infra_net') or 0)}p net and optional convenience {fmt(infra.get('optional') or 0)}p unchanged; account-bound/earned 0p)",
         '', '## 10 largest increases (Realistic, counted in the reconstruction)'] + [f'- {lab(x)}' for x in inc] + ['', '## 10 largest decreases'] + [f'- {lab(x)}' for x in dec] + \
        ['', f'## Moves of 20%+ or 25p+ ({len(moves)})'] + [f'- {lab(x)}' + ('' if x[0].get('Counted in Player-Trade Total?') == 'Yes' else ' [not in totals]') for x in sorted(moves, key=lambda x: -abs(dR(x)))[:40]] + \
        ['', f'## Newly THIN MARKET ({len(nthin)})'] + [f"- {r['Item']} ({r['Category']})" for r in nthin] + \
        ['', f'## Newly unavailable market data ({len(nunav)}); previous verified values kept'] + [f"- {r['Item']} ({r['Category']})" for r in nunav] + \
        ['', f'## Anomalous quotes held ({len(held)})'] + [f"- {r['Item']}: {r['Status']}" for r in held] + \
        ['', '## Content check', *(['**CONTENT AUDIT REQUIRED** - roster/builds NOT changed by this refresh:'] + [f'- {x}' for x in caf] if caf else ['No new tradeable content detected.']),
         '', 'Frozen model check: PASS - only price cells changed; build specification remains Phase 3 v4.3 FINAL.' + (' (DRY RUN: workbook and log not updated)' if a.dry_run else '')]
    rep = '\n'.join(L)
    if not a.dry_run:
        os.makedirs(REPORT_DIR, exist_ok=True); open(os.path.join(REPORT_DIR, f"{now:%Y-%m-%d_%H%M}_{a.mode}.md"), 'w').write(rep + '\n')
    print(rep)


if __name__ == '__main__':
    main()
