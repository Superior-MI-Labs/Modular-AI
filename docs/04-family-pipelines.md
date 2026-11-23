# 04 — Family-specific workflow templates

All templates use the common registry, contract validator, execution context and artifacts; the **workflow runner** differs by family. Do not force every model through a language-token interface.

## A. Minimal deterministic decision engine (first to implement)

`Environment.reset/step → versioned Observation → legal-action filter → stable utility scorer → Action → Environment.step → reward/metrics`

Swappable: utility scorer, rule set, policy (neural or symbolic), memory strategy, state encoder, reward definition (requires separate experiment baseline). Decision quality is measured against the same environment and seeds. For RL use Gymnasium-style `reset` and `step` semantics rather than inventing an incompatible environment API.

## B. Autoregressive text

`Raw text → tokenizer → token IDs → embeddings → predictor (Transformer / RNN / SSM) → logits → sampling policy → token IDs → detokenizer`

A tokenizer replacement can require new embedding/output weights and training. The sampler may be swappable if it receives compatible logits and the same token semantics.

## C. Classifier / perception

`Raw image or sensor array → normalizer → CNN / Transformer / graph encoder → prediction head → calibrated label/output`

Swappable: backbone with matched head inputs, preprocessors with explicit schema change, calibrated decision rules. Pixel scaling and label IDs are part of the contract.

## D. Image diffusion / flow

`Prompt / conditioning → condition encoder → latent initializer → iterative denoiser or vector-field model + sampler/schedule → VAE/codec decoder → image`

Swappable: schedulers compatible with the network's prediction target; some compatible encoders/denoisers/codecs; guidance and postprocessors. Not arbitrary. A text conditioner and latent decoder are trained dependencies.

## E. Video generation

`Text/image/audio condition → spatial-temporal latent representation → video denoiser / next-frame predictor → temporal sampling/control → frame decoder → output frames + timing/audio synchronization`

Extra contracts: frame rate, clip length, temporal/spatial compression, frame masks, camera motion and shot consistency. Sliding-window decoding and chunked generation may be separate strategies. Do not treat video as independent still images if temporal coherence matters.

## F. Audio / speech

`Waveform or transcript → acoustic/text encoder → sequence or diffusion model → acoustic token/spectrogram representation → vocoder/audio decoder`.

Extra contracts: sample rate, channels, codec, timing, speaker identity, chunking/stream latency and alignment.

## G. World model / multi-agent / affective state research

`Observation → encoder → recurrent/world state → prediction model → policy → action → environment → feedback`. Memory and optional affective state are independent, versioned modules. VAD coordinates can be a testable state schema, **not** assumed to establish subjective emotion, consciousness, or empathy.

## Why a workflow plugin?

Autoregression adds one token per step, diffusion iterates a time/noise schedule, RL loops on environment steps, and video generation imposes temporal state. Their *control flow* is not interchangeable even if they share tensor operations and model loaders.
