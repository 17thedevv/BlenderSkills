#!/usr/bin/env python3
"""Structural VRM 1.0 audit (NO Blender, NO aesthetic or runtime verification).

Usage:
    python scripts/audit_vrm.py outputs/character_final.vrm \
        --output outputs/reports/vrm_audit.json

Parses the GLB JSON chunk; checks VRM 1.0 extension, required humanoid mapping,
expression preset bindings, and reports exported lookAt / springBone metadata.
Does not parse geometry or certify app playback.
"""

import argparse
import json
import struct
import sys
from pathlib import Path

GLB_HEADER = struct.Struct('<4sII')
CHUNK_HEADER = struct.Struct('<II')
JSON_CHUNK = 0x4E4F534A  # ASCII JSON in GLB little-endian encoding

EXPECTED_PRESETS = (
    'blink', 'blinkLeft', 'blinkRight',
    'aa', 'ih', 'ou', 'ee', 'oh',
    'happy', 'angry', 'sad', 'relaxed', 'surprised',
)
ESSENTIAL_BONES = (
    'hips', 'spine', 'neck', 'head',
    'leftUpperArm', 'leftLowerArm', 'leftHand',
    'rightUpperArm', 'rightLowerArm', 'rightHand',
    'leftUpperLeg', 'leftLowerLeg', 'leftFoot',
    'rightUpperLeg', 'rightLowerLeg', 'rightFoot',
)
EXPR_FIELDS = ('morphTargetBinds', 'materialColorBinds', 'textureTransformBinds')


def read_glb_json(path):
    data = path.read_bytes()
    if len(data) < GLB_HEADER.size + CHUNK_HEADER.size:
        raise ValueError('File is too small to be a GLB container')
    magic, version, length = GLB_HEADER.unpack_from(data)
    if magic != b'glTF' or version != 2:
        raise ValueError('Not a glTF 2.0 GLB; VRM 1.0 requires GLB 2.0')
    if length != len(data):
        raise ValueError(f'GLB header length {length} != actual {len(data)}')
    offset = GLB_HEADER.size
    while offset + CHUNK_HEADER.size <= len(data):
        chunk_len, chunk_type = CHUNK_HEADER.unpack_from(data, offset)
        offset += CHUNK_HEADER.size
        if chunk_len % 4 != 0 or offset + chunk_len > len(data):
            raise ValueError('Invalid GLB chunk alignment or length')
        if chunk_type == JSON_CHUNK:
            try:
                obj = json.loads(data[offset:offset+chunk_len].decode('utf-8').rstrip(' \t\r\n\0'))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError(f'JSON chunk malformed: {exc}') from exc
            if not isinstance(obj, dict):
                raise ValueError('GLB JSON root is not an object')
            return obj
        offset += chunk_len
    raise ValueError('GLB JSON chunk not found')


def audit(doc, source):
    errors, warnings = [], []
    extensions = doc.get('extensions') or {}
    vrm = extensions.get('VRMC_vrm')
    if not isinstance(vrm, dict):
        errors.append('Missing root extensions.VRMC_vrm (not VRM 1.0)')
        vrm = {}
    if vrm.get('specVersion') != '1.0':
        errors.append(f'Unsupported VRM specVersion: {vrm.get("specVersion")!r}')
    if 'VRMC_vrm' not in (doc.get('extensionsUsed') or []):
        warnings.append('VRMC_vrm is not listed in extensionsUsed')
    human_bones = ((vrm.get('humanoid') or {}).get('humanBones') or {})
    nodes = doc.get('nodes') or []
    missing_bones = [n for n in ESSENTIAL_BONES if n not in human_bones]
    if missing_bones:
        errors.append('Missing required target rig bone mappings: '+ ', '.join(missing_bones))
    for name, val in human_bones.items():
        idx = val.get('node') if isinstance(val, dict) else None
        if not isinstance(idx, int) or isinstance(idx,bool) or idx < 0 or idx >= len(nodes):
            errors.append(f'Invalid humanoid bone node mapping: {name} -> {idx}')
    if 'leftEye' not in human_bones or 'rightEye' not in human_bones:
        warnings.append('Eye bones absent or incompletely mapped: bone-based gaze may not work')
    expressions = vrm.get('expressions') or {}
    preset = expressions.get('preset') or {}
    missing_expr = [n for n in EXPECTED_PRESETS if n not in preset]
    if missing_expr:
        errors.append('Missing target expressions: '+', '.join(missing_expr))
    empty_expr = []
    for name in EXPECTED_PRESETS:
        val = preset.get(name)
        if val is None:
            continue
        if not isinstance(val, dict) or not any(val.get(k) for k in EXPR_FIELDS):
            empty_expr.append(name)
    if empty_expr:
        errors.append('Expressions with no morph/material/texture binding: '+', '.join(empty_expr))
    look = vrm.get('lookAt') or {}
    gaze_mode = look.get('type')
    if gaze_mode != 'bone':
        warnings.append(f'Expected bone LookAt for webcam MVP; found {gaze_mode!r}')
    if 'VRMC_springBone' not in extensions:
        warnings.append('No VRMC_springBone extension; static hair is permitted for MVP')
    return {
        'source_file': str(source), 'vrm_spec_version': vrm.get('specVersion'),
        'vrm_1_0_root_present': 'VRMC_vrm' in extensions,
        'humanoid_bone_count': len(human_bones), 'essential_bone_count': len(ESSENTIAL_BONES),
        'missing_essential_bones': missing_bones,
        'required_expression_count': len(EXPECTED_PRESETS),
        'available_target_expressions': [e for e in EXPECTED_PRESETS if e in preset],
        'missing_target_expressions': missing_expr, 'unbound_target_expressions': empty_expr,
        'lookat_type': gaze_mode,
        'spring_bone_extension_present': 'VRMC_springBone' in extensions,
        'warnings': warnings, 'errors': errors,
        'structural_status': 'FAIL' if errors else 'PASS_WITH_WARNINGS' if warnings else 'PASS',
        'visual_quality': 'NOT_TESTED', 'webcam_tracking': 'NOT_TESTED',
        'warudo_import': 'NOT_TESTED', 'obs_capture': 'NOT_TESTED',
    }


def main():
    ap = argparse.ArgumentParser(description='Audit VRM 1.0 GLB structure for anime webcam avatar')
    ap.add_argument('vrm', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    try:
        report = audit(read_glb_json(args.vrm), args.vrm)
    except (OSError, ValueError) as exc:
        report = {'source_file':str(args.vrm), 'structural_status':'FAIL',
                  'errors':[str(exc)], 'visual_quality':'NOT_TESTED',
                  'webcam_tracking':'NOT_TESTED', 'obs_capture':'NOT_TESTED'}
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered+'\n', encoding='utf-8')
    print(rendered)
    sys.exit(0 if report['structural_status'] != 'FAIL' else 1)

if __name__ == '__main__':
    main()
