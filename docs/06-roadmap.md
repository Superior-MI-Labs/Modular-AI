# 06 — Milestone roadmap (planned, not claimed complete)

**Current stage: website + contract prototype.** The executable core does not yet exist. See [core freeze specification](08-core-freeze-plan.md) for exact files, public contract types and acceptance tests, and [architecture audit](09-architecture-audit.md) for unresolved risks.

| Stage | Deliverable | Exit criterion |
|---|---|---|
| 0. Learning and design | 20 diagrams, website, manifest examples, reference checker | Static atlas and reference tests pass **(done)** |
| 1. Typed contract kernel | Immutable manifests, typed ports, registry, capabilities, strict artifact bindings | Reject wrong schema, tokenizer identity, codec and unsupported capability before factory call |
| 2. Execution and decision | Reference toy environment, two policies, explicit context and controller | Swap policies through config alone; reproduce deterministic episode and fail safely |
| 3. Workflow + artifact readiness | Reference token/iterative/training/transform controllers, small CPU model, artifacts | Train, checkpoint/resume, generate references, create immutable derivatives |
| 4. Core freeze v1 | Reliability, extension and docs gates (all eight) | Independent module/controller installs with no core edit; tag `core-v1.0` |
| 5. Module expansion | Real text, image, video, memory, training and optimization modules | Every module passes its contract, quality, safety and resource gates |

## Stop rules

- **Do not declare core complete based on architecture docs or passing JSON tests alone.**
- The core must not learn or depend on model-specific tensors, token IDs, noise schedules or action types.
- Workflow controllers implement the frozen controller protocol. Adding a new family should not add a case to the generic runner.
- One registry is authoritative for module metadata. Python validators and static site build read it; JavaScript only renders generated results.
- No eager entry-point loading of unknown packages or remote code from a manifest. Third-party factories require an allowlist/trust model.
- No custom tensor framework or plugin marketplace; both would expand the project before validating its research purpose.
- Treat any incompatible representation as a migration question rather than an implicit cast or numerical reshape.

## Scope of the first real proof

Start with a CPU-only toy episode and two policies. Then show that **the same core** can execute a token loop and an iterative generator using test doubles. Once that works, add a tiny trainable reference network and artifact lineage so a subsequent quantizer or diffusion implementation is genuinely modular.
