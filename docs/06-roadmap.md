# 06 — Implementation roadmap (planned, not progress claimed)

| Milestone | Deliverable | Exit criterion |
|---|---|---|
| 0. Architecture | Contracts, examples, diagrams, invariants | Reviewed and approved; no ambiguity in port ownership |
| 1. Baseline kernel | Registry, validator, immutable experiment manifest, tiny episode runner | One deterministic environment/policy passes tests |
| 2. Real swapping | Two policies using one state/action schema, comparable runs | Tested change via config only; unsupported change rejected |
| 3. Neural training | Tiny trainable policy or predictor, dataset, trainer, checkpoint, evaluator | Train→resume→evaluate verified |
| 4. Optimization | Precision policy, one quantization path, immutable derivatives | Quality/latency/memory comparisons on target device |
| 5. Generative image | Latent codec, conditioning, denoiser, sampler workflow | Reproducible image experiment with compatibility tests |
| 6. Temporal video | Video codec, temporal schema, sampler, chunking as needed | Temporal tests, resource budget and frame consistency |
| 7. Extensions/UI | Entry-point discovery, optional graphical editor, additional families | UI uses exact same registry/manifest/runner pipeline |

### Scope discipline

- Start CPU-first with a toy task and real contract tests. Do not start by building a GPU plugin manager.
- Add PyTorch for learned modules, not as a dependency of the pure schema/registry core.
- Introduce a plugin loader only once a second independently packaged module is needed.
- Avoid a custom tensor framework; use established tensors with semantic metadata at module boundaries.
- Do not support mid-episode or mid-training hot swaps initially. Stop, snapshot, validate, compare.
- Avoid a universal `AIBaseModel` class that incorrectly conflates prediction, action selection and sampling.

### Potential names

Neutral repo/workspace name: `Modular AI Research Framework` or `AI Architecture Atlas`. Preserve boundaries so it can integrate with Superior MI Studio later without coupling core design to its UI.
