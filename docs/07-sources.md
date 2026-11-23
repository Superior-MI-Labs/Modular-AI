# 07 — Primary documentation and references

- Python Packaging User Guide, [Creating and discovering plugins](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/): standard Python entry points and discovery options.
- [Hugging Face Diffusers — ModularPipeline](https://huggingface.co/docs/diffusers/main/modular_diffusers/modular_pipeline): pipeline blocks can be assembled and exchanged, under component constraints.
- [Hugging Face Diffusers — Pipelines](https://huggingface.co/docs/diffusers/en/api/pipelines/overview): common denoiser, codec, scheduler components.
- [Hugging Face Transformers — Tokenizers](https://huggingface.co/docs/transformers/en/main_classes/tokenizer): adding tokens and resizing embedding matrices.
- [PyTorch torchao — QAT](https://docs.pytorch.org/ao/stable/workflows/qat.html): quantization-aware training and precision tradeoffs.
- [PyTorch torchao — Quantization](https://docs.pytorch.org/ao/stable/contributing/quantization_overview.html): quantized models and training/inference.
- [Gymnasium — Environment API](https://gymnasium.farama.org/api/env/): conventional `reset`/`step` episode boundary.
- [ONNX Runtime — Execution Providers](https://onnxruntime.ai/docs/execution-providers/index.html): backend-specific graph execution.

These are reference designs and tooling, not dependencies automatically required by the framework. No claim is made that these libraries share one universal checkpoint format.
