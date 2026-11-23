# 01 — Architecture decisions

## Two approaches considered

| Approach | Advantage | Main cost | Decision |
|---|---|---|---|
| A. Everything is pluggable, including state objects, math operations, UI, trainer loops, and graph execution | Maximum theoretical flexibility | Unstable interfaces, huge adapter count, hard debugging, accidental compatibility | **Reject for v1** |
| B. Thin stable kernel + versioned ports + workflow plugins + typed, family-specific modules | Controlled experimentation without one mega-interface | Some changes require migrations and new workflow adapters | **Adopt** |

### Locked core responsibilities

1. **Registry**: maps immutable module identifiers and versions to factories plus immutable port/capability specs.
2. **Validator**: validates a whole graph and artifact dependency set *before* allocating large models.
3. **Executor**: runs a selected workflow under an explicit execution context and resource budget.
4. **Artifact manager**: reads/writes versioned and hashed datasets, tokenizers/codecs, checkpoints, quantized derivatives, and metrics.
5. **Experiment record**: freezes config, versions, RNG seeds, environment, hardware, errors and measurement results.

The core should **not** know what a token, diffusion timestep, or reward is. Those details belong in named port schemas and workflow implementations.

### Chosen patterns

- **Ports and adapters** for component boundaries. Port definitions declare semantic schema and constraints.
- **Strategy** for policies, samplers, schedulers, optimizers, and other replaceable algorithms.
- **Registry/factory** for module discovery and construction from a manifest; Python entry points can later provide optional third-party discovery.
- **Pipeline / dataflow graph** for acyclic processing; explicit **episode or iterative controllers** for feedback loops. Do not disguise a feedback loop as a DAG.
- **Adapter** only when there is a real conversion with testable semantics (for example, normalized pixels to a particular latent codec). Never silently reshape or coerce incompatible data.
- **Artifact snapshot** for deployment and reproducibility.

### Deliberately out of scope in v1

Visual node editor, distributed plugin sandbox, plugin marketplace, dynamic remote module injection, arbitrary hot reload, unified tensor class across all frameworks, universal model checkpoint converter, neural-symbolic 'intelligence bus'. These are attractive but premature.

### Explicit boundary for the base decision system

Use a deterministic baseline that receives a versioned `Observation`, enumerates legal actions, applies constraints, assigns utility scores and stable tie-breaking, and returns a versioned `Action` with scored candidates and reasons. No neural model or training is needed. An RL policy can replace it when it accepts the same observation/action schemas and passes the same environment tests.

### Important architectural correction

**Not everything can be a drop-in swap.** `Tokenizer B` can generate entirely different token IDs from `Tokenizer A`, making an old embedding matrix and output head semantically wrong even when dimensions match. Similar couplings exist between image VAEs/latent spaces, video frame rates and temporal encodings, model heads, and decision action spaces. We version these as *artifact dependencies*, not only software interfaces.
