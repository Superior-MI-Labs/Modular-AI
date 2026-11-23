# 02 — Ports, data representations, and safe swaps

## Minimal kernel contract (conceptual)

```
ModuleDefinition:
  immutable_id, version, category, input_ports, output_ports,
  capabilities, artifact_dependencies, factory

PortSpec:
  kind, semantic_schema_id, semantic_version,
  optional shape constraints, dtype, layout, units, timebase,
  tokenizer_id / codec_id / action_space_id as applicable

ExecutionContext:
  seed, device, precision_policy, budget, cancellation,
  metrics_sink, artifact_store

WorkflowDefinition:
  slots, required capabilities, allowed graph topology,
  runner, state-lifetime semantics

ExperimentManifest:
  workflow_id, selected module IDs, parameter overrides,
  artifact IDs, seed, runtime settings, evaluation plan
```

Module definitions declare ports; the experiment manifest must not duplicate port contracts. A manifest selects versions. A validator resolves the full graph and verifies wiring and artifacts.

## Representations are not interchangeable just because they are tensors

| Representation | Invariant compatibility requirements |
|---|---|
| Text token IDs | Tokenizer identity + vocabulary hash, special tokens, offset/padding semantics |
| Embeddings | Feature width **and** learned representation alignment; numeric dimensions alone are insufficient |
| Image tensors | Color space, scaling, channel layout, resolution/cropping, device/dtype |
| Image latents | Specific trained codec/latent scale and channel semantics, spatial stride |
| Video latents | Image latent constraints **plus** frame rate/timebase, frame count, temporal stride, causality |
| Observations | Schema version, units, value ranges, history, missing-value rules |
| Actions | Action-space ID, legal action set, parameter schema, preconditions |
| Model checkpoint | Architecture config, parameter names/shapes, tokenizer/codec dependencies, precision format |
| Training checkpoint | All model dependencies **plus** optimizer and scheduler state, RNG states and step counters |

### Compatibility outcomes

- **Exact**: same semantic schema, immutable dependencies, compatible type/shape/layout; safe to test as replacement.
- **Adaptable**: a named, tested conversion exists with a declared precision/quality cost.
- **Requires migration**: adjust model embeddings, heads, positional structures, optimizer state, data or re-train/fine-tune.
- **Incompatible**: do not load, do not silently cast.

### Practical swap matrix

| Change | Usually allowed without retraining? | Conditions |
|---|---|---|
| Deterministic policy A → policy B | Yes | Same observation and action contracts; evaluate behavior |
| Sampler strategy A → B | Often | Same score/noise prediction target and valid schedule |
| Inference CPU → GPU backend | Often | Operators supported and numerics validated |
| FP16 → 8/4-bit weights | No, not as a raw module swap | Explicit quantization transform and post-quant evaluation |
| Tokenizer vocabulary → new vocabulary | Generally no | New token embeddings/output mapping and training/migration |
| Image decoder/latent codec A → B | Generally no | Latent distribution and training alignment must be compatible |
| Text Transformer → diffusion generator | No | Different objective, inference controller and weights |
| Decision observation/action schema | Generally no | Explicit migration of policies, datasets and tests |
| Video scheduler | Sometimes | Prediction target, temporal and noise schedule must agree |

## Lifecycle semantics

- **Instantiation**: resolve graph, validate ports and artifact dependencies, check availability and memory budget.
- **Execution**: immutable component specs; state scoped explicitly to `step`, `sequence`, `episode`, or `run`.
- **Swap**: for v1, stop old run, snapshot, create a new manifest, validate and start a new run; compare with identical tests.
- **Failure**: fail closed on schema/version mismatch, unknown units, incorrect tokenizer or incompatible codec.

## Third-party extensions

Only after the core proves stable: package implementations with Python packaging entry points, namespaced immutable IDs and semver-like contract compatibility. A discovered module is **not** automatically trusted, GPU-compatible, or executable; explicit allowlists, dependency checks, resource limits and tests remain necessary.

## Current prototype scope (2026-11-23)

`src/modular_ai/core/compatibility.py` currently checks declared workflow slots, registry-owned port IDs and example artifact fingerprints. It does **not** yet implement typed shape/dtype/layout/unit constraints, immutable artifact storage, safe plugin loading or actual model execution. The [file-level freeze plan](08-core-freeze-plan.md) is the implementation contract for those missing features.
