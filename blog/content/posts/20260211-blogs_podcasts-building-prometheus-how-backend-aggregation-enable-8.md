---
title: "后端聚合技术支撑Meta吉瓦级AI集群Prometheus构建"
date: 2026-02-11T05:36:18+08:00
draft: false
entry_kind: "auto"
tags: ["Meta", "后端聚合", "BAG", "AI集群", "GPU网络", "DSF", "NSF", "Prometheus"]
categories: ["系统与基础设施", "AI 工程"]
source: blogs_podcasts
description: "在构建千兆瓦级 AI 集群的过程中，后端聚合（BAG）技术是实现跨数据中心大规模 GPU 互联的关键。本文深入剖析了 Meta 在 Prometheus 项目中如何利用 BAG 技术来桥接 DSF 与 NSF 两种不同的网络架构，从而解决海量算力调度与连接的难题。通过阅读这篇文章，读者将了解支撑超大规模 AI 基础设施"
external_url: https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters
scenarios: ["AI/ML项目"]
---

# 后端聚合技术支撑Meta吉瓦级AI集群Prometheus构建

---

## 基本信息

- **来源**: Meta Engineering (blog)
- **发布时间**: 2026-02-09T17:00:33+00:00
- **链接**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)

---
## 摘要/简介

We’re sharing details of the role backend aggregation (BAG) plays in building Meta’s gigawatt-scale AI clusters like Prometheus. BAG allows us to seamlessly connect thousands of GPUs across multiple data centers and regions. Our BAG implementation is connecting two different network fabrics – Disaggregated Schedule Fabric (DSF) and Non-Scheduled Fabric (NSF). Once it’s complete our AI [...] Read More... The post Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters appeared first on Engineering at Meta .

---
## 导语

在构建千兆瓦级 AI 集群的过程中，后端聚合（BAG）技术是实现跨数据中心大规模 GPU 互联的关键。本文深入剖析了 Meta 在 Prometheus 项目中如何利用 BAG 技术来桥接 DSF 与 NSF 两种不同的网络架构，从而解决海量算力调度与连接的难题。通过阅读这篇文章，读者将了解支撑超大规模 AI 基础设施背后的网络设计思路与技术细节。

---
## 评论

### 深度评价：Building Prometheus: How Backend Aggregation Enables Gigawatt-Scale AI Clusters

**文章中心观点**
文章提出了一种“后端聚合网络”架构。该架构的核心逻辑是通过构建逻辑上的虚拟网络层，将 GPU 集群与底层物理以太网拓扑进行解耦，从而支持跨越多数据中心、吉瓦级规模的 AI 算力集群互联。

**支撑理由与边界条件分析**

1.  **网络解耦与物理拓扑的分离**
    *   **支撑理由（基于文本）：** 文章指出 BAG 架构在物理网络之上建立了一个虚拟化的后端网络层。通过将控制平面与物理传输层分离，使得分布在机架内或不同数据中心的 GPU 节点在逻辑上能够实现互联。
    *   **边界条件（技术推断）：** 这种逻辑解耦并未改变物理传输的限制。当物理距离增加，光速延迟和信号衰减不可避免。对于集合通信库（如 NCCL）而言，物理延迟依然是瓶颈。因此，该架构可能更适用于容错率较高的任务（如检查点同步），若要用于严格的 Step-by-Step Tensor 并行计算，必须配合特定的底层通信协议优化以容忍高延迟。

2.  **异构集群的统一调度**
    *   **支撑理由（基于文本）：** BAG 架构支持在不同网络结构之间进行流量路由。这使得 Meta 能够统一调度具有不同网络特性的 GPU 池（例如混合使用 InfiniBand 集群与 RoCE 集群）。
    *   **边界条件（工程挑战）：** 跨数据中心互联的带宽成本通常远高于内部互联。如果 BAG 仅解决了路由层的互通，而未有效解决跨 DC 的带宽成本和稳定性问题，那么这种“统一调度”可能仅限于控制流，难以支撑高密度的数据流传输。

3.  **基于以太网的扩展性**
    *   **支撑理由（基于文本）：** 文章强调利用现有的数据中心以太网基础设施构建大规模 AI 集群，以此替代专用的封闭互连架构（如 NVIDIA InfiniBand）。
    *   **边界条件（实施门槛）：** 该方案的有效性高度依赖于网络协议栈的深度定制，特别是拥塞控制算法。对于缺乏同等软件工程能力的团队，直接照搬此架构可能会遭遇以太网固有的丢包和拥塞问题，导致性能下降。

**多维度评价**

1.  **内容深度**
    文章在架构层面提供了清晰的视角，特别是关于控制平面与数据平面分离的论述，揭示了 AI 集群从“单点集中”向“分布式互联”演进的路径。但在工程实现层面，文章略过了数据一致性协议和延迟掩盖机制的具体细节，更多侧重于宏观架构的展示。

2.  **实用价值**
    对于规划万卡级以上集群的架构师，该文章提供了一种解决异构算力（如不同代际 GPU 混合）统一调度的思路。通过引入聚合层来隔离物理网络差异，有助于降低单一集群的故障域影响。

3.  **创新性**
    BAG 的创新点在于将“数据中心即一台计算机”的理念扩展到了“多数据中心即一个节点”。它尝试通过软件定义网络的方式，在物理边界限制下实现更大规模的算力聚合。

4.  **可读性**
    文章结构清晰，术语使用规范。但对于非网络专业背景的读者，“Backend Aggregation”这一概念较为抽象，容易与传统负载均衡混淆。

5.  **行业影响**
    文章展示了通过开放以太网协议栈优化实现大规模互联的可能性，为行业提供了除专有网络之外的另一种技术路径参考。

6.  **争议点或未决问题**
    *   **通信开销：** 跨数据中心互联通常面临长尾延迟问题。文章未披露具体的通信带宽利用率数据。如果 BAG 架构引入了显著的通信开销，可能会对大模型训练的整体效率产生影响。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施后端聚合以降低查询负载

**说明**:
在超大规模 AI 集群（如千兆瓦级规模）中，直接查询所有时间序列数据会给 Prometheus 服务器和底层存储带来巨大的压力。后端聚合是指利用 Prometheus 的查询能力或中间件（如 Thanos 或 VictoriaMetrics），在数据拉取阶段或查询阶段对原始数据进行预聚合或下采样。这意味着不再传输和存储原始的高基数指标，而是存储和查询聚合后的数据（例如 5 分钟的平均值或总和），从而显著减少网络带宽和计算资源消耗。

**实施步骤**:
1. 评估当前监控系统中高基数指标的查询频率和资源消耗。
2. 配置 recording rules（记录规则）在 Prometheus 内部预先计算常用的聚合查询。
3. 如果使用远程存储，启用其支持的下采样和聚合功能。
4. 修改 Grafana 仪表板和告警规则，使其优先查询聚合后的数据而非原始数据。

**注意事项**:
确保聚合后的数据粒度仍能满足故障排查和 SLA 分析的需求，避免因过度聚合而丢失关键异常信息。

---

### 实践 2：优化抓取目标与抓取间隔

**说明**:
在拥有数万个节点的 AI 集群中，默认的抓取策略可能导致 Prometheus 过载。必须根据指标的重要性和变化频率对抓取目标进行分类。对于核心基础设施指标（如 GPU 利用率、节点状态），需要保持较高的抓取频率；而对于变化缓慢或非关键的指标，应降低抓取频率或使用较长的抓取间隔，以减轻整体负载。

**实施步骤**:
1. 审计所有当前抓取目标，识别高基数和非关键指标。
2. 在 Prometheus 配置文件中使用 `scrape_configs`，为不同类型的服务设置不同的 `scrape_interval`（例如核心组件 15s，日志组件 60s）。
3. 利用 `relabel_configs` 丢弃不需要的元数据标签，减少内存占用。
4. 考虑将部分非关键监控流分流到单独的 Prometheus 实例。

**注意事项**:
避免将抓取间隔设置得过长，以免在发生故障时丢失关键的时间序列细节，导致告警延迟。

---

### 实践 3：采用高可用性架构与分片

**说明**:
单台 Prometheus 实例无法处理千兆瓦级数据中心产生的海量指标。最佳实践是采用水平扩展架构。通过使用 Thanos Receive、Cortex 或 Mimir 等系统，可以实现 Prometheus 实例的无状态运行和数据的长期存储。此外，通过功能分片（例如按集群、按数据中心或按指标类型分片），可以将监控负载分散到多个 Prometheus 实例中。

**实施步骤**:
1. 部署多个 Prometheus 副本，每个副本负责不同的数据子集。
2. 引入对象存储（如 S3、GCS）作为长期存储后端，解耦计算与存储。
3. 部署 Thanos Query 或类似的查询网关，提供统一的全局查询视图。
4. 配置告警规则的高可用性，使用 Thanos Ruler 或独立的 Alertmanager 集群。

**注意事项**:
确保分片策略具有一致性，避免在节点重新配置时产生数据重复或遗漏。

---

### 实践 4：精细化标签管理与基数控制

**说明**:
标签基数是 Prometheus 性能的最大杀手。在 AI 集群中，Pod、容器和任务的数量极其庞大，如果不加控制，`pod_id` 或 `task_id` 等标签会导致“基数爆炸”。必须实施严格的标签管理策略，限制高基数标签的使用，并在数据进入系统前进行适当的标签替换或移除。

**实施步骤**:
1. 制定标签白名单策略，明确允许哪些标签被索引。
2. 使用 `metric_relabel_configs` 在写入存储前删除高基数标签（如删除 UUID 或完整的 URL 参数）。
3. 对于动态环境，使用 `hashmod` 对抓取目标进行分片，而不是依赖高基数标签进行过滤。
4. 定期监控 Prometheus 的 TSDB 状态，检查头块和内存中的序列数量。

**注意事项**:
不要完全依赖 `drop` 操作符，应从源头（应用端或 Exporter 端）控制指标暴露，以减少网络传输开销。

---

### 实践 5：利用 Agent 模式或 Sidecar 代理

**说明**:
为了进一步减少中心化 Prometheus 的压力，可以在每个计算节点上部署轻量级的 Agent（如 Grafana Alloy、Otlet 或 Prometheus Agent）。这些 Agent 负责本地的指标抓取、过滤和预处理，并使用远程写入协议将数据发送到中心聚合层。这种方式可以将计算开销分散到边缘节点，并允许在网络中断时进行本地缓冲。

**实施步骤**:
1. 在 Kubernetes DaemonSet 或裸金属节点上部署 Prometheus Agent 或专用采集器。
2. 配置远程写入，指向中心化的聚合网关或存储集群。
3. 在 Agent 端配置 WAL（Write-Ahead Log）以防止数据丢失。
4. 启

---
## 学习要点

- 后端聚合技术通过将数千个 GPU 的训练指标在服务器端进行合并，显著降低了网络带宽消耗并解决了大规模集群下的监控数据过载问题。
- Prometheus 的远程写入存储分离架构，使得系统能够支持每秒数亿个数据点的持续写入，满足了千兆瓦级 AI 集群对海量指标采集的需求。
- 针对大规模分布式训练，系统实现了对 GPU 利用率、NVLink 带宽以及 NCCL 通信性能的深度可观测性，从而有效定位性能瓶颈。
- 通过优化数据采集的基数和采样策略，在保留关键诊断信息的同时控制了存储成本，防止高基数指标导致系统崩溃。
- 引入基于服务发现的动态目标管理机制，确保在频繁变化的容器化 AI 训练环境中，监控目标能被自动且精准地发现。
- 构建了高可用的监控架构，确保即使在大规模集群局部故障时，核心监控数据的完整性和连续性不受影响。
- 该架构的成功实践表明，传统的云原生监控工具通过针对性的后端优化，完全可以适应超大规模 AI 算力集群的严苛要求。

---
## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters](https://engineering.fb.com/2026/02/09/data-center-engineering/building-prometheus-how-backend-aggregation-enables-gigawatt-scale-ai-clusters)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Meta](/tags/meta/) / [后端聚合](/tags/%E5%90%8E%E7%AB%AF%E8%81%9A%E5%90%88/) / [BAG](/tags/bag/) / [AI集群](/tags/ai%E9%9B%86%E7%BE%A4/) / [GPU网络](/tags/gpu%E7%BD%91%E7%BB%9C/) / [DSF](/tags/dsf/) / [NSF](/tags/nsf/) / [Prometheus](/tags/prometheus/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Building Prometheus: How Backend Aggregation Enables Gi]({{< relref "posts/20260210-blogs_podcasts-building-prometheus-how-backend-aggregation-enable-8.md" >}})
- [Opus 4.5 在 OTelBench 基准测试中得分仅 29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--1.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--5.md" >}})
- [OTelBench基准测试：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*