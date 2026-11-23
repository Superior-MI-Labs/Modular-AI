"""Dependency-free structural checks for the generated website."""
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {'index','learn','atlas','architecture','roadmap'}

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(['python3',str(ROOT/'tools/build_site.py')],check=True,cwd=ROOT,capture_output=True)

    def test_every_diagram_has_source_and_generated_svg(self):
        entries=json.loads((ROOT/'diagrams/catalog.json').read_text())
        self.assertEqual(len(entries),20)
        self.assertEqual(len({entry['id'] for entry in entries}),20)
        for entry in entries:
            self.assertTrue((ROOT/entry['source']).is_file(),entry)
            self.assertTrue((ROOT/'.site-dist'/entry['svg']).is_file(),entry)

    def test_all_pages_have_navigation_and_assets(self):
        for page in PAGES:
            html=(ROOT/'.site-dist'/f'{page}.html').read_text()
            for link in PAGES:
                self.assertIn(f'href="{link}.html"',html)
            self.assertIn('assets/site.css',html)
            self.assertIn('assets/site.js',html)
            self.assertNotIn('{{BODY}}',html)
            self.assertIn(f'data-page="{"home" if page=="index" else page}"',html)

    def test_no_node_or_external_build_dependency(self):
        self.assertTrue((ROOT/'.site-dist'/'.nojekyll').exists())
        self.assertTrue((ROOT/'.site-dist'/'diagrams/catalog.json').exists())
        self.assertFalse((ROOT/'.site-dist'/'package.json').exists())

if __name__=='__main__': unittest.main()
