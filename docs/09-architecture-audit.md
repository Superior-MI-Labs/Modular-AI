# 09 — Architecture audit and corrections

**Review date:** 2026-11-23. Distinguish fixed reference-design issues from unimplemented runtime requirements.

| Finding | Why it matters | Resolution |
|---|---|---|
| Generated diagrams used Graphviz white background, while the site also forced white panels | Color bug reappeared on every build | **Fixed:** Graphviz dark-blue background, high-contrast node/edge palette; CSS uses one `--diagram-bg` variable |
| Reference validation encoded workflow connections in the test script | A second wiring definition could drift from the registry | **Fixed:** registry declares typed links; one Python compatibility checker validates all manifests and supplies website results |
| Matching port labels were treated as safe without checking trained dependencies | Same-shape token IDs and latents can encode different meanings | **Fixed for examples:** declared artifact fingerprints and negative cases; real checkpoints remain unverified |
| Episode evaluator was listed but not connected to an episode output | An apparent slot had no verified input | **Fixed:** episode result port and environment → evaluator connection are explicit |
| UI could reimplement compatibility checks | Separate browser and runtime truth | **Prevented:** precomputed outcomes are generated from the Python validator; the site only renders them |
| Example manifests contain unresolved checkpoint/codec IDs | Could be misrepresented as executable models | **Explicit:** `unverified` status and demo-only labels, no execution claim |
| Protocols do not yet encode full shape/dtype/layout/units/timebase/capability constraints | Port string equality is only a prototype, not production compatibility | **Open gate 1:** typed `PortSpec`, schema validation and capability matching |
| No executable runner or safe plugin factories | Can't actually switch installed models or run workflows | **Open gates 2–3:** explicit registry, controller interface, runner; no arbitrary code import |
| No content-addressed artifact store, training resume or optimization lineage | Irreproducible experiments and unchecked deployment conversions | **Open gates 3–5:** immutable artifacts, RNG and optimizer snapshots, calibration and comparative evaluation |
| Static explorer permutations grow combinatorially | Unbounded generated site data will eventually be expensive | **Bounded:** the generator rejects >512 variants per reference workflow; future arbitrary catalogs need server-side validation or curated scenarios |

## Decisions to continue challenging

- Do **not** build a universal trainable model base class. Use differentiated predictor, policy, encoder, codec and optimizer contracts.
- Do **not** equate transport shape matching with semantic equivalence or model quality. Compatibility has separate structural and artifact dimensions, with empirical evaluation after loading.
- Do **not** implement hot module swaps in the middle of a training step or episode. At v1, only switch between isolated runs.
- Do **not** build a general-purpose visual programming engine in this repository. The UI can later consume the same manifest and port metadata as Superior MI Studio, without forking its graph implementation.
- Do **not** claim “core complete” until the core has actually run several different workflows and survived negative integration tests. A stable manifest schema by itself is not enough.
