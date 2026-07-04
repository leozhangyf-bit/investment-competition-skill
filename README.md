# Investment Competition Skill

Reusable Codex skill for recurring investment or securities competition ranking projects.

It covers weekly data updates, adjusted/total-return validation, historical snapshots, workbook and web output checks, deployment gates, production verification, and annual season rollover.

## Install

Clone this repository into your Codex skills directory:

```text
~/.codex/skills/investment-competition
```

Then invoke it with:

```text
$investment-competition
```

Season-specific participants, holdings, dates, data-source credentials, and deployment targets belong in each season project and are intentionally not included here.

## Contents

- `SKILL.md` — workflow instructions
- `agents/openai.yaml` — display metadata
- `references/season-project-contract.md` — reusable project contract
- `scripts/preflight.py` — deterministic publication checks

