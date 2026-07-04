# Season project contract

## Contents

- Stable workflow versus season configuration
- Expected project artifacts
- Weekly operating contract
- Annual rollover checklist

## Stable workflow versus season configuration

The global skill owns the sequence: discover context, update, validate, review, obtain deployment approval, deploy, verify production, and record memory.

Each season project owns all values that may change:

| Season-owned value | Typical location |
| --- | --- |
| Competition rules, participants, holdings, weights | Rules workbook or season config |
| Baseline date and return formula | Project memory and update code |
| Symbol/market mappings and special formulas | Rules workbook and data-fetch layer |
| Manual overrides | Season override workbook |
| Data-source priority and adjustment convention | Project memory and fetch layer |
| Output names and public schema | Update/report scripts |
| Deployment target | Project memory and provider config |

## Expected project artifacts

Prefer this structure when starting a new season, but adapt to an existing documented project rather than renaming files gratuitously:

```text
PROJECT_MEMORY.md
README.md
data/
  competition_rules.xlsx
  manual_override.xlsx
  daily_prices/
  master/
  excel/
  validation/
  preview/
public/
  index.html
  report_data.json
scripts/
  update_weekly_data.py
```

The formal pipeline should produce a dated master, a human-review workbook, a validation report, and public web data. The frontend should display precomputed rankings rather than recalculating financial results.

## Weekly operating contract

1. Determine the last usable trading/NAV date.
2. Fetch adjusted or total-return-compatible data according to the season policy.
3. Apply special formulas, then manual overrides last.
4. Write price cache, formal master, workbook, validation report, and web assets.
5. Fail closed on missing prices, untrusted fallback data, date mismatches, or validation errors.
6. Review locally before production deployment.
7. Deploy only after explicit approval and verify the production data response.
8. Record the run, warnings, top ranking, deploy status, and deploy ID in project memory.

## Annual rollover checklist

1. Create a new year/season directory; do not overwrite the completed season.
2. Copy reusable scripts, frontend layout, workbook styling, and deployment configuration only after reviewing them.
3. Create a fresh rules workbook and override workbook.
4. Replace every participant, holding, code, weight, and special formula from the new rules.
5. Set the new baseline date and document whether returns use adjusted price, NAV, total return, or another approved convention.
6. Clear generated masters, caches, previews, validation reports, and public report data from the copied template.
7. Decide whether to reuse the public URL or create a new season site; record the decision in the new `PROJECT_MEMORY.md`.
8. Validate symbol coverage across all markets and funds before the first official week.
9. Run a baseline test where all valid assets begin at zero return, followed by one sample week.
10. Review the workbook and website, then use a preview deployment before the first production release.
