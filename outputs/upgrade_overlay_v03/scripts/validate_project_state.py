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
    p = actual_file(root, candidate.get("path"), errors, "current_candidate")
    digest = candidate.get("sha256")
    if p:
        if not digest:
            errors.append("current_candidate: missing sha256")
        elif digest.lower() != sha256(p):
            errors.append("current_candidate: hash mismatch (stale artifact or changed file)")
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
    if not data.get("current_gate"):
        errors.append("current_gate missing")
    if data.get("blocking_issues"):
        warnings.append("blocking_issues remain; this does not invalidate unrelated technical references")
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
