---
title: Amazon Bedrock 新增 CloudWatch 指标，提升推理任务可观测性
date: 2026-03-13 07:36:38+08:00
draft: false
entry_kind: auto
tags:
- blogs_podcasts
categories:
- 效率与方法论
source: blogs_podcasts
description: 以下是对该内容的中文总结： **标题：利用 Amazon CloudWatch 新指标提升 Amazon Bedrock 推理工作负载的可见性**
  亚马逊云科技（AWS）近日宣布推出两项针对 Amazon Bedrock 的新 Amazon CloudWatch 指标：**TimeToFirstToken**（首个令牌
external_url: https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption
scenarios:
- Web应用开发
---

# Amazon Bedrock 新增 CloudWatch 指标，提升推理任务可观测性

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:20:17+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)

---

## 摘要/简介

今天，我们宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。在这篇文章中，我们将介绍这两项指标的工作原理，以及如何利用它们设置告警、建立基线并主动管理容量。

---

## 导语

在管理大语言模型推理任务时，对性能的实时监控和资源配额的精准把控是保障服务稳定的关键。本文介绍了 Amazon Bedrock 新推出的两项 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。通过解析这两项指标的工作原理，我们将向您展示如何利用它们设置有效告警、建立性能基线，并主动管理模型调用容量，从而提升系统的可观测性与运维效率。

---

## 摘要

以下是对该内容的中文总结：

**标题：利用 Amazon CloudWatch 新指标提升 Amazon Bedrock 推理工作负载的可见性**

亚马逊云科技（AWS）近日宣布推出两项针对 Amazon Bedrock 的新 Amazon CloudWatch 指标：**TimeToFirstToken**（首个令牌时间，TTFT）和 **EstimatedTPMQuotaUsage**（预估每分钟令牌配额使用率）。

**核心功能：**

1.  **TimeToFirstToken (TTFT)：**
    *   **作用：** 衡量模型生成首个输出令牌之前所需的延迟时间。
    *   **价值：** 这是衡量生成式 AI 应用响应速度和用户体验的关键指标。通过监控 TTFT，用户可以直观地评估模型的启动速度和交互流畅度。

2.  **EstimatedTPMQuotaUsage：**
    *   **作用：** 提供对模型每分钟令牌（TPM）配额使用情况的估算。
    *   **价值：** 帮助用户实时了解资源消耗相对于配额限制的比例，从而避免因触及限额而导致的服务中断。

**应用场景：**

此次更新允许用户更深入地洞察推理工作负载的运行状况。借助这些新指标，您可以：

*   **设置告警：** 在性能下降（如 TTFT 变长）或配额使用接近阈值时及时收到通知。
*   **建立基线：** 确定应用程序在正常状态下的性能标准和资源消耗模式。
*   **主动管理容量：** 基于数据预测和规划，确保持续、稳定地运行 AI 工作负载，无需担心突发的容量瓶颈。

简而言之，这两项新功能旨在帮助开发者通过数据驱动的方式，优化 Bedrock 上的模型性能并主动管理资源配额。

---

## 评论

**中心观点**
这篇文章代表了云服务商在LLM（大语言模型）应用层监控领域的一次重要补齐，标志着行业焦点从“模型可用性”向“生成式推理性能精细化治理”的实质性转变。

**深入评价**

**1. 内容深度与论证严谨性**
*   **[事实陈述]** 文章填补了生成式AI监控的一个关键盲区。传统的CloudWatch指标（如Latency或Invocations）对于LLM流式输出过于粗糙，无法区分“首字生成时间”（TTFT）和“Token生成速率”。
*   **[你的推断]** 引入TTFT（Time to First Token）作为一级指标，表明AWS深刻理解LLM的用户体验瓶颈。TTFT涵盖了网络延迟、模型加载时间、首字Prompt处理时间，是衡量“冷启动”和“并发压力”的核心指标。
*   **[作者观点]** 论证逻辑严密，将技术指标（TTFT）与业务指标（Quota）结合，构建了完整的“性能-容量”闭环。特别是`EstimatedTPMQuotaUsage`，解决了长久以来用户无法实时感知配额消耗进度的痛点，防止因突发流量导致的限流（Throttling）。

**2. 实用价值与创新性**
*   **[事实陈述]** 文章不仅发布了指标，还提供了基于CloudWatch Alarms的自动化运维样板代码。这对于生产环境至关重要。
*   **[你的推断]** 实用价值极高。在RAG（检索增强生成）场景中，LLM的调用链路复杂，TTFT突增往往意味着向量数据库检索慢或上下文过长。该指标可作为RAG系统的“心跳监测”。
*   **[作者观点]** 创新性在于将“估算配额”透明化。在SaaS化模型服务中，配额往往是黑盒。AWS将其通过CloudWatch暴露，实际上是在推行一种“可观测性即服务”的理念，帮助用户在无需手动计算的情况下，动态调整On-Demand模式的限额。

**3. 支撑理由与边界条件**
*   **支撑理由：**
    1.  **用户体验量化：** TTFT直接对应对话的“响应速度”体感，是降低用户流失率的关键监控项。
    2.  **成本与容量平衡：** `EstimatedTPMQuotaUsage`允许用户根据实时负载动态调整预留吞吐量，避免过度配置或因突发流量导致的服务不可用。
    3.  **故障排查定位：** 结合TTFT高与TPM高，可快速判断是模型端过载还是应用端网络问题。

*   **反例/边界条件：**
    1.  **流式输出的盲区：** TTFT仅衡量首字，若网络抖动导致后续Token卡顿，TTFT无法体现。必须配合`OutputTokenCount`和时间差计算“Inter-token Latency”才能完整评估性能。
    2.  **多模型聚合的复杂性：** 若应用层使用了多个Bedrock模型（如Claude 3和Llama 3），单一的TPM指标无法反映具体哪个模型触发了限额，需要应用层代码配合打标签。
    3.  **估算的滞后性：** `EstimatedTPMQuotaUsage`基于滑动窗口估算，在极速扩容场景下可能存在1-2分钟的显示滞后，依赖它做毫秒级自动熔断可能不够精确。

**4. 行业影响与争议点**
*   **[你的推断]** 此举将迫使竞争对手（如Azure OpenAI Service、Google Vertex AI）跟进类似的细粒度监控指标。行业将不再满足于“API是否调通”，而是进入“API调得有多快”的军备竞赛。
*   **[争议点]** 数据隐私与监控的边界。虽然监控的是元数据，但在企业级合规场景下，将Prompt/Response的详细日志与性能指标关联时，仍需严格的权限控制。此外，AWS仅提供估算值而非精确计费值，可能在极端对账场景下引发争议。

**实际应用建议**
1.  **建立分层告警：** 不要仅设置单一阈值。建议设置P50、P90、P99的TTFT告警。例如，当P90 TTFT超过2秒时触发扩容，而非等到平均值飙升。
2.  **关联业务标签：** 在调用Bedrock时，务必在`TraceId`中嵌入业务ID。这样当CloudWatch报警时，能反向追踪到是哪个具体的用户查询导致了长TTFT。
3.  **区分冷热启动：** 利用TTFT监控模型的“预热”状态。如果发现TTFT呈现周期性尖峰（如每小时整点），可能是底层实例回收导致的冷启动，需考虑预留容量。

---

## 技术分析

以下是对文章《Improve operational visibility for inference workloads on Amazon Bedrock with new CloudWatch metrics for TTFT and Estimated Quota Consumption》的深入分析报告。

---

### 1. 核心观点深度解读

**主要观点：**
文章的核心观点在于：**在大模型应用从“实验验证”走向“生产环境”的过程中，仅关注模型输出的准确性是不够的，必须建立针对“生成式推理（Generative Inference）”特有的可观测性体系。** 亚马逊通过引入 `TimeToFirstToken` (TTFT) 和 `EstimatedTPMQuotaUsage` 两个新指标，填补了 Bedrock 服务在**用户体验延迟**和**资源配额管理**这两个关键维度的监控盲区。

**核心思想：**
作者传达了“精细化运维”的思想。LLM（大语言模型）的推理具有流式输出和资源消耗波动的特性。传统的 CPU/内存监控无法反映 LLM 的服务质量。作者主张通过量化“首字延迟”来锁定用户感知的响应速度，通过量化“配额使用率”来防止服务因超限而中断。这是一种**从“可用性监控”向“性能与容量治理”**的范式转变。

**观点的创新性与深度：**
*   **针对性：** 传统的 CloudWatch 指标（如 Latency）通常包含整个请求的生命周期。TTFT 专门剥离出“模型开始思考”到“吐出第一个字”的时间，这是 LLM 用户体验最敏感的指标。
*   **预测性：** `EstimatedTPMQuotaUsage` 不仅仅是历史统计，它提供了接近实时的配额消耗估算，允许用户在触及硬性限制前采取行动，变“被动报错”为“主动扩容”。

**重要性：**
随着企业将 AI 载入核心业务流（如客服、数据分析），系统的不可用或响应迟缓将直接导致业务损失。这两个指标是保障生成式 AI 应用**SLA（服务等级协议）**和**成本控制**的基石。

---

### 2. 关键技术要点

**涉及的关键技术概念：**
1.  **TimeToFirstToken (TTFT)：** 首字生成时间。指从客户端发送完整的 Prompt 到接收到模型生成的第一个 Token 的时间片段。
2.  **TPM (Tokens Per Minute)：** 每分钟处理的 Token 数量，是衡量 LLM 吞吐量和计费的核心单位。
3.  **Service Quotas（服务配额）：** 云厂商为了保护后端模型稳定性和防止滥用而设置的速率限制。
4.  **Streaming Inference（流式推理）：** 数据以流的形式逐个 Token 返回，而非一次性返回全部结果。

**技术原理与实现方式：**
*   **TTFT 捕获原理：** Bedrock 服务端在接收到请求后，会经过负载均衡、模型加载（如果模型未激活）、Prompt 处理（预处理）、以及第一次前向推理计算。CloudWatch 通过在服务端记录请求开始时间戳和第一个字节发出的时间戳，计算出差值。这排除了网络传输延迟，纯粹反映服务端处理 Prompt 的效率。
*   **配额估算原理：** 系统并非简单统计已完成的请求数，而是基于当前活跃连接的 Prompt 长度、生成的 Token 数量以及模型配置，实时计算对 TPM 的占用率，并与设定的 Quota 阈值进行比较。

**技术难点与解决方案：**
*   **难点：** 在流式响应中，TPM 是动态变化的。如果等到请求结束再统计，会有明显的滞后，导致用户在不知不觉中超限。
*   **方案：** 使用“估算”机制。系统在流式传输过程中累加 Token 计数，实时更新配额使用率指标。

---

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **性能调优：** 开发人员可以通过 TTFT 区分是 Prompt 太长导致预处理慢，还是模型负载高导致排队。
*   **成本与容量规划：** 通过监控 `EstimatedTPMQuotaUsage`，企业可以决定是否需要申请提高配额上限，或者是否需要实施“退避”策略。

**应用场景：**
1.  **实时对话系统：** 如智能客服。TTFT 直接决定了用户是否感觉“卡顿”。如果 TTFT 超过 2 秒，用户体验会急剧下降。
2.  **批量处理任务：** 如夜间文档总结。此时 TPM 监控至关重要，防止因任务爆发导致触发限流，从而中断整批任务。
3.  **A/B 测试：** 比较不同模型（如 Claude 3 Sonnet vs Opus）或不同 Prompt 长度对响应速度的影响。

**需要注意的问题：**
*   **指标粒度：** CloudWatch 指标通常有聚合周期（如 1 分钟、5 分钟）。极高并发的突发流量可能会在分钟级聚合中被“平滑”掉，导致瞬间峰值被掩盖。
*   **TTFT 的组成：** TTFT 包含了排队时间。如果 Bedrock 后端拥堵，TTFT 会升高，但这不代表模型推理速度变慢，而是资源不足。

**实施建议：**
*   建立 Dashboard，将 TTFT 和 TPM 放在同一视图中观察。
*   设置 CloudWatch Alarms：例如 TPM > 80% 时发送 SNS 通知，TTFT > 3000ms 时触发告警。

---

### 4. 行业影响分析

**对行业的启示：**
这标志着云厂商对 LLM 的监控支持开始**标准化与专业化**。此前，用户需要在应用层自己打点记录这些数据，现在 Bedrock 将其下沉到了基础设施层。这降低了企业使用大模型的门槛，提高了运维的标准化程度。

**可能的变革：**
*   **FinOps（云财务运营）的融合：** TPM 直接关联费用。未来的监控工具将更紧密地结合性能指标与成本指标，实现“性能与成本的最佳平衡点”。
*   **自动扩缩容：** 基于 `EstimatedTPMQuotaUsage`，用户可以编写 Lambda 函数，在接近配额时自动申请提高配额或动态切换到备用模型（如从高配额模型切换到低配额模型）。

---

### 5. 延伸思考

**引发的思考：**
*   **Token 计费的透明度：** 既然有了 `EstimatedTPMQuotaUsage`，服务商是否能提供更细粒度的“实时计费”功能，让用户不仅看到配额占用，还能看到实时产生的费用？
*   **多模型路由：** 如果我们能监控到 TPM 即将耗尽，是否可以构建一个智能路由层，自动将溢出的流量转发到其他云厂商或自托管模型？

**未来趋势：**
*   **可观测性左移：** 监控指标将不仅仅用于生产环境，还会集成到 CI/CD 流水线中，用于评估新 Prompt 或新模型版本的“性能等级”。

---

### 6. 实践建议

**如何应用到自己的项目：**
1.  **启用指标：** 确认你的 Bedrock 调用代码（无论是通过 SDK 还是 LangChain）已正确配置了 CloudWatch 日志组。
2.  **构建基线：** 在业务低峰期和高峰期分别运行一周，记录你的应用正常的 TTFT 范围（例如 500ms-1500ms）和 TPM 峰值。
3.  **配置分级告警：**
    *   **Warning:** TPM > 70%（开始准备扩容或限流）。
    *   **Critical:** TTFT > 5000ms（用户明显感到卡顿）或 TPM > 90%（服务即将中断）。

**需补充的知识：**
*   学习 Amazon CloudWatch Logs Insights 查询语法，以便从日志中提取更详细的 TTFT 数据（如 P50, P90, P99 分位数）。
*   了解 Bedrock 的 On-Demand 模式与 Provisioned Throughput 模式的区别，后者在 TPM 管理上有不同的表现。

---

### 7. 案例分析

**成功案例（模拟）：某电商智能客服助手**
*   **背景：** 该客服在“黑色星期五”大促期间流量激增。
*   **问题：** 运维团队发现客服回复变慢，但不知道是网络问题还是模型问题。
*   **应用：** 引入 TTFT 监控后，发现 TTFT 从平均 800ms 飙升至 5000ms，同时 `EstimatedTPMQuotaUsage` 达到 100%。
*   **解决：** 团队意识到是触发了模型的速率限制。他们立即申请了临时配额提升，并实施了简单的用户排队机制。
*   **结果：** TTFT 恢复正常，用户流失率降低。

**失败反思：忽视配额监控的代价**
*   **场景：** 某初创公司利用 Bedrock 批量处理法律文档。
*   **失误：** 没有设置 TPM 告警。
*   **后果：** 在任务运行到 90% 时，账户触发 ThrottlingException，导致任务中断。由于没有断点续传机制，数小时的处理工作前功尽弃，且第二天凌晨才能重新申请到配额。

---

### 8. 哲学与逻辑：论证地图

**中心命题:**
为了保障生产环境中生成式 AI 应用的性能稳定性与业务连续性，运维团队必须依赖 Amazon Bedrock 新增的 `TimeToFirstToken` (TTFT) 和 `EstimatedTPMQuotaUsage` 指标来构建主动式的监控与告警体系。

**支撑理由:**
1.  **用户体验的量化依据:** TTFT 是衡量用户感知响应速度的最直接代理指标。
    *   *依据:* 心理学研究表明，用户对系统响应的感知在首字反馈时最为敏感；流式生成的交互模式决定了首字延迟是“系统死活”的判断标准。
2.  **容量管理的预测性需求:** `EstimatedTPMQuotaUsage` 提供了接近实时的资源消耗视图，使得在触及硬性限制前进行干预成为可能。
    *   *依据:* 云资源的配额是硬限制，一旦超出会导致请求直接被拒绝（HTTP 429），这比服务变慢更致命。
3.  **传统指标的局限性:** 传统的 CPU/内存利用率或平均 Latency 无法准确反映 LLM 推理的特性（如 Token 生成速度、Prompt 处理耗时）。
    *   *依据:* 平均 Latency 可能掩盖了流式输出的特点；CPU 利用率在托管服务中通常是不可见的。

**反例与边界条件:**
1.  **非流式模式:** 如果应用采用非流式（等待完整响应）模式，TTFT 的重要性会降低，此时 Total Latency 更关键。
2.  **极低并发/离线任务:** 对于对延迟不敏感的离线批处理任务，TTFT 的优先级低于 TPM（吞吐量）。
3.  **自托管模型:** 如果用户使用 SageMaker 自托管模型，他们关注的是 GPU 利用率和显存，而非 Bedrock 的 TPM 配额。

**命题性质分析:**
*   **事实判断:** Bedrock 确实发布了这两个指标。
*   **价值判断:** “必须依赖”是一种价值判断，隐含了“生产环境稳定性 > 配置监控的成本”的价值观。
*   **可检验预测:** 如果使用了这两个指标并设置告警，生产环境的 MTTR（平均恢复时间）应显著低于未使用的情况。

---

## 最佳实践

### 实践 1：建立基于 TTFT 的用户体验监控体系

**说明**: 首次令牌时间 (TTFT) 是衡量生成式 AI 应用响应速度的关键指标，直接影响用户对应用“卡顿”程度的感知。利用新的 CloudWatch 指标，应专门针对 TTFT 设置告警和基准测试，以量化并优化用户等待首字生成的体验。

**实施步骤**:
1. 在 CloudWatch 控制台中找到针对 Bedrock 的命名空间，定位到 `TTFT` 指标。
2. 为不同的模型（如 Claude 3, Llama 3）和不同的提示词类型（简单/复杂）创建独立的仪表板视图。
3. 根据业务需求设定 TTFT 的阈值告警（例如：超过 2 秒触发警告），以便及时发现模型响应延迟的异常波动。

**注意事项**: TTFT 会受到提示词长度和模型复杂度的影响，建议在设置基准时区分“冷启动”和“热启动”场景。

---

### 实践 2：利用配额消耗指标优化成本与容量规划

**说明**: 新增的“估算配额消耗” 指标提供了对 Token 使用情况的实时可见性。通过监控此指标，可以准确了解当前工作负载对模型配额的消耗速度，从而在达到硬性限制之前进行扩容申请或流量控制，避免服务因配额耗尽而中断。

**实施步骤**:
1. 创建 CloudWatch 告警来监控 `EstimatedQuotaConsumption` 指标，当使用率超过账户限制的 80% 时触发通知。
2. 结合 CloudWatch Dashboard 可视化不同模型或不同应用程序的配额消耗趋势。
3. 基于历史数据，分析业务高峰期的配额需求，提前向 AWS Support 申请提高服务限额。

**注意事项**: 该指标是估算值，建议将其与 Amazon CloudWatch Logs 中的实际调用记录和成本 Explorer 数据进行定期比对，以确保计费与监控的一致性。

---

### 实践 3：实施多维度指标聚合与故障排查

**说明**: 单一的指标往往不足以定位复杂的性能瓶颈。最佳实践是将 TTFT 和配额消耗指标与现有的 Bedrock 调用指标（如调用延迟、错误率）结合，并按维度（如模型 ID、模型提供方）进行聚合，以快速定位是特定模型性能下降还是全局性的配额问题。

**实施步骤**:
1. 在 CloudWatch 中使用“数学表达式”或“指标洞察”来关联 TTFT 和 `InvocationLatency`。
2. 创建复合告警：例如，当 TTFT 升高且配额消耗接近上限时，判定为高优先级告警。
3. 利用 CloudWatch Contributor Insights 分析高延迟或高消耗的主要来源（例如特定的 API Key 或用户组）。

**注意事项**: 确保在应用程序代码中传递适当的 `ModelId` 标签，以便在 CloudWatch 中进行精确的维度过滤。

---

### 实践 4：构建自动化扩缩容与限流机制

**说明**: 仅仅监控是不够的，需要根据监控指标采取行动。利用配额消耗指标，可以构建自动化反馈回路。当检测到配额消耗过快或 TTFT 恶化时，自动触发限流策略或动态调整请求路由，以保护系统稳定性。

**实施步骤**:
1. 编写 Lambda 函数，订阅 CloudWatch 告警的 SNS 主题。
2. 当接收到高配额消耗告警时，通过 Lambda 动态调整 API Gateway 或应用程序客户端的限流参数。
3. 对于关键任务应用，配置自动路由逻辑，在主模型配额耗尽时，将非关键流量切换到备用模型或备用区域。

**注意事项**: 自动化限流应设计为“降级服务”而非“阻断服务”，确保核心功能在资源受限时仍可用。

---

### 实践 5：通过指标对比优化模型选择与提示词工程

**说明**: 不同的模型在处理相同任务时，TTFT 和 Token 消耗率差异巨大。利用这些新指标，可以进行 A/B 测试，对比不同模型（例如 Claude 3 Sonnet vs Haiku）在特定业务场景下的性能与成本效率，从而做出最优的模型选型决策。

**实施步骤**:
1. 针对同一业务任务，部署使用不同模型的推理端点。
2. 在测试环境中收集并对比各模型的 TTFT 和 `EstimatedQuotaConsumption` 数据。
3. 分析提示词长度对 TTFT 的影响，优化提示词以减少不必要的输入 Token，从而降低配额消耗并提高响应速度。

**注意事项**: 在进行模型对比时，应同时关注输出质量（通过人工评估或自动化评分）与性能指标，避免为了速度而牺牲准确性。

---

### 实践 6：长期趋势分析与容量预测

**说明**: 将 TTFT 和配额消耗指标长期存储（例如通过 CloudWatch Logs 或将指标导出至 Amazon S3/Athena），用于分析业务增长趋势。这有助于预测未来的成本和容量需求，为预算制定

---

## 学习要点

- Amazon Bedrock 新增了首字生成时间 (TTFT) 和预估配额消耗量两项关键 CloudWatch 指标，填补了推理工作负载精细监控的空白。
- TTFT 指标能够精确量化生成式 AI 模型开始输出首个 Token 之前的延迟，是衡量用户交互体验和模型响应速度的核心标准。
- 预估配额消耗量指标允许用户实时追踪模型使用情况，从而更有效地管理成本并避免因触及服务配额限制而导致的业务中断。
- 通过将这些指标与 CloudWatch 告警和仪表板集成，用户可以实现自动化运维，在性能下降或资源不足时即时触发响应。
- 新增的监控能力显著提升了推理工作负载的可观测性，使开发者能够基于数据而非直觉进行模型调优和资源规划。
- 这些指标适用于 Amazon Bedrock 上的多种基础模型和推理选项，帮助用户在混合模型架构中保持一致的性能监控标准。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [blogs_podcasts](/tags/blogs-podcasts/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [OpenAI与Anthropic模型之争：Claude Opus 4.6对决GPT 5.3 Codex]({{< relref "posts/20260210-blogs_podcasts-ainews-openai-and-anthropic-go-to-war-claude-opus--8.md" >}})
- [亚马逊利用 Nova 模型自动化新履约中心运营就绪测试]({{< relref "posts/20260210-blogs_podcasts-how-amazon-uses-amazon-nova-models-to-automate-ope-0.md" >}})
- [OpenAI在ChatGPT测试广告以支持免费访问]({{< relref "posts/20260210-blogs_podcasts-testing-ads-in-chatgpt-1.md" >}})
- [Transformers.js v4 预览版已发布 NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-3.md" >}})
- [Transformers.js v4 Preview: Now Available on NPM]({{< relref "posts/20260210-blogs_podcasts-transformersjs-v4-preview-now-available-on-npm-4.md" >}})
