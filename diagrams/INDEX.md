# Diagram index

Each diagram has one editable `.mmd` file. `PREVIEW.md` renders the same Mermaid sources on GitHub and compatible Markdown viewers.

| # | Diagram | Purpose |
|---|---|---|
| 01 | [AI Landscape](mermaid/01_ai_landscape.mmd) | Conceptual taxonomy: model architectures, learning paradigms, and systems overlap; this is not a strict inheritance tree. |
| 02 | [Generic AI System](mermaid/02_system_overview.mmd) | Optional state and memory are external modules, not automatically updated neural weights. |
| 03 | [Training vs Inference](mermaid/03_training_vs_inference.mmd) | Training and inference are distinct workflows; many inference deployments never update weights. |
| 04 | [Transformer Internals](mermaid/04_transformer.mmd) | Illustrative single-block attention; practical Transformers use multihead variants, multiple blocks, normalization details, and task-specific heads. |
| 05 | [Diffusion Training and Sampling](mermaid/05_diffusion.mmd) | Simplified denoising diffusion; flow-matching variants can use different training targets and sampling rules. |
| 06 | [Decision and Reinforcement Learning](mermaid/06_decision_rl.mmd) | Policy is pluggable: deterministic rules, utility scores, supervised action model, or RL policy. |
| 07 | [Graph Neural Network](mermaid/07_graph_neural_network.mmd) | Graph message passing is one possible graph-network design. |
| 08 | [Recurrent / State-space Model](mermaid/08_state_space.mmd) | Recurrent/state-space models differ internally; a state update is the shared conceptual motif. |
| 09 | [Representations and Tensors](mermaid/09_data_representations.mmd) | Tensor shapes must have semantic definitions; matching numeric dimensions alone is insufficient. |
| 10 | [Single Artificial Neuron](mermaid/10_single_neuron.mmd) | Numerical example: z = (0.5×0.8)+(-1×-0.2)+0.1 = 0.7; sigmoid(z) ≈ 0.668. |
| 11 | [Gradient Learning Loop](mermaid/11_gradient_update.mmd) | Applies to differentiable learning; symbolic search and tree algorithms do not necessarily use backpropagation. |
| 12 | [Hardware Execution](mermaid/12_hardware_execution.mmd) | The data paths are representative; hardware and runtime differ by backend. |
| 13 | [Illustrative Hybrid AI](mermaid/13_hybrid_architecture.mmd) | Research concept only, not proof of general intelligence or subjective experience. |
| 14 | [Modular Platform Kernel](mermaid/14_platform_core.mmd) | Framework boundary: stable registry, validators, orchestration, and lineage; family-specific behavior stays outside. |
| 15 | [Contract-checked Module Swap](mermaid/15_contract_swap.mmd) | Replacement requires matching semantics and checkpoint compatibility, not simply matching function names. |
| 16 | [Training, Evaluation, Deployment](mermaid/16_model_lifecycle.mmd) | Quantized outputs are versioned derived artifacts and must be separately evaluated. |
| 17 | [Text, Image, and Video Pipelines](mermaid/17_modalities.mmd) | A shared runtime can orchestrate distinct family-specific pipelines. Not every family needs the same modules. |
| 18 | [Experiment Lineage and Compatibility](mermaid/18_artifact_lineage.mmd) | Record dependencies to reproduce experiments, reject invalid swaps, and roll back. |
| 19 | [Runtime State vs Learned Weights](mermaid/19_state_memory.mmd) | Working state and external memory can change without weight updates. |
| 20 | [Deterministic Decision Baseline](mermaid/20_decision_baseline.mmd) | Use a deterministic baseline as the invariant reference when developing neural decisions. |
