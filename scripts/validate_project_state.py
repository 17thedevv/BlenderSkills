"""Validate project artifact/evidence references independently of structural Skills checks.

Usage:
 python scripts/validate_project_state.py --root path/to/your/repo --state config/project_state.json

Strict rules: if an approval says APPROVED_BY_USER it MUST link to actual evidence.
A missing current candidate cannot be validated as a production artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

APPROVED = "APPROVED_BY_USER"
STATUS = {"PENDING_EVIDENCE", "NOT_APPROVED", "NOT_TESTED", "APPROVED_BY_USER", "REJECTED_BY_USER"}


def actual_file(root: Path, raw: str | None, issues: list[str], label: str) -> Path | None:
    if not raw or not isinstance(raw, str):
        issues.append(f"{label}: missing path")
        return None
    p = (root / raw).resolve()
    try:
        p.relative_to(root)
    except ValueError:
        issues.append(f"{label}: path outside workspace: {raw}")
        return None
    if not p.is_file():
        issues.append(f"{label}: nonexistent file: {raw}")
        return None
    return p


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def hashed_artifact(root, record, errors, label):
    if not isinstance(record, dict):
        errors.append(f'{label}: expected object')
        return None
    p = actual_file(root, record.get('path'), errors, label)
    digest = record.get('sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
        errors.append(f'{label}: invalid or missing sha256')
    elif p and digest.lower() != sha256(p):
        errors.append(f'{label}: hash mismatch (stale artifact or changed file)')
    return p


def validate(root: Path, state_path: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"state load failed: {exc}"], []
    if data.get("project") != "Kagari":
        errors.append("wrong project name: expected Kagari")
    candidate = data.get("current_candidate", {})
    if not isinstance(candidate, dict):
        candidate = {}
        errors.append("current_candidate must be object")
    p = hashed_artifact(root, candidate, errors, 'current_candidate')
    if not isinstance(candidate.get('version'), str) or not candidate['version'].strip():
        errors.append('current_candidate: missing version')
    if data.get('baseline') is not None:
        hashed_artifact(root, data['baseline'], errors, 'baseline')
    for i, record in enumerate(data.get('artifact_records', [])):
        hashed_artifact(root, record, errors, f'artifact_records[{i}]')
    for i, e in enumerate(data.get("evidence", [])):
        if not isinstance(e, str):
            errors.append(f"evidence[{i}]: expected path string")
        else:
            actual_file(root, e, errors, f"evidence[{i}]")
    for i, ref in enumerate(data.get("reference_files", [])):
        if not isinstance(ref, str):
            errors.append(f"reference_files[{i}]: expected path string")
        else:
            actual_file(root, ref, errors, f"reference_files[{i}]")
    for gate, approval in data.get("approvals", {}).items():
        if not isinstance(approval, dict):
            errors.append(f"approvals.{gate}: expected object")
            continue
        status = approval.get("status")
        if status not in STATUS:
            errors.append(f"approvals.{gate}: invalid status {status}")
        if status == APPROVED:
            actual_file(root, approval.get("evidence"), errors, f"approvals.{gate}.evidence")
            if approval.get('evidence_type') not in {'user_message', 'user_signed_file'}:
                errors.append(f'approvals.{gate}: explicit user evidence_type required')
            if not re.fullmatch(r'[0-9a-fA-F]{64}', str(approval.get('artifact_sha256', ''))):
                errors.append(f'approvals.{gate}: reviewed artifact_sha256 required')
    if data.get('delivery_manifest'):
        delivery = actual_file(root, data['delivery_manifest'], errors, 'delivery_manifest')
        if delivery:
            text = delivery.read_text(encoding='utf-8-sig')
            matches = re.findall(r'<!-- PROJECT_STATE_BEGIN -->\s*```json\s*(.*?)\s*```\s*<!-- PROJECT_STATE_END -->', text, re.S)
            if len(matches) != 1:
                errors.append('DELIVERY: exactly one project state block required')
            else:
                try:
                    block = json.loads(matches[0])
                    expected = {'candidate_path': candidate.get('path'), 'candidate_sha256': candidate.get('sha256'),
                                'candidate_version': candidate.get('version'), 'decision': data.get('decision')}
                    if block != expected:
                        errors.append('DELIVERY: artifact/version/SHA/decision differs from project state')
                except (ValueError, TypeError):
                    errors.append('DELIVERY: invalid project state JSON block')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if re.match(r'https?://|mailto:', target):
                    continue
                if target.startswith('file://'):
                    errors.append('DELIVERY: use workspace-relative links instead of stale file URIs')
                    continue
                link = (delivery.parent / target.split('#')[0]).resolve()
                if not link.is_relative_to(root) or not link.is_file():
                    errors.append(f'DELIVERY: broken or outside-workspace link: {target}')
    if not data.get("current_gate"):
        errors.append("current_gate missing")
    if data.get("blocking_issues"):
        warnings.append("blocking_issues remain; this does not invalidate unrelated technical references")
    pending = [g for g, a in data.get('approvals', {}).items() if isinstance(a, dict) and a.get('status') != APPROVED]
    if pending:
        warnings.append('Human/runtime stages not approved: ' + ', '.join(pending))
    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--state", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    state = Path(args.state)
    if not state.is_absolute():
        state = root / state
    errors, warnings = validate(root, state)
    print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors,
                      "warnings": warnings}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
