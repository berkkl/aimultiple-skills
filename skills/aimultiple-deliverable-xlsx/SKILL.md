---
name: aimultiple-deliverable-xlsx
description: |
  Produces formula-driven xlsx workbooks for Cem, Meir, and external reviewers. Uses Raw + Summary + Notes sheet pattern so aggregates recompute when raw cells change. Activates whenever a deliverable goes outside the working directory (Sheets import, email, vendor share). Without this skill, CSV exports keep numbers as strings, break Sheets sort/filter/SUM, and read like Python output pasted into Word.
---

# AIMultiple Deliverable: XLSX

## Why this exists

Cem and Meir review numbers in Google Sheets. CSV imports keep many fields as strings (especially `"1/1"` or `"5/20"` ratios), so SUM, COUNTIF, sort, and filter do not work. Cem's exact framing (s32): "kontrol edilemiyor, rakam olmadıkları için, excel'i PDF'e çeviriyor." A flat CSV with mixed types is the same as a PDF for review purposes. Spreadsheet deliverables must be xlsx with real numbers and live formulas.

## Activation

Use whenever an artifact is shared with a recipient who will read it as a spreadsheet:

- Anything going to Cem, Meir, or a sponsor.
- Anything labelled "summary", "leaderboard", "results" for review.
- Anything that will be imported to Google Sheets (Drive upload, paste).
- Any "deliverable" that aggregates per-row data.

Do not use for pipeline-internal artifacts (per-call CSV from a runner, intermediate dataframes, raw logs). Those stay as CSV.

## Required inputs

- A grading or measurement dataset with one row per atomic unit (cell, call, task). One numeric outcome column per unit.
- The aggregation rules the recipient cares about (per provider, per tier, per window, success rate, average time, etc).
- Tier / category definitions if any.

## Sheet structure

Every deliverable workbook has at least three sheets:

1. **Summary** (open first; placed first in tab order)
   - One row per top-level entity (provider, vendor, task family).
   - Aggregate columns use `COUNTIFS` / `SUMIFS` / `AVERAGEIFS` against Raw. Never hardcode aggregate constants.
   - Percentage cells use `0%` or `0.0%` number format, not text like `"55%"`.
   - Add a totals/grand row if useful; same formula pattern.
   - Freeze header row. Bold and color the header.

2. **Raw**
   - One row per atomic measurement unit.
   - Numeric outcome columns are real numbers (1, 0, 327, 12.5), not strings ("1/1", "PASS", "12.5s").
   - Categorical columns (provider, tier, window, task_id) are short strings, no quotes embedded.
   - Helpful derived columns (`total_pass = run_1 + run_2`) are formulas, not pre-computed constants.
   - Wrap as an Excel Table (`openpyxl.worksheet.table.Table`) so the recipient gets one-click sort and filter.
   - Last column may be a free-text column (final response, notes) up to a reasonable cap (~500 chars). Truncate aggressively; the workbook is for review, not archival.

3. **Notes**
   - Tier and category definitions.
   - PASS/FAIL rules in one sentence each.
   - Which columns are formulas vs raw data.
   - Caveats (N=1 vs N=3, infra-fail exclusions, runs ran under old prompts, etc).
   - Source pipeline reference (`grade_v2_cells.py`, `run_load.py`, etc) so recipient can ask follow-up questions to the right script.

Optional extra sheets when relevant:

- **Per-tier** or **Per-axis** breakdown sheets with their own Summary + Raw if the dataset is large enough that a single Summary is too wide.
- **Methodology** sheet for spec references, window names, replication schedule.

## Numeric rules

- `1/1`, `0/1`, `3/5` strings are banned. Use one of:
  - Two integer columns: `pass`, `total`.
  - Single integer + implicit denominator stated in the column header (`run_1 (out of 1)`).
- Wall times, byte counts, token counts: integers (or floats with explicit number format like `0` or `#,##0`).
- Percentages: numeric value with `0%` or `0.0%` cell format. Never write the literal string `"55%"`.
- Currency: numeric value with `"$"#,##0.00` format, or document the currency in the column header.
- Booleans: write `1`/`0`, not `"TRUE"`/`"FALSE"`/`"PASS"`/`"FAIL"`. The text status can live in a parallel column for readability if useful.

## Formula rules

- Every Summary aggregate cell references Raw via `COUNTIFS` / `SUMIFS` / `AVERAGEIFS`. Editing Raw must recompute Summary.
- Use absolute references for fixed lookups (`Raw!$B:$B`) where the formula will be copied down.
- Match keys (provider name, tier label) are read from the Summary row's own cells (`A2`, etc), not hardcoded strings, so the recipient can rename a label and the formula keeps working.
- Percentages are computed in the formula (`=N2/40`), not pre-computed.
- Use `IFERROR(..., "")` around `AVERAGEIFS` because zero matches return `#DIV/0`.

## Tooling

Stdlib + `openpyxl` (Python). Install:

```
pip3 install --user --break-system-packages openpyxl
```

Minimal template:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = openpyxl.Workbook()

# Sheet 1: Summary (placed at index 0)
summ = wb.active
summ.title = "Summary"
summ.append(["Vendor", "Run 1 PASS", "Run 1 %", "Total PASS", "Total %"])
for c in summ[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="305496")
    c.alignment = Alignment(horizontal="center", wrap_text=True)
for i, vendor in enumerate(VENDORS, start=2):
    summ.cell(row=i, column=1, value=vendor)
    summ.cell(row=i, column=2,
              value=f'=COUNTIFS(Raw!C:C,A{i},Raw!D:D,1)')
    summ.cell(row=i, column=3, value=f"=B{i}/20")
    summ.cell(row=i, column=3).number_format = "0%"
    # ... etc

# Sheet 2: Raw
raw = wb.create_sheet("Raw")
raw.append(["task_id","tier","vendor","run_1","run_2","total_pass","pass_rate"])
for r in rows:
    raw.append([r.task_id, r.tier, r.vendor, r.run_1, r.run_2, None, None])
# Add formulas for derived columns
for i in range(2, len(rows)+2):
    raw.cell(row=i, column=6, value=f"=D{i}+E{i}")
    raw.cell(row=i, column=7, value=f"=F{i}/2")
    raw.cell(row=i, column=7).number_format = "0%"

# Wrap Raw as a Table for filterability
last_row = len(rows) + 1
tab = Table(displayName="RawData", ref=f"A1:G{last_row}")
tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2",
                                    showRowStripes=True)
raw.add_table(tab)

# Sheet 3: Notes
notes = wb.create_sheet("Notes")
notes.append(["Tier definitions", ""])
notes.append(["T0", "Control fixtures (3 tasks)"])
# ... etc

# Freeze panes
summ.freeze_panes = "B2"
raw.freeze_panes = "D2"

wb.save("deliverable.xlsx")
```

## Workflow

1. **Identify the recipient and the question.** What is Cem trying to do with this sheet? If the answer is "sort by success rate" or "filter to bd-mcp only", that drives which columns and which sort-on-Raw is needed.
2. **Build the Raw rows.** One row per atomic unit. Numeric where possible.
3. **Build the Summary formulas.** Reference Raw cells, not hardcoded numbers.
4. **Add a Notes sheet.** Definitions and caveats.
5. **Verify by opening the file.** Confirm: numbers are right-aligned (default for numeric type), percentages display as `%`, formulas appear in the formula bar when you click an aggregate cell, sort/filter works on the Raw table.
6. **Ship.** Drop the xlsx into a zip or share directly. Do not ship the source CSV with the xlsx unless the recipient asked.

## Failure cases

- **Recipient sees numbers as text:** check that Raw cells were written with integer/float values, not strings. `openpyxl` writes whatever Python type you pass.
- **`=COUNTIFS` returns `0` when it should match:** check that the lookup value type matches. `COUNTIFS(Raw!C:C, "bd-mcp", Raw!D:D, 1)` works only if Raw column C is text and column D is integer. `COUNTIFS(..., "1")` against integer 1 will not match in Sheets (Excel can be more forgiving).
- **`=AVERAGEIFS` returns `#DIV/0`:** wrap in `IFERROR(..., "")`.
- **Filter or sort options missing:** Raw sheet must be wrapped as a `Table`, not just plain rows.
- **`=N2/40` shows `0.55` instead of `55%`:** set `cell.number_format = "0%"`.

## Anti-patterns to refuse

- Writing `"1/1"` strings instead of two int columns.
- Calling the file a "summary spreadsheet" while pre-computing aggregates in Python and hardcoding them.
- Putting everything on one sheet so Summary, Raw, and Notes are tangled.
- Saving as `.csv` because "Sheets opens it." Cem's feedback explicitly rules this out for review deliverables.
- Adding columns that mix two units (`Wall time / Tool calls`).
- Truncating Raw to the rows that "look interesting." Cem wants drill-down; deliver complete Raw.

## Integration points

- Pairs with `skills/aimultiple-publication-quality-gate/SKILL.md` (run quality gate before sharing externally).
- Source data usually comes from a grading script (`grade_v2_cells.py`, `grade_load.py`, etc.) or an analysis CSV in `tier3-results-summary/`.
- Internal pipeline CSVs (per-call, per-cell) feed Raw; do not duplicate them inside the xlsx.

## Reference example

`scripts/web-exec-benchmark/tier-0-1-2-summary.xlsx` is the canonical example: Raw sheet with 120 rows × 10 columns (numeric run_1, run_2, avg_time_s, avg_tools, plus task_id/tier/vendor/total_pass formula/pass_rate formula/final_response text), wrapped as `RawData` Excel Table; Summary sheet with 6 vendor rows × 15 columns of which 12 are formulas (`=COUNTIFS(...)`, `=AVERAGEIFS(...)`, `=E2+J2`, `=N2/40`); Notes sheet documenting tier definitions, PASS rule, formula source.

The build script is reproducible from `grade_v2_summary-r2.csv` + `grade_v2_summary-r3.csv` plus the per-cell JSON outputs at `runs-20-v2-hc-r{2,3}/<provider>/T*.json`.
