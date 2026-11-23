#!/usr/bin/env python3
"""Publish a dependency-light static website from one set of diagram sources."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.site-dist'
PAGES = {'index':'Overview', 'learn':'Visual learning', 'atlas':'Diagram atlas',
         'architecture':'Architecture', 'roadmap':'Roadmap'}


def build():
    subprocess.run(['python3',str(ROOT/'tools/export_svg.py')],check=True,cwd=ROOT)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    layout = (ROOT/'site/layout.html').read_text(encoding='utf-8')
    for page, title in PAGES.items():
        body = (ROOT/f'site/pages/{page}.html').read_text(encoding='utf-8')
        html = layout.replace('{{TITLE}}',title).replace('{{PAGE}}', 'home' if page=='index' else page).replace('{{BODY}}',body)
        (OUTPUT/f'{page}.html').write_text(html,encoding='utf-8')
    shutil.copytree(ROOT/'site/assets',OUTPUT/'assets')
    diagrams = OUTPUT/'diagrams'
    diagrams.mkdir()
    for folder in ('svg','mermaid'):
        shutil.copytree(ROOT/'diagrams'/folder,diagrams/folder)
    shutil.copy2(ROOT/'diagrams/catalog.json',diagrams/'catalog.json')
    (OUTPUT/'.nojekyll').touch()
    print(f'Generated {len(PAGES)} pages and {len(list((diagrams/"svg").glob("*.svg")))} diagrams at {OUTPUT}')

if __name__=='__main__': build()
