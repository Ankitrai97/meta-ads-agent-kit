import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("project", ROOT / "scripts" / "project.py")
project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project)


class CampaignRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")
        self.run = project.init_run(self.root, "example-hvac", "live")
        self.state = project.load_state(self.run)

    def ready(self):
        state = copy.deepcopy(self.state)
        state["configuration"] = {
            "business": {"name": "Example HVAC", "service": "Replacement estimates", "service_area": ["Example suburb"], "customer": "Residents requesting estimates", "offer": "No special offer", "capacity": 5},
            "account": {"id": "example-account", "page_id": "example-page", "currency": "USD", "timezone": "America/Chicago"},
            "budget": {"amount": 20, "type": "daily", "currency": "USD", "start": "2030-06-01T08:00:00-05:00", "end": "2030-06-08T08:00:00-05:00", "max_total": 200},
            "settings": {"objective": "LEADS", "geography": ["Example suburb"], "audience": "Reviewed supported audience", "placements": "Reviewed placements", "optimization": "Leads", "category": "Actual applicability checked"},
            "destination": {"type": "instant_form", "reference": "example-form", "privacy_url": "https://example.com/privacy"},
            "ads": [{"id": "example-ad", "concept": "Replacement process", "copy": "Approved example copy", "asset": "approved-image-sha256:example", "destination": "example-form"}],
            "objects": [{"kind": kind, "id": identity, "status": "PAUSED"} for kind, identity in (("campaign", "example-campaign"), ("ad_set", "example-ad-set"), ("ad", "example-ad"))],
            "lead_route": {"owner": "Example owner", "method": "Approved manual follow-up", "destination": "Private lead tool", "response_expectation": "Agreed business hours"},
        }
        for name in project.CHECKS:
            evidence = f"evidence/{name}.md"
            (self.run / evidence).write_text("Synthetic test fixture: not real external verification.\n", encoding="utf-8")
            state["checks"][name] = {"passed": True, "evidence": evidence}
        state["approval"] = {"decision": "activate", "by": "Synthetic owner fixture", "at": "2030-05-31T12:00:00-05:00", "source": "Synthetic test approval, not a real decision", "config_sha256": project.config_digest(state)}
        return state

    def test_new_run_is_incomplete_and_defaults_to_demo(self):
        run = project.init_run(self.root, "second-business")
        state = project.load_state(run)
        self.assertEqual(state["mode"], "demo")
        self.assertTrue(project.validate_state(state, run))
        self.assertIsNone(state["approval"]["decision"])
        self.assertTrue((run / "NEXT.md").is_file())

    def test_init_does_not_overwrite_existing_work(self):
        sentinel = self.run / "brief.md"
        sentinel.write_text("Owner's saved answers", encoding="utf-8")
        with self.assertRaises(ValueError):
            project.init_run(self.root, "example-hvac")
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "Owner's saved answers")

    def test_slug_cannot_escape_workspace_or_use_reserved_names(self):
        for slug in ("../outside", "C:\\outside", "a/b", "UPPER", "con", "nul", "lpt1", "a" * 64):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                project.run_path(self.root, slug)

    def test_complete_local_records_pass_both_checks(self):
        state = self.ready()
        self.assertEqual(project.validate_state(state, self.run), [])
        self.assertEqual(project.validate_state(state, self.run, launch=True), [])

    def test_demo_can_be_prepared_but_cannot_launch(self):
        state = self.ready()
        state["mode"] = "demo"
        self.assertEqual(project.validate_state(state, self.run), [])
        self.assertTrue(any("Demo mode" in e for e in project.validate_state(state, self.run, True)))

    def test_configuration_change_invalidates_approval(self):
        for group, key, value in (("budget", "amount", 25), ("destination", "reference", "other-form"), ("lead_route", "destination", "other-crm")):
            state = self.ready()
            state["configuration"][group][key] = value
            with self.subTest(group=group):
                self.assertTrue(any("stale" in e for e in project.validate_state(state, self.run, True)))

    def test_asset_version_change_invalidates_approval(self):
        state = self.ready()
        state["configuration"]["ads"][0]["asset"] = "new-version"
        self.assertTrue(any("stale" in e for e in project.validate_state(state, self.run, True)))

    def test_progress_updates_do_not_change_configuration_digest(self):
        state = self.ready()
        previous = project.config_digest(state)
        state["stage"] = "review"
        self.assertEqual(project.config_digest(state), previous)

    def test_missing_empty_or_outside_evidence_blocks_readiness(self):
        state = self.ready()
        for evidence in (None, "evidence/missing.md", "../outside.md", str((self.run / "brief.md").resolve())):
            with self.subTest(evidence=evidence):
                state["checks"]["lead_test_passed"]["evidence"] = evidence
                self.assertTrue(any("lead_test_passed" in e for e in project.validate_state(state, self.run)))
        (self.run / "evidence" / "empty.md").touch()
        state["checks"]["lead_test_passed"]["evidence"] = "evidence/empty.md"
        self.assertTrue(project.validate_state(state, self.run))

    def test_truthy_strings_do_not_pass_a_check(self):
        state = self.ready()
        state["checks"]["lead_test_passed"]["passed"] = "true"
        self.assertTrue(any("Not verified: lead_test_passed" in e for e in project.validate_state(state, self.run)))

    def test_active_objects_block_prelaunch_review(self):
        state = self.ready()
        state["configuration"]["objects"][0]["status"] = "ACTIVE"
        self.assertTrue(any("PAUSED" in e for e in project.validate_state(state, self.run)))

    def test_missing_or_wrong_ad_mapping_is_detected(self):
        state = self.ready()
        state["configuration"]["ads"][0]["id"] = "different-ad"
        self.assertTrue(any("match the saved ad IDs" in e for e in project.validate_state(state, self.run)))
        state["configuration"]["objects"].pop()
        self.assertTrue(any("include campaign" in e for e in project.validate_state(state, self.run)))

    def test_invalid_spend_and_currency_are_blocked(self):
        for value in (True, -1, 0, float("nan"), float("inf"), "20"):
            state = self.ready()
            state["configuration"]["budget"]["amount"] = value
            with self.subTest(value=value):
                self.assertTrue(any("budget.amount" in e for e in project.validate_state(state, self.run)))
        state = self.ready()
        state["configuration"]["budget"]["amount"] = 500
        state["configuration"]["budget"]["currency"] = "EUR"
        errors = project.validate_state(state, self.run)
        self.assertTrue(any("exceeds" in e for e in errors))
        self.assertTrue(any("match the actual account currency" in e for e in errors))

    def test_dates_need_offsets_and_order(self):
        state = self.ready()
        state["configuration"]["budget"]["start"] = "2030-06-01"
        self.assertTrue(any("timezone offsets" in e for e in project.validate_state(state, self.run)))
        state["configuration"]["budget"]["start"] = "2031-06-01T00:00:00Z"
        self.assertTrue(any("later than start" in e for e in project.validate_state(state, self.run)))

    def test_malformed_groups_are_reported_instead_of_crashing(self):
        for group in ("business", "settings", "account", "budget", "destination", "lead_route"):
            state = self.ready()
            state["configuration"][group] = []
            with self.subTest(group=group):
                self.assertTrue(project.validate_state(state, self.run))
        for value in (None, {}, [], "https://[invalid"):
            state = self.ready()
            state["configuration"]["destination"]["privacy_url"] = value
            self.assertTrue(project.validate_state(state, self.run))

    def test_no_owner_approval_is_not_launch_ready(self):
        state = self.ready()
        state["approval"] = {}
        self.assertEqual(project.validate_state(state, self.run), [])
        self.assertTrue(any("owner decision" in e for e in project.validate_state(state, self.run, True)))

    def test_bom_state_files_can_be_read(self):
        (self.run / "state.json").write_text(json.dumps(self.state), encoding="utf-8-sig")
        self.assertEqual(project.load_state(self.run), self.state)

    def test_documented_cli_runs_in_an_isolated_workspace(self):
        (self.root / "scripts").mkdir()
        script = self.root / "scripts" / "project.py"
        shutil.copyfile(ROOT / "scripts" / "project.py", script)
        for args, code in ((["init", "cli-demo"], 0), (["status", "cli-demo"], 0), (["check", "cli-demo"], 1), (["check", "cli-demo", "--launch"], 1)):
            result = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, check=False)
            with self.subTest(args=args):
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertIn("Demo mode cannot", result.stdout)


if __name__ == "__main__":
    unittest.main()
