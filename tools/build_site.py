#!/usr/bin/env python3
"""Build a dependency-light static site and a read-only contract explorer."""
from __future__ import annotations

from itertools import product
from pathlib import Path
import copy
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from modular_ai.core.compatibility import validate_manifest  # noqa: E402

OUTPUT = ROOT / '.site-dist'
PAGES = {'index': 'Overview', 'learn': 'Visual learning', 'atlas': 'Diagram atlas',
         'swap': 'Module lab', 'architecture': 'Architecture', 'core': 'Core plan',
         'roadmap': 'Roadmap'}
EXPERIMENTS = (
    ('decision_baseline', 'Decision system', 'Try a VAD state encoder with or without a matching policy.'),
    ('text_autoregressive', 'Language system', 'Compare sampling strategies and a tokenizer identity change.'),
    ('image_diffusion', 'Image generation', 'Check latent codec and denoiser requirements.'),
    ('video_diffusion', 'Video generation', 'Check temporal representations and codec dependencies.'),
)


def build_explorer(output: Path) -> int:
    """Precompute a *bounded* collection of outcomes using the Python validator.

    Browser code only presents results; it does not implement a competing checker.
    This is a demonstration against the reference registry, not arbitrary plugins.
    """
    registry = json.loads((ROOT / 'registry/reference_modules.json').read_text())
    definitions = registry['modules']
    workflows = []
    for filename, title, subtitle in EXPERIMENTS:
        base = json.loads((ROOT / 'examples' / f'{filename}.json').read_text())
        wf_id = base['workflow']['use']
        definition = definitions[wf_id]
        names = definition['slots'] + definition.get('optional_slots', [])
        slots = []
        for name in names:
            category = definition['slot_categories'][name]
            options = [dict(id=module_id, label=module_id.removeprefix('ref.').replace('@1', ''))
                       for module_id, spec in definitions.items() if spec['category'] == category]
            if name in definition.get('optional_slots', []):
                options.insert(0, dict(id='', label='None (direct input)'))
            slots.append(dict(name=name, category=category, options=options))
        combinations = 1
        for slot in slots:
            combinations *= len(slot['options'])
        if combinations > 512:
            raise ValueError(f'{filename} has {combinations} permutations; curate demo options to avoid combinatorial growth')
        cases = {}
        for choice in product(*(s['options'] for s in slots)):
            selected = {s['name']: m['id'] for s, m in zip(slots, choice) if m['id']}
            candidate = copy.deepcopy(base)
            candidate['workflow']['slots'] = selected
            key = json.dumps([m['id'] for m in choice], separators=(',', ':'))
            cases[key] = validate_manifest(candidate, registry).as_dict()
        workflows.append(dict(id=filename, title=title, subtitle=subtitle,
                              slots=slots, defaults=base['workflow']['slots'], cases=cases))
    (output / 'data').mkdir()
    (output / 'data' / 'compatibility.json').write_text(
        json.dumps({'note': 'Design-time contract checks only; not a running AI system.',
                    'workflows': workflows}, indent=2) + '\n', encoding='utf-8')
    return sum(len(w['cases']) for w in workflows)


def build():
    subprocess.run(['python3', str(ROOT / 'tools/export_svg.py')], check=True, cwd=ROOT)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    layout = (ROOT / 'site/layout.html').read_text(encoding='utf-8')
    for page, title in PAGES.items():
        body = (ROOT / f'site/pages/{page}.html').read_text(encoding='utf-8')
        html = layout.replace('{{TITLE}}', title).replace('{{PAGE}}', 'home' if page == 'index' else page).replace('{{BODY}}', body)
        (OUTPUT / f'{page}.html').write_text(html, encoding='utf-8')
    shutil.copytree(ROOT / 'site/assets', OUTPUT / 'assets')
    diagrams = OUTPUT / 'diagrams'
    diagrams.mkdir()
    for folder in ('svg', 'mermaid'):
        shutil.copytree(ROOT / 'diagrams' / folder, diagrams / folder)
    shutil.copy2(ROOT / 'diagrams/catalog.json', diagrams / 'catalog.json')
    count = build_explorer(OUTPUT)
    (OUTPUT / '.nojekyll').touch()
    print(f'Generated {len(PAGES)} pages, {len(list((diagrams/"svg").glob("*.svg")))} diagrams and {count} compatibility scenarios at {OUTPUT}')


if __name__ == '__main__':
    build()
