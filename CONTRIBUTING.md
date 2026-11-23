# Contributing

This is currently an architecture and visual-education repository, not a completed AI engine.

- Fix inaccuracies in the Mermaid diagrams (`diagrams/mermaid/`) rather than editing generated SVGs.
- Add a catalog entry to `diagrams/catalog.json` for each new diagram. Keep diagrams factual and mark hypothetical architecture as such.
- Run `python3 tests/validate_bundle.py` and `python3 -m unittest discover -s tests -p 'test_site.py'` before submitting changes.
- Runtime code should only be introduced alongside a written contract, acceptance tests and one end-to-end runnable example.
- Preserve the source-of-truth distinction: manifests select modules; the registry defines port semantics; artifact records capture checkpoint/codec/tokenizer dependencies.
- Prefer adjusting an existing module or workflow to adding new registries, plugins, adapters or compatibility shims.

The project is experimental. Claims about emergent cognition, empathy or intelligence require separate empirical evidence.
