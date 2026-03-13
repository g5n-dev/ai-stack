---
title: "Amazon Bedrock 新增 CloudWatch 指标：监控 TTFT 与配额消耗"
date: 2026-03-13T05:22:54+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "CloudWatch", "TTFT", "配额监控", "可观测性", "推理优化", "性能监控", "TPM"]
categories: ["大模型", "系统与基础设施"]
source: blogs_podcasts
description: "亚马逊 Bedrock 推出两项新 CloudWatch 指标，提升推理工作负载的可观测性。**TimeToFirstToken**（首个令牌时间）用于测量模型生成首个令牌的延迟，反映响应速度；**EstimatedTPMQuotaUsage**（预估 TPM 配额使用率）则帮助监控每分钟令牌（TPM）的配额消耗情况。"
external_url: https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption
scenarios: ["Web应用开发"]
---

# Amazon Bedrock 新增 CloudWatch 指标：监控 TTFT 与配额消耗

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:20:17+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)

---
## 摘要/简介

今天，我们宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。在这篇文章中，我们将介绍它们的工作原理，以及如何利用它们设置告警、建立基线并主动管理容量。

---
## 导语

在处理推理工作负载时，精确的性能监控与资源管理对于维持系统稳定性至关重要。本文介绍了 Amazon Bedrock 新推出的两项 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。通过阅读本文，您将了解这两项指标的工作原理，并掌握如何利用它们设置精准告警、建立性能基线，从而更主动地管理模型调用容量。

---
## 摘要

亚马逊 Bedrock 推出两项新 CloudWatch 指标，提升推理工作负载的可观测性。**TimeToFirstToken**（首个令牌时间）用于测量模型生成首个令牌的延迟，反映响应速度；**EstimatedTPMQuotaUsage**（预估 TPM 配额使用率）则帮助监控每分钟令牌（TPM）的配额消耗情况。通过设置告警、建立基线并主动管理容量，用户可更高效地优化性能与资源使用。

---
## 评论

### 深度评价：Amazon Bedrock 新增 CloudWatch 指标的技术与行业价值

**中心观点**
这篇文章标志着企业级生成式 AI 从“功能可用”向“生产可观测”转型的关键一步，通过引入 TimeToFirstToken (TTFT) 和配额使用率指标，旨在解决 LLM（大语言模型）应用中难以量化的用户体验瓶颈和资源规划难题。

**支撑理由与深度分析**

**1. 内容深度：精准切中 GenOps 的核心痛点**
*   **理由：** 文章不仅仅发布了两个指标，而是构建了一个完整的监控闭环。TTFT 是衡量 LLM 响应速度的核心指标，直接影响用户对“速度”的感知；而 EstimatedTPMQuotaUsage 则解决了生产环境中最棘手的“隐形限流”问题。
*   **深度分析：** 在传统的 Web 应用中，我们关注延迟和吞吐量。但在推理场景中，延迟被分解为 TTFT（首字生成时间）和 TPOT（两字间生成时间）。文章聚焦 TTFT，抓住了对话式 AI 体验的“七寸”——用户能容忍生成速度慢，但不能容忍“发呆”。
*   **事实陈述：** 文章详细描述了如何通过 CloudWatch 获取这些维度数据。
*   **你的推断：** AWS 选择这两个指标，说明其内部数据表明客户在 Bedrock 上的主要痛点已从“模型效果”转向“服务稳定性与性能可预测性”。

**2. 实用价值：从“被动救火”转向“容量治理”**
*   **理由：** 文章提供了具体的告警设置建议。这对 FinOps（云成本优化）和 SRE（站点可靠性工程）极具价值。
*   **结合实际案例：** 想象一个电商客服机器人，在“黑五”大促期间流量激增。如果没有 `EstimatedTPMQuotaUsage` 指标，系统可能会在毫无预警的情况下触发 429 (Too Many Requests) 错误，导致客服瘫痪。有了该指标，团队可以提前设置阈值（如 80%），触发自动扩容或降级策略。
*   **作者观点：** 这种将配额可视化的做法，实际上是把“隐性资源”变成了“显性资产”，是企业将 AI 实验室项目转化为生产级应用的必要条件。

**3. 创新性：填补了托管型 LLM 服务的监控空白**
*   **理由：** 在 Bedrock 等全托管服务中，用户无法访问底层 GPU 实例的监控数据（如 NVIDIA GPU Utilization）。
*   **创新点：** AWS 提供了“业务层”的指标来映射“资源层”的状态。`EstimatedTPMQuotaUsage` 是一种创新，它不是告诉你服务器负载多少，而是告诉你“离被平台封禁还有多远”。这是在多租户隔离架构下，对用户最有意义的“容量”定义。

**反例与边界条件**

1.  **指标粒度的局限性（反例）：**
    *   **你的推断：** TTFT 和 TPM 仅仅是宏观指标。如果 TTFT 升高，文章并未提供根因分析工具。是因为模型本身变慢了？还是 Bedrock 后端冷启动？还是网络延迟？仅凭这两个指标，运维人员依然处于“盲人摸象”的状态，无法定位是模型提供商的问题还是 AWS 网络的问题。

2.  **估算值的可信度风险（边界条件）：**
    *   **事实陈述：** 指标名称包含 `Estimated`（估算）。
    *   **作者观点：** “估算”意味着存在误差。在极端突发流量下，估算值可能滞后于实际限制。如果用户完全依赖此指标进行自动扩容，可能会遇到“指标显示 70%，但实际已经开始被限流”的情况。文章未明确说明该估算值的刷新频率和滞后容忍度。

**可验证的检查方式**

1.  **TTFT 与模型大小的相关性实验：**
    *   *操作：* 选用同一模型系列（如 Claude 3 Haiku 和 Opus），发送相同 Prompt，记录 TTFT。
    *   *预期：* 验证 TTFT 是否随模型参数量级线性增加，并观察 Prompt 长度对 TTFT 的影响系数。

2.  **配额限流阈值压力测试：**
    *   *操作：* 编写脚本持续发送请求，直至 TPM 配额耗尽。
    *   *观察窗口：* 观察 `EstimatedTPMQuotaUsage` 达到 100% 时，是否立即伴随出现 `ThrottlingException` 错误。
    *   *验证点：* 验证该指标作为“熔断前兆”的准确性和提前量。

3.  **跨区域基线对比：**
    *   *操作：* 在不同 AWS 区域（如 us-east-1 与 eu-west-1）部署相同负载。
    *   *预期：* 由于底层算力分布不同，不同区域的 TTFT 基线可能存在差异，验证该指标能否反映出区域性的性能劣化。

**总结评价**

这篇文章虽然篇幅不长，但技术定位极其精准。它没有谈论炫酷的模型算法，而是聚焦于“最后一公里”的工程稳定性。

**行业影响：** 这标志着 MaaS（Model as a Service）厂商开始内卷“可观测性”。此前，OpenAI、Anthropic 等主要关注 API 能力，而 AWS Bedrock 通过集成 CloudWatch，展示了云厂商在“企业级落地”层面的护城河——即不仅仅是卖模型，而是卖

---
## 技术分析

以下是对 AWS 官方博客文章《Improve operational visibility for inference workloads on Amazon Bedrock with new CloudWatch metrics for TTFT and Estimated Quota Consumption》的深度分析。

---

# 1. 核心观点深度解读

**主要观点：**
文章的核心在于宣布并阐释 Amazon Bedrock 引入的两项关键 Amazon CloudWatch 指标：**TimeToFirstToken (TTFT)** 和 **EstimatedTPMQuotaUsage**。作者主张，通过这两项指标，开发者可以将生成式 AI 应用的监控从“黑盒”状态转变为“可观测、可量化”的状态，从而实现更精细的容量规划和用户体验优化。

**核心思想：**
作者传达的核心思想是**“可观测性是生产级 AI 应用的基石”**。在生成式 AI 领域，仅关注模型是否“调用成功”是不够的，必须深入到模型的响应延迟（性能）和配额消耗（资源）维度。AWS 通过将底层基础设施指标暴露给用户，赋予了用户主动管理服务稳定性和成本的能力。

**观点的创新性与深度：**
*   **从“可用性”到“体验性”的转变：** 传统监控多关注 API 错误率（如 200/500），而 TTFT 直接关联到最终用户的“感知延迟”。这是将监控视角从运维层提升到了业务体验层。
*   **从“被动限流”到“主动规划”的转变：** 引入 `EstimatedTPMQuotaUsage` 解决了云端托管模型最大的痛点之一——配额盲区。用户不再需要等到触发 429 (Too Many Requests) 错误才知道限额已满，而是可以提前预测并申请提升。

**重要性：**
随着企业将大语言模型（LLM）从原型实验推向生产环境，**延迟波动**和**并发限制**成为了两大核心瓶颈。这两项指标的发布，直接击中了生产环境运维的痛点，对于保障 SLA（服务等级协议）和维持业务连续性至关重要。

# 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **Time To First Token (TTFT)：** 首个令牌生成时间。即从发送请求到接收到模型生成的第一个字符的时间跨度。
2.  **Estimated TPM Quota Usage：** 估算的每分钟 Token 配额使用率。
3.  **Amazon CloudWatch：** AWS 的监控和可观测性服务。
4.  **Throttling (限流)：** 当请求超过系统预设容量时的保护机制。

**技术原理和实现方式：**
*   **TTFT 的测量原理：** TTFT 包含了三个时间段的总和：**网络传输时间**（请求发往服务器）+ **首字节处理时间**（模型加载上下文、预热）+ **推理计算时间**（生成第一个 Token）。Bedrock 在服务端记录请求开始时间和首字节输出时间，差值即为 TTFT。
*   **配额估算原理：** 系统基于当前时间窗口（如 1 分钟或 10 分钟，取决于具体的计费/限制逻辑）内实际处理的输入（Prompt）和输出（Completion）Token 数量，计算出一个相对于当前账户限额的百分比。

**技术难点与解决方案：**
*   **难点：流式输出的统计。** 在流式响应中，数据是分块返回的，很难精确界定“第一个 Token”何时到达客户端。
*   **解决方案：** Bedrock 在底层基础设施层拦截并记录这一事件，将其作为标准指标推送至 CloudWatch，无需用户在应用代码层面手动编写复杂的计时逻辑。

**技术创新点分析：**
*   **配额的“预测性”：** 传统的配额监控往往是后置的（即：超了才报错）。`Estimated` 一词表明该指标可能包含了一定的滑动窗口算法或趋势预测，使得用户能“看到”即将发生的限流，而不仅仅是记录已发生的限流。

# 3. 实际应用价值

**对实际工作的指导意义：**
*   **性能基线建立：** 开发者可以利用 TTFT 确定不同模型（如 Claude 3 vs. Llama 3）在特定 Prompt 长度下的标准响应时间。
*   **成本与容量控制：** 通过监控配额使用率，财务和运维团队可以避免因突发流量导致的意外限流，确保业务高峰期的服务可用性。

**应用场景：**
1.  **实时聊天机器人：** TTFT 是衡量用户“等待感”的核心指标。若 TTFT > 2秒，用户体验会显著下降。
2.  **批量文本处理任务：** 在处理大量文档时，监控 TPM 配额使用率可以最大化吞吐量，同时避免因触发限流而导致任务失败。
3.  **A/B 测试：** 比较不同 Prompt 工程策略对 TTFT 的影响，从而优化 Prompt 以减少首字延迟。

**需要注意的问题：**
*   **Token 计算的复杂性：** 输入 Token 和输出 Token 的计费权重可能不同，且不同模型的 Tokenizer 不同，监控时需区分。
*   **区域差异：** 配额通常是按区域隔离的，需要在部署的每个区域分别设置监控。

**实施建议：**
*   立即为 Bedrock 调用配置 CloudWatch Alarms。
*   **TTFT 告警：** 设置阈值（例如 P95 > 3秒），用于检测模型冷启动或网络拥塞。
*   **配额告警：** 设置阈值（例如 > 80%），触发自动化工单以申请提高限额。

# 4. 行业影响分析

**对行业的启示：**
这标志着**云原生 AI 服务正在走向成熟**。早期的 AI PaaS 往往只关注模型本身的准确性，而现在的竞争点已经扩展到了**工程化能力**（Observability, Scalability, Reliability）。可观测性正在成为 MaaS（Model as a Service）的标准配置。

**可能带来的变革：**
*   **SLA 标准化：** 企业客户在与 AI 服务提供商谈判时，将开始要求包含 TTFT 和配额透明度的 SLA 条款。
*   **FinOps 的兴起：** 精确的 Token 配额监控将推动 AI 成本管理的精细化，企业将更倾向于基于实时配额使用率来动态调整请求速率。

**相关领域的发展趋势：**
*   **OpenTelemetry for LLM：** 业界正在推动 LLM 调用的标准化追踪，AWS 的这一举措是对该趋势的响应，同时也可能推动其私有指标向开源标准靠拢。

# 5. 延伸思考

**引发的思考：**
*   **模型路由：** 如果我们能实时监控 TTFT，是否可以构建一个动态路由层？当某个模型实例变慢（TTFT 升高）时，自动将流量切换到另一个模型或备用区域。
*   **冷启动优化：** TTFT 的飙升往往源于模型的冷启动。如何利用这一指标来触发“预热”请求，保持模型处于热状态？

**未来研究方向：**
*   **端到端追踪：** 将 Bedrock 的 TTFT 与前端应用的“首屏渲染时间”结合，构建全链路延迟分析。
*   **智能限流算法：** 基于 `EstimatedTPMQuotaUsage` 实现客户端的平滑限流，而非服务端的硬性拒绝。

# 6. 实践建议

**如何应用到自己的项目：**
1.  **启用指标：** 确认 Bedrock 应用已开启 CloudWatch Logs 和 Metrics 发布。
2.  **构建仪表盘：**
    *   创建一个包含 `TTFT` (Avg, P90, P95) 的图表。
    *   创建一个包含 `EstimatedTPMQuotaUsage` 的图表，并叠加 `ModelInvocationSuccess` 线。
3.  **配置告警：**
    *   **Alarm 1:** `EstimatedTPMQuotaUsage > 70%` (持续 5 分钟) -> 发送通知给运维团队。
    *   **Alarm 2:** `TTFT P95 > 2000ms` -> 检查网络或模型状态。

**具体行动建议：**
*   **代码层面：** 在你的 Boto3 或 LangChain 代码中，确保捕获 `InvocationMetrics` 部分并记录下来，即使 CloudWatch 已经提供了概览，应用层面的日志有助于排查单个具体的失败案例。
*   **容量规划：** 根据业务增长曲线，提前在 AWS Support Console 申请提高 Model Invocation 的 Quota，不要等到报警响了才去申请。

**注意事项：**
*   CloudWatch 指标可能产生额外费用，需注意高频采样或高基数指标的成本。
*   `Estimated` 是估算值，在极端突发流量下可能存在滞后，需留出安全余量。

# 7. 案例分析

**成功案例（假设场景）：**
一家电商公司构建了基于 Bedrock 的 AI 客服助手。
*   **问题：** 大促期间，用户反馈“转圈圈”时间过长，且部分请求报错。
*   **分析：** 查看 CloudWatch 发现，大促开始时 TTFT 从 500ms 飙升至 3500ms（模型过载/冷启动），同时 `EstimatedTPMQuotaUsage` 达到 100%。
*   **解决：**
    1.  利用 TTFT 指标发现是 Prompt 过长导致加载慢，优化了 System Prompt。
    2.  提前一周根据配额监控趋势申请了 3 倍的 TPM 限额。
*   **结果：** 大促期间 TTFT 稳定在 800ms 以内，无 429 错误。

**失败反思：**
某初创公司直接调用 Bedrock 而未设置配额告警。
*   **后果：** 某天营销活动带来 10 倍流量，触发 AWS 硬限制，所有 API 返回 429。由于没有监控，开发人员 1 小时后才察觉。
*   **教训：** 缺乏可观测性的 AI 生产环境是“裸奔”，必须依赖 `EstimatedTPMQuotaUsage` 进行主动防御。

# 8. 哲学与逻辑：论证地图

**中心命题：**
**在生产环境中部署生成式 AI 应用时，必须依赖 TTFT 和配额消耗指标等精细化可观测性工具，才能确保系统的可靠性、用户体验的可控性以及资源规划的前瞻性。**

**支撑理由与依据：**
1.  **理由 1：用户体验由感知延迟决定。**
    *   *依据：* 心理学研究表明，2秒以上的延迟会导致用户流失率显著上升。TTFT 是衡量用户“等待感”的直接代理指标。
2.  **理由 2：云端资源存在硬性物理限制。**
    *   *依据：* GPU 算力是有限的，云厂商为了保护基础设施必须设置 TPM (Tokens Per Minute) 限额。无视这一限制会导致服务不可用。
3.  **理由 3：被动响应不如主动规划。**
    *   *依据：* 系统工程理论表明，预防性维护优于故障后修复。实时监控配额使用率允许在系统崩溃前进行扩容。

**反例或边界条件：**
1.  **反例 1：非实时/离线批处理场景。**
    *   如果是夜间生成报表，TTFT 的长短对用户体验几乎没有影响，此时 Throughput（吞吐量）比 TTFT 更重要。
2.  **反例 2：无限额或自托管模型。**
    *

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立基于 TTFT 的延迟性能基线

**说明**:
首字时间（TTFT）是衡量生成式 AI 应用响应速度的关键指标，直接影响用户体验。利用新的 CloudWatch 指标，您应当为不同的模型和提示词类型建立性能基线，以便在性能退化时迅速察觉。

**实施步骤**:
1. 在 CloudWatch 控制台中，针对特定的 Bedrock 模型创建自定义仪表板。
2. 将 `TTFT` 指标添加到仪表板，并按 `ModelId` 和 `Operation`（如 `InvokeModel` 或 `InvokeModelWithResponseStream`）进行分组。
3. 配置“异常检测”带，以自动识别偏离正常范围的延迟峰值。
4. 根据业务需求设置告警阈值，例如当 P95 TTFT 超过 2 秒时触发警报。

**注意事项**:
流式响应（`InvokeModelWithResponseStream`）和非流式响应（`InvokeModel`）的 TTFT 基线可能不同，建议分别建立监控标准。

---

### 实践 2：利用 Estimated Quota Consumption 优化成本与配额管理

**说明**:
新的“预估配额消耗”指标让您能够实时监控模型调用的资源消耗情况。通过监控此指标，可以防止因意外激增而触及服务配额限制，从而避免应用中断，并更好地预测成本。

**实施步骤**:
1. 在 CloudWatch 中查看 `EstimatedQuotaConsumption` 指标，了解当前账户下特定模型的配额使用率。
2. 创建复合告警，结合 `EstimatedQuotaConsumption` 和 `Throttles` 指标。
3. 如果发现配额使用率持续接近上限（如超过 80%），在 AWS 控制台中通过 Service Quotas 控制台申请提升配额。
4. 将此指标集成到成本监控仪表板中，关联模型调用次数与计费影响。

**注意事项**:
该指标是“预估”值，主要用于运营可见性和趋势分析，不应将其作为精确的计费依据，实际账单请参考 Cost Explorer。

---

### 实践 3：通过指标维度分析不同模型变体的性能

**说明**:
Bedrock 提供多种模型（如 Anthropic Claude, Meta Llama 等）。利用 CloudWatch 指标的维度功能，对比不同模型在相同负载下的 TTFT 和吞吐量，有助于为特定应用场景选择最具性价比的模型。

**实施步骤**:
1. 在 CloudWatch Logs Insights 或 Metrics Insights 中编写查询，对比多个 `ModelId` 的 `TTFT` 和 `InvocationLatency`。
2. 绘制图表，比较不同模型在处理相同 Prompt 时的响应速度和资源消耗。
3. 基于数据决定将非关键任务的工作负载迁移到延迟更低或配额更充裕的模型上。

**注意事项**:
不同模型的 Token 计费方式不同，在对比性能时，应同时结合延迟指标（TTFT）和消耗指标进行综合评估。

---

### 实践 4：设置基于 TTFT 的自动扩缩容策略

**说明**:
如果您的应用部署在 Amazon ECS 或 Kubernetes 上，且后端调用 Bedrock，可以根据 Bedrock 返回的 TTFT 指标动态调整应用实例的数量。高 TTFT 可能意味着后端压力大或网络延迟高，增加前端实例可能有助于维持整体吞吐量。

**实施步骤**:
1. 确保您的应用已将 Bedrock 的调用日志发送到 CloudWatch。
2. 创建 CloudWatch Alarm，监控平均 TTFT 的上升趋势。
3. 配置 AWS Auto Scaling 或 Application Auto Scaling 策略，将上述 Alarm 作为触发源。
4. 当 TTFT 超过阈值时，自动增加应用容器或实例数量，以维持用户请求的处理能力。

**注意事项**:
TTFT 升高不一定总是需要扩容前端应用，有时是 Bedrock 服务端或网络问题。建议结合错误率和超时率共同作为扩容指标。

---

### 实践 5：实施多层级告警以区分性能波动与严重故障

**说明**:
单一维度的监控容易产生误报。建议实施多层级告警策略，将“轻微的性能抖动”与“严重的可用性问题”区分开来，从而减少告警疲劳并确保关键问题得到及时处理。

**实施步骤**:
1. **第一级（警告）**: 设置当 `TTFT` 连续 5 分钟高于平均值 20% 时发送 SNS 通知给开发团队。
2. **第二级（严重）**: 设置当 `TTFT` 超过硬性阈值（如 10 秒）或 `EstimatedQuotaConsumption` 达到 95% 时，触发 PagerDuty 或直接致电值班人员。
3. 利用 CloudWatch Composite Alarms（组合告警）逻辑，确保只有在 `TTFT` 高且 `ErrorRate` 同时上升时才触发最高级别警报。

**注意事项**:
在设置阈值前，请务必收集至少一周的历史数据以确定合理的基准值，避免在正常

---
## 学习要点

- Amazon Bedrock 新增了 CloudWatch 指标，用于监控推理工作负载的运营可见性。
- 新增的首个 Token 生成时间（TTFT）指标，可帮助用户衡量并优化模型响应的初始延迟。
- 新增的估算配额消耗（Estimated Quota Consumption）指标，能够实时追踪模型使用量以防止触及服务限额。
- 通过监控 TTFT，开发者可以识别性能瓶颈并改善最终用户的交互体验。
- 利用配额消耗指标，团队可以更精准地进行容量规划，确保生产环境的稳定性。
- 这些新指标通过 Amazon CloudWatch 集成，无需额外工具即可实现统一的监控和告警管理。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [CloudWatch](/tags/cloudwatch/) / [TTFT](/tags/ttft/) / [配额监控](/tags/%E9%85%8D%E9%A2%9D%E7%9B%91%E6%8E%A7/) / [可观测性](/tags/%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [性能监控](/tags/%E6%80%A7%E8%83%BD%E7%9B%91%E6%8E%A7/) / [TPM](/tags/tpm/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Amazon Bedrock 新增 CloudWatch 指标：TTFT 与估算配额使用率]({{< relref "posts/20260312-blogs_podcasts-improve-operational-visibility-for-inference-workl-1.md" >}})
- [Amazon Bedrock新增CloudWatch指标：TTFT与配额消耗监控]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-2.md" >}})
- [2025年亚马逊SageMaker AI：增强可观测性与模型定制托管功能]({{< relref "posts/20260224-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--11.md" >}})
- [Amazon SageMaker AI 2025回顾：灵活训练计划与推理性价比优化]({{< relref "posts/20260222-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025回顾：弹性训练计划与推理性价比提升]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*