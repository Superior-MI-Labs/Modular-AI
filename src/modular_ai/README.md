# Future runtime package (not implemented)

This directory records the intended *boundaries*, not pretend code. Avoid introducing empty Python classes or parallel registries before milestone 1 proves the contract. The approved first deliverable is one deterministic decision episode with two swappable policies.

- `core/`: configuration, versioned ports, registry resolution and compatibility checks.
- `workflows/`: family-specific control loops; episode first, then token and diffusion loops.
- `modules/`: reference implementations adhering to core contracts.
- `training/`: optimization/update orchestration, datasets and checkpoint writing.
- `evaluation/`: baselines, metrics and regression comparisons.
- `optimization/`: quantization, pruning and post-training artifact conversion.
- `backends/`: device allocation, tensor execution and optional acceleration adapters.

Do not add runtime dependencies to the documentation website. See [architecture decisions](../../docs/01-architecture-decisions.md) and [the roadmap](../../docs/06-roadmap.md).
