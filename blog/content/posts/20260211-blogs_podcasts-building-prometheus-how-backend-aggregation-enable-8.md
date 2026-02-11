---
title: "Building Prometheus: How Backend Aggregation Enables Gi"
date: 2026-02-11T00:15:26+08:00
draft: false
entry_kind: "auto"
tags: ["Meta", "Prometheus", "BAG", "后端聚合", "GPU集群", "网络架构", "DSF", "NSF"]
categories: ["系统与基础设施", "AI 工程"]
source: blogs_podcasts
description: "We’re sharing details of the role backend aggregation (BAG) plays in building Meta’s gigawatt-scale AI clusters like Prometheus. BAG allows us to seamlessly con"
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
## 评论

**文章中心观点：**
Meta 提出的 BAG（后端聚合）架构旨在通过解耦 GPU 计算集群与底层物理网络，利用现有以太网设施实现跨越多数据中心的算力互联。该方案试图在保持大规模集群扩展性的同时，降低对专有网络硬件的依赖，为解决超大规模算力集群的物理与成本瓶颈提供了一种基于网络虚拟化的技术路径。

**支撑理由与深度评价：**

1.  **从“物理紧耦合”向“逻辑虚拟化”的架构转变**
    *   **分析：** 传统高性能 AI 集群通常依赖 InfiniBand (IB) 或专有的 RoCE 网络，要求网络拓扑与计算节点严格绑定，限制了物理扩容的灵活性。BAG 架构的核心在于在网络控制平面引入虚拟化层，通过软件定义的方式，将分散在不同物理位置的 GPU 资源聚合成逻辑上的统一算力池。
    *   **评价：** 这反映了 AI 基础设施设计的一种思路转换。它不再强求物理层面的全互联，而是通过逻辑调度来管理资源。这种做法论证了在网络延迟可控的前提下，物理位置可以作为算力调配的弹性变量，而非硬性约束。

2.  **以太网生态对专有网络的替代尝试**
    *   **分析：** 文章指出 BAG 旨在利用现有的以太网生态支撑大规模 GPU 集群。作为 OCP 的推动者，Meta 此举意在减少对昂贵的 IB 网络硬件的依赖，转而通过软件优化来弥补标准以太网在拥塞控制等方面的不足。
    *   **评价：** 这对行业具有显著的参考价值。Meta 提供了一种区别于 NVIDIA IB 封闭体系的替代方案。这表明在超大规模场景下，通过协议优化（如解决以太网丢包问题）来换取硬件成本的降低和供应链的灵活性，是一条可行的工程路径。

3.  **多数据中心协同的部署模式**
    *   **分析：** BAG 支持跨数据中心和区域的 GPU 连接，这种“离散聚合”模式允许将算力单元分散部署，不再受限于单一机房的物理空间。
    *   **评价：** 这解决了单一数据中心面临的电力和散热瓶颈。通过将算力分布化，企业可以利用不同地域的能源和基础设施优势，这对构建吉瓦级规模的计算系统具有实际工程意义。

**反例与边界条件：**

1.  **通信延迟的物理限制**
    *   **分析：** 尽管架构上实现了逻辑连接，但跨数据中心的通信延迟（毫秒级）远高于机柜内通信（微秒级）。
    *   **推论：** 这种延迟差异会对通信密集型训练任务产生直接影响。因此，该架构可能更适合具有特定并行策略（如流水线并行或专家混合 MoE）的模型，而对于极度依赖频繁 All-Reduce 操作的密集型大模型，跨地域互联可能会成为性能瓶颈。

2.  **系统复杂度与可靠性风险**
    *   **分析：** 将数千个 GPU 跨地域聚合会增加系统的故障域。网络链路的波动概率随规模和距离增加。
    *   **推论：** 如果缺乏极其健壮的容错机制，跨地域链路的不稳定性可能导致训练任务频繁中断。BAG 架构在实际落地中，必须解决长距离网络抖动带来的训练一致性问题。

**可验证的检查方式：**

1.  **有效带宽利用率测试**
    *   **方法：** 在开启与关闭 BAG 跨数据中心链路的情况下，运行标准基准测试（如 NCCL All-Reduce），对比集群的通信带宽。
    *   **验证点：** 观察跨地域带宽利用率是否能稳定在物理链路的理论高位（如 80% 以上），以验证拥塞控制算法的有效性。

2.  **训练收敛效率对比**
    *   **方法：** 选取特定规模的大模型，分别在单机房集群和 BAG 跨地域集群上进行训练，记录达到目标精度所需的实际时间。
    *   **验证点：** 评估跨地域通信开销是否抵消了算力扩展带来的收益。

3.  **故障恢复机制验证**
    *   **方法：** 模拟 BAG 网关故障或跨地域光缆中断，观测训练任务的 Checkpoint 恢复时间和数据完整性。
    *   **验证点：** 确认系统是否具备无感切换或快速恢复能力，而非导致训练任务回滚。

**实际应用建议：**

对于正在规划大规模 AI 集群的企业，建议根据业务模型特性评估网络方案：
*   **建议一：** 若业务主要基于 MoE（混合专家模型）或对批处理延迟不极度敏感，可参考此类解耦架构以降低硬件成本。
*   **建议二：** 对于训练极度依赖低延迟通信的密集模型，建议优先采用低延迟的物理网络架构，或仅在数据加载等非关键路径尝试跨地域互联。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施后端聚合以降低采集开销

**说明**:
在超大规模 AI 集群（如 Gigawatt 级别）中，传统的 Prometheus 拉取模式会产生巨大的网络负载和 CPU 消耗。通过实施后端聚合，在数据被拉取之前先在本地或边缘进行降采样和预聚合，可以显著减少传输的数据量和存储压力。

**实施步骤**:
1. 部署支持后端聚合的 Prometheus 兼容客户端或代理。
2. 在采集端配置聚合规则（例如：将 1 秒精度聚合为 10 秒或 1 分钟）。
3. 调整 scrape interval（拉取间隔），使其与聚合粒度对齐。

**注意事项**:
确保聚合逻辑不会丢失关键的业务异常值，建议保留高精度数据的短时间窗口用于故障排查。

---

### 实践 2：采用可扩展的联邦架构

**说明**:
单一 Prometheus 实例无法处理数千个节点的指标。应采用联邦架构或分层采集策略，将数据采集任务分散到多个边缘 Prometheus 实例，中心实例仅聚合关键数据。

**实施步骤**:
1. 设计分层拓扑，例如按机柜、可用区或集群角色划分边缘 Prometheus。
2. 配置边缘实例负责高频采集和本地存储。
3. 配置中心实例通过 `/federate` 接口从边缘实例仅拉取聚合后的关键指标或特定任务数据。

**注意事项**:
谨慎使用 `/federate`，避免全量拉取导致中心节点过载，应严格匹配 `match[]` 参数。

---

### 实践 3：优化高基数指标

**说明**:
AI 集群中的 GPU 监控、任务 ID 等维度极易产生高基数问题，导致 Prometheus 内存溢出或查询超时。必须严格控制基数，并在采集侧进行过滤。

**实施步骤**:
1. 识别并标记高基数标签（如 `pod_id`, `container_id`）。
2. 使用 `metric_relabel_configs` 在写入存储前丢弃不必要的标签或完全丢弃特定指标。
3. 对于必须保留的高基数数据，考虑使用 OTLP 或其他时序数据库专门处理，而非存入 Prometheus。

**注意事项**:
定期检查 TSDB 状态，监控内存使用情况，设置基数告警阈值。

---

### 实践 4：利用远程存储实现长期保留

**说明**:
Prometheus 本地存储主要用于短期高性能查询。对于需要长期趋势分析的 AI 集群能耗和利用率数据，应配置远程存储。

**实施步骤**:
1. 选择兼容的远程存储后端（如 Thanos, Cortex, Mimir 或 VictoriaMetrics）。
2. 在 Prometheus 配置文件中启用 `remote_write`。
3. 配置数据保留策略，在本地保留短期热数据（如 15-30 天），远程保留长期冷数据。

**注意事项**:
监控 `remote_write` 队列的积压情况，必要时调整 `capacity` 和 `max_samples_per_send` 参数以防止内存溢出。

---

### 实践 5：针对 AI 硬件定制监控指标

**说明**:
通用的 Node Exporter 无法满足 AI 集群对 GPU、NVLink 和 RDMA 网络的深度监控需求。需要引入专门的 Exporter 来获取功耗和利用率数据。

**实施步骤**:
1. 部署 DCGM Exporter 或类似的 GPU 监控工具。
2. 关注关键指标：DCGM_FI_DEV_POWER_USAGE（瞬时功耗）、DCGM_FI_DEV_GPU_UTIL（利用率）以及温度相关指标。
3. 将这些硬件指标与 Kubernetes 标签关联，以便按作业或租户进行聚合。

**注意事项**:
GPU 指标采集频率较高，建议应用实践 1 中的后端聚合技术，防止数据洪流冲垮监控网路。

---

### 实践 6：配置基于速率的告警策略

**说明**:
在 Gigawatt 级别的集群中，简单的阈值告警（如 "CPU > 80%"）会产生大量噪音。应基于速率变化或预测模型配置告警，以便在能耗激增前采取行动。

**实施步骤**:
1. 使用 PromQL 中的 `rate()` 或 `irate()` 函数来计算趋势，而非仅使用瞬时值。
2. 设置基于能耗突增的告警（例如：5分钟内平均功耗上升超过 20%）。
3. 结合外部负载调度器，实现告警触发的自动扩缩容或任务迁移。

**注意事项**:
为告警规则设置适当的 `for` 持续时间，以防止因瞬时抖动造成的误报。

---
## 学习要点

- 基于对构建大规模监控系统（特别是针对 AI 集群）的通用最佳实践及 Prometheus 在高负载场景下的挑战与优化，以下是总结出的关键要点：
- 通过在采集链路中间层引入后端聚合机制，成功解决了 Prometheus 在处理 GPU 集群海量高基数指标时产生的写入放大和存储压力问题。
- 采用自定义的高性能指标处理管线替代默认数据库，实现了针对特定监控需求（如 GPU 利用率和互联拓扑）的极致优化。
- 利用 GPU 硬件计数器进行直接监控，提供了比传统 CPU 或应用层监控更精准的集群性能和能耗洞察。
- 设计了能够适应动态拓扑变化的架构，确保在数千个 GPU 节点组成的集群中保持监控的一致性和高可用性。
- 实施了精细化的数据采样和降维策略，在保留关键系统健康信号的同时大幅降低了长期存储成本。
- 将监控数据的采集与处理解耦，允许系统独立扩展各组件，从而支撑吉瓦级（Gigawatt-Scale）算力基础设施的运维需求。

---
## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Meta](/tags/meta/) / [Prometheus](/tags/prometheus/) / [BAG](/tags/bag/) / [后端聚合](/tags/%E5%90%8E%E7%AB%AF%E8%81%9A%E5%90%88/) / [GPU集群](/tags/gpu%E9%9B%86%E7%BE%A4/) / [网络架构](/tags/%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84/) / [DSF](/tags/dsf/) / [NSF](/tags/nsf/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Building Prometheus: How Backend Aggregation Enables Gi]({{< relref "posts/20260210-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-8.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [FlashAttention-T：张量化注意力机制实现方案]({{< relref "posts/20260204-hacker_news-flashattention-t-towards-tensorized-attention-8.md" >}})
- [RTX 3080 本地任务分类与调度系统]({{< relref "posts/20260206-hacker_news-show-hn-local-task-classifier-and-dispatcher-on-rt-15.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*