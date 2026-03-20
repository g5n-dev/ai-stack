---
title: Amazon Bedrock 新增 CloudWatch 指标，支持监控推理时延与配额消耗
date: 2026-03-17 01:17:58+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- CloudWatch
- LLM
- TTFT
- 推理监控
- 可观测性
- 配额管理
- AWS
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: '**关于 Amazon Bedrock 新增 CloudWatch 指标的总结** **核心内容** Amazon 发布了针对 Amazon
  Bedrock 的两项全新 Amazon CloudWatch 指标：**TimeToFirstToken (TTFT)** 和 **EstimatedTPMQuotaUsage'
external_url: https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption
scenarios:
- 大语言模型
---

# Amazon Bedrock 新增 CloudWatch 指标，支持监控推理时延与配额消耗

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:20:17+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)

---

## 摘要/简介

今天，我们宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。在这篇文章中，我们将介绍它们的工作原理，以及如何使用它们设置告警、建立基线并主动管理容量。

---

## 导语

在 Amazon Bedrock 上运行推理工作负载时，对性能和资源消耗的实时监控至关重要。今天，我们推出了两项新的 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage，旨在帮助用户更细致地观测首字生成延迟和模型配额使用情况。本文将详细解读这些指标的工作原理，并演示如何利用它们设置告警与基线，从而实现更主动的容量管理和性能优化。

---

## 摘要

**关于 Amazon Bedrock 新增 CloudWatch 指标的总结**

**核心内容**
Amazon 发布了针对 Amazon Bedrock 的两项全新 Amazon CloudWatch 指标：**TimeToFirstToken (TTFT)** 和 **EstimatedTPMQuotaUsage**。这些指标旨在提升推理工作负载的运营可见性，帮助用户更好地监控性能和管理配额。

**主要功能与用途**
1.  **TimeToFirstToken (TTFT)**：
    *   **功能**：衡量从发送请求到接收首个生成令牌的时间延迟。
    *   **用途**：直接反映模型的响应速度和用户体验，是评估应用交互流畅度的关键指标。

2.  **EstimatedTPMQuotaUsage**：
    *   **功能**：估算每分钟令牌（TPM）配额的使用情况。
    *   **用途**：帮助用户实时掌握资源消耗速率，避免因突发流量超出配额限制而导致的服务中断。

**应用场景**
通过这两项指标，用户可以：
*   **设置告警**：在响应变慢或配额即将耗尽时及时收到通知。
*   **建立基线**：了解工作负载的正常性能表现和资源消耗模式。
*   **主动管理**：基于数据预测容量需求，提前进行扩容或调整，确保服务稳定性。

---

## 评论

**中心观点**
这篇文章的核心观点是：通过引入 **TimeToFirstToken (TTFT)** 和 **EstimatedTPMQuotaUsage** 这两个细粒度的 CloudWatch 指标，Amazon Bedrock 试图将生成式 AI 的运维从“盲飞”状态转变为“可观测、可量化”的数据驱动运营，从而解决企业在生产环境中对模型延迟敏感度与配额管理不可控的痛点。

**支撑理由与评价**

**1. 内容深度：从“黑盒”到“白盒”的关键拆解**
*   **事实陈述**：文章明确指出了 LLM（大语言模型）推理性能的两个核心维度：用户体验（首字生成速度）和资源成本（Token 吞吐量配额）。
*   **作者观点**：TTFT 是衡量模型响应“即时感”的黄金标准，直接影响用户对系统智能度的感知；而 TPM（Tokens Per Minute）配额则是企业级 SLA（服务等级协议）的硬约束。
*   **深度评价**：文章没有停留在 API 层面的介绍，而是深入到了运维层面。它揭示了 Bedrock 作为一个托管服务，虽然隐藏了 GPU 细节，但必须暴露逻辑层面的性能指标。这种深度切中了当前 GenAI 落地的最大痛点——**不可观测性**。没有 TTFT，优化模型就是盲人摸象；没有配额监控，业务爆发期就会触发限流。

**2. 实用价值：主动防御与成本优化的结合**
*   **事实陈述**：文中展示了如何设置 CloudWatch 告警。
*   **你的推断**：对于实际运维而言，最大的价值在于“Estimated Quota Consumption”中的 **Estimated**（估算）一词。这意味着 AWS 正在试图解决“突增性流量”导致的限流问题。
*   **实际案例说明**：假设一家客服系统在促销活动中流量激增，以往只有当 API 返回 429 错误时，运维才知道配额用完了。现在，通过监控 `EstimatedTPMQuotaUsage`，团队可以在流量达到配额的 80% 时就触发扩容或降级策略（如切换到更小、更快的模型），从而避免服务中断。

**3. 创新性：定义了 GenAI 运维的标准范式**
*   **作者观点**：虽然 CloudWatch 是老工具，但将其应用于 GenAI 的流式输出监控具有范式创新意义。
*   **分析**：在传统的 Web 服务中，我们监控 RT（Response Time）和 QPS（Queries Per Second）。但在 LLM 时代，**QPS 失去了意义，TPM 才是真实算力消耗；RT 被拆解为 TTFT（首字延迟）和 TPOT（Token 生成间隔）**。这篇文章实际上是在推行一套新的 GenAI 运维标准体系。

**反例与边界条件**

1.  **边界条件一：指标粒度的滞后性**
    *   **你的推断**：CloudWatch 指标通常有 1 分钟左右的聚合延迟。对于高频交易或实时对话系统，1 分钟前的配额使用率数据可能已经过时。如果流量在 10 秒内瞬间打满，基于 CloudWatch 的告警可能来不及反应，导致瞬间的 429 错误。因此，这套机制更适用于“趋势预测”而非“瞬时熔断”。

2.  **边界条件二：TTFT 的片面性**
    *   **作者观点**：TTFT 仅衡量了“开始说话”的时间，并未衡量“说完话”的速度。
    *   **反例**：一个模型可能 TTFT 极快（0.5秒），但生成速度极慢（每秒 1 个 Token）。用户可能会觉得模型反应快，但“说话吞吞吐吐”，体验依然很差。仅监控 TTFT 可能会掩盖生成吞吐量低的问题。

**可验证的检查方式**

1.  **TTFT 波动性实验**：
    *   **操作**：针对同一 Prompt（如“总结这篇文章”）进行 100 次调用，记录 TTFT 指标。
    *   **验证**：观察 P50 和 P99 延迟的差异。如果 P99 远大于 P50，说明 Bedrock 底层存在冷启动或资源争抢问题，单纯依靠平均值告警是不可靠的。

2.  **配额估算精度测试**：
    *   **操作**：编写脚本以恒定速率发送固定 Token 数量的请求，同时监控 `EstimatedTPMQuotaUsage`。
    *   **验证**：对比 CloudWatch 显示的数值与实际发送的 Token 数量。观察是否存在“估算偏差”。如果偏差超过 10%，则该指标不能用于精确的自动扩缩容触发器。

3.  **跨区域/跨模型对比观察**：
    *   **操作**：在 US-EAST-1 和 US-WEST-2 同时部署相同负载，对比 TTFT。
    *   **验证**：验证是否存在区域性的性能差异。这有助于验证文章中隐含的假设——即 Bedrock 的全托管一致性是否在所有地理区域均成立。

**总结**

这篇文章虽然在技术实现上只是介绍了两个新指标，但在行业层面，它标志着 **GenAI 基础设施正从“功能可用”向“生产级可运维”演进**。对于架构师而言，这意味着不能再把 LLM 当作黑盒调用，而必须建立基于 Token 经济学和延迟感知的监控体系。文章的局限性在于未涉及 TPOT（Time Per Output Token）和端到端延迟的优化建议，且依赖 Cloud

---

## 技术分析

以下是对 AWS 官方博客文章《Improve operational visibility for inference workloads on Amazon Bedrock with new CloudWatch metrics for TTFT and Estimated Quota Consumption》的深度分析报告。

---

### 深度分析报告：Amazon Bedrock 新指标与推理工作负载的可观测性

### 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点在于：**在大模型应用从“实验验证”走向“生产环境”的过程中，仅关注模型本身的准确性是不够的，必须建立基于“延迟（TTFT）”和“资源消耗（配额）”的精细化可观测体系，以实现从被动响应到主动容量管理的转变。**

### 作者想要传达的核心思想
作者传达了**“可观测性是 LLM 落地最后一公里”**的思想。通过引入 `TimeToFirstToken` (TTFT) 和 `EstimatedTPMQuotaUsage` 两个新指标，AWS 试图解决生成式 AI 应用中两个最棘手的运维痛点：
1.  **用户体验的不可感知性：** 传统 Web 请求看响应时间，但流式 LLM 的首字生成时间才是用户感知“卡顿”的关键。
2.  **资源管理的盲目性：** LLM 推理消耗的是昂贵的 GPU 资源（TPM/RPM），在突发流量下如何不超限又不浪费，需要数据支撑而非猜测。

### 观点的创新性和深度
**创新性：** 将传统的云监控指标与 LLM 的特定行为模式（Token 生成流）深度绑定。TTFT 是 LLM 特有的性能指标，它综合了网络延迟、模型加载时间、首字计算复杂度，比单纯的 HTTP Latency 更能反映推理引擎的效率。
**深度：** 文章不仅给出了指标，还隐含了 SLO（服务等级目标）的定义方法论。它暗示了运维的边界条件——即配额管理不应是“事后救火”，而应基于“预估用量”进行“事前扩容”。

### 为什么这个观点重要
随着企业将核心业务接入 LLM，系统的稳定性直接关联业务收入。如果用户等待首字生成时间过长（高 TTFT），会直接导致流失；如果触发生效配额限制，服务直接中断。这两个指标是保障 LLM 应用**可用性**和**稳定性**的基石。

### 2. 关键技术要点

### 涉及的关键技术或概念
1.  **TimeToFirstToken (TTFT)：** 从发起推理请求到模型生成第一个 Token 的时间戳。它衡量了系统的响应速度和冷启动/热启动性能。
2.  **EstimatedTPMQuotaUsage (预估 TPM 配额使用率)：** 基于当前模型调用情况，对每分钟 Token 数（TPM）配额消耗的实时估算值。
3.  **Amazon CloudWatch & Alarms：** AWS 原生的监控与告警服务，用于设置阈值触发动作。
4.  **On-Demand vs. Provisioned Throughput：** Bedrock 的两种计费与容量模式。新指标对于管理 Provisioned Throughput 尤为关键。

### 技术原理和实现方式
*   **TTFT 采集原理：** Bedrock 服务端在接收到 Prompt 后，开始进行推理计算。当模型流式输出第一个 Token 时，服务端记录时间戳并推送到 CloudWatch。这通常涉及对推理引擎（如 FFM 或 Triton）侧的钩子拦截。
*   **配额估算原理：** 系统并非在请求结束时才计算 Token，而是根据输入 Prompt 的长度和模型处理速度，或者基于已发送的 Token 流量，实时计算当前分钟内的累积 TPM 占比。这需要一个高频的采样和聚合器。

### 技术难点和解决方案
*   **难点：流式输出的指标一致性。** 在流式响应中，网络抖动可能导致 Token 到达时间不均，如何准确计算 TTFT？
*   **解决方案：** 服务端计算。TTFT 由 Bedrock 后端计算，排除了客户端网络延迟的影响，确保了指标反映的是模型推理性能而非用户网络质量。
*   **难点：配额的动态调整。**
*   **解决方案：** 引入“预估”指标。虽然不是绝对实时的账单数据，但提供了足够近似的滑动窗口值，用于触发自动扩缩容策略。

### 技术创新点分析
**从“资源监控”转向“业务体验监控”：** 传统的 CPU/内存监控无法反映 LLM 的用户体验。TTFT 直接映射到用户心理的“等待焦虑”。**从“硬限制”转向“软熔断”：** 通过监控 `EstimatedTPMQuotaUsage`，开发者可以在达到硬性 API 限流（429错误）之前，提前触发告警或实施降级策略。

### 3. 实际应用价值

### 对实际工作的指导意义
*   **性能基线建立：** 开发者可以量化不同 Prompt 复杂度下的 TTFT，从而设定合理的超时时间。
*   **成本控制：** 通过监控 TPM 使用率，可以判断是否需要购买 Provisioned Throughput（预留吞吐量）来降低成本，或者是否在为闲置资源买单。

### 可以应用到哪些场景
1.  **实时对话系统：** TTFT 是对话流畅度的核心指标。如果 TTFT > 2秒，用户会感觉机器人反应迟钝。
2.  **批量文档处理：** 在处理大量文档时，监控 TPM 可以避免任务因配额耗尽而批量失败。
3.  **自动扩缩容系统：** 利用 CloudWatch Alarms 关联 Auto Scaling，当 TPM 使用率超过 80% 时自动增加 Bedrock 实例容量。

### 需要注意的问题
*   **TTFT 的波动性：** TTFT 受 Prompt 长度影响极大。短 Prompt 和长 Prompt（如 RAG 检索后的上下文）的 TTFT 基线不同，不能设置单一阈值。
*   **估算的滞后性：** `EstimatedTPMQuotaUsage` 是估算值，在极高频突发流量下可能存在短暂的统计偏差。

### 实施建议
1.  **分位数监控：** 不要监控平均 TTFT，应监控 P90 或 P95 TTFT，因为长尾效应才是用户体验的杀手。
2.  **分级告警：** 设置 TTFT > 1s 为警告，> 3s 为严重；TPM > 80% 为扩容预警，> 95% 为紧急限流。

### 4. 行业影响分析

### 对行业的启示
这标志着**云厂商对 LLM Ops（大模型运维）的标准化**正在加速。行业正在从“拼模型参数”转向“拼工程化落地能力”。可观测性不再是锦上添花，而是生产环境的必选项。

### 可能带来的变革
*   **SLA 定义的重构：** 传统的“可用性 99.9%”将演变为“TTFT < 500ms 的概率 > 99%”。
*   **FinOps 的精细化：** 企业将更倾向于基于实际 Token 吞吐量来优化 Prompt 工程（减少废话以降低 TPM 消耗和延迟）。

### 相关领域的发展趋势
*   **OpenTelemetry for LLM：** 社区将推动更通用的 LLM 监控标准，不仅限于 Bedrock，而是覆盖所有模型提供商。
*   **智能限流：** 基于配额使用率的预测性限流算法将成为 AI 网关的标准功能。

### 5. 延伸思考

### 引发的其他思考
*   **TTFT 与 Input Length 的非线性关系：** 随着上下文窗口增大（如 128k 或 1M token），TTFT 会如何变化？是否需要引入“每千字首字时间”作为归一化指标？
*   **成本与体验的博弈：** 为了降低 TTFT，可能需要使用更强的模型或更大的实例，这增加了成本。如何建立 TTFT-成本-满意度 的效用函数？

### 可以拓展的方向
*   **多链路追踪：** 将 TTFT 与 RAG 系统的检索延迟结合，分析整个链路的瓶颈是在数据库还是在模型推理。
*   **Token 吞吐量（TPOT）：** 除了首字时间，生成速度（Time Per Output Token）同样重要，未来应期待更多关于生成吞吐量的原生指标。

### 7. 案例分析

### 成功案例分析
**场景：某电商智能客服助手**
*   **背景：** 黑色星期五大促，流量激增。
*   **应用：** 运维团队设置了 `EstimatedTPMQuotaUsage > 75%` 的告警。
*   **结果：** 在流量峰值前 10 分钟收到告警，通过 Service Quota 服务临时提升了模型限额，并启用了备用模型进行分流。虽然 TTFT 从平均 800ms 上升到了 1.5s，但服务未中断，成功支撑了大促。

### 失败案例反思
**场景：金融文档分析工具**
*   **问题：** 仅监控了 API 成功率，未监控 TTFT。
*   **现象：** 由于 Prompt 包含大量长文本，模型推理排队严重，API 虽然最终返回了 200 OK，但 TTFT 长达 20 秒。
*   **后果：** 用户以为系统死机，反复点击提交，导致雪崩效应，触发 429 限流。
*   **教训：** **“成功”不代表“可用”**。必须监控延迟指标，即使请求在技术层面是成功的。

---

## 最佳实践

### 实践 1：建立基于 TTFT 的用户体验监控基线

**说明**: 首次令牌时间 (TTFT) 是衡量生成式 AI 应用响应速度的关键指标，直接影响用户对应用“卡顿”程度的感知。通过 CloudWatch 新增的 TTFT 指标，可以量化模型生成第一个字节所需的延迟。

**实施步骤**:
1. 在 CloudWatch 控制台中，针对特定的 Bedrock 模型调用创建自定义仪表板。
2. 将 `TTFT` 指标添加到视图，并设置统计周期为 1 分钟或 5 分钟以获得平滑的视觉曲线。
3. 为不同模型或不同应用场景（如 RAG 检索增强生成）建立独立的基线。

**注意事项**: TTFT 会受到 Prompt 长度和模型复杂度的影响，建议在分析时结合 `InputTokenCount` 指标一起查看，以区分是模型性能问题还是输入负载过大导致的延迟。

---

### 实践 2：设置动态配额告警以防止服务中断

**说明**: 新增的“估算配额消耗” 指标能够实时反映您的账户接近模型速率限制 的程度。监控此指标可防止因突发流量超出配额导致的 429 (Throttling) 错误。

**实施步骤**:
1. 导航至 CloudWatch Logs Metrics 或 Bedrock 指标命名空间，找到 `EstimatedQuotaConsumption` 指标。
2. 创建 CloudWatch 告警，当配额使用率超过 80%（或根据业务需求设定的阈值）时触发。
3. 配置 SNS 主题通知运维团队，或配置自动化的扩容逻辑（如切换到预留容量）。

**注意事项**: 这是一个“估算”值，实际限流可能因后台策略调整而略有不同。建议在告警阈值上留出一定的缓冲空间，不要等到 100% 才触发告警。

---

### 实践 3：优化 Prompt 工程以降低延迟和配额消耗

**说明**: 通过监控 TTFT 和配额消耗，可以反向评估 Prompt 的效率。冗余的上下文或复杂的指令不仅会增加 TTFT，还会加速消耗配额。

**实施步骤**:
1. 分析高 TTFT 或高配额消耗时段的请求日志。
2. 对比不同 Prompt 模板下的 TTFT 表现，识别导致响应变慢的特定指令结构。
3. 实施 Prompt 压缩或精简策略，移除对生成结果无用的输入 Token。

**注意事项**: 在优化 Prompt 时，需平衡“响应速度”与“生成质量”。不要为了单纯追求低 TTFT 而牺牲了输出结果的准确性。

---

### 实践 4：实施成本归因与多模型性能对比

**说明**: 利用配额消耗指标，可以精确计算不同业务线或不同模型版本的使用成本。同时，对比不同模型（如 Claude 3 Sonnet vs Haiku）在相同负载下的 TTFT 性能。

**实施步骤**:
1. 在调用 Bedrock API 时，使用标签 区分不同的业务部门或项目。
2. 在 CloudWatch 中利用标签过滤指标，创建分部门的配额消耗报表。
3. 建立对比仪表板，并排显示不同模型在类似请求下的 TTFT 和吞吐量。

**注意事项**: 不同模型的定价策略不同，低配额消耗不一定代表低成本。建议将配额指标与 CloudWatch Cost Explorer 数据结合进行综合分析。

---

### 实践 5：构建自动化扩缩容策略

**说明**: 当 `EstimatedQuotaConsumption` 持续处于高位时，表明当前的按需配额已无法满足业务需求，需要考虑申请提升限额或购买预留容量。

**实施步骤**:
1. 编写 Lambda 函数，订阅 CloudWatch 告警状态。
2. 当配额消耗告警持续触发（例如连续 15 分钟超过 85%），自动通过 AWS Support API 提交提升限额的请求，或发送通知给管理员进行人工审批。
3. 对于生产环境关键路径，配置自动切换逻辑，在按需配额耗尽时，将非关键请求路由到成本较低但性能稍弱的模型，或排队处理。

**注意事项**: 提升服务限额 通常需要 AWS 审核时间，不要完全依赖自动化扩容来应对瞬时流量洪峰，应在业务侧实现客户端重试和退避逻辑。

---

### 实践 6：关联 CloudWatch Logs Insights 进行根因分析

**说明**: 单纯的指标只能告诉你“发生了什么”，而日志能告诉你“为什么”。将指标异常与日志关联，可以深入分析具体的请求参数或错误信息。

**实施步骤**:
1. 确保启用了 Bedrock 的模型调用日志记录到 CloudWatch Logs。
2. 当 TTFT 异常升高时，使用 CloudWatch Logs Insights 查询该时间段内的日志。
3. 过滤出 `ResponseTime` 较高的记录，检查对应的 `InputText` 或 `SystemPrompt` 是否包含异常长的上下文。

**注意事项**: 日志存储会产生费用。建议

---

## 学习要点

- Amazon Bedrock 新增了 Time to First Token (TTFT) 和 Estimated Quota Consumption 两项关键 CloudWatch 指标，填补了推理工作负载在性能监控与配额管理方面的空白。
- 通过监控 TTFT 指标，用户可以精确衡量模型生成首个令牌的延迟，从而有效评估并优化最终用户的响应体验。
- 利用 Estimated Quota Consumption 指标，用户能够实时追踪模型配额的使用情况，进而提前规划资源以避免触及服务限制。
- 这些新指标与现有的延迟和指标数指标协同工作，提供了更全面的端到端可观测性，有助于实现更精细的运营监控。
- 借助这些数据，用户可以实施基于实际使用情况的自动扩缩容策略，在保障性能的同时优化推理成本。
- 新增的监控能力支持对不同模型和配置进行 A/B 测试对比，帮助开发者做出更明智的模型选择决策。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [CloudWatch](/tags/cloudwatch/) / [LLM](/tags/llm/) / [TTFT](/tags/ttft/) / [推理监控](/tags/%E6%8E%A8%E7%90%86%E7%9B%91%E6%8E%A7/) / [可观测性](/tags/%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7/) / [配额管理](/tags/%E9%85%8D%E9%A2%9D%E7%AE%A1%E7%90%86/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Amazon Bedrock新增CloudWatch指标：TTFT与配额消耗监控]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-2.md" >}})
- [Amazon Bedrock 新增 CloudWatch 指标：TTFT 与预估配额消耗]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-5.md" >}})
- [Improve operational visibility for inference workloads]({{< relref "posts/20260316-blogs_podcasts-improve-operational-visibility-for-inference-workl-14.md" >}})
- [Amazon Bedrock 新增 CloudWatch 指标，支持监控 TTFT 和配额消耗]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-4.md" >}})
- [Amazon Bedrock 新增 CloudWatch 指标：TTFT 与配额监控]({{< relref "posts/20260314-blogs_podcasts-improve-operational-visibility-for-inference-workl-6.md" >}})
