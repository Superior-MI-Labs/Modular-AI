"""Regression checks for module swapping semantics and artifact identity."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from modular_ai.core.compatibility import validate_manifest  # noqa: E402


class CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / 'registry/reference_modules.json').read_text())

    def manifest(self, name):
        return json.loads((ROOT / 'examples' / f'{name}.json').read_text())

    def test_baseline_and_policy_swap(self):
        baseline = self.manifest('decision_baseline')
        self.assertEqual(validate_manifest(baseline, self.registry).status, 'compatible')
        baseline['workflow']['slots']['policy'] = 'ref.policy.utility_alternative@1'
        self.assertEqual(validate_manifest(baseline, self.registry).status, 'compatible')

    def test_vad_state_requires_matching_policy(self):
        manifest = self.manifest('decision_baseline')
        manifest['workflow']['slots']['state_encoder'] = 'ref.state_encoder.vad@1'
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')
        manifest['workflow']['slots']['policy'] = 'ref.policy.vad_utility@1'
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'compatible')
        del manifest['workflow']['slots']['state_encoder']
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')

    def test_schema_identical_different_vocabulary_is_not_safe(self):
        manifest = self.manifest('text_autoregressive')
        manifest['workflow']['slots']['tokenizer'] = 'ref.tokenizer.custom_demo@1'
        report = validate_manifest(manifest, self.registry)
        self.assertEqual(report.status, 'migration')
        self.assertTrue(any(d.code == 'artifact-mismatch' for d in report.diagnostics))
        self.assertTrue(all(link['matches'] for link in report.connections))

    def test_image_and_video_codec_identity_changes_require_migration(self):
        for filename, module_id in (
            ('image_diffusion', 'ref.codec.image_alt@1'),
            ('video_diffusion', 'ref.codec.video_alt@1'),
        ):
            with self.subTest(filename=filename):
                manifest = self.manifest(filename)
                manifest['workflow']['slots']['codec'] = module_id
                self.assertEqual(validate_manifest(manifest, self.registry).status, 'migration')

    def test_wrong_family_and_slot_category_rejected(self):
        manifest = self.manifest('image_diffusion')
        manifest['workflow']['slots']['codec'] = 'ref.codec.video@1'
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')
        manifest['workflow']['slots']['codec'] = 'ref.policy.utility@1'
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')

    def test_missing_slot_and_unknown_module_rejected(self):
        manifest = self.manifest('decision_baseline')
        del manifest['workflow']['slots']['evaluator']
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')
        manifest['workflow']['slots']['evaluator'] = 'ref.evaluator.nonexistent@1'
        self.assertEqual(validate_manifest(manifest, self.registry).status, 'incompatible')

    def test_evaluator_wiring_is_validated(self):
        manifest = self.manifest('decision_baseline')
        registry = copy.deepcopy(self.registry)
        registry['modules']['ref.environment.toy@1']['output']['episode'] = 'wrong.episode@1'
        report = validate_manifest(manifest, registry)
        self.assertEqual(report.status, 'incompatible')
        self.assertIn('environment.episode', ' '.join(d.message for d in report.diagnostics))

    def test_missing_real_artifacts_are_not_claimed_safe(self):
        for name in ('text_autoregressive', 'image_diffusion', 'video_diffusion'):
            with self.subTest(name=name):
                report = validate_manifest(self.manifest(name), self.registry)
                self.assertEqual(report.status, 'unverified')
                self.assertTrue(any(d.code == 'unresolved-artifact' for d in report.diagnostics))


if __name__ == '__main__':
    unittest.main()
