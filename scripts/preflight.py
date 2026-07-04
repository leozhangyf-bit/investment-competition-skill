from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def snapshot_rows(value: Any, item_date: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        node = next((item for item in value if item.get("date") == item_date), None)
    elif isinstance(value, dict):
        node = value.get(item_date)
    else:
        node = None
    if isinstance(node, dict):
        node = node.get("ranking", [])
    return node if isinstance(node, list) else []


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate investment competition outputs before publication.")
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--date", dest="report_date")
    args = parser.parse_args()

    root = args.project.resolve()
    public_path = root / "public" / "report_data.json"
    checks: list[dict[str, Any]] = []
    warnings: list[str] = []

    if not public_path.exists():
        print(json.dumps({"passed": False, "error": f"Missing {public_path}"}, ensure_ascii=False, indent=2))
        return 1

    public = load_json(public_path)
    report_date = args.report_date or public.get("updateDate")
    if not report_date:
        print(json.dumps({"passed": False, "error": "Cannot determine report date"}, ensure_ascii=False, indent=2))
        return 1

    master_path = root / "data" / "master" / f"master_{report_date}.json"
    validation_path = root / "data" / "validation" / f"validation_report_{report_date}.txt"
    cache_path = root / "data" / "daily_prices" / f"prices_{report_date}.json"
    for label, path in [("master", master_path), ("validation", validation_path), ("price cache", cache_path)]:
        add_check(checks, f"{label}_exists", path.exists(), str(path))

    if not all(path.exists() for path in [master_path, validation_path, cache_path]):
        result = {"passed": False, "date": report_date, "checks": checks, "warnings": warnings}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    master = load_json(master_path)
    cache = load_json(cache_path)
    validation = validation_path.read_text(encoding="utf-8-sig", errors="replace")
    validation_warnings = [line for line in validation.splitlines() if "[WARN]" in line]
    warnings.extend(validation_warnings)

    add_check(checks, "validation_has_no_error", "[ERROR]" not in validation, "validation report")
    add_check(checks, "public_date_matches", public.get("updateDate") == report_date, str(public.get("updateDate")))
    add_check(checks, "master_date_matches", master.get("updateDate") == report_date, str(master.get("updateDate")))

    rankings = master.get("ranking", [])
    public_rankings = public.get("ranking", [])
    add_check(checks, "ranking_not_empty", bool(rankings and public_rankings), f"master={len(rankings)}, public={len(public_rankings)}")
    if rankings and public_rankings:
        add_check(
            checks,
            "current_first_place_matches",
            rankings[0].get("participant") == public_rankings[0].get("participant"),
            f"master={rankings[0].get('participant')}, public={public_rankings[0].get('participant')}",
        )

    expected_assets = master.get("assetCount")
    add_check(checks, "asset_count_matches", expected_assets is None or len(cache) == expected_assets, f"cache={len(cache)}, master={expected_assets}")
    fallback = [code for code, item in cache.items() if isinstance(item, dict) and item.get("fetch_status") == "fallback"]
    add_check(checks, "no_untrusted_fallback", not fallback, ", ".join(fallback) or "none")

    available_dates = public.get("availableDates", [])
    weekly_dates = master.get("weeklyDates", [])
    add_check(checks, "final_available_date_matches", bool(available_dates) and available_dates[-1] == report_date, str(available_dates[-1] if available_dates else None))
    add_check(checks, "weekly_date_contains_current", report_date in weekly_dates, report_date)

    invalid_nodes: list[str] = []
    for node_date in sorted(set(available_dates) | set(weekly_dates)):
        node_cache_path = root / "data" / "daily_prices" / f"prices_{node_date}.json"
        if not node_cache_path.exists():
            continue
        node_cache = load_json(node_cache_path)
        dated = [item for item in node_cache.values() if isinstance(item, dict) and item.get("latest_date") == node_date]
        if node_cache and not dated:
            invalid_nodes.append(node_date)
    add_check(checks, "no_invalid_formal_dates", not invalid_nodes, ", ".join(invalid_nodes) or "none")

    master_current = snapshot_rows(master.get("snapshots"), report_date)
    public_current = snapshot_rows(public.get("snapshots"), report_date)
    snapshot_ok = bool(master_current and public_current and rankings)
    if snapshot_ok:
        first = rankings[0].get("participant")
        snapshot_ok = master_current[0].get("participant") == first == public_current[0].get("participant")
    add_check(checks, "current_snapshot_matches", snapshot_ok, report_date)

    index_path = root / "public" / "index.html"
    generated_path = root / "public" / "report_data.generated.js"
    generated_required = index_path.exists() and "report_data.generated.js" in index_path.read_text(encoding="utf-8", errors="ignore")
    add_check(checks, "required_web_assets_exist", not generated_required or generated_path.exists(), str(generated_path))

    passed = all(item["passed"] for item in checks)
    result = {
        "passed": passed,
        "date": report_date,
        "firstPlace": rankings[0].get("participant") if rankings else None,
        "checks": checks,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
