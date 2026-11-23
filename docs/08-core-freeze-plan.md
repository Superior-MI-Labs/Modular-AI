# 08 — Core freeze specification (proposed v1 contract)

**Status: design reviewed; not implemented or frozen.** There is a prototype compatibility checker and a static website. A complete executable core does **not** yet exist.

## The rule

The **core is the experiment operating system**, not a universal neural network. It loads an immutable experiment specification, resolves allowlisted modules, validates semantic and artifact contracts, schedules a workflow controller, manages execution context and immutable outputs, and records comparable results. It cannot assume tokens, images, policies, gradients, or a specific tensor framework.

After core v1 passes its gates and is frozen, a new AI family or algorithm should normally be added by registering **module implementations, workflow controllers, schemas and tests** without changing core interfaces. A core change after freeze requires an explicit architecture decision, contract-version bump, migration and compatibility tests. This is a stability policy, not a promise that no core bug will ever be found.

## Three things that must remain separate

1. **System graph:** which registered modules communicate, via schema-specific ports.
2. **Calculation graph:** framework-owned tensors, gradients, optimizer operations. The kernel does not implement autograd.
3. **Execution graph:** where operators execute, budgets, cancellation, device placement and data transfer. Backends own hardware-specific behavior.

An episodic policy loop, autoregressive token loop, and diffusion sampler are different **workflow controllers**. Do not force them into an acyclic pipeline or duplicate their control logic in the generic runner.

## Contract types to freeze

| Contract | Stable responsibility | Does **not** do |
|---|---|---|
| `ModuleSpec` | Immutable namespaced ID, implementation version, ports, capabilities, artifact requirements, factory reference | Construct weights at validation time |
| `PortSpec` | Semantic schema/version, shape and dtype constraints, layout, units, timebase, representation fingerprint | Guarantee learned feature alignment from shape alone |
| `WorkflowSpec` | Named slots, declared graph links, control type, state lifetime | Encode a specific model's algorithm |
| `ExperimentManifest` | Workflow and module selections, immutable references, seed, execution limits, evaluation plan | Copy registry-owned port specs |
| `ExecutionContext` | Device policy, RNG, resource limits, cancellation, metrics, artifact service | Implicit global mutable state |
| `ArtifactRef` | Content hash, media type, schema ID/version, dependencies, producer metadata | Point at mutable “latest model” targets |
| `RunResult` | Outputs, metrics, immutable references, diagnostics, reproducibility metadata | Silently treat a failed/partial run as success |
| `CompatibilityReport` | Typed issues and clear verdict: compatible, unverified, migration, incompatible | Equate matching tensor dimensions with matching semantics |

### Non-negotiable validation checks

- Required/optional slots and category/capability requirements match.
- Each graph edge has compatible semantic IDs and versions; structured checks eventually cover dtype/shape/layout/device/unit/timebase.
- Every tokenizer/codec/action-space identity needed by a checkpoint is verified against artifact metadata; missing hashes are **unverified**, not “safe”.
- No arbitrary Python imports or remote code execution from a manifest. Only explicit allowlisted factories can construct components.
- A swap is allowed only at a run boundary in v1: stop, snapshot, create new manifest, validate and restart. No live weight swapping.
- Determinism is tested within defined platform/precision tolerances; never promise bitwise parity across different hardware.
- Runtime errors, cancellation, budget exhaustion and partial artifacts are explicit recorded states.
- Core has no compulsory PyTorch, Transformers, Graphviz, browser or GPU dependency.

## File-by-file implementation map

Create files only when the corresponding feature is implemented. Existing READMEs describe boundaries; do **not** scaffold dozens of empty Python modules.

| Path | Owner | Gate |
|---|---|---|
| `pyproject.toml` | Package metadata, extras for optional ML backends | 1 |
| `src/modular_ai/__init__.py` | Public API and package version | 1 |
| `src/modular_ai/core/contracts.py` | Frozen `PortSpec`, `ModuleSpec`, `WorkflowSpec` value types | 1 |
| `src/modular_ai/core/manifest.py` | Immutable experiment manifest parsing, normalization, stable hash | 1 |
| `src/modular_ai/core/registry.py` | ID/version resolution and explicit allowlisted factories | 1 |
| `src/modular_ai/core/compatibility.py` | **Existing prototype**; evolve to sole graph and artifact validator | 1–2 |
| `src/modular_ai/core/context.py` | RNG, cancellation, execution limits, metrics and device policy | 2 |
| `src/modular_ai/core/runner.py` | Controller dispatch, lifecycle, failure handling and result recording | 2 |
| `src/modular_ai/core/artifacts.py` | Immutable content-addressed artifacts, checkpoint dependencies and lineage | 2–3 |
| `src/modular_ai/core/results.py` | Typed results, diagnostics, reproducibility records | 2–3 |
| `src/modular_ai/workflows/episode.py` | Reference episode controller, outside core | 2 |
| `src/modular_ai/modules/reference_decision.py` | Tiny environment, utility policy, alternate policy, evaluator | 2 |
| `src/modular_ai/workflows/autoregressive.py` | Reference token loop controller (may use a dummy predictor) | 3 |
| `src/modular_ai/workflows/iterative.py` | Reference iterative sampler controller (can use a dummy denoiser) | 3 |
| `src/modular_ai/workflows/train.py` | Training-loop controller; gradient mechanics are backend/module-owned | 3 |
| `src/modular_ai/workflows/transform.py` | Versioned transforms, including quantization/compilation pipelines | 3 |
| `src/modular_ai/modules/reference_numeric.py` | Tiny CPU model, objective, optimizer, toy latent and reference transform adapters | 3 |
| `tests/test_contracts.py` | Port compatibility, versioning, missing/extra fields, migrations | 1 |
| `tests/test_compatibility.py` | Existing and new positive/negative swap cases, fingerprint rejection | 1 |
| `tests/test_runner.py` | Lifecycle, state scope, errors, cancellation and resource budgets | 2 |
| `tests/test_artifacts.py` | Hash integrity, lineage, idempotent writes and mismatch rejection | 2–3 |
| `tests/test_workflows.py` | Deterministic decision, token, iterative and training mocks | 2–3 |
| `tests/test_reproducibility.py` | Same seed/inputs; resume from checkpoint and metrics comparisons | 3 |
| `tests/test_extensions.py` | Independently implemented plugin with no core-file modifications | 4 |
| `tests/test_site.py` | Static site, diagram export and read-only explorer checks | Existing |
| `tests/validate_bundle.py` | Reference manifests checked by **the same** compatibility module | Existing |
| `registry/reference_modules.json` | Reference module and workflow specs; prototype registry, not installed modules | Existing |
| `schemas/experiment.schema.json` | Versioned manifest schema; upgrade in place when runtime fields are finalized | Existing |

### Avoid these duplicate abstractions

- No second compatibility engine in the browser. The static explorer presents generated validator results.
- No general-purpose tensor or autograd library. Torch/NumPy/JAX may be behind adapters.
- No `AIBaseModel` that mixes every modality and execution loop.
- No model-specific branches inside `runner.py`.
- No parallel checkpoint formats invented by training, quantization and inference modules.
- No mutable module `current_state` shared across unrelated experiments.

## Core completion acceptance gates

The core is **complete v1** only when all gates below pass with documented evidence:

1. **Contract gate:** immutable manifest, IDs, ports, representations, capabilities and artifact fingerprints are validated before any expensive initialization. Negative tests reject same-shape/different-identity vocabularies, codecs and action spaces.
2. **Swap gate:** switch two independently implemented decision policies by configuration alone. An incompatible VAD encoder/policy combination must be rejected.
3. **Workflow gate:** run a deterministic episode plus reference token and iterative controllers with test doubles, without changing core. Controller-specific loops reside outside the kernel.
4. **Training gate:** train a tiny CPU model, save and resume with RNG and optimizer state, and reproduce defined test metrics. No full LLM training is required.
5. **Artifact gate:** original weights, training checkpoints, quantized derivatives, datasets and metrics have immutable provenance. A reference transformation creates a new artifact and never overwrites its parent.
6. **Reliability gate:** fail-closed invalid input, budget failure, cancellation, interrupted checkpoint recovery and well-formed error records all have tests.
7. **Extension gate:** an independently packaged/registered workflow and module use the public API, with zero core file edits. External plugin trust remains an explicit policy.
8. **Documentation gate:** public API, capability boundaries, versioning/migration rules, one reference experiment per loop, and diagnostic examples match actual behavior.

**Freeze decision:** mark `core-v1.0` only with a full passing gate report, pinned dependencies and a tagged release. The diagram website can reach “complete” earlier; that is not evidence that the runtime core is complete.

## After freeze — module-only development

The following belong in replaceable implementations, registered with stable contracts:

- Decision policies: utility rules, search, model-based planning, learned RL, world-state estimators.
- Text: custom tokenizers/vocabularies, Transformer/recurrent/state-space models, memory strategies, samplers, adapters and checkpoint migrations.
- Image: pixel/latent codecs, diffusion and flow predictors, schedulers, guidance, decoders, evaluators.
- Video: frame/timebase encoders, temporal models, chunk schedulers, motion consistency evaluation.
- Training: dataset transforms, loss functions, optimizers, LoRA/PEFT, distillation, gradient accumulation.
- Optimization: post-training quantization, QAT, pruning, compilation, kernel adapters, runtime benchmarks.
- Hardware: CPU/GPU/accelerator execution adapters, resource estimation and model sharding.

A truly new type of execution loop is installed as a new **workflow controller** using the frozen workflow interface; it is not patched into the kernel. New representation contracts can be versioned without modifying existing contracts. A genuinely novel unmet kernel requirement is reviewed rather than hidden behind a shim.
