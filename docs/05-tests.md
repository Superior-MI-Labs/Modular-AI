# 05 — Tests and quality gates

## Minimum v1 tests (no neural models needed)

1. Registry resolves immutable module IDs/versions and rejects duplicate IDs.
2. Validator rejects wrong semantic schema even if dimensions match; rejects unknown units, missing codecs, mismatched tokenizer hashes.
3. Configuration validation rejects malformed profiles, unrecognized workflow IDs, invalid module capabilities and unsupported backend requests.
4. Deterministic decision baseline produces the same action/score for equal observation + seed, with documented tie-breaks.
5. Environment episode reproduces terminal conditions, `terminated` vs `truncated`, reset seed and bounded steps.
6. Incompatible neural policy and environment action spaces fail **before** model allocation.
7. Replace one compatible deterministic policy and confirm same valid action format, different behavior where expected.
8. Snapshot/resume preserves run state only for declared stateful modules.
9. Artifact lineage records config and module hashes and links parent → optimized derivative without mutating parent.
10. Every optimizer/quantization path has a reference-quality report and hardware resource report.

## Later, once actual neural implementations exist

- Property and shape tests, finite values/NaN detection, gradient checks for trainable modules.
- Precision tolerance checks FP32 vs BF16/FP16 vs quantized; per-family quality thresholds.
- Tokenizer round-trip and special-token invariants.
- Image/VAE codec reconstruction and latent-scale tests.
- Video frame order, FPS/timebase, temporal latent shapes, clip boundary tests.
- Diffusion deterministic sampling with fixed RNG and matching scheduler parameterization.
- Training reproducibility (within explicit numerical tolerances), resume from step N, fixed-holdout evaluation.
- Hardware availability, fallbacks, out-of-memory failure/recovery, batch limits.
- Golden task cases, measurement of memory peak, throughput, latency and energy when available.

## Stop gates

**Gate 1:** one deterministic end-to-end episode and contract validator. **Gate 2:** configurable policy swap with reproducible before/after evidence. **Gate 3:** one tiny trainable model, checkpoint/resume and evaluator. **Gate 4:** optimization artifacts with independent benchmarking. **Gate 5:** image pipeline; **Gate 6:** temporal video pipeline. New abstractions must justify themselves by removing duplication or enabling a verified swap.
