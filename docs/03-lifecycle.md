# 03 — Training, evaluation, optimization and deployment

## Separate workflows, shared artifacts

**Dataset preparation:** source → license/provenance checks → versioned transform → train/validation/test split → cached shards. Keep training split separate from final holdout. Log transforms, sample hashes, preprocessing versions and tokenizers/codecs.

**Training:** initialize model with declared dependencies → batch/sequence generation → forward → objective/loss → backward (where differentiable) → optimizer step → checkpoints. Account for gradient accumulation, clipping, learning-rate schedules, random seeds, resumption and metrics.

**Model families:**

- Autoregressive text: token targets, cross-entropy, context masks, token-generation evaluation.
- Diffusion/flow: noisy latents, timestep/noise distribution, denoising/flow target, sampling evaluation.
- Decision/RL: environment reset/step, policy and reward/advantage learning as applicable, reproducible episode results.
- Video: spatial + temporal latents, timebase conditioning, clip datasets, temporal consistency and motion evaluation.
- Hybrid system: separate objective ownership; do not assume every module needs joint end-to-end gradients.

**Evaluation gates:** task metrics, held-out cases, reproducibility, latency, memory, speed, quality degradation, numerical agreement, robustness under changing state/sequence lengths, failure logging.

**Optimization is a post-training branch, not an overwrite:**

1. Baseline FP32/BF16/FP16 checkpoint and evaluation.
2. Optional mixed precision, kernel compilation/fusion, efficient attention, cache strategy, dynamic batching.
3. Optional PEFT/LoRA, distillation, structured sparsity/pruning; each changes training or model properties and requires new artifacts.
4. Quantization modes: post-training dynamic/weight-only, post-training activation-aware/static with calibration, quantization-aware training (QAT). Exact support depends on operator/backend/hardware.
5. Re-run quality, latency, throughput, memory and numeric stability tests before deployment.
6. Export with backend-specific constraints (for example ONNX Runtime or a chosen native backend).

Quantization does not magically make every model faster; speed and memory effects depend on the backend kernels, shape, device and task. Record calibration provenance, target hardware and numerical tradeoffs.

## Required artifact metadata

`model_id`, architecture/version, tensor-state hash, tokenizer/codec IDs and hashes, training data split hash, optimizer/scheduler (training checkpoint only), precision/quant scheme, calibration dataset hash, target backend, seed and library/driver versions, eval report, parent checkpoint. Store immutable versions, not mutable labels like `latest` as the sole reference.

## Train / optimize / run are separate commands

Future CLI contract (not implemented):

```
ai validate experiments/decision_baseline.json
ai train experiments/text_autoregressive.json
ai eval --artifact <artifact-id> --suite <suite-id>
ai optimize --artifact <artifact-id> --recipe <recipe-id>
ai run experiments/image_diffusion.json
ai compare --left <run-id> --right <run-id>
```

The same experiment manifest should be loadable through CLI or a future graphical IDE. Do not make UI-specific logic a second pipeline.
