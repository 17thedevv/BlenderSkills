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
    def make_state(self, root, **extra):
        (root / 'candidate.blend').write_bytes(b'fixture')
        d={'project':'Kagari','current_gate':'CLAY','current_candidate':{'path':'candidate.blend','sha256':hashlib.sha256(b'fixture').hexdigest(),'version':'fixture-v1'},'approvals':{}}
        d.update(extra)
        state=root/'state.json'
        state.write_text(json.dumps(d))
        return state,d

    def test_modified_candidate_hash_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state,_=self.make_state(root)
            (root/'candidate.blend').write_bytes(b'changed')
            errors,_=m.validate(root,state)
            self.assertTrue(any('hash mismatch' in e for e in errors))

    def test_reference_path_escape_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state,_=self.make_state(root,reference_files=['../outside.png'])
            errors,_=m.validate(root,state)
            self.assertTrue(any('outside workspace' in e for e in errors))

    def test_delivery_different_version_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state,d=self.make_state(root,delivery_manifest='DELIVERY.md')
            block={'candidate_path':'candidate.blend','candidate_sha256':d['current_candidate']['sha256'],'candidate_version':'stale-v0','decision':None}
            (root/'DELIVERY.md').write_text('<!-- PROJECT_STATE_BEGIN -->\n```json\n'+json.dumps(block)+'\n```\n<!-- PROJECT_STATE_END -->')
            errors,_=m.validate(root,state)
            self.assertTrue(any('differs' in e for e in errors))

    def test_broken_delivery_link_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state,d=self.make_state(root,delivery_manifest='DELIVERY.md')
            block={'candidate_path':'candidate.blend','candidate_sha256':d['current_candidate']['sha256'],'candidate_version':'fixture-v1','decision':None}
            (root/'DELIVERY.md').write_text('<!-- PROJECT_STATE_BEGIN -->\n```json\n'+json.dumps(block)+'\n```\n<!-- PROJECT_STATE_END -->\n[broken](missing.png)')
            errors,_=m.validate(root,state)
            self.assertTrue(any('broken' in e for e in errors))

    def test_stale_evidence_hash_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state,_=self.make_state(root,artifact_records=[{'path':'candidate.blend','sha256':'0'*64}])
            errors,_=m.validate(root,state)
            self.assertTrue(any('artifact_records[0]: hash mismatch' in e for e in errors))

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
            state.write_text(json.dumps({"project": "Kagari", "current_gate": "B", "current_candidate": {"path": "candidate.blend", "sha256": h, "version": "fixture-v1"}, "approvals": {"garment_clay": {"status": "NOT_APPROVED", "evidence": None}}}))
            errors, _ = m.validate(root, state)
            self.assertEqual(errors, [])

    def test_unbacked_approval_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "candidate.blend").write_bytes(b"fixture")
            h = hashlib.sha256(b"fixture").hexdigest()
            state = root / "state.json"
            state.write_text(json.dumps({"project": "Kagari", "current_gate": "B", "current_candidate": {"path": "candidate.blend", "sha256": h, "version": "fixture-v1"}, "approvals": {"garment_clay": {"status": "APPROVED_BY_USER", "evidence": None}}}))
            errors, _ = m.validate(root, state)
            self.assertTrue(any("approvals.garment_clay.evidence" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
