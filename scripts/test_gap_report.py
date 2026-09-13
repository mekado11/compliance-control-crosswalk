#!/usr/bin/env python3
"""Self-tests for gap_report.py. Standard library only; run with: python3 scripts/test_gap_report.py

These are not exhaustive unit tests. They check the properties that, if broken, would make the
report quietly wrong rather than loudly broken - which is the failure mode that matters for a
compliance artifact.
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import gap_report as gr  # noqa: E402

LIB = os.path.join(ROOT, "library", "control-library.csv")
XW = os.path.join(ROOT, "crosswalk", "crosswalk.csv")
STATUS = os.path.join(ROOT, "examples", "implementation-status.csv")
SCOPES = [os.path.join(ROOT, "examples", f) for f in
          ("scope-profile-core.json", "scope-profile-fedramp-pursuit.json",
           "scope-profile-ot-division.json")]


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class TestDataIntegrity(unittest.TestCase):
    def test_library_ids_unique(self):
        ids = [r["control_id"] for r in rows(LIB)]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_control_has_evidence_and_test(self):
        for r in rows(LIB):
            self.assertTrue(r["evidence_requirement"].strip(), r["control_id"])
            self.assertTrue(r["test_procedure"].strip(), r["control_id"])
            self.assertTrue(r["owner_role"].strip(), r["control_id"])
            self.assertIn(int(r["automation_feasibility"]), range(1, 6))

    def test_crosswalk_references_known_controls(self):
        known = {r["control_id"] for r in rows(LIB)}
        for r in rows(XW):
            self.assertIn(r["control_id"], known)
            self.assertIn(r["mapping_strength"], ("full", "partial", "supporting"))

    def test_status_covers_library(self):
        self.assertEqual({r["control_id"] for r in rows(LIB)},
                         {r["control_id"] for r in rows(STATUS)})

    def test_every_control_maps_somewhere(self):
        mapped = {r["control_id"] for r in rows(XW)}
        self.assertEqual(mapped, {r["control_id"] for r in rows(LIB)})


class TestScoring(unittest.TestCase):
    def test_supporting_mapping_never_closes_an_obligation(self):
        xw = [{"control_id": "X", "framework_key": "ISO", "framework_control_id": "A.1",
               "mapping_strength": "supporting"}]
        status = {"X": {"implementation_status": "implemented"}}
        cov = gr.obligation_coverage(xw, status)
        self.assertEqual(cov[("ISO", "A.1")]["state"], "gap")

    def test_partial_implementation_of_full_mapping_is_partial(self):
        xw = [{"control_id": "X", "framework_key": "ISO", "framework_control_id": "A.1",
               "mapping_strength": "full"}]
        cov = gr.obligation_coverage(xw, {"X": {"implementation_status": "partial"}})
        self.assertEqual(cov[("ISO", "A.1")]["state"], "partial")

    def test_best_contributing_control_wins(self):
        xw = [{"control_id": "X", "framework_key": "ISO", "framework_control_id": "A.1",
               "mapping_strength": "partial"},
              {"control_id": "Y", "framework_key": "ISO", "framework_control_id": "A.1",
               "mapping_strength": "full"}]
        status = {"X": {"implementation_status": "implemented"},
                  "Y": {"implementation_status": "implemented"}}
        cov = gr.obligation_coverage(xw, status)
        self.assertEqual(cov[("ISO", "A.1")]["state"], "met")

    def test_not_applicable_is_excluded_not_failed(self):
        xw = [{"control_id": "X", "framework_key": "ISO", "framework_control_id": "A.1",
               "mapping_strength": "full"}]
        cov = gr.obligation_coverage(xw, {"X": {"implementation_status": "not-applicable"}})
        self.assertNotIn(("ISO", "A.1"), cov)


class TestScopeValidation(unittest.TestCase):
    def _write(self, obj):
        fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(obj, fh)
        fh.close()
        return fh.name

    def test_missing_key_rejected(self):
        with self.assertRaises(gr.ScopeError):
            gr.load_scope(self._write({"profile_name": "x"}))

    def test_empty_framework_list_rejected(self):
        with self.assertRaises(gr.ScopeError):
            gr.load_scope(self._write({"profile_name": "x", "in_scope_frameworks": [],
                                       "status_file": STATUS}))

    def test_unknown_excluded_control_rejected(self):
        scope = gr.load_scope(SCOPES[0])
        scope["excluded_controls"] = {"ZZ-99": "typo"}
        with self.assertRaises(gr.ScopeError):
            gr.build_model(scope, LIB, XW, STATUS)


class TestEndToEnd(unittest.TestCase):
    def test_all_example_profiles_render(self):
        for scope_path in SCOPES:
            with tempfile.TemporaryDirectory() as d:
                out = os.path.join(d, "r.md")
                rc = subprocess.call(
                    [sys.executable, os.path.join(ROOT, "scripts", "gap_report.py"),
                     "--scope", scope_path, "--out", out],
                    stdout=subprocess.DEVNULL)
                self.assertEqual(rc, 0, scope_path)
                body = open(out, encoding="utf-8").read()
                self.assertIn("## 1. Summary", body)
                self.assertIn("## 5. Evidence burden and reuse", body)
                self.assertGreater(len(body.splitlines()), 100)

    def test_fail_on_gap_exit_code(self):
        rc = subprocess.call(
            [sys.executable, os.path.join(ROOT, "scripts", "gap_report.py"),
             "--scope", SCOPES[0], "--fail-on-gap"],
            stdout=subprocess.DEVNULL)
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
