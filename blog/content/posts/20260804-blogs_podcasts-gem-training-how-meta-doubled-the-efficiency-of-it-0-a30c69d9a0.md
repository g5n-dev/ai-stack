---
title: "GEM Training: How Meta Doubled the Efficiency of Its LLM-Scale Ads Foundation Model"
date: 2026-08-04T04:02:07+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Research", "Data Infrastructure", "ML Applications", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:93f374453f50c50d47443e5d54f365e6f820f1d84200b12b57500f112aec9c36"
source_payload_sha256: "sha256:831909d08c8818a1f4b67f6cc73f798a87bce9835ba36e350accafb5304462db"
observation_id: obs_a30c69d9a0e9c22ef86157cbb92f165a12fbb4cdd365a8253cd8b42ec2fd597f
event_id: evt_8f420f90263d2fa5533a0f3c2dbb281792e5bb29896fbf50d11d91aabdde1645
revision_id: rev_95f5492ac33589633c5bde56c8c602a081887ae50fcd093a147c5044ffafc7c2
source_published_at: 2026-08-03T18:00:17Z
first_seen_at: 2026-08-03T20:12:33Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 83
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://engineering.fb.com/2026/08/03/ml-applications/training-gem-at-llm-scale-meta-ads-recommendation-foundation-model
parent_observation_id: null
last_seen_at: 2026-08-06T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/08/03/ml-applications/training-gem-at-llm-scale-meta-ads-recommendation-foundation-model](https://engineering.fb.com/2026/08/03/ml-applications/training-gem-at-llm-scale-meta-ads-recommendation-foundation-model)
- **发布域名**: engineering.fb.com

## 来源摘要/节选

> Meta’s Generative Ads Recommendation Model (GEM), the foundation model behind ads recommendations across Instagram and Facebook, now trains at LLM scale on several thousand of the latest-generation GPUs. This post goes into the details on how we achieved: doubling end-to-end (E2E) training efficiency to 20–25% Model FLOPs Utilization (MFU) while scaling training FLOPs 4x in 12 months, by co-designing kernels, precision, parallelism, networking, and memory together.
>
> Training GEM presents unique engineering challenges at the intersection of recommendation systems and LLMs as the model combines a hybrid architecture plus recommendations-domain data properties that are unlike typical LLM workloads.
>
> AI infrastructure optimized for LLM training (kernels, parallelism, low precision recipes etc.) does not directly transfer, requiring significant innovation and hardware/software co-design to reach LLM-scale training for recommendation models efficiently.
>
> We tackled these challenges through complementary compute efficiency and scaling efficiency innovations:
>
> Compute efficiency: Achieved through a customized recommendation kernel library — Jagged Flash Attention (JFA), Generalized Dot-Product Attention (GDPA), BlockAttention, etc. — and mixed ultra-low precision training (including MXFP8 attention and MLP) optimized for recommendation workloads, purpose-built to exploit latest generation GPU’s architecture.
>
> Scaling efficiency: Topology-aware 5D parallelism with Streaming Multiprocessor (SM)-free collectives — 2D FSDP + Expert Parallelism for dense parameters, combined with Fully Sharded 2D Model Parallelism for sparse parameters — co-designed with Meta’s multi-tiered network hierarchy to reduce communication overhead.
>
> The results: we doubled GEM’s E2E training efficiency to 20-25% MFU while scaling total training FLOPs 4x over the past 12 months.
>
> GEM’s Architecture And Its Unique Training Challenges
>
> GEM is the central recommendations foundation model behind Meta’s ads system. It has a hybrid architecture with trillions of sparse embedding parameters and billions of dense parameters. GEM is trained on ad content and user engagement data with two categories of features: sequence features (e.g., user activity history) and non-sequence features (e.g., user location, ad creative representation). Customized attention mechanisms are applied to each group independently, while also enabling cross-feature learning.
>
> The interplay between this hybrid architecture and rec-domain data properties is what makes GEM’s training uniquely challenging.
>
> Challenge 1: Achieving High Per-GPU Utilization
>
> Today’s data center GPUs and their software stacks are mostly optimized for LLM workloads, whereas recommendation workloads have a fundamentally different profile due to unique data characteristics and rich user &amp; ads signal interaction patterns that make it extremely difficult to achieve high GPU compute utilization for training a foundational recommendation model of GEM’s size.
>
> Jagged Inputs: Training samples have highly variable sequence length as user activity history can vary wildly. Padding to max length would waste up to 50% compute.
>
> Diverse interaction patterns and asymmetric sequences: Self-attention operates on extremely long sequences (activity history) but short attention window; cross-attention learns user x ads interaction with long queries but short key/value; pooled multi-head attention (PMA) compress user activity history, resulting in short queries but long key/value. These asymmetric shapes make intra kernel pipelining less effective to saturate compute units.
>
> Memory-bound operations: e.g., small embedding dimension for MLP and various normalizations for model quality and training stability leave compute units underutilized.
>
> Numerical sensitivity: Ads optimization tasks (CTR/CVR prediction) are highly sensitive to numerical change (e.g., precision), making naïve low-precision training prone to quality regression.
>
> Challenge 2: Scaling Efficiently Across Thousands of GPUs
>
> Training GEM across thousands of GPUs with trillions of sparse embedding parameters and billions of dense parameters requires scaling efficiently, not just scaling up. Simply adding more GPUs does not translate to proportional speedup. In distributed training, E2E latency per training step is determined by:
>
> E2E Latency = Max across GPU Rank (Max(Local Compute Time, Communication Time))
>
> Near-linear scaling requires four conditions:
>
> Total compute time &gt;&gt; total communication time.
>
> Communication hidden behind compute without contention.
>
> Minimal recomputation from memory pressure.
>
> Good load balancing across ranks.
>
> GEM’s workload threatens every one of these:
>
> O(Trillion) sparse parameters and O(Billion) dense parameters drive heavy communication with mixed compute patterns.
>
> Architecture diversity across layers makes overlap windows uneven; resource contention between communication and computation makes hiding communication non-trivial.
>
> Long sequences with large activations push memory usage toward its limit, forcing activation recomputation that erodes efficiency.
>
> Jagged sequences across samples create data-driven load skew that varies across ranks.
>
> Our Approach and Efficiency Framework
>
> Given the challenges outlined above, we needed a framework that turned a sprawling co-design effort into a small number of technical levers. We measure training efficiency through E2E MFU, which decomposes into two factors:
>
> E2E MFU = Local MFU (compute efficiency) × Scaling Ratio (scaling efficiency)
>
> These factors describe two related but distinct optimization problems.
>
> Local MFU (compute efficiency)  measures how well a single GPU’s compute units are utilized — how close the workload runs to the hardware roofline. It is determined by kernel design, numerical precision, and how well the workload’s compute patterns (data dimensions, sequence lengths) map onto GPU architecture (Tensor cores, memory hierarchy, streaming multiprocessor scheduling).
>
> Scaling Ratio (scaling efficiency) measures how much single-GPU performance is retained when distributing across thousands of GPUs. A scaling ratio of 1.0 means perfect linear scaling; in practice, communication overhead, load imbalance, straggler effects, and activation recomputation from memory pressure all erode it.
>
> To isolate local MFU, we run model layers individually on a single GPU and compute a weighted average MFU without activation recomputation or communication exposure. The scaling ratio is derived as the ratio between local and E2E MFU.
>
> This decomposition matters because it lets us treat compute efficiency and scaling efficiency as related but distinct optimization problems, each with its own dedicated set of techniques:
>
> Compute efficiency is a kernel-level and numerical-precision problem. The levers are kernel design and ultra-low-precision training — both targeting the per-GPU roofline.
>
> Scaling efficiency is a distributed-systems problem. The levers are parallelism strategy, network topology mapping, networking efficiency, memory management, and load balancing — all targeting the gap between single-GPU and multi-GPU throughput.
>
> Both must be addressed to maximize end-to-end MFU.
>
> Optimizing Compute Efficiency With Recommendation Kernels and Ultra-Low-Precision Training
>
> To address the recommendations-system-specific challenges mentioned above and push up GPU FLOPS utilization, we built a custom kernel library and an ultra-low-precision training recipe custom-built and optimized for recommendation workloads on the latest GPU hardware.
>
> JFA — eliminates the up-to-50% compute waste from padding jagged inputs.
>
> BlockAttention — reduces long user-history self-attention cost from O(L²) to O(L) while preserving model quality and efficiency
>
> GDPA — unifies and accelerates GEM’s diverse, asymmetric attention modules where FlashAttention’s dense long-sequence assumptions break down
>
> MXFP8 attention + MLP — turns lower-precision Tensor Core throughput into real end-to-end speedups without regressing precision-sensitive CTR/CVR objectives
>
> Inside the Customized Kernel Library for Recommendation
>
> Jagged Sequence Flash Attention
>
> FlashAttention is designed for dense, fixed-length sequences common in LLMs. In recommendation models, user sequences are inherently jagged — varying from hundreds to tens of thousands of tokens per sample — and padding to max length could waste up to 50% of compute.
>
> Standard FlashAttention implementations assume uniform sequence lengths for efficient tiling and parallelization; with jagged inputs, naive approaches either pad (wasting compute) or leave SMs idle when short sequences finish early. We developed JFA, a custom FlashAttention implementation that operates directly on variable-length jagged tensors, eliminating padding overhead while supporting rec-specific features such as custom attention biases, asymmetric query/key-value lengths, and efficient backward passes.
>
> We evolved JFA through four generations, progressively closing the gap from being slower than padded SDPA (scaled dot-product attention) to matching SOTA CUDA/Cutlass performance on latest-generation GPUs:
>
> Jagged masking via subtraction scheme: Traditional 2D masking for jagged boundaries (marking invalid positions with -inf) consumes significant non-tensor-core instructions (~28% of executed instructions). We replaced this with a novel subtraction scheme — masking Query/Key with zeros (which the Tensor Memory Accelerator (TMA) does for free) and subtracting the extra exponents — producing numerically equivalent results without the masking overhead.
>
> Backward parallelization: FlashAttention’s backward pass requires accumulating dQ across sequence tiles, typically via costly atomic adds. We explored multiple schemes (seq-parallel with atomics, no seq-parallel, seq-parallel with recompute, split dQ/dKdV) and found that for rec workloads with high batch x heads, a non-seq-parallel scheme with split dQ computation delivers 21-40% backward speedup by eliminating both atomic writes and redundant recomputation.
>
> Warp specialization and persistent kernels: Upgrading to Triton Low-Level Extensions (TLX) enabled explicit warp specialization, along with use of TMA, and persistent kernel scheduling — unlocking 30-100% TFLOPS improvement by leveraging the latest hardware feature.
>
> JFA v4 (TLX) achieves 40-140% TFLOPS improvement over JFA v2, which delivers consistent gains under production jagged distributions (sparsity 0.5), contributing to 18.5% relative local MFU gain and 12% QPS gain.
>
> Generalized Dot-Product Attention (GDPA)
>
> GEM uses diverse attention-like interaction patterns — self-attention, PMA, and cross-attention — that share a common structure: two matrix multiplications with an element-wise activation in between, but replace softmax with activations like GELU or SiLU. We unify these modules under a single GDPA kernel optimized for production RecSys training workloads on latest generation GPUs.
>
> Existing FlashAttention kernels are designed for LLM-style dense, long-sequence inputs and perform poorly under real production traffic. We observed a 2.6x forward performance gap and up to 4x worst-case gap between real-world workloads and synthetic benchmarks driven by short/asymmetric K/V sequences, jagged inputs, and large batch sizes that break pipeline occupancy assumptions.
>
> We redesigned the kernel pipeline, scheduling, and math to close the performance gap between real-world traffic and hardware roofline.
>
> Pipeline redesign for non-softmax activations: Eliminating the softmax correction stage frees four warps and their registers. For short K/V sequences, outer-loop software pipelining recovers ~10% performance lost by inner-loop pipelining when the inner loop runs only 1–2 iterations.
>
> Software-level tile scheduling for jagged tensors: precompute valid tiles on CPU, skip empty tiles entirely, and apply zigzag assignment across SMs — reducing workload skew from 6x to near-balanced.
>
> ALU-only activation approximation: Replace GELU’s SFU-bound tanh with a 6th-order Taylor expansion (ALU-only), accurate within the bounded input range enforced by QK-norm (query/key normalization). Eliminates SFU contention in both forward and backward passes.
>
> With these optimizations, the optimized GDPA kernel achieves 2x forward speedup (1,145 BF16 TFLOPs, ~97% Tensor Core utilization) and 1.6x backward speedup over baseline. Under short K/V production settings, it achieves up to 3.5x forward speedup over Flash Attention 4 (FA4). Applied across the full model, these kernels deliver over 30% end-to-end training throughput improvement.
>
> BlockAttention
>
> For GEM self-attention, the core efficiency challenge was scaling long user sequences without paying the quadratic cost of full attention. We first moved the layer from full self-attention to sliding-window attention, limiting each token to nearby events and reducing complexity from O(L2) to O(L * window). This made longer sequences practical. The Sliding Window Attention (SWA) kernel skipped off-window tiles in JFA and reduced long-sequence self-attention latency by up to 68% with neutral NE (normalized entropy, a model-quality metric).
>
> We then pushed the structure further with block-aligned attention. Since GEM could safely use fixed 64-token blocks, each Q block only attends to its corresponding K/V block, turning attention into independent 64×64 problems. This removes the partial-window masking and multi-tile iteration still present in SWA, and lets a dedicated TLX kernel eliminate FlashAttention overheads such as online softmax correction, logsumexp HBM traffic, and separate Di preprocessing.
>
> Fusing RoPE backward into the attention epilogue removes another memory-bound kernel and keeps gradients in FP32 registers. Together, TLX block attention + fused rotary improves self-attention layer MFU by +30.6% over Triton block attention, or roughly +44% over the SWA baseline.
>
> Mixed Ultra-Low-Precision Training
>
> On a GPU, lower precision directly translates to higher Tensor core throughput. For the latest generation GPU, FP8 delivers 2x peak FLOPS over FP16, and FP4 delivers 4x. We expect the peak FLOPS of low precision to increase faster in next-generation GPUs. This makes low-precision training increasingly attractive as hardware vendors scale low-precision FLOPS faster than FP16.
>
> However, making low-precision training work without quality regression — addressing both numerical stability and quantization overhead — remains an industry-wide challenge. We developed MXFP8 Attention and MLP with numerical stability enhancement, which addressed both training stability and quantization overhead.
>
> Low Precision Flash Attention
>
> We extended the FA4 kernel with end-to-end MXFP8 blockscaled MMA for both forward and backward passes leveraging latest generation GPUs’ native support for low precision. The main challenge is that low precision attention is not just a datatype swap. Scale factors must be generated along each GEMM’s (General Matrix Multiplications) K dimension, staged through shared memory (SMEM) / tensor memory (TMEM) despite FA4’s already full TMEM footprint, and computed online for intermediates such as softmax P and backward dS.
>
> To make the Tensor core speedup survive at module level, quantization was fused into upstream normalization and projection kernels, emitting FP8 activations and tensor-core-friendly scale layouts directly while avoiding extra BF16 global-memory traffic. For GEM’s jagged recommendation workloads, FP8 data stays at unpadded positions and only compact scale factors are scattered/padded for TMA. This turns MXFP8 block-scaled MMA support into practical E2E attention speedups without introducing model quality regressions.
>
> To meet our unique requirements we had to develop three new innovations at the kernel level:
>
> TMEM scale factor placement: The original FA4 fully utilized 512-column TMEM for accumulators, leaving no room for block-scale factors. We solve this by overlapping scale factors with temporarily-unused TMEM regions (e.g., placing S(i) scale factors in the S(1-i) accumulator region), requiring only one additional lightweight barrier that is hidden behind existing GEMM latency.
>
> Online P-to-MXFP8 conversion: Softmax output (P) is quantized to MXFP8 in-place within the softmax warp, reusing the row-max already computed for softmax normalization to avoid redundant reductions. Scale factors are derived via optimized PTX bit-manipulation sequences instead of expensive log2/round/clamp operations.
>
> Block-wise Quantization: We use [32, 32] square quantization computing one scale factor per 32×32 block via redux.sync.max.abs.f32 warp-wide reduction — making quantization transpose-invariant so each tensor is quantized only once. This is useful for the backward pass, where transposed Q,K values are needed.
>
> On GEM representative shapes, measured on Meta internal power capped latest generation GPU, we achieved &gt;1.3x speedup for the forward kernel with MXFP8. For the backward kernel, we achieved &gt;1.5x speedup with MXFP8.
>
> Handling Quantization Overhead
>
> Quantization overhead mainly comes from two sources, model parameters (weights) and intermediate tensors (activations). If handled naively, the extra casting, scaling, and data movement can offset the compute speedup from low-precision Tensor cores.
>
> Weight – quantization on Fully Sharded Data Parallel (FSDP) shard
>
> Pre-all-gather shard quantization: quantize each rank’s local shard before FSDP all-gather to amortize the quantization cost across ranks, this avoids re-quantizing the fully gathered weight on every rank.
>
> Quantized FSDP communication: communicate low-precision payloads (vs. BF16) to reduce all-gather volume and cut all-gather latency which further neutralizes the quantization overhead.
>
> Activation – kernel fusion
>
> Linear modules: Instead of doing a separate quantization step with extra kernel launch + HBM traffic, we fused activation quantization into the preceding normalization (PreNorm fusion) to avoid the overhead.
>
> Attention modules: In addition to PreNorm fusion, we also fused quantization into the preceding projection so the attention kernel consumes low-precision activations directly with no extra quantization step.
>
> Addressing Numerical Stability
>
> Quantization errors, outliers, and rounding bias can make low-precision training  numerically fragile, especially for gradient computation. We addressed these challenges with:
>
> Outlier mitigation:
>
> We applied Random Hadamard Transforms spread outliers and smooth distributions prior to low precision quantization.
>
> Recipe tuning (fine-grained controls):
>
> We used stochastic rounding to eliminate deterministic rounding bias.
>
> Skipping / higher-precision weight-gradient (WGrad): We observed activations and gradients can exhibit more severe outlier behavior; selectively skipping WGrad or using higher precision can materially improve model quality.
>
> Mixed precision:
>
> We use ultra low precision  where it will have the most benefit  (e.g., large GEMMs) and fall back to BF16 (e.g., later layers in the model are more sensitive to quantization errors) where ultra low  precision is insufficient to meet model quality targets.
>
> Scaling Efficiency: 5D Parallelism, Networking, Memory, And Load Balancing
>
> As mentioned above, for large scale distributed training:
>
> E2E Latency = Max across GPU Rank (Max(Local Compute Time, Communication Time))
>
> Near-linear scaling requires four conditions: total compute time &gt; communication time, compute / communication overlapping without contention, minimal recomputation, and good load balancing.  Our optimizations address each condition to push up GEM’s scaling efficiency.
>
> Condition
>
> GEM’s Challenges
>
> Optimizations
>
> Total compute time &gt; total communication time
>
> O(Trillion) sparse parameters and O(Billion) dense parameters drive heavy communication with mixed compute patterns.
>
> Topology-aware 5D Parallelism
>
> Communication hidden behind compute without contention
>
> Resource contention between communication and computation
>
> SM Free Communication
>
> Minimal recomputation from memory pressure
>
> Long sequences with large activations push memory usage toward its limit, forcing activation recomputation
>
> Automatic Activation Checkpointing with Quantization
>
> Good load balancing across ranks
>
> Jagged sequences across samples create data-driven load skew that varies across ranks
>
> Sequence length aware load balancing
>
> 5D Parallelism, Optimized with Meta’s Network Topology
>
> GEM’s hybrid architecture requires distinct parallelism strategies for each component as dense and sparse parameters have different compute and communication patterns. We use 5D parallelism to scale GEM’s training efficiently across thousands of GPUs: 2D FSDP with Expert Parallelism (EP) for dense parameters, and Fully Sharded 2D Model Parallelism for sparse parameters.
>
> The design principle is to match communication volume to available bandwidth across the topology hierarchy. When a collective becomes a bottleneck on a given tier, we introduce a new parallelism dimension that reduces message volume or group size on that tier.
>
> Meta’s training cluster used by GEM has a three-tier network hierarchy: Eight GPUs per host connected via NVLink , hosts within an AI zone connected via RoCE, and AI zones connected via oversubscribed RoCE with bandwidth reduction.
>
> Dense Parallelism Evolution: From 1D to 3D Parallelism
>
> GEM’s O(Billion) dense parameters are sharded using FSDP. Parameters are distributed across GPUs and reconstructed via all-gather before computation, with gradients synchronized via reduce-scatter. We add two dimensions on top of FSDP — a replica (DDP) dimension (making it 2D FSDP) and EP — for a total of three dense parallelism dimensions (3D dense parallelism).
>
> Parallelism Dimension
>
> Collectives
>
> Topology Tier
>
> Bandwidth
>
> EP (Expert Parallelism)
>
> All-gather / reduce-scatter
>
> Intra-node NVLink
>
> High
>
> FSDP (within group)
>
> All-gather / reduce-scatter
>
> Inter-node (within AI zone)
>
> Medium
>
> DDP (across groups)
>
> All-reduce
>
> Inter-node (potentially cross zone)
>
> Low(Oversubscribed)
>
> This topology-aware distributed training is what makes 3D dense parallelism efficient — each dimension’s communication cost is matched to the bandwidth available at its topology level.
>
> Why 2D FSDP: Reducing Group Size for Better Bandwidth
>
> At several thousands GPU scale, standard FSDP requires collectives across the full rank count, where effective bandwidth degrades with group size —  particularly when spanning multiple AI zones. 2D FSDP solves this by splitting the communication into two topology-aware tiers:
>
> FSDP shard group : Parameters are sharded and reconstructed via all-gather / reduce-scatter across a much smaller group (e.g., 128-256 GPUs). The reduced group size achieves higher effective bandwidth.
>
> DDP replica group : Gradients are synchronized via all-reduce across replica groups. Because parameters are already sharded by FSDP, each rank sends only a fraction — the message size is small enough to even tolerate the lower cross-zone bandwidth.
>
> We aggressively pre-fetch parameter all-gathers, pipelining each module’s communication with the previous module’s compute to maximize overlap. This works well for most modules — however, large modules like DHEN (Deep Hierarchical Ensemble Network) experts have parameter sizes where communication time still outweighs neighboring compute time, becoming exposed and slowing down E2E efficiency.
>
> Adding Expert Parallelism: Pushing Heavy Communication to the Fastest Links
>
> To address communication exposure from large dense expert modules, we layer EP on top of 2D FSDP. With EP, each rank holds only one expert, shrinking the FSDP all-gather to a single expert’s parameters — reducing both group size and message size.
>
> The extra EP communication is placed on intra-node NVLink with high bandwidth  making it easily hidden. The forward and backward passes coordinate FSDP and EP collectives:
>
> Forward: FSDP all-gather expert params (16-way, inter-node) → EP all-gather activations (2-way, intra-node NVLink) → compute local experts on full batch → EP reduce-scatter outputs (2-way, intra-node NVLink).
>
> Backward: FSDP all-gather expert params (16-way, inter-node) → EP all-gather output gradients (2-way, intra-node NVLink) → compute expert gradients → EP reduce-scatter input gradients (2-way,

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。