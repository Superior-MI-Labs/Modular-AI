# Modular AI · Superior MI Labs

**[Explore the live visual website →](https://superior-mi-labs.github.io/Modular-AI/)** · [Visual lessons](https://superior-mi-labs.github.io/Modular-AI/learn.html) · [Diagram atlas](https://superior-mi-labs.github.io/Modular-AI/atlas.html) · **[Module compatibility lab](https://superior-mi-labs.github.io/Modular-AI/swap.html)** · [Core completion plan](https://superior-mi-labs.github.io/Modular-AI/core.html) · [Architecture](https://superior-mi-labs.github.io/Modular-AI/architecture.html) · [Roadmap](https://superior-mi-labs.github.io/Modular-AI/roadmap.html)

> A visual learning atlas and architecture blueprint for a small-core, modular AI research framework. **Status: design, static visual compatibility lab, and a prototype contract validator. No executable AI runtime, trained model, or actual model-swapping implementation yet.**

## From entire systems to individual calculations

```mermaid
flowchart LR
    A[AI landscape] --> B[System internals]
    B --> C[Models and algorithms]
    C --> D[Variables and tensors]
    D --> E[Training and learning]
    E --> F[Hardware execution]
    F --> G[Modular experimentation]
```

**20 dark-blue blueprint diagrams** explain transformers, diffusion, decision systems, reinforcement learning, graph networks, state-space models, tokens, vectors, training gradients, hardware and modular design. Each diagram has one editable Mermaid source; the website publishes SVG exports and lets visitors search, filter, inspect and download sources.

## The intended modular kernel

```mermaid
flowchart TD
    CONFIG[Experiment manifest] --> REG[Module registry]
    REG --> VALID[Compatibility validator]
    VALID --> RUN[Workflow executor]
    RUN --> A[Encoder / tokenizer]
    RUN --> B[Model / policy]
    RUN --> C[Sampler / decoder]
    RUN --> D[Training / evaluation]
    RUN --> E[Versioned model artifacts]
```

The design favors **Ports and Adapters**, **Strategy**, and a **Registry/Factory** over an indiscriminate plugin system. The [module lab](https://superior-mi-labs.github.io/Modular-AI/swap.html) uses the same Python design-time validator as the tests and includes incompatible and migration-required scenarios. A valid swap must preserve semantic port contracts, data layouts, and checkpoint dependencies. Changing a tokenizer or latent codec may require remapping weights or retraining the model.

## Explore the repository

| Area | Description |
|---|---|
| [`site/`](site/) | Lightweight multi-page learning website, no frontend package dependencies |
| [`diagrams/`](diagrams/) | 20 editable Mermaid sources, generated SVGs, structured diagram catalog |
| [`docs/`](docs/) | Architecture decisions, lifecycle, audited risks, [file-by-file core freeze plan](docs/08-core-freeze-plan.md), tests and sources |
| [`examples/`](examples/) | Five illustrative experiment manifests: decision, text, image, video and VAD state |
| [`registry/`](registry/) + [`schemas/`](schemas/) | Conceptual module definitions and experiment validation schema |
| [`src/modular_ai/`](src/modular_ai/) | Planned boundaries and prototype semantic/artifact compatibility checker (no runner yet) |
| [`tools/`](tools/) + [`tests/`](tests/) | Diagram export, site publishing, and structural validation |

## Build and validate locally

Graphviz `dot` and Python 3 are required. On Linux Mint/Ubuntu, install Graphviz with `sudo apt install graphviz`.

```bash
python3 tests/validate_bundle.py
python3 -m unittest discover -s tests -p 'test_site.py'
python3 tools/build_site.py
python3 -m http.server 8000 --directory .site-dist
```

Open `http://localhost:8000/` to preview. Publishing uses one GitHub Actions workflow, scoped to website and architecture changes, and deploys the generated `.site-dist/` artifact to GitHub Pages.

## Development direction

1. **Contracts:** finalize typed schemas, registry, manifest, capability and artifact validation.
2. **Execution:** prove deterministic decision module swaps and bounded workflow execution.
3. **Core freeze:** reference token, iterative and training loops; checkpoint/resume, immutable derivatives, extension and failure tests.
4. **After core v1:** add text, image, audio and video model implementations, training algorithms and quantization strategies as modules, not kernel patches.

Start with the [core freeze specification](docs/08-core-freeze-plan.md), [architecture audit](docs/09-architecture-audit.md), [roadmap](docs/06-roadmap.md) and [acceptance tests](docs/05-tests.md). The modular design should be proven by tests before it is generalized.

Contributions: [CONTRIBUTING.md](CONTRIBUTING.md). Sources and reading material: [docs/07-sources.md](docs/07-sources.md).
