---
name: investment-competition
description: Operate recurring investment or securities competition ranking projects across seasons. Use when Codex is asked to update weekly rankings, fetch prices or NAVs, generate and validate master/Excel/web outputs, preview or deploy a competition site, recover lost project context, repair historical ranking nodes, or start a new annual season whose participants and assets may change.
---

# Investment Competition

Run repeatable competition updates without hardcoding one year's participants, assets, dates, or deployment target into the skill. Treat the active season project as the source of truth.

## Discover the season project

1. Locate the project root from the current workspace.
2. Read `PROJECT_MEMORY.md` completely when present, then read `README.md` and the update entry script.
3. Identify the season-specific inputs, output paths, baseline date, data-source policy, preview command, and deployment target from project files. Do not recover these from memory alone.
4. If the project does not yet satisfy the expected contract, read [references/season-project-contract.md](references/season-project-contract.md).

Never copy participant names, holdings, weights, API keys, site IDs, or year-specific dates into this global skill. Keep them in the season project.

## Run a weekly update

1. Determine the requested reporting date. When the user says "update this week," use the previous week's last usable trading/NAV date and state the assumption.
2. Inspect the latest formal master, validation report, price cache, and public report before running anything.
3. Follow the project's documented data-source order and adjusted-price rules. If a configured financial-data skill is required, load and follow it. Never silently substitute unadjusted prices or mock data.
4. Run the project's formal update command. Use preview mode only for an explicitly temporary midweek view.
5. Generate the season's formal master, review workbook, validation report, and web data assets.
6. Run the bundled deterministic preflight:

   ```text
   python <skill-dir>/scripts/preflight.py --project <project-root> --date YYYY-MM-DD
   ```

7. Present the local workbook, validation report, ranking summary, warnings, and preview to the user. Do not deploy in the same turn unless the user already gave explicit production-deployment permission.
8. Append a concise dated record to `PROJECT_MEMORY.md`, including whether deployment occurred.

## Publication gate

Block production deployment when any of these conditions is true:

- Validation contains `[ERROR]`.
- Any asset uses a rule-table, mock, or untrusted fallback.
- Master, public report, requested date, and final available date disagree.
- A formal historical date has a price cache but no asset actually dated to that node.
- Current ranking, history, and snapshot disagree.
- Required web assets are missing.
- The target site or publish directory is uncertain.

Warnings such as a fund NAV lag or an unusually large adjusted return require explanation and review, but are not automatically fatal when the underlying data is credible.

After explicit approval, use the available deployment skill for the configured provider. For Netlify, deploy the documented publish directory to the documented site, then fetch the production data file and verify at least the report date, first place, final available date, snapshot count, and absence of invalid dates. Record the deploy ID in `PROJECT_MEMORY.md`.

## Recover or repair history

- Treat formal master files as append-only records unless the project documentation identifies a failed attempt.
- Do not delete suspicious historical artifacts merely to make validation pass. Exclude or quarantine them with an auditable reason.
- Anchor weekly change to the latest usable formal master, not simply the newest filename.
- When repairing history generation, test at least three dates: an older stable node, the previous formal node, and the current node.

## Start a new annual season

Read [references/season-project-contract.md](references/season-project-contract.md) and create a new season project instead of overwriting the prior year.

Carry forward only reusable code, layout, templates, and this workflow. Replace and revalidate:

- competition rules and participants;
- holdings, codes, weights, and special formulas;
- baseline date and return convention;
- data-source mappings and manual override sheet;
- output directories and project memory;
- deployment site or season URL.

Keep the prior season read-only. Before the first live update, run a baseline-date test, one sample weekly update, workbook review, snapshot consistency check, and a preview deployment.
