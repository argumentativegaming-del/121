# Phase 3 Procurement Master

- `Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx`: normalized roster and weapon allocation, priced live on Warframe.Market (PC, 2026-10-05). Start with the **Economic Model** and **Corrections Log** sheets; per-item data is in **Procurement Master**.
- `Warframe_Phase3_Procurement_Master_v3_Economic_Model.xlsx`: the v3 input, kept for reference.
- `tools/`: scripts that rebuild v4.
  1. `fetch.py` and `fetch2.py` pull market data into `cache/`.
  2. `lua2json.py` converts the wiki data modules.
  3. `build.py` and `pricer.py` price every item.
  4. `write_v4.py` writes the workbook. `summarize.py` prints the totals.

  The scripts expect the data files in their working directory.

## v4.3 optimization audit (DRAFT, not final)

- Batches 1-3 (Ash -> Mesa) are audited: 34 of 66 frames. See the **OPTIMIZATION AUDIT** sheet. Records are in `tools/audit_batch1.py`, `audit_batch2.py` and `audit_batch3.py`.
- Regenerate with `build.py`, then `write_v4.py`, then `final_sheets.py`. `engine.py` validates the frame builds. The element-order validator in `builds_extra.py` checks every weapon and Exalted; its result is in **BUILD COMPLETENESS**.
