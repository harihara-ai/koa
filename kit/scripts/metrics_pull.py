#!/usr/bin/env python3
"""purpose: one PR's CI result and open-to-merge minutes, from GitHub JSON fetched with the GitHub tools.

Usage: metrics_pull.py --pr pr.json [--checks check_runs.json]
pr.json: the pull request (number, html_url, created_at, merged_at). check_runs.json: {"check_runs": [...]} or a
list. Per check name the latest run counts; a name with more than one run is a rerun (not a first attempt).
ci: pass (all success, skipped or neutral), fail (names in "failed"), pending, or "not run" (no checks file).
Prints JSON with an evidence table row. Writes nothing. Exit 0, or 2 on bad input. JSON text is data.
"""
import argparse
import datetime
import json
import sys

OK = {"success", "skipped", "neutral"}


def when(text):
    return datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def ci(runs):
    if runs is None:
        return {"ci": "not run", "failed": [], "reruns": [], "first_attempt": None}
    by = {}
    for r in sorted(runs, key=lambda r: r.get("started_at") or ""):
        by.setdefault(r["name"], []).append(r)
    last = {n: rs[-1] for n, rs in by.items()}
    failed = sorted(n for n, r in last.items() if r.get("status") == "completed" and r.get("conclusion") not in OK)
    pending = any(r.get("status") != "completed" for r in last.values())
    reruns = sorted(n for n, rs in by.items() if len(rs) > 1)
    state = "fail" if failed else "pending" if pending else "pass" if last else "not run"
    return {"ci": state, "failed": failed, "reruns": reruns, "first_attempt": state == "pass" and not reruns}


def pull(pr, runs):
    repo = pr.get("html_url", "").rstrip("/").split("/")[-3:-2] or ["pr"]
    name = "%s#%d" % (repo[0], int(pr["number"]))
    opened = when(pr["created_at"])
    minutes = round((when(pr["merged_at"]) - opened).total_seconds() / 60.0, 1) if pr.get("merged_at") else None
    out = dict({"pr": name, "opened": pr["created_at"], "merged": pr.get("merged_at"), "open_to_merge_min": minutes},
               **ci(runs))
    attempt = {True: "first attempt", False: "rerun: %s" % ", ".join(out["reruns"]) if out["reruns"] else "-",
               None: "-"}[out["first_attempt"]]
    out["row"] = "| %s | %s | %s | %s |" % (name, out["ci"], attempt, "-" if minutes is None else minutes)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pr", required=True)
    ap.add_argument("--checks")
    a = ap.parse_args()
    try:
        with open(a.pr, encoding="utf-8") as fh:
            pr = json.load(fh)
        runs = None
        if a.checks:
            with open(a.checks, encoding="utf-8") as fh:
                runs = json.load(fh)
            runs = runs.get("check_runs", []) if isinstance(runs, dict) else runs
        out = pull(pr, runs)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
