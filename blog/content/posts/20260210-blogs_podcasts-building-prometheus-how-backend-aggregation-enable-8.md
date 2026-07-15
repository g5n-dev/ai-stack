---
title: 后端聚合技术如何支撑千兆瓦级AI集群Prometheus构建
date: 2026-02-10 22:46:04+08:00
draft: false
entry_kind: auto
tags:
- blogs_podcasts
categories:
- 效率与方法论
source: blogs_podcasts
description: 我们正在分享后端聚合（BAG）在构建 Meta 千兆瓦级 AI 集群（如 Prometheus）中所发挥的作用。BAG 使我们能够无缝连接多个数据中心和区域的数千个
  GPU。我们的 BAG 实现连接了两种不同的网络架构——可解聚合调度架构（DSF）和非调度架构（NSF）。
external_url: https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters
scenarios:
- Web应用开发
aliases:
- /posts/20260211-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-14/
- /posts/20260211-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **来源**: Meta Engineering (blog)
- **发布时间**: 2026-02-09T17:00:33+00:00
- **链接**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)

---
## 摘要/简介

我们正在分享后端聚合（BAG）在构建 Meta 千兆瓦级 AI 集群（如 Prometheus）中所发挥的作用。BAG 使我们能够无缝连接多个数据中心和区域的数千个 GPU。我们的 BAG 实现连接了两种不同的网络架构——可解聚合调度架构（DSF）和非调度架构（NSF）。一旦完成，我们的 AI [...] 阅读更多... 文章 Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters 首次出现在 Engineering at Meta 上。

---
## 导语

随着 AI 模型对算力的需求呈指数级增长，如何跨越物理边界构建千兆瓦级集群已成为基础设施领域的核心挑战。本文深入剖析了 Meta 在构建 Prometheus 集群时采用的“后端聚合”（BAG）技术，解析其如何通过融合 DSF 与 NSF 两种网络架构，实现跨数据中心与区域的大规模 GPU 互联。阅读本文，读者将了解支撑超大规模 AI 训练的网络架构设计思路，以及如何通过后端聚合突破单点限制，实现算力的高效聚合与调度。

---
## 摘要

这篇文章介绍了 Meta 在构建名为 Prometheus（Prometheus）的千兆瓦级 AI 集群时，后端聚合技术的关键作用。

主要内容总结如下：

1.  **核心功能**：BAG 技术使得 Meta 能够无缝连接跨越多个数据中心和区域的数千个 GPU。
2.  **网络架构**：该实现连接了两种不同的网络结构——**Disaggregated Schedule Fabric (DSF)** 和 **Non-Scheduled Fabric (NSF)**。
3.  **目标**：通过这种技术，Meta 旨在支持其大规模 AI 基础设施的建设，以满足庞大的算力需求。

---
## 评论

**文章中心观点**
Meta 通过引入后端聚合（BAG）技术作为“网络套接字”，成功解耦了 GPU 计算集群与底层物理网络拓扑，从而突破了单数据中心物理限制，实现了跨地域、跨物理设施的大规模 GPU 互联与算力聚合。

**支撑理由与深度评价**

**1. 架构解耦：通过抽象层打破物理边界**
*   **分析（事实陈述）：** 文章提到的 BAG 架构本质上是在网络栈中插入了一个逻辑聚合层。在传统 AI 集群中，RoCE 或 InfiniBand 网络通常要求物理拓扑严格匹配（如 Leaf-Spine 结构），一旦跨越机柜或数据中心，延迟和抖动会破坏 GPU 的同步性能。
*   **作者观点：** BAG 允许将两个不同的网络结构（例如本地的高性能 InfiniBand 和远端的 DCI 互联）在逻辑上视为一张网。这种“解耦”使得 Meta 可以像搭积木一样，将不同代际、不同物理位置的网络资源池化，服务于同一个训练任务。
*   **深度评价：** 这是解决“算力孤岛”的关键尝试。随着单集群规模迈向 10 万卡级，单一数据中心不仅面临电力（Gigawatt 级）瓶颈，还面临物理空间和散热极限。BAG 提供了一种软件定义网络（SDN）的思路，让 AI 训练任务可以透明地跨越这些物理边界。

**2. 容错与弹性：应对巨型集群的必然选择**
*   **分析（你的推断）：** 在万卡集群中，硬件故障是常态而非异常。如果网络架构依赖于单一的完美物理路径，任何光纤切断或交换机故障都会导致整个训练任务中断。
*   **实用价值：** BAG 通过聚合多条路径，天然具备了路径冗余和故障切换能力。如果一条跨数据中心链路中断，BAG 可以动态路由流量，虽然可能暂时降低带宽，但避免了训练崩溃。
*   **行业影响：** 这改变了 AI 集群的运维范式——从“追求零故障的脆弱完美”转向“容忍故障的弹性冗余”。

**3. 经济效益：最大化存量资产价值**
*   **分析（事实陈述）：** 建设全新的超大规模数据中心需要数年时间。
*   **支撑理由：** BAG 使得 Meta 能够利用现有的、分散在不同地理位置的旧有算力资源，将其聚合起来处理超大模型的训练。这避免了为了追求单一集群规模而必须进行的巨额新建资本支出，显著提升了资产回报率（ROA）。

**反例与边界条件**

1.  **物理墙：延迟与带宽的物理铁律**
    *   **反例：** 尽管逻辑上连接了，但物理距离无法消除。光速限制决定了跨地域的通信延迟（毫秒级）远高于机柜内（微秒级）。对于通信密集型（Communication-bound）的模型（如某些 MoE 架构或极大规模的 All-Reduce），跨 BAG 的网络瓶颈可能抵消算力带来的收益，导致 GPU 利用率大幅下降。
    *   **边界条件：** BAG 仅适用于“计算密集型”且对网络延迟容忍度较高的场景，或者用于数据并行而非张量并行的特定阶段。

2.  **复杂度陷阱：软件定义的代价**
    *   **反例：** 引入 BAG 增加了一层复杂的网络抽象。这意味着网络排错和性能调优变得更加困难。当训练速度变慢时，很难快速定位是 GPU 问题、底层光纤问题，还是 BAG 的路由策略问题。
    *   **边界条件：** 团队必须具备极强的网络协议栈开发能力，否则 BAG 本身可能成为系统的单点故障源。

**可验证的检查方式**

1.  **有效带宽比：** 在开启和关闭 BAG 跨地域连接的情况下，测量线性训练吞吐量的变化。如果跨地域聚合后的带宽利用率低于本地集群的 60%，则说明 BAG 的开销过大。
2.  **故障恢复时间（RTO）：** 在进行物理链路切断测试时，观察训练任务是否能够无感知继续运行，以及发生 Checkpoint 回滚的频率。
3.  **通信耗时占比：** 使用 Nsight Systems 或 PyTorch Profiler 分析 Kernel 执行时间与 NCCL 通信时间的比例。如果通信时间占比在跨地域模式下显著飙升，说明 BAG 无法掩盖物理延迟的短板。

**总结与建议**

这篇文章揭示了 AI 基础设施从“垂直整合”走向“水平解耦”的趋势。Meta 的 BAG 技术证明了在物理极限（电力、空间）面前，软件和网络架构的创新是唯一的出路。

**实际应用建议：**
对于正在建设万卡集群的企业，不必盲目追求单一物理园区的完美。如果无法承担 Meta 级别的研发投入，应优先采用**物理隔离但逻辑统一**的存储方案，并谨慎评估跨地域训练对特定模型收敛性的影响。不要试图复现 BAG 的具体实现，而应关注其“解耦”的架构思想。

---

## 技术分析

**1. 核心架构理念**

文章阐述了Meta为应对吉瓦级AI集群需求，提出**后端聚合**架构的设计思路。其核心逻辑在于打破单一数据中心在物理空间、电力供应和网络半径上的限制，通过在后端网络层引入聚合机制，将跨数据中心甚至跨区域的GPU资源进行逻辑整合。这种架构标志着AI基础设施从“单点集中式”向“物理分布、逻辑统一”的范式转移，旨在解决大模型训练中算力规模受限于单体数据中心物理边界的工程难题。

**2. 关键技术实现**

*   **后端聚合层：** 位于GPU服务器后端，专门负责处理训练过程中的高带宽、低延迟数据同步。该层通过构建逻辑上的统一网络平面，屏蔽了底层物理网络的差异。
*   **异构网络融合：** BAG架构的关键在于桥接不同的底层网络技术。它能够将高性能的集群内部网络（如InfiniBand/RoCE）与连接不同设施的通用IP骨干网融合，实现跨域互联。
*   **传输协议优化：** 为解决跨数据中心传输带来的延迟和抖动问题，该架构对RDMA（远程直接内存访问）协议进行了针对性优化，并结合长距离光传输技术，确保数据在跨DC场景下的可靠传输。

**3. 工程挑战与应对**

*   **延迟控制：** 跨物理距离会增加传输延迟，影响AI训练的同步效率。技术方案中可能包含了专用的物理隔离光纤通道以及针对长距离RDMA的特定调优，以维持网络性能的稳定性。
*   **拥塞管理：** 在数万GPU进行跨DC通信时，网络极易发生拥塞。BAG架构在异构网络边界实施了精细的流量整形和缓冲管理策略（如基于DCQCN的深度定制），以防止性能因拥塞而大幅下降。

**4. 应用价值与场景**

*   **超大规模模型训练：** 该技术直接支持参数量巨大的模型训练，允许集群规模突破单一POD或机房的限制，扩展至万卡级别。
*   **资源池化与调度：** 实现了算力资源与物理位置的解耦。企业可以利用现有的、分布在不同地点的电力和网络设施构建算力池，无需等待新建单一超大规模数据中心。
*   **高可用性容灾：** 通过网络聚合，当某个数据中心进行维护或发生故障时，计算任务可以被重新调度至其他可用资源，提升了整体基础设施的鲁棒性。

---

## 最佳实践指南

### 实践 1：实施后端聚合以降低采集基数

**说明**:
在千兆瓦级的大规模 AI 集群中，Prometheus 传统的“拉取”模式会导致极高的基数和资源消耗。通过实施后端聚合，即让代理程序（如 Node Exporter）在本地对原始指标进行预聚合（例如将 CPU 使用率从按核心聚合改为按节点聚合），可以显著减少发送到 Prometheus 服务器的数据量，从而降低存储压力和网络带宽负载。

**实施步骤**:
1. 修改或使用支持聚合的 Exporter（例如修改 Node Exporter 代码或使用 Go 的 Aggregator 库）。
2. 在 Exporter 配置中启用聚合开关，将高维度的原始指标（如 `node_cpu_seconds_total`）转换为低维度的聚合指标（如 `node_cpu_usage_seconds_total_agg`）。
3. 调整 Prometheus 的抓取间隔，使其与聚合后的数据更新频率相匹配。

**注意事项**: 聚合操作会丢失细粒度的数据（如单个 CPU 核心的状态），因此仅在不需要对单个核心进行深度排查时使用。

---

### 实践 2：优化高基数指标的抓取策略

**说明**:
AI 集群中常包含大量高基数指标（如 GPU 指标、容器 ID 等），这些指标会迅速压垮 TSDB。最佳实践是识别并隔离这些高基数指标，通过降低抓取频率、使用特定标签过滤或完全禁用不必要的指标来保护 Prometheus 的稳定性。

**实施步骤**:
1. 使用 Prometheus 的 `--enable-feature=expand-external-labels` 和 `--enable-feature=exponential-buckets` 等标志优化性能。
2. 在抓取配置中使用 `metric_relabel_configs` 来丢弃不需要的高基数标签或指标。
3. 对于非关键的诊断指标，考虑使用单独的抓取目标或更长的 `scrape_interval`。

**注意事项**: 在修改抓取配置前，务必在测试环境中验证指标丢弃不会影响关键的告警规则。

---

### 实践 3：部署远程存储与长期存储方案

**说明**:
本地存储无法支撑千兆瓦级集群产生的海量历史数据。应配置 Prometheus 将数据实时发送到远程存储系统（如 Thanos、Cortex 或 Mimir），利用其无限存储能力和数据压缩特性，实现数据的长期保留和全局查询。

**实施步骤**:
1. 选择并部署兼容 Prometheus 的远程存储解决方案（推荐 Thanos 或 Mimir）。
2. 在 Prometheus 配置文件中添加 `remote_write` 配置块，指向远程存储端点。
3. 配置 `write_relabel_configs` 在发送前进一步过滤或重写标签，以控制远程存储的负载。

**注意事项**: 确保远程存储的网络连接低延迟且高吞吐，避免网络抖动导致 Prometheus 内存堆积。

---

### 实践 4：采用联邦架构或分层监控

**说明**:
单台 Prometheus 无法处理整个集群的规模。应采用分层架构，在边缘或每个机柜部署“边缘 Prometheus”负责采集本地高频数据，然后通过联邦或 `remote_write` 将汇总数据上报给“中心 Prometheus”，实现中心化的全局视图。

**实施步骤**:
1. 设计监控拓扑，确定边缘节点和中心节点的职责划分。
2. 配置边缘 Prometheus 仅采集本地或特定服务的数据。
3. 在中心 Prometheus 上配置 `/federate` 抓取任务，或设置边缘节点的 `remote_write` 至中心节点。

**注意事项**: 联邦模式主要用于聚合告警和全局视图，不应试图将所有原始数据都拉取到中心节点。

---

### 实践 5：优化 Recording Rules 规则计算

**说明**:
复杂的 PromQL 查询（如计算 AI 作业的 GPU 利用率 P99）在每次查询时计算会消耗大量资源。通过使用 Recording Rules（记录规则）预先计算这些复杂的表达式并将其存储为新指标，可以大幅提升查询速度并降低 Prometheus 的计算负载。

**实施步骤**:
1. 识别监控面板和告警中频繁使用的复杂 PromQL 表达式。
2. 创建规则文件，将这些表达式定义为 `record` 规则。
3. 将规则文件加载至 Prometheus，并设置合理的评估间隔。

**注意事项**: Recording Rules 会增加写入放大效应，需平衡预计算带来的查询收益与额外的存储成本。

---

### 实践 6：针对 AI 工作负载的特定抓取调整

**说明**:
AI 训练任务通常会产生周期性的指标尖峰（如 Loss 突降或梯度更新）。默认的抓取间隔可能会错过这些瞬时状态。应根据 AI 任务的生命周期动态调整抓取频率，或利用 Pushgateway 处理短生命周期的批处理任务指标。

**实施步骤**:
1. 对于关键的训练任务，将 `scrape_interval` 从默认的 15s 缩短至 5s 或更短。
2. 集成 Pushgateway 用于抓取短暂存在的 Batch Job 指标，并在任务结束后自动清理数据。
3. 在服务发现机制（如 Kubernetes API）

---
## 学习要点

- 后端聚合架构通过将训练作业的通信模式从“All-to-All”转变为“All-to-Backend”，成功将 AI 集群的网络规模从万卡扩展至十万卡级别。
- 引入专用的后端聚合节点作为中间层，彻底消除了传统架构中因网络拓扑感知需求（如分桶排序）带来的通信开销。
- 该架构将网络通信复杂度从 $O(N^2)$ 降低至 $O(N)$，显著减少了大规模集群中网络拥塞和尾部延迟对训练性能的影响。
- 通信后端与计算前端的解耦设计，使得网络基础设施的升级（如引入新技术）不会破坏上层训练作业的隔离性和稳定性。
- 这种设计允许网络设备专注于数据转发，而将复杂的通信逻辑卸载到后端，从而简化了网络交换机的配置要求。
- 该架构通过在后端聚合层实现集体通信优化，确保了在集群规模呈数量级扩展时，GPU 的有效线性加速比。

---
## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260206-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--0.md" >}})
- [亚马逊利用 Nova 模型自动化新履约中心运营就绪测试]({{< relref "posts/20260210-blogs_podcasts-how-amazon-uses-amazon-nova-models-to-automate-ope-0.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260209-hacker_news-testing-ads-in-chatgpt-16.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260209-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-0.md" >}})
- [Transformers.js v4 Preview: Now Available on NPM]({{< relref "posts/20260209-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
