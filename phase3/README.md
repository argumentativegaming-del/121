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
- Account-bound build requirements, Helminth donors and the rulings on untradeable alternatives are in **EARNED REQUIREMENTS**. `tools/archived_list.json` is the wiki's {{Archived}} list that `build.py` and `xcheck.py` read.
