# Phase 3 Procurement Master

- `Warframe_Phase3_Procurement_Master_v4_Economic_Model.xlsx`: normalized roster and weapon allocation, priced live on Warframe.Market (PC, 2026-10-05). Start with the **Economic Model** and **Corrections Log** sheets; per-item data is in **Procurement Master**.
- `Warframe_Phase3_Procurement_Master_v3_Economic_Model.xlsx`: the v3 input, kept for reference.
- `tools/`: scripts that rebuild v4.
  1. `fetch.py` and `fetch2.py` pull market data into `cache/`.
  2. `lua2json.py` converts the wiki data modules.
  3. `build.py` and `pricer.py` price every item.
  4. `write_v4.py` writes the workbook. `summarize.py` prints the totals.

  The scripts expect the data files in their working directory.
