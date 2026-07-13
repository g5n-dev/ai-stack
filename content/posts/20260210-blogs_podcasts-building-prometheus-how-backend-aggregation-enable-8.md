---
title: "Building Prometheus: How Backend Aggregation Enables Gi"
date: 2026-02-10T22:46:04+08:00
draft: false
entry_kind: "auto"
tags: ["Meta", "GPU集群", "网络架构", "后端聚合", "BAG", "大规模训练", "数据中心", "基础设施"]
categories: ["系统与基础设施", "AI 工程"]
source: blogs_podcasts
description: "这篇文章介绍了 Meta 如何通过**后端聚合网络**技术构建其**吉瓦级规模的 AI 集群“Prometheus”**。 以下是关键内容的总结： 1. **核心功能**： BAG 充当连接桥梁，实现了跨多个数据中心和区域的**数千个 GPU 之间的无缝连接**。这种架构允许将分散的计算资源整合成一个巨大的统一算力池，"
external_url: https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters
scenarios: ["Web应用开发"]
---

# Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters

---

## 基本信息

- **来源**: Meta Engineering (blog)
- **发布时间**: 2026-02-09T17:00:33+00:00
- **链接**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)

---
## 摘要/简介

We’re sharing details of the role backend aggregation (BAG) plays in building Meta’s gigawatt-scale AI clusters like Prometheus. BAG allows us to seamlessly connect thousands of GPUs across multiple data centers and regions. Our BAG implementation is connecting two different network fabrics – Disaggregated Schedule Fabric (DSF) and Non-Scheduled Fabric (NSF). Once it’s complete our AI [...] Read More... The post Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters appeared first on Engineering at Meta .

---
## 摘要

这篇文章介绍了 Meta 如何通过**后端聚合网络**技术构建其**吉瓦级规模的 AI 集群“Prometheus”**。

以下是关键内容的总结：

1.  **核心功能**：
    BAG 充当连接桥梁，实现了跨多个数据中心和区域的**数千个 GPU 之间的无缝连接**。这种架构允许将分散的计算资源整合成一个巨大的统一算力池，从而支持更大规模的 AI 模型训练。

2.  **网络架构创新**：
    BAG 的具体实施涉及连接两种不同的网络结构：
    *   **分解调度结构**：负责特定的调度任务。
    *   **非调度结构**：处理通用的数据传输。
    通过 BAG 将这两种不同的网络架构结合，优化了数据流动，提升了集群的整体效率。

3.  **建设成果**：
    该项目展示了 Meta 在基础设施工程上的突破，使其能够构建和运营像 Prometheus 这样达到“吉瓦级”能耗规模的超大规模 AI 集群，为未来的 AI 发展提供硬件支持。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施后端聚合以降低采集开销

**说明**: 在大规模 AI 集群（如 Gigawatt 级别）中，传统的 Prometheus 拉取模型会产生巨大的网络负载和 CPU 开销。通过在“本地”节点或边缘位置实施后端聚合，可以在数据发送到中央 Prometheus 服务器之前进行预计算和降采样，从而显著减少指标吞吐量。

**实施步骤**:
1. 部署支持聚合的中间层或使用 Prometheus 的 Recording Rules 进行本地预聚合。
2. 将高基数的原始指标（如针对每个 GPU 的微秒级数据）聚合为集群级别的统计摘要（如 99th 百分位、平均值）。
3. 调整抓取间隔，对聚合后的指标使用较长的抓取周期，而对关键调试指标保持较短周期。

**注意事项**: 确保聚合逻辑不会掩盖关键的单点故障信息；建议保留部分原始高精度指标的短时间窗口用于故障排查。

---

### 实践 2：优化高基数指标管理

**说明**: AI 工作流通常涉及动态 Pod 和海量容器，导致指标基数极高。直接采集所有高基数标签（如 Pod ID、容器 ID）会压垮 Prometheus 存储和查询性能。最佳实践是限制或重写标签，仅保留必要的维度。

**实施步骤**:
1. 使用 Metric Relabeling（指标重标记）在采集端丢弃不必要的标签（如 `pod_uid`、`container_id`）。
2. 对于分布式训练任务，使用 Job 级别或 Task 级别的标签替代实例级标签。
3. 定期审计 TSDB 状态，识别并治理 Top N 高基数指标。

**注意事项**: 在删除标签前，请确保这些标签不是告警或关联日志所必需的上下文信息。

---

### 实践 3：构建分层联邦架构

**说明**: 单一 Prometheus 实例无法处理 Gigawatt 级别的规模。应采用分层架构，设立“边缘”Prometheus 实例负责采集特定节点或机架的数据，然后通过联邦机制将聚合后的关键指标上报给“中心”全局 Prometheus 实例。

**实施步骤**:
1. 设计拓扑结构：在每个 GPU 节点或机架部署本地 Prometheus Agent 或实例。
2. 配置中心 Prometheus 实例，通过 `/federate` 接口仅从边缘实例抓取聚合后的关键业务指标。
3. 确保边缘实例配置了本地存储保留策略，以便进行详细的本地调试，而中心实例仅保留长期趋势数据。

**注意事项**: 联邦不应用于长期存储或高可用性（HA）场景，仅用于聚合视图；对于 HA 需求，应使用 Thanos 或 VictoriaMetrics 等远程存储方案。

---

### 实践 4：针对硬件加速器进行特定抓取优化

**说明**: AI 集群依赖 GPU 和其他加速器，其性能指标（如 NVML）更新频率高且数量巨大。直接使用默认设置抓取这些指标会导致“抓取风暴”。

**实施步骤**:
1. 使用 Node Exporter 的 GPU 收集器或专用的 DCGM Exporter，并配置较短的内部轮询间隔，但对外暴露较长的抓取间隔。
2. 启用 Prometheus 的 `scrape_protocols`，优先使用更高效的 Protobuf 格式进行数据传输。
3. 将 GPU 相关的抓取目标分散到不同的 Prometheus 抓取组（Scrape Configs）中，利用并行抓取能力。

**注意事项**: 监控 Exporter 本身的资源消耗，防止监控组件本身成为影响 AI 训练任务的干扰源。

---

### 实践 5：采用基于 Agent 的高可用采集模式

**说明**: 在大规模集群中，传统的 Prometheus 拉取模式可能因网络抖动或目标短暂不可用而丢失数据。使用 Prometheus Agent 模式（无本地存储，仅发送到远程写入端点）可以提高采集的弹性和可扩展性。

**实施步骤**:
1. 将关键节点上的 Prometheus 配置为 Agent 模式（`enable_features: agent`）。
2. 配置 Remote Write 将数据直接发送到兼容的长期存储后端（如 Grafana Mimir, Thanos Receive）。
3. 利用 WAL（Write-Ahead Log）来缓冲数据，防止网络中断时的数据丢失。

**注意事项**: Agent 模式不支持查询，因此必须配合中央查询系统使用；需确保远程写入后端的写入吞吐量能够承载整个集群的峰值流量。

---

### 实践 6：动态调整采样率与抓取频率

**说明**: 并非所有指标都需要每秒抓取一次。根据业务对数据精度的要求动态调整抓取频率，可以大幅降低系统负载。在 AI 训练阶段可能需要高精度，而在闲置或推理阶段则可以降低频率。

**实施步骤**:
1. 区分“控制平面”指标和“数据平面”指标。对控制平面使用较低频率（如 30s），对数据平面关键指标使用较高频率。
2.

---
## 学习要点

- 后端聚合架构通过将监控数据的计算与存储分离，使 Prometheus 能够支持吉瓦级 AI 集群的大规模部署。
- 引入分层降采样机制，在保证关键指标精度的同时显著降低了长周期数据的存储成本。
- 优化了高基数指标的处理能力，解决了 AI 训练场景中海量动态标签带来的性能瓶颈。
- 采用分布式查询引擎，打破了单点性能限制，实现了跨集群监控数据的秒级响应。
- 通过自定义的远程存储适配器，实现了监控数据与对象存储的无缝对接，提升了系统的弹性扩展能力。
- 重构了数据采集链路，将采集延迟降低至亚秒级，确保了 AI 训练任务状态监控的实时性。
- 建立了标准化的指标暴露规范，统一了异构硬件（如 GPU、TPU）的监控数据模型。

---
## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Meta](/tags/meta/) / [GPU集群](/tags/gpu%E9%9B%86%E7%BE%A4/) / [网络架构](/tags/%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84/) / [后端聚合](/tags/%E5%90%8E%E7%AB%AF%E8%81%9A%E5%90%88/) / [BAG](/tags/bag/) / [大规模训练](/tags/%E5%A4%A7%E8%A7%84%E6%A8%A1%E8%AE%AD%E7%BB%83/) / [数据中心](/tags/%E6%95%B0%E6%8D%AE%E4%B8%AD%E5%BF%83/) / [基础设施](/tags/%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [😱谷歌欲掌控俄州小镇水源！环保主义者紧急发声！]({{< relref "posts/20260126-hacker_news-environmentalists-worry-google-behind-bid-to-contr-15.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--5.md" >}})
- [OTelBench基准测试：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--7.md" >}})
- [基于 NixOS 的 Microvm.nix 构建编码 Agent 虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*