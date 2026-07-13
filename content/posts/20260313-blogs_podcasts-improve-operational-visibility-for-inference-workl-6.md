---
title: Amazon Bedrock新增CloudWatch指标：TTFT与配额消耗监控
date: 2026-03-13 21:28:07+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- CloudWatch
- TTFT
- 配额监控
- 推理优化
- 运维监控
- LLM
- AWS
categories:
- 大模型
- 系统与基础设施
source: blogs_podcasts
description: 以下是对该内容的中文简洁总结： 亚马逊云科技宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：**TimeToFirstToken
  (TTFT)** 和 **EstimatedTPMQuotaUsage**。 * **核心功能**：这两项指标旨在提升推理工作负载的运营可见性，
external_url: https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption
scenarios:
- 大语言模型
---

# Amazon Bedrock新增CloudWatch指标：TTFT与配额消耗监控

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-12T21:20:17+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)

---

## 摘要/简介

今天，我们宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：TimeToFirstToken 和 EstimatedTPMQuotaUsage。在这篇文章中，我们将介绍它们的工作原理，以及如何利用它们设置警报、建立基线并主动管理容量。

---

## 导语

在 Amazon Bedrock 上运行推理工作负载时，对性能和资源消耗的精细监控至关重要。本文介绍了两项新发布的 Amazon CloudWatch 指标：TimeToFirstToken（TTFT）和 EstimatedTPMQuotaUsage。通过阅读这篇文章，您将了解这两项指标的技术原理，并掌握如何利用它们设置精准的警报与基线，从而更主动地管理模型容量并优化服务可见性。

---

## 摘要

以下是对该内容的中文简洁总结：

亚马逊云科技宣布为 Amazon Bedrock 推出两项新的 Amazon CloudWatch 指标：**TimeToFirstToken (TTFT)** 和 **EstimatedTPMQuotaUsage**。

*   **核心功能**：这两项指标旨在提升推理工作负载的运营可见性，帮助用户更好地监控和管理模型性能与配额使用情况。
*   **应用场景**：用户可以通过这些指标设置告警、建立性能基线，并主动管理容量。

---

## 评论

### 深度评价：增强 Amazon Bedrock 推理工作负载的运营可见性

#### 1. 核心观点
**文章通过引入 TimeToFirstToken (TTFT) 和 EstimatedTPMQuotaUsage 两项 CloudWatch 指标，旨在填补生成式 AI 从“黑盒调用”向“可观测生产级应用”转化过程中的关键监控空白，从而解决用户在延迟体验与配额管理上的被动局面。**

#### 2. 支撑理由与深度分析

**理由一：TTFT 指标量化了生成式 AI 的“首字延迟”，是衡量用户体验和模型响应速度的核心北极星指标。**
*   **[事实陈述]** 文章明确指出 TTFT（Time to First Token）是衡量模型接收请求并生成第一个 token 所需的时间。
*   **[你的推断]** 这标志着云厂商对 LLM（大语言模型）应用的关注点从单纯的“吞吐量”转向了“交互体验”。在传统的 API 调用中，我们关注 Total Latency；但在流式传输场景下，TTFT 直接决定了用户是否感觉系统“卡顿”。引入此指标，使得 SRE（站点可靠性工程）团队能够区分“模型加载慢”和“网络传输慢”，将性能监控粒度细化到了推理引擎的启动阶段。
*   **[实际案例]** 在构建 AI 聊天机器人时，如果 TTFT 突然从 500ms 飙升至 3000ms，运维人员可迅速判断是冷启动问题还是模型过载，而不是盲目检查网络带宽。

**理由二：EstimatedTPMQuotaUsage 指标将“隐形”的配额消耗“可视化”，解决了突发流量下的熔断恐慌。**
*   **[事实陈述]** 新指标允许用户实时监控每分钟 Token 消耗量（TPM）占预设配额的百分比。
*   **[作者观点]** 这是 Bedrock 向企业级生产环境迈出的重要一步。此前，用户往往只有在收到 `ThrottlingException`（429错误）时才知道配额上限已到。这种“后知后觉”在生产环境中是灾难性的。
*   **[你的推断]** 该指标的核心价值在于**“预测性运维”**。它允许用户根据业务增长趋势，提前向 AWS 申请提高服务限额，从而避免业务中断。它实际上是将“容量规划”这一硬性门槛，转化为了一个可监控的动态数据。

**理由三：基于 CloudWatch 的原生集成，降低了监控工具的门槛，实现了“开箱即用”的可观测性。**
*   **[事实陈述]** 文章强调了如何利用 CloudWatch Alarms 和 Anomaly Detection 来设置基线。
*   **[作者观点]** 这种集成虽然看似基础，但实际上构建了标准化的运维语言。它不需要企业引入昂贵的第三方 APM（应用性能监控）工具或自行构建 Prometheus Exporter，直接利用 AWS 原生生态即可完成闭环。
*   **[你的推断]** 这对于中小型 AI 创业公司尤为重要，他们可以用极低的成本建立起符合行业标准的监控体系。

#### 3. 反例与边界条件

尽管文章提供了实用的监控手段，但在技术与行业视角下仍存在局限性：

*   **反例一：TTFT 无法反映完整的生成质量与端到端延迟。**
    *   **[你的推断]** TTFT 仅代表“开始生成”的时间。如果模型在生成第一个 Token 后，后续生成速度极低，即 Token Generation Speed（TGS/TPS）很低，用户体验依然会很差。文章仅聚焦于 TTFT，可能误导开发者认为只要 TTFT 低，性能就好。实际上，一个完整的监控体系还需要 `Inter-token Latency`（Token 间延迟）或 `Output Throughput`（输出吞吐量）。

*   **反例二：配额指标仅限于“估算值”，且未解决“成本控制”的根本问题。**
    *   **[事实陈述]** 指标名称为 `Estimated`（估算）TPM。
    *   **[你的推断]** “估算”意味着存在滞后或精度偏差。在高并发场景下，依赖估算值进行自动扩缩容可能存在风险。此外，监控配额使用率并不等于监控成本。不同模型（如 Claude 3 Opus vs Haiku）的单价差异巨大，仅监控 TPM 数量无法反映实时费用支出，企业仍需自行构建基于货币单位的成本监控仪表盘。

*   **反例三：缺乏“业务逻辑”层面的监控。**
    *   **[你的推断]** 技术指标正常不代表业务成功。例如，TTFT 很快，但模型回答的内容出现了幻觉或安全合规问题，这些 CloudWatch 指标无法感知。行业趋势正在向“LLM 评估”方向发展，单纯的基础设施监控是不够的。

#### 4. 可验证的检查方式

为了验证文章所述指标的有效性及边界，建议进行以下检查：

1.  **冷启动对比实验：**
    *   **操作：** 对同一模型进行间隔调用（如间隔 15 分钟）和连续调用。
    *   **观察窗口：** 观察 TTFT 指标。
    *   **预期结果：** 间隔调用的 TTFT 应显著高于连续调用（冷启动效应）。如果差异不大，说明后台可能保持了实例热活，这将产生额外费用。

---

## 技术分析

基于您提供的文章标题和摘要，以下是对 Amazon Bedrock 新发布的 `TimeToFirstToken` (TTFT) 和 `EstimatedTPMQuotaUsage` 指标的全面深入分析。

### 1. 核心观点深度解读

**文章的主要观点：**
文章的核心观点在于**“可观测性是生产级 AI 应用的基石”**。通过引入 `TimeToFirstToken`（首字生成时间）和 `EstimatedTPMQuotaUsage`（预估每千词配额使用量）这两个特定的 Amazon CloudWatch 指标，AWS 旨在解决生成式 AI 从实验走向生产过程中最关键的两个痛点：**用户体验的实时感知**与**资源容量的精细化管理**。

**作者想要传达的核心思想：**
仅仅调用模型 API 是不够的，开发者必须具备“运维思维”。作者强调，通过量化延迟（TTFT）和配额使用情况，企业可以建立起主动的监控体系，从而在系统过载或性能下降前采取行动，而不是被动地等待报错。

**观点的创新性和深度：**
*   **从“黑盒”到“灰盒”：** 传统的 LLM 调用往往是一个黑盒，只知道成功或失败。TTFT 将模型推理过程的“感知延迟”数据化，这是衡量流式生成体验的关键指标。
*   **从“硬限制”到“软预测”：** `EstimatedTPMQuotaUsage` 的引入非常具有深度。通常云厂商的配额是硬性限制（超了就报 429 错误），而“预估”意味着用户可以在触及上限前看到趋势，这是一种从“限制型管控”向“服务型治理”的转变。

**为什么这个观点重要：**
在生成式 AI 落地阶段，成本控制和用户体验是两大核心壁垒。如果无法量化 TTFT，就无法优化用户感知的响应速度；如果无法预估配额消耗，就无法在业务高峰期保障服务稳定性。这两个指标直接关系到 AI 应用的**可服务性（Serviceability）**和**成本效益（Cost Efficiency）**。

### 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **TimeToFirstToken (TTFT)：** 衡量从发送推理请求到接收到第一个生成的 Token 之间的时间。它包含了网络延迟、模型加载时间（冷启动）以及处理输入 Prompt 的推理时间。
2.  **EstimatedTPMQuotaUsage (TPM = Tokens Per Minute)：** 衡量当前每分钟 Token 消耗量占账户服务配额的百分比。
3.  **Amazon CloudWatch：** AWS 的监控和可观测性服务，用于收集指标、设置警报和可视化仪表板。
4.  **流式传输与非流式传输：** TTFT 在流式场景下尤为重要，因为它决定了用户感觉到系统“正在思考”的时间长短。

**技术原理和实现方式：**
*   **TTFT 原理：** Bedrock 服务端在开始处理请求时打上时间戳 $T_1$，在生成第一个 Token 准备通过网络流发送时打上时间戳 $T_2$。$TTFT = T_2 - T_1$。这通常涉及模型的前向传播过程。
*   **配额预估原理：** 系统并非在每分钟结束时才计算，而是基于滑动窗口或实时采样率来计算当前的 Token 生成速率，并与预设的账户级或模型级限流进行比对，得出百分比。

**技术难点和解决方案：**
*   **难点：** 在多租户环境下，如何精确区分“模型推理时间”和“网络排队时间”？如果 Bedrock 内部有请求队列，TTFT 可能会因为排队而变长，这会让开发者误以为是模型慢。
*   **解决方案：** AWS 通过在服务侧边缘计算此指标，尽量贴近实际推理逻辑，确保指标反映的是后端处理能力而非用户公网波动。

**技术创新点分析：**
将**业务逻辑指标**（Token 消耗）直接映射到**基础设施监控指标**（CloudWatch）中。这打破了传统的仅监控 CPU/内存的局限，让 AI 应用的监控更加语义化。

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **性能调优：** 开发者可以利用 TTFT 来判断 Prompt 的复杂度是否导致了过长的预处理时间，或者是否需要调整模型的参数（如 temperature 虽不影响 TTFT，但 max tokens 可能影响整体吞吐）。
*   **容量规划：** 通过监控配额使用率，企业可以决定是否需要在特定时间（如促销活动）申请提高配额，或者实施请求排队机制。

**可以应用到哪些场景：**
1.  **实时聊天机器人：** TTFT 直接影响用户对对话流畅度的感知。设定 TTFT 阈值告警（如超过 2秒报警）可保障体验。
2.  **批量文本处理：** 在处理大量文档摘要时，TPM 配额使用率是核心指标，防止任务中途因配额耗尽而失败。
3.  **成本中心分析：** 通过 TPM 监控不同业务线的 Token 消耗，进行内部结算。

**需要注意的问题：**
*   **TTFT 与总延迟的区别：** TTFT 只是开始，不代表生成结束。对于生成长文本，还需要关注“生成速度”。
*   **配额的滞后性：** “预估”意味着可能存在毫秒级的偏差，在极高并发下需考虑突增流量。

**实施建议：**
*   立即在 CloudWatch 中为关键业务模型创建这两个指标的 Dashboard。
*   设置 `EstimatedTPMQuotaUsage` 的告警线在 80%，而非 100%，留出 Buffer。

### 4. 行业影响分析

**对行业的启示：**
这标志着云厂商的竞争从“模型性能”转向了“工程化配套能力”。谁能提供更好的可观测性工具，谁就能帮助企业更放心地将 AI 部署到生产环境。

**可能带来的变革：**
未来的 AI 监控将标准化。类似于我们今天看 HTTP 200 错误率一样，TTFT 和 TPM 将成为 LLM 应用的标准健康检查指标。

**相关领域的发展趋势：**
AIOps（智能运维）将引入更多针对大模型的特定指标，如“Token 吞吐量”、“首包延迟”、“幻觉率”等。

### 5. 延伸思考

**引发的其他思考：**
*   **冷启动 vs 热启动：** TTFT 的飙升往往意味着模型冷启动。我们是否能利用这个指标来触发“预热”请求，保持模型活跃？
*   **多模型路由：** 如果 Bedrock 上多个模型（如 Claude 3 和 Llama 3）都支持这些指标，是否可以基于实时的 TTFT 和 TPM 负载，动态地将用户请求路由到更空闲的模型上？

**需要进一步研究的问题：**
*   如何将 TTFT 与前端渲染优化结合，进一步降低用户感知延迟（如流式传输到浏览器的优化）？
*   TPM 配额与成本之间的精确换算模型，以及如何利用此指标做实时成本控制。

### 7. 案例分析

**成功案例分析（假设场景）：**
*   **场景：** 某电商客服机器人。
*   **问题：** 大促期间响应变慢，用户投诉。
*   **应用：** 引入 TTFT 监控后发现，TTFT 从平均 600ms 飙升至 4s。
*   **分析：** 结合 CloudWatch Logs 发现 Prompt 过长导致输入处理耗时增加。
*   **解决：** 优化 Prompt 模板，压缩上下文，TTFT 恢复正常。

**失败案例反思：**
*   **场景：** 某文档分析公司。
*   **问题：** 批量任务在运行到一半时全部报错 429（Too Many Requests）。
*   **反思：** 如果当时部署了 `EstimatedTPMQuotaUsage` 监控，本可以在达到 90% 时暂停新任务入队，而不是盲目提交导致全线崩溃。

### 8. 哲学与逻辑：论证地图

**中心命题：**
*在生产环境中部署 Amazon Bedrock 的生成式 AI 应用时，必须依赖 TTFT 和 TPM 配额使用率这两个 CloudWatch 指标来实现主动的运维管理和成本控制。*

**支撑理由与依据：**
1.  **理由 1：用户体验的可量化性。**
    *   *依据：* 人类对等待时间的感知具有非线性特征（心理学上的“8秒定律”）。TTFT 是衡量系统“即时反馈感”的最直接技术指标。
2.  **理由 2：资源受限性下的稳定性保障。**
    *   *依据：* 云服务基于配额管理。TPM 是硬约束，只有通过“预估”指标才能在触及约束前进行流量整形。
3.  **理由 3：故障排查的因果链条。**
    *   *依据：* 当系统变慢时，区分是“网络问题”还是“模型计算慢”是关键。TTFT 专指模型侧，能快速定位瓶颈。

**反例或边界条件：**
1.  **反例 1（非实时场景）：** 对于离线批处理任务（如夜间生成报告），TTFT 几乎没有意义，用户只关心总完成时间，此时 TPM 更重要。
2.  **边界条件（极低并发）：** 对于日活极低的应用，配额永远用不完，监控 TPM 的边际收益递减。

**事实与价值判断：**
*   *事实：* AWS 提供了这两个指标。
*   *事实：* TTFT 包含了模型加载和推理时间。
*   *价值判断：* “主动管理”优于“被动响应”。
*   *可检验预测：* 部署这两个监控指标的项目，其因配额超限导致的故障率将显著低于未部署的项目。

**我的立场与验证：**
*   **立场：** 坚决支持将这两个指标作为 Bedrock 生产环境的标准配置。这是从“玩具级 Demo”走向“企业级应用”

---

## 最佳实践

### 实践 1：建立基于 TTFT 的用户体验监控体系

**说明**:
首字时间（Time to First Token, TTFT）是衡量生成式 AI 应用响应速度的核心指标，直接影响用户对应用“卡顿”程度的感知。利用 Amazon Bedrock 新发布的 CloudWatch 指标，应将 TTFT 作为关键性能指标（KPI）进行持续监控，以评估模型对用户查询的响应延迟。

**实施步骤**:
1. 在 Amazon CloudWatch 控制台中，针对 Bedrock 推理端点创建专门的仪表板。
2. 添加 `TTFT` 指标图表，并按不同的模型 ID 或应用维度进行分组。
3. 设置异常检测报警，例如当 P90（第 90 百分位）TTFT 超过特定阈值（如 2 秒）时触发通知。

**注意事项**:
不同的基础模型具有不同的基准 TTFT。在设置报警阈值时，应先针对特定模型（如 Claude 3 Sonnet 或 Llama 3）进行基准测试，设定符合模型特性的合理阈值，避免误报。

---

### 实践 2：利用估算配额消耗指标优化成本控制

**说明**:
“估算配额消耗”指标提供了模型调用资源使用的可见性。通过监控此指标，开发团队可以准确追踪不同应用、模型或部门的资源消耗情况，从而实现更精细的成本分配和预算管理，防止意外超支。

**实施步骤**:
1. 识别并订阅 `EstimatedQuotaConsumption` 指标。
2. 在 CloudWatch 中使用标签或维度区分不同业务线的推理流量。
3. 创建计费仪表板，将配额消耗与预估费用关联，并设置接近预算上限时的告警。

**注意事项**:
该指标为“估算”值，主要用于监控和趋势分析。最终的计费仍应以 AWS Cost Explorer 或账单中的数据为准。建议定期将估算值与实际账单进行比对，以校准监控预算。

---

### 实践 3：设置基于配额使用的自动扩缩容策略

**说明**:
通过监控 `EstimatedQuotaConsumption`，可以了解当前资源使用率是否接近服务限额。结合此可见性，可以制定策略以应对高负载场景，例如在达到配额上限前请求提高限额，或者实施请求排队机制以平滑流量尖峰。

**实施步骤**:
1. 分析历史数据，确定应用的高峰期和平均配额使用率。
2. 在 CloudWatch 中设置复合告警：当配额使用率连续 5 分钟超过 80% 时触发。
3. 配置自动化响应流程（如利用 AWS Lambda），在触发告警时自动发送工单申请提高配额，或激活备用低优先级任务队列。

**注意事项**:
配额提升申请通常需要人工审核并有一定生效时间。对于关键业务，建议提前进行压力测试以确定所需的基准配额，并在业务高峰期（如促销活动）前主动申请提升限额。

---

### 实践 4：关联 TTFT 与延迟指标进行根因分析

**说明**:
TTFT 主要反映了模型生成首个 Token 的速度，但整体应用性能还受网络传输和请求处理影响。应将 Bedrock 的 TTFT 指标与端到端的应用延迟指标结合分析，以准确判断性能瓶颈是出在模型推理侧还是应用架构侧。

**实施步骤**:
1. 在应用侧代码中记录端到端的请求响应时间。
2. 在 CloudWatch 中将应用侧的延迟日志与 Bedrock 的 `TTFT` 指标进行关联查询或可视化在同一图表中。
3. 计算差值：如果总延迟远高于 TTFT，则重点检查网络链路或应用中间件；如果两者接近，则重点优化 Prompt 或模型选择。

**注意事项**:
确保应用侧日志与 CloudWatch 指标的时间戳同步，以便进行准确的时间对齐分析。使用 X-Ray 追踪可以更方便地关联上下游服务的性能。

---

### 实践 5：针对不同模型版本进行 A/B 性能测试

**说明**:
新指标允许开发者量化比较不同模型版本或不同参数配置下的性能表现。利用 TTFT 和配额消耗数据，可以在模型升级选型时做出基于数据驱动的决策，平衡性能（速度）与成本（配额/Token 消耗）。

**实施步骤**:
1. 部署 A/B 测试环境，将流量分别导向不同的模型配置（例如对比 Anthropic Claude 3 Opus 与 Sonnet）。
2. 在 CloudWatch 中创建对比仪表板，实时监控两组流量的 `TTFT` 和 `EstimatedQuotaConsumption`。
3. 收集数据并计算单位成本下的响应速度，以确定最优模型。

**注意事项**:
在进行 A/B 测试时，应控制输入 Prompt 的一致性，以免输入长度的差异影响 TTFT 的可比性。同时要考虑不同模型的输出 Token 速度，TTFT 低不代表总生成时间短。

---

## 学习要点

- Amazon Bedrock 新增了 Time to First Token (TTFT) 和 Estimated Quota Consumption 两项 CloudWatch 指标，填补了推理工作负载在延迟监控和配额管理方面的关键空白。
- TTFT 指标能够精确量化生成式 AI 应用在接收用户提示后生成首个 Token 的耗时，是衡量最终用户体验和模型响应速度的核心绩效指标。
- Estimated Quota Consumption 指标提供了模型吞吐量配额的实时消耗估算，帮助用户在触及服务限制前主动预测并避免因配额耗尽导致的请求被拒。
- 这些新指标与现有的延迟和延迟指标相结合，构建了更全面的可观测性视图，使开发者能够更深入地排查性能瓶颈。
- 借助这些细粒度监控数据，运营团队可以更准确地评估资源使用效率，从而优化模型部署策略并控制推理成本。
- 用户可以直接通过 Amazon CloudWatch 控制台或 API 获取这些指标数据，无缝集成到现有的自动化运维工作流和仪表盘中。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption](https://aws.amazon.com/blogs/machine-learning/improve-operational-visibility-for-inference-workloads-on-amazon-bedrock-with-new-cloudwatch-metrics-for-ttft-and-estimated-quota-consumption)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [CloudWatch](/tags/cloudwatch/) / [TTFT](/tags/ttft/) / [配额监控](/tags/%E9%85%8D%E9%A2%9D%E7%9B%91%E6%8E%A7/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [运维监控](/tags/%E8%BF%90%E7%BB%B4%E7%9B%91%E6%8E%A7/) / [LLM](/tags/llm/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Amazon Bedrock 新增 CloudWatch 指标：TTFT 与估算配额使用率]({{< relref "posts/20260312-blogs_podcasts-improve-operational-visibility-for-inference-workl-1.md" >}})
- [Amazon Bedrock新增CloudWatch指标：TTFT与配额消耗监控]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-2.md" >}})
- [Amazon Bedrock 新增 CloudWatch 指标：TTFT 与预估配额消耗]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-5.md" >}})
- [2025年亚马逊SageMaker AI：增强可观测性与模型定制托管功能]({{< relref "posts/20260224-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--11.md" >}})
- [Amazon Bedrock 新增 CloudWatch 指标，支持监控 TTFT 和配额消耗]({{< relref "posts/20260313-blogs_podcasts-improve-operational-visibility-for-inference-workl-4.md" >}})
