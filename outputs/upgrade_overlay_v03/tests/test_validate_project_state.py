"""Run: python -m unittest discover -s tests -v"""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "validate_project_state.py"
spec = importlib.util.spec_from_file_location("validate_state", MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ValidationTests(unittest.TestCase):
    def test_missing_candidate_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "state.json"
            state.write_text(json.dumps({"project": "Kagari", "current_gate": "B", "current_candidate": {"path": "missing.blend", "sha256": "abc"}, "approvals": {}}))
            errors, _ = m.validate(root, state)
            self.assertTrue(any("nonexistent" in e for e in errors))

    def test_valid_hashed_candidate_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "candidate.blend").write_bytes(b"fixture")
            h = hashlib.sha256(b"fixture").hexdigest()
            state = root / "state.json"
            state.write_text(json.dumps({"project": "Kagari", "current_gate": "B", "current_candidate": {"path": "candidate.blend", "sha256": h}, "approvals": {"garment_clay": {"status": "NOT_APPROVED", "evidence": None}}}))
            errors, _ = m.validate(root, state)
            self.assertEqual(errors, [])

    def test_unbacked_approval_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "candidate.blend").write_bytes(b"fixture")
            h = hashlib.sha256(b"fixture").hexdigest()
            state = root / "state.json"
            state.write_text(json.dumps({"project": "Kagari", "current_gate": "B", "current_candidate": {"path": "candidate.blend", "sha256": h}, "approvals": {"garment_clay": {"status": "APPROVED_BY_USER", "evidence": None}}}))
            errors, _ = m.validate(root, state)
            self.assertTrue(any("approvals.garment_clay.evidence" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
