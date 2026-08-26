---
title: "MetaRoCE: A New RDMA Transport Built for AI-Scale Ethernet"
date: 2026-08-25T15:59:55+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "Data Center Engineering", "Data Infrastructure", "Networking & Traffic", "Open Source", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:a34982068d77f0de5e90209bd994399cb627c99f5b78f3fa94bfccb7e00cc595"
source_payload_sha256: "sha256:944fa150d947b6c75b28d42c9bbfc052ad523f41bbf2c2da780ae2d81ba5a6f8"
observation_id: obs_bc03a0c77f5011fd44c8fe87459f917e8c75860ebcfa7c7708852a63160f9d22
event_id: evt_ec6f1e88d5ec81fbd09244805876d411868d5756059588836d79188d1e67029d
revision_id: rev_c751f3b45742b360a5971d0ab475a2d8f2ee34ece44ea28561b1a9ee5be9e3ae
source_published_at: 2026-08-24T18:02:29Z
first_seen_at: 2026-08-25T08:09:04Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
interpretation_sha256: "sha256:2efca6b1e1c8ef99360ccd3e47bf7540a1a529be7976125c16036b0c9bebc85a"
description: "MetaRoCE 是 Meta 为在大规模 AI 训练和推理场景下利用普通以太网实现高效、可靠数据传输而全新设计的 RDMA 传输协议。"
external_url: https://engineering.fb.com/2026/08/24/networking-traffic/metaroce-rdma-transport-ai-ethernet
parent_observation_id: null
last_seen_at: 2026-08-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/08/24/networking-traffic/metaroce-rdma-transport-ai-ethernet](https://engineering.fb.com/2026/08/24/networking-traffic/metaroce-rdma-transport-ai-ethernet)
- **发布域名**: engineering.fb.com

## 要点解读

### 这是什么
MetaRoCE 是 Meta 为在大规模 AI 训练和推理场景下利用普通以太网实现高效、可靠数据传输而全新设计的 RDMA 传输协议。

### 用在哪里
适用于需要跨大量 GPU、跨多个数据中心进行高速集合通信的 AI 集群网络；对网络架构师和 AI 基础设施工程师在构建大规模分布式训练或推理平台时具有直接参考价值。

### 可以推断的
- 推测：该协议的开放规范有望加速行业在以太网基础上部署 AI 网络，降低对专有互连技术的依赖。  
- 推测：采用无阻塞、无优先级流控制的 loss‑tolerance 设计，可在保持低延迟的同时简化网络运维。

## 来源摘要/节选

> Training and serving frontier AI models depends on fast, reliable networks that move data between GPUs without wasting compute cycles.
>
> To meet this challenge at scale, Meta designed MetaRoCE – a clean-sheet RDMA transport protocol purpose-built for AI workloads on commodity Ethernet.
>
> We’re releasing the MetaRoCE specification, a reference software implementation and a compliance test suite through the Open Compute Project (OCP) to enable the broader industry to adopt, implement, and build on it.
>
> At Meta, we’ve been a strong driver behind the industry’s growing consensus that Ethernet should be the fabric of choice for AI infrastructure. We’ve already shown that RoCE can power distributed AI training at scale. Now, we’re building on that work with MetaRoCE, protocol designed from the ground up for Ethernet at million-GPU scale.
>
> We’ve scaled up clusters of hundreds of thousands of GPUs, spread over multiple data centers and regions. Whether these clusters are training the next frontier model or serving inference at global scale, the network is in the critical path.
>
> Collective operations like all-reduce and all-to-all synchronize thousands of accelerators during training, and the slowest transfer sets the pace for the entire job. In inference, low-latency communication between distributed model shards directly impacts response times for hundreds of millions of users. Even small amounts of network friction directly strand significant compute capacity.
>
> Standard RoCE expects the network to deliver every frame in order, leveraging PFC and discouraging the packet spraying that provides performance in multiplane and large scale networks.  MetaRoCE is built to provide high throughput, low tail latency, and operational simplicity as the network grows in the number of accelerators and the distances between them.
>
> How MetaRoCE Works
>
> MetaRoCE’s core insight is simple: The fabric sees packets, but the NIC sees intent. Traditional architectures centralize intelligence in the fabric, relying on switches to enforce losslessness and maintain order.
>
> By moving intelligence to the endpoint MetaRoCE decomposes the network into many fine-grained logical paths, each with its own real-time telemetry – per-path RTT, ECN state, and utilization. This visibility unlocks capabilities that are difficult to achieve with traditional RDMA.
>
> Native Out-of-Order Delivery
>
> MetaRoce sprays packets across many paths, so they arrive out of order by design. The transport treats out-of-order arrival as the normal case. Every packet carries its own destination, so data is written straight to its final memory location as it lands, with no reorder buffer and no head-of-line blocking.
>
> Writes carry their destination in every packet. Sends carry the match to a posted receive buffer, so a Send lands correctly even when the messages ahead of it have not arrived, and without a round trip to learn where the data goes. Collective libraries can use two-sided messaging where it suits them rather than reducing everything to Write.
>
> Native Multipathing
>
> MetaRoCE gives each connection first class paths and sprays across them packet by packet. Each path carries a distinct UDP source port as its ECMP entropy, which the NIC can change at any time to move traffic off a bad route. On multiplane fabrics, plane selection falls entirely to the NIC, and the fabric is used only as well as the NIC sprays. Because each path keeps its own window and round trip estimate, the transport can tell congestion from failure and rebalance explicitly, so a hot or broken link slows one path instead of stalling the connection.
>
> Loss Tolerance by Design
>
> MetaRoCE treats the Ethernet fabric as lossy and does not ask it to be otherwise – no PFC, no pause frames. Because each path carries its own ordered sequence, a gap in its 256-bit selective acknowledgment bitvector is evidence of loss rather than of reordering. In other protocols a SACK mostly avoids resending data that already arrived; here it triggers retransmission of exactly the missing packet, on the path that lost it, the moment the gap appears.
>
> Congestion Control From Both Sides
>
> MetaRoCE combines a conventional ECN-based, sender-driven AIMD congestion control with receiver-driven fair-share rate hints. Windows are kept per path as well as per connection, so a congestion mark trims the path that saw it and steers the next packets toward paths that are clear. In every acknowledgment, the receiver returns the share of its inbound bandwidth it has allocated to that sender, so senders approach the right speed directly rather than searching for it. Incast resolves in one or two round trips, with better fairness and lower tail latency.
>
> Topology Independence
>
> MetaRoCE asks the fabric for two things every switch already has, ECN marking and ECMP. It does not require packet trimming, in-network telemetry, credit-based flow control, or switch-side spraying, and it does not break when a fabric offers them. The same transport runs over fat-tree, multiplane, deep-buffer, and shallow-buffer fabrics, and over vendor clouds whose configuration you don’t control. Nothing proprietary is involved, so the fabric stays free to optimize for cost and cabling.
>
> Unified Connections at Scale
>
> A queue pair (QP) carries both an ordered stream of messages and bandwidth. Traditional RDMA gets more of either by opening more QPs (dozens per node pair), each with a congestion window blind to the rest and its own state on the NIC.
>
> MetaRoCE separates the two. A single connection carries many independent ordered streams above, one per communicator or collective, and many paths below, under one congestion controller. The connection state stops growing with the parallelism of the workload.
>
> The application layer remains mostly untouched – existing RDMA Verbs APIs and software stacks work without modification. Enhanced features like multiplane support are supported through extension APIs.
>
> Meta-RoCE in Practice
>
> To accelerate hardware validation, we worked with AMD to implement MetaRoCE on their Pensando programmable NICs.
>
> On a 64-node AMD GPU cluster running RCCL collectives, we directly compared MetaRoCE against RoCEv2 across all-reduce and all-to-all operations. The results were consistent with the design goals:
>
> MetaRoCE consistently delivers higher throughput and lower flow completion times than RoCEv2.
>
> Under packet loss conditions that would degrade RoCEv2, MetaRoCE maintains ~86% throughput at 1% packet loss and continues delivering useful bandwidth even at extreme 10% loss rates – converging gracefully rather than collapsing.
>
> Multiplane validation across 4-plane and 8-plane topologies with up to 4,000 concurrent connections confirmed that throughput scales linearly with plane count.
>
> During simulated plane failures, the protocol demonstrates graceful autonomous recovery – traffic redistributes without application involvement or operator intervention.
>
> These results support MetaRoce’s core design choice. By designing for loss from day one and pushing intelligence to the edge, you get a transport that performs better in ideal conditions and degrades gracefully when things go wrong.
>
> Open By Design
>
> AI infrastructure benefits from shared standards that accelerate innovation across the ecosystem. MetaRoCE extends the same open, multi-vendor philosophy that the Open Compute Project (OCP’s) Ethernet Scalable Unified Network (ESUN) initiative established for the fabric into the transport layer.
>
> That’s why we’re opening MetaRoCE:
>
> Open specification via OCP: The full protocol spec is being contributed to OCP, available for any vendor to implement and build interoperable hardware.
>
> Multiple NIC implementations: MetaRoCE is designed to run across diverse NIC architectures – programmable and fixed-function alike. We’ve proven it on AMD Pensando hardware, with additional implementations underway from other vendors.
>
> Production compliance suite: We have developed a compliance suite that gives hardware vendors the tools to prove their implementations match the protocol spec.
>
> Software reference implementation: Our libsoftmetaroce library provides a complete, functional transport stack that runs on commodity Linux over standard UDP sockets without specialized hardware. It serves as the authoritative behavioral model for silicon development and the foundation of our unified compliance framework.
>
> The Road Ahead
>
> With MetaRoCE, we’ve made strong progress on scale-out networking – high-performance, resilient transport within the data center on commodity Ethernet. But AI infrastructure spans multiple distance and latency regimes, and each brings distinct challenges we’re actively working on:
>
> Scale-up: Within a rack, accelerators trade small messages where every nanosecond matters. MetaRoCE removes two main sources of latency, the reorder buffer and PFC. We are now optimizing the fast signaling path for short memory operations issued directly from one processing element to another.
>
> Scale-across: Scale-across enables a single job to span buildings thousands of kilometers apart. Round trips stretch into milliseconds, and small differences between paths add up. Treating paths as first class entities is what lets MetaRoCE adapt, preferring the uncongested ones and seeking fairness at every level. The work ahead is in fairly sharing contended long-haul links.
>
> Storage/Kv-cache use cases: Distributed storage invites incast,where a single read fans out to many servers and they all reply at once. Receiver-driven rate hints let whichever side is receiving(a storage server taking writes or a client taking reads) moderate the inbound rate, whether the request went to ten servers or a thousand. The new dimension is keeping that rate accurate with networks of varying speed and requests of varying size.
>
> Help Us Build the Future of Ethernet for AI Infrastructure
>
> In October, we’ll release the MetaRoCE specification, a DPDK-optimized software reference implementation, and our production compliance framework at the 2026 OCP Global Summit.
>
> We’re building this in the open because the challenges ahead benefit from broad industry collaboration. If you’re building NICs, switches, or AI infrastructure, we invite you to join us.
>
> The post MetaRoCE: A New RDMA Transport Built for AI-Scale Ethernet appeared first on Engineering at Meta.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。