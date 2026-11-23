#!/usr/bin/env python3
"""Validate illustrative manifests via the *same* contract checker used by the site.

The examples are not runnable model artifacts. An `unverified` result is expected
for language/image/video examples that deliberately lack actual checkpoints.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from modular_ai.core.compatibility import validate_manifest  # noqa: E402

REGISTRY = json.loads((ROOT / 'registry/reference_modules.json').read_text())
SCHEMA = json.loads((ROOT / 'schemas/experiment.schema.json').read_text())
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None


def verify(path: Path) -> tuple[str, str]:
    manifest = json.loads(path.read_text())
    if Draft202012Validator is not None:
        Draft202012Validator(SCHEMA).validate(manifest)
    assert manifest['schema_version'] == 1
    assert manifest['experiment_id']
    report = validate_manifest(manifest, REGISTRY)
    assert report.status in ('compatible', 'unverified'), (path.name, report)
    return manifest['experiment_id'], report.status


if __name__ == '__main__':
    files = sorted((ROOT / 'examples').glob('*.json'))
    for f in files:
        name, status = verify(f)
        print('PASS', name, f'({status})')
    mermaids = sorted((ROOT / 'diagrams/mermaid').glob('*.mmd'))
    svgs = sorted((ROOT / 'diagrams/svg').glob('*.svg'))
    assert len(mermaids) == 20 and len(svgs) == 20
    assert {x.stem for x in mermaids} == {x.stem for x in svgs}
    print(f'PASS {len(files)} sample manifests, {len(mermaids)} Mermaid and SVG diagrams')
