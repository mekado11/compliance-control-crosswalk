#!/usr/bin/env python3
"""Generate a compliance gap report for a declared set of in-scope frameworks.

The report answers four questions an audit committee actually asks:

  1. Against the frameworks we have declared in scope, which obligations are not met?
  2. Which single remediations close obligations in the most frameworks at once?
  3. Where are we relying on a partial mapping and calling it coverage?
  4. What does the evidence burden look like, and how much of it is reusable?

Inputs
  library/control-library.csv      control definitions, evidence, tests, automation rating
  crosswalk/crosswalk.csv          control -> framework control identifier, with strength
  <scope profile>.json             declared frameworks, control applicability, status file

Output
  markdown, to stdout or to --out

Standard library only, deliberately: this script has to run inside change-controlled
environments where installing packages is itself a change request. See DECISIONS.md ADR-004.

Usage
  python3 scripts/gap_report.py --scope examples/scope-profile-core.json
  python3 scripts/gap_report.py --scope examples/scope-profile-fedramp-pursuit.json \
      --out reports/gap-report-fedramp-pursuit.md
  python3 scripts/gap_report.py --scope examples/scope-profile-core.json --fail-on-gap
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Weight of an implementation status toward satisfying a mapped obligation.
STATUS_CREDIT = {
    "implemented": 1.0,
    "partial": 0.5,
    "planned": 0.0,
    "not-implemented": 0.0,
    "not-applicable": None,   # excluded from the denominator entirely
}

# Credit multiplier by mapping strength. A supporting mapping never closes an obligation
# on its own; treating it as if it did is the most common way a crosswalk lies.
STRENGTH_CREDIT = {"full": 1.0, "partial": 0.5, "supporting": 0.0}

STATUS_ORDER = ["implemented", "partial", "planned", "not-implemented", "not-applicable"]


class ScopeError(Exception):
    pass


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_scope(path):
    with open(path, encoding="utf-8") as fh:
        scope = json.load(fh)
    for key in ("profile_name", "in_scope_frameworks", "status_file"):
        if key not in scope:
            raise ScopeError(f"scope profile missing required key: {key}")
    if not scope["in_scope_frameworks"]:
        raise ScopeError("in_scope_frameworks is empty; nothing to assess")
    scope.setdefault("excluded_controls", {})
    scope.setdefault("notes", "")
    scope.setdefault("assessment_date", date.today().isoformat())
    return scope


def build_model(scope, lib_path, xw_path, status_path):
    library = {r["control_id"]: r for r in read_csv(lib_path)}
    if not library:
        raise ScopeError("control library is empty")

    crosswalk = [r for r in read_csv(xw_path)
                 if r["framework_key"] in scope["in_scope_frameworks"]]

    status = {}
    for r in read_csv(status_path):
        cid = r["control_id"]
        if cid not in library:
            raise ScopeError(f"status file references unknown control {cid}")
        st = r["implementation_status"].strip().lower()
        if st not in STATUS_CREDIT:
            raise ScopeError(f"{cid}: unknown implementation_status '{st}'")
        status[cid] = r

    # controls explicitly excluded by the scope profile are marked not-applicable
    for cid, reason in scope["excluded_controls"].items():
        if cid not in library:
            raise ScopeError(f"excluded_controls references unknown control {cid}")
        status.setdefault(cid, {"control_id": cid})
        status[cid] = dict(status[cid])
        status[cid]["implementation_status"] = "not-applicable"
        status[cid]["notes"] = f"excluded by scope profile: {reason}"

    missing = [c for c in library if c not in status]
    if missing:
        raise ScopeError(
            "status file does not cover every control in the library; missing: "
            + ", ".join(sorted(missing)))

    return library, crosswalk, status


def obligation_coverage(crosswalk, status):
    """Per framework obligation (framework_control_id), compute best available credit."""
    oblig = defaultdict(list)      # (fw, fw_control_id) -> [(control_id, credit)]
    for r in crosswalk:
        cid = r["control_id"]
        st = status[cid]["implementation_status"].strip().lower()
        base = STATUS_CREDIT[st]
        if base is None:
            continue  # not applicable: contributes nothing, and is not a gap
        credit = base * STRENGTH_CREDIT[r["mapping_strength"]]
        oblig[(r["framework_key"], r["framework_control_id"])].append((cid, credit))
    summary = {}
    for key, entries in oblig.items():
        best = max(c for _, c in entries)
        summary[key] = {
            "credit": best,
            "state": "met" if best >= 1.0 else ("partial" if best > 0 else "gap"),
            "controls": sorted(entries, key=lambda t: -t[1]),
        }
    return summary


def leverage(crosswalk, status, in_scope):
    """Frameworks closed per control if that control were brought to implemented."""
    out = {}
    for cid in {r["control_id"] for r in crosswalk}:
        st = status[cid]["implementation_status"].strip().lower()
        if st in ("implemented", "not-applicable"):
            continue
        rows = [r for r in crosswalk if r["control_id"] == cid]
        fws = {r["framework_key"] for r in rows if r["mapping_strength"] in ("full", "partial")}
        obligations = {(r["framework_key"], r["framework_control_id"]) for r in rows
                       if r["mapping_strength"] in ("full", "partial")}
        out[cid] = {"frameworks": sorted(fws & set(in_scope)),
                    "obligation_count": len(obligations),
                    "status": st}
    return out


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return out


def render(scope, library, crosswalk, status, cov, lev):
    fws = scope["in_scope_frameworks"]
    L = []
    a = L.append

    a(f"# Compliance gap report — {scope['profile_name']}")
    a("")
    a(f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by `scripts/gap_report.py` from "
      f"`{os.path.basename(scope['status_file'])}`. All data is synthetic and illustrative.")
    a("")
    if scope["notes"]:
        a(f"**Scope note.** {scope['notes']}")
        a("")

    # ---- 1 summary -------------------------------------------------------------
    a("## 1. Summary")
    a("")
    total_ob = len(cov)
    met = sum(1 for v in cov.values() if v["state"] == "met")
    part = sum(1 for v in cov.values() if v["state"] == "partial")
    gap = sum(1 for v in cov.values() if v["state"] == "gap")
    a(f"{len(library)} controls in the library. {len(fws)} frameworks declared in scope. "
      f"{total_ob} distinct framework obligations are mapped from those controls.")
    a("")
    a(f"- **Met** (a fully mapped, implemented control exists): {met} "
      f"({met / total_ob:.0%})")
    a(f"- **Partial** (implemented but only partially mapped, or mapped but only partially "
      f"implemented): {part} ({part / total_ob:.0%})")
    a(f"- **Gap** (no implemented control contributes): {gap} ({gap / total_ob:.0%})")
    a("")
    a("Partial is the row that matters. A program reporting 'compliant' on a partially mapped "
      "obligation is making a claim the crosswalk does not support, and it is the claim an auditor "
      "tests first.")
    a("")

    # ---- 2 per framework --------------------------------------------------------
    a("## 2. Coverage by framework")
    a("")
    rows = []
    for fw in fws:
        entries = [v for (f, _), v in cov.items() if f == fw]
        if not entries:
            rows.append([fw, 0, "—", "—", "—", "no mapped obligations"])
            continue
        m = sum(1 for v in entries if v["state"] == "met")
        p = sum(1 for v in entries if v["state"] == "partial")
        g = sum(1 for v in entries if v["state"] == "gap")
        rows.append([fw, len(entries), m, p, g, f"{m / len(entries):.0%} met"])
    L.extend(md_table(["Framework", "Obligations mapped", "Met", "Partial", "Gap", "Met rate"], rows))
    a("")

    # ---- 3 gaps ------------------------------------------------------------------
    a("## 3. Open gaps, by control")
    a("")
    a("An obligation is attributed to the control that provides the most credit toward it. A "
      "control shown as `implemented` still appears here when its mapping to an obligation is "
      "partial or supporting: the control operates, but it does not close that obligation by "
      "itself. Those rows are where a second control has to be named, not where remediation is "
      "owed.")
    a("")
    gapped = defaultdict(list)
    for (fw, fid), v in cov.items():
        if v["state"] in ("gap", "partial"):
            owner_ctl = v["controls"][0][0] if v["controls"] else "—"
            gapped[owner_ctl].append((fw, fid, v["state"]))
    rows = []
    for cid in sorted(gapped, key=lambda c: (-len(gapped[c]), c)):
        c = library[cid]
        st = status[cid]["implementation_status"]
        linked = status[cid].get("linked_exception_or_acceptance", "")
        fw_list = sorted({f for f, _, _ in gapped[cid]})
        rows.append([cid, c["title"], st, len(gapped[cid]), " ".join(fw_list),
                     linked or "**none**", c["owner_role"]])
    L.extend(md_table(
        ["Control", "Title", "Status", "Affected obligations", "Frameworks",
         "Exception / acceptance", "Owner role"], rows))
    a("")
    unregistered = [r[0] for r in rows if r[5] == "**none**"
                    and status[r[0]]["implementation_status"] in ("planned", "not-implemented")]
    if unregistered:
        a(f"**{len(unregistered)} control(s) are unimplemented with no registered exception or "
          f"acceptance: {', '.join(unregistered)}.** An unimplemented control without a record is "
          "not a risk decision, it is an undocumented deviation, and it is the finding an auditor "
          "writes up as a governance failure rather than a control failure.")
        a("")

    # ---- 4 leverage ---------------------------------------------------------------
    a("## 4. Highest-leverage remediations")
    a("")
    a("Ranked by the number of in-scope framework obligations closed by bringing one control to "
      "fully implemented. This is the ordering a resource-constrained program should work in, "
      "adjusted for the risk reduction each control delivers — which this script deliberately does "
      "not model, because obligation count and risk reduction are different quantities and "
      "collapsing them hides the trade-off.")
    a("")
    rows = []
    for cid, d in sorted(lev.items(), key=lambda kv: (-kv[1]["obligation_count"], kv[0]))[:15]:
        c = library[cid]
        rows.append([cid, c["title"], d["status"], d["obligation_count"],
                     len(d["frameworks"]), " ".join(d["frameworks"]),
                     c["automation_feasibility"]])
    L.extend(md_table(["Control", "Title", "Current status", "Obligations closed",
                       "Frameworks touched", "Which", "Automation rating"], rows))
    a("")

    # ---- 5 evidence ----------------------------------------------------------------
    a("## 5. Evidence burden and reuse")
    a("")
    reuse = []
    for cid, c in library.items():
        if status[cid]["implementation_status"] == "not-applicable":
            continue
        rows_for = [r for r in crosswalk if r["control_id"] == cid]
        fw_hit = {r["framework_key"] for r in rows_for}
        if fw_hit:
            reuse.append((cid, c["title"], len(fw_hit), len(rows_for), c["test_frequency"],
                          c["automation_feasibility"]))
    reuse.sort(key=lambda t: (-t[2], -t[3]))
    total_oblig_refs = sum(t[3] for t in reuse)
    a(f"{len(reuse)} evidence-producing controls are in scope. They carry {total_oblig_refs} "
      f"obligation references across {len(fws)} frameworks — a reuse ratio of "
      f"**{total_oblig_refs / len(reuse):.1f} obligations satisfied per evidence artifact**. "
      "Collecting the same artifact once per framework instead would multiply the collection cost "
      "by roughly that factor. See `docs/evidence-reuse-model.md`.")
    a("")
    L.extend(md_table(
        ["Control", "Title", "Frameworks", "Obligation refs", "Test frequency", "Automation"],
        [list(t) for t in reuse[:12]]))
    a("")
    auto = Counter(int(c["automation_feasibility"]) for cid, c in library.items()
                   if status[cid]["implementation_status"] != "not-applicable")
    a("Automation feasibility distribution across in-scope controls "
      "(5 = evidence generated by machine, 1 = manual by nature):")
    a("")
    L.extend(md_table(["Rating", "Controls", "Share"],
                      [[k, auto[k], f"{auto[k] / sum(auto.values()):.0%}"]
                       for k in sorted(auto, reverse=True)]))
    a("")
    manual = sum(v for k, v in auto.items() if k <= 2)
    a(f"{manual} in-scope controls rate 2 or below, meaning their evidence will be assembled by a "
      "human every cycle regardless of tooling investment. Any automation business case that "
      "promises to eliminate the compliance calendar has mis-scoped these.")
    a("")

    # ---- 6 testing calendar ----------------------------------------------------------
    a("## 6. Testing calendar load")
    a("")
    freq = Counter(c["test_frequency"] for cid, c in library.items()
                   if status[cid]["implementation_status"] != "not-applicable")
    L.extend(md_table(["Test frequency", "Controls"],
                      [[k, v] for k, v in sorted(freq.items(), key=lambda kv: -kv[1])]))
    a("")

    # ---- 7 status ---------------------------------------------------------------------
    a("## 7. Control implementation status")
    a("")
    sc = Counter(status[cid]["implementation_status"] for cid in library)
    L.extend(md_table(["Status", "Controls", "Share"],
                      [[s, sc[s], f"{sc[s] / len(library):.0%}"]
                       for s in STATUS_ORDER if sc[s]]))
    a("")
    stale = []
    for cid, c in library.items():
        lt = status[cid].get("last_tested", "")
        if status[cid]["implementation_status"] in ("implemented", "partial") and not lt:
            stale.append(cid)
    if stale:
        a(f"**Controls asserted as implemented or partial with no recorded test date: "
          f"{', '.join(sorted(stale))}.** An untested control is an assertion, not a control.")
        a("")

    a("---")
    a("")
    a("Mapping strength credit: full 1.0, partial 0.5, supporting 0.0. Implementation credit: "
      "implemented 1.0, partial 0.5, planned and not-implemented 0.0. An obligation is **met** only "
      "at combined credit 1.0. The reasoning behind these weights is in "
      "`docs/mapping-methodology.md` §4.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, help="path to a scope profile JSON file")
    ap.add_argument("--library", default=os.path.join(ROOT, "library", "control-library.csv"))
    ap.add_argument("--crosswalk", default=os.path.join(ROOT, "crosswalk", "crosswalk.csv"))
    ap.add_argument("--out", help="write markdown here instead of stdout")
    ap.add_argument("--fail-on-gap", action="store_true",
                    help="exit 2 if any in-scope obligation is in gap state (for pipeline use)")
    args = ap.parse_args(argv)

    try:
        scope = load_scope(args.scope)
        status_path = scope["status_file"]
        if not os.path.isabs(status_path):
            status_path = os.path.join(ROOT, status_path)
        library, crosswalk, status = build_model(scope, args.library, args.crosswalk, status_path)
    except (ScopeError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not crosswalk:
        print("error: no crosswalk rows matched the declared frameworks; check "
              "in_scope_frameworks keys against crosswalk/crosswalk.csv", file=sys.stderr)
        return 1

    cov = obligation_coverage(crosswalk, status)
    lev = leverage(crosswalk, status, scope["in_scope_frameworks"])
    md = render(scope, library, crosswalk, status, cov, lev)

    if args.out:
        out = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(md)
        gaps = sum(1 for v in cov.values() if v["state"] == "gap")
        print(f"wrote {out} ({len(md.splitlines())} lines, {len(cov)} obligations, {gaps} gaps)")
    else:
        sys.stdout.write(md)

    if args.fail_on_gap and any(v["state"] == "gap" for v in cov.values()):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
