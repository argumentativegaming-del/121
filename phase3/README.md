# Phase 3 Procurement Master

- `Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx`: normalized roster and weapon allocation, priced live on Warframe.Market (PC, 2026-10-05). Start with the **Economic Model** and **Corrections Log** sheets; per-item data is in **Procurement Master**.
- `Warframe_Phase3_Procurement_Master_v3_Economic_Model.xlsx`: the v3 input, kept for reference.
- `tools/`: scripts that rebuild v4.
  1. `fetch.py` and `fetch2.py` pull market data into `cache/`.
  2. `lua2json.py` converts the wiki data modules.
  3. `build.py` and `pricer.py` price every item.
  4. `write_v4.py` writes the workbook. `summarize.py` prints the totals.

  The scripts expect the data files in their working directory.

## v4.3 FINAL (frozen)

- All 66 frames audited; final cross-roster consistency audit passed (v4.3 FINAL). See the **OPTIMIZATION AUDIT** sheet. Records are in `tools/audit_batch1.py`, `audit_batch2.py`, `audit_batch3.py`, `audit_batch4.py` and `audit_batch5.py`.
- Regenerate with `build.py`, then `write_v4.py`, then `final_sheets.py`. `engine.py` validates the frame builds. The element-order validator in `builds_extra.py` checks every weapon and Exalted; its result is in **BUILD COMPLETENESS**.
- `xcheck.py` reruns the cross-roster consistency audit; its results are in the **CROSS-ROSTER AUDIT** sheet.
- Final-candidate corrections:
  - Primed Shred was restored on 5 builds.
  - Amalgam Organ Shatter is now on the 5 heavy-attack builds.
  - Two archived mods were replaced: Swift Deth by Assault Mode, and Corroding Barrage by Rousing Plunder.
  - Base Banshee is now framed as the Helminth donor for Silence.
  - Deconstructor Prime has its own glaive-class melee build. The beast claw build no longer pairs two incompatible claw mods.
  - Forma estimates are computed per weapon by `tools/capcheck.py`, from max-rank drains, innate polarities and Catalyst/rank-40 capacity.
- Account-bound build requirements, Helminth donors and the rulings on untradeable alternatives are in **EARNED REQUIREMENTS**. `tools/archived_list.json` is the wiki's {{Archived}} list that `build.py` and `xcheck.py` read.

## Price maintenance (standing workflow)

The v4.3 build model is frozen. This workflow refreshes market prices and economic totals only.

- **Weekly LIGHT refresh** (`tools/refresh.py --mode light`). Covers about 575 rows:
  - Prime frame sets and traded weapons;
  - Kuva/Tenet adversary auctions;
  - required Arcanes and companion sets;
  - every row at about 45p+ Realistic;
  - Primed/Archon/Galvanized mods;
  - anything flagged THIN / VOLATILE / UNAVAILABLE / ANOMALY.
- **Monthly FULL refresh** (`--mode full`). Covers every row that carries a player-trade price (about 1,735).
- **Never queried:** account-bound, Daily Tribute, quest-only or farm-only items, shards, Focus, fixed-price Reactors/Catalysts and slots.
- **Same methodology as v4.3** (`pricer.py`):
  - Floor = cheapest credible seller.
  - Realistic = median of the 3–5 cheapest credible sellers, bounded by trade history.
  - Conservative = the liquidity allowance.
  - Mods are priced at the exact required rank; Arcanes at full rank, with the R0-copies alternative.
  - Adversary weapons are priced by target element at >=58% valence.
- **Anti-churn rules:**
  - A failed or empty lookup keeps the previous verified value and is flagged `MARKET REFRESH UNAVAILABLE` with the check time. It never drops to 0p.
  - A book with 0 credible sellers keeps the previous Realistic and is marked THIN MARKET.
  - A 1–2 seller quote that moves more than 2x, unsupported by trade history, is `ANOMALY HELD`.
  - In a thin market, Conservative is kept at no less than 1.25x Realistic.
- **Frozen-model guard:** the script edits only price cells (Procurement Master price columns and their mirrors in Frames/Companions/Arcanes/Mods/Adversary) plus the refresh fields. If any other cell differs it refuses to save (exit 2). It also re-evaluates the Economic Model formulas and checks them against its own sums (exit 3 on mismatch).
- **History:**
  - `market_refresh_log.json` is append-only and is rendered as the **MARKET REFRESH LOG** sheet. `final_sheets.py` re-renders it, so regenerating the workbook keeps the history.
  - Each run writes a delta report to `refresh_reports/`.
  - The build specification stays "Phase 3 v4.3 FINAL"; only "MARKET DATA REFRESHED" changes.
- **Content sentinel:** each run compares the Warframe.Market catalogue against `tools/wfm_catalog_v43.json`. A new tradeable Prime/weapon/mod/Arcane/companion, a removed workbook slug, or an API version change is reported as **CONTENT AUDIT REQUIRED**. The roster is not changed.
- After any content-audit regeneration (`build.py` -> `write_v4.py` -> `final_sheets.py`, which reprices from the build-time cache), run a FULL refresh.
