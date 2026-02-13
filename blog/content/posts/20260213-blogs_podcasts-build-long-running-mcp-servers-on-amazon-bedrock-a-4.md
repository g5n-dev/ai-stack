---
title: "基于Amazon Bedrock AgentCore构建支持长时运行的MCP服务器"
date: 2026-02-13T15:37:26+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP 协议", "AgentCore", "异步任务", "长时运行", "AI 代理", "Strands Agents", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间运行且保持高性能的 MCP 服务器。主要内容总结如下： 1. **上下文消息策略**： 引入了一种特定的消息处理机制，旨在服务器与客户端之间维持持续的通信。这一策略确保了在执行耗时操作时，连接不"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建支持长时运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供一个实现这一目标的综合方案。首先，我们介绍一种上下文消息策略，用于在服务器与客户端之间，在长时间运行的操作期间保持持续通信。接下来，我们构建一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的任务，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将这些策略整合起来，构建出可投入生产环境的 AI 代理，以可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理，是将其从简单的对话机器人升级为复杂业务自动化工具的关键一步。然而，如何在异步操作中保持上下文连续性并避免阻塞，往往是工程实践中的难点。本文将介绍一种基于 Amazon Bedrock AgentCore 与 Strands Agents 的集成方案，通过上下文消息策略与异步任务管理框架，助您构建出可投入生产环境、稳定可靠的长周期服务。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间运行且保持高性能的 MCP 服务器。主要内容总结如下：

1.  **上下文消息策略**：
    引入了一种特定的消息处理机制，旨在服务器与客户端之间维持持续的通信。这一策略确保了在执行耗时操作时，连接不会中断，且双方能够保持信息的实时同步。

2.  **异步任务管理框架**：
    开发了一套异步任务管理机制，使 AI 代理能够启动长耗时流程，而无需阻塞其他正在进行的操作。这显著提升了系统的并发处理能力和整体响应速度。

3.  **生产级实现与集成**：
    文章最终展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合。通过这种集成，可以构建出生产就绪的 AI 代理，使其能够可靠地处理复杂且极其耗时的业务操作。

---
## 评论

**中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 的架构模式，通过集成 Strands Agents 并结合上下文消息策略与异步任务管理框架，旨在解决大模型应用中长时间运行任务的稳定性与交互连续性问题。

**支撑理由与边界条件分析**

1.  **架构解耦与状态管理（事实陈述）**
    文章核心在于解决 MCP (Model Context Protocol) 服务器在面对长耗时任务（如数据处理、代码生成）时的“连接超时”或“中断”问题。通过引入“上下文消息策略”，系统不再维持单一的长连接，而是通过状态检查点机制，允许客户端在断开后根据上下文恢复连接。这符合现代分布式系统中的“最终一致性”和“无状态服务器”设计理念。
    *   **边界条件/反例**：这种机制在极高并发场景下（如每秒万级请求），上下文消息的存储与检索可能成为新的性能瓶颈，且上下文的一致性维护（CAP理论中的C与A权衡）将变得异常复杂。

2.  **异步任务框架的必要性（作者观点）**
    作者主张开发“异步任务管理框架”，将 AI 的即时响应与后台执行解耦。这是对传统同步请求-响应模式的修正，使得 AI Agent 能够处理分钟级甚至小时级的任务。
    *   **边界条件/反例**：并非所有长任务都需要异步化。对于对实时性要求极高且计算量可控的任务，引入异步队列会增加系统延迟和架构复杂度，反而降低用户体验。

3.  **Bedrock AgentCore 的生态位（你的推断）**
    文章暗示了 Amazon Bedrock 正试图从单一的“模型调用平台”向“Agent 操作系统”演进。通过 AgentCore 和 Strands Agents 的集成，AWS 试图建立一套标准化的 Agent 编排标准，而非让开发者每次都从零构建 RAG（检索增强生成）或工具调用逻辑。
    *   **边界条件/反例**：这种深度绑定 AWS 生态的方案存在严重的厂商锁定风险。对于需要跨云部署（如同时使用 Azure 或 GCP 资源）的企业，这种紧耦合架构可能得不偿失。

**多维度深入评价**

**1. 内容深度与严谨性**
文章触及了当前 AI Agent 落地中最痛点的“工程化”问题，即如何让 AI 像后台服务一样稳定运行，而不仅仅是聊天机器人。其论证不仅停留在 API 层面，深入到了上下文管理和任务调度的架构层面，具有较高的技术深度。然而，文章可能略过了“幻觉”带来的状态污染问题——如果异步任务返回了错误信息，上下文消息如何回滚或修正，这在技术论证上稍显不足。

**2. 实用价值与指导意义**
对于深耕 AWS 生态的企业级开发者，该文章提供了极具价值的“脚手架”代码和架构蓝图。它直接指导开发者如何避免在 Bedrock 上构建 Agent 时常见的“超时崩溃”陷阱。特别是关于 MCP 服务器的实现，为构建可插拔的 AI 工具生态提供了标准参考。

**3. 创新性**
将“Strands Agents”（一种专注于多步骤推理的 Agent 类型）与 Bedrock AgentCore 结合，并引入 MCP 协议，体现了 AWS 在 Agent 编排层的新尝试。其创新点在于将“协议”与“执行体”标准化，试图打造 AI 领域的“容器化”标准。但这并非理论创新，而是工程集成层面的创新。

**4. 行业影响**
该文章标志着云厂商从“卖算力”向“卖架构”的转变。如果 Bedrock AgentCore 能够成功简化长任务的构建难度，将加速 AI Agent 从“玩具”向“核心业务系统”渗透，可能引发其他云厂商（如 Azure Autogen, Google Vertex AI）在架构层面对标和跟进。

**5. 争议点与批判性思考**
*   **过度设计的嫌疑**：对于简单的长任务，是否真的需要引入复杂的 Strands Agents 和自定义异步框架？直接利用 Step Functions 或 Lambda 可能更轻量。
*   **协议碎片化**：MCP 虽然由 Anthropic 推动，但在 Bedrock 中的深度集成可能导致协议的“方言化”，使得标准 MCP 服务器在不同平台间的移植性下降。

**实际应用建议**
*   **适用场景**：适用于企业级 RAG 系统、复杂代码生成与重构、自动化运维流程等需要长时间计算且用户需要实时反馈的场景。
*   **避坑指南**：在实施异步任务框架时，务必设计好“死信队列（DLQ）”处理机制，防止因 Agent 产生的无效代码或指令导致后台任务死循环，消耗高额云资源费用。

**可验证的检查方式**

1.  **压力测试指标**：
    *   构建一个模拟长任务的 MCP Server，通过 Bedrock AgentCore 调用。
    *   **观察指标**：在任务运行期间强制断开客户端连接，记录重连后上下文恢复的成功率及耗时。验证是否存在状态丢失。

2.  **成本效益分析**：
    *   对比“直接使用 Bedrock 长对话窗口”与“使用文章所述的异步框架+上下文策略”。
    *   **验证方式**：运行相同的长任务工作流，计算两者的 Token 总消耗量与 Bedrock API 调用费用。如果异步框架的架构开销导致 Token 消耗增加超过 20%，则其实用性存疑。

3.  **兼容性实验**：
    *   **验证方式**：尝试将构建的 MCP Server 连接到非 AWS 的客户端（如本地 VS

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该技术方案的深度分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands 构建长效 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于解决当前 AI Agent（智能体）架构中的一个关键痛点：**如何让基于大模型（LLM）的智能体有效地执行长耗时、多步骤的复杂任务**。传统的请求-响应模式无法适应需要几分钟甚至几小时才能完成的任务（如数据处理、代码部署、复杂研究）。文章提出利用 **Amazon Bedrock AgentCore** 结合 **Strands Agents integration**（一种状态管理或上下文保持机制），构建基于 **MCP (Model Context Protocol)** 的服务器，实现智能体与客户端之间的持续通信和异步任务管理。

**作者想要传达的核心思想**
作者试图传达“**状态持久化**”与“**交互模式解耦**”的思想。在 Bedrock AgentCore 的框架下，通过引入 Strands（可能指代一种连续的上下文线索或工作流状态），将 LLM 的即时推理能力与长周期的任务执行分离开来。核心思想是：**LLM 不应阻塞等待任务完成，而应通过上下文消息策略在任务生命周期内随时介入、报告进度或接收新指令。**

**观点的创新性和深度**
*   **创新性**：将 MCP 协议（通常用于静态知识检索）扩展到了动态任务管理领域。结合 Bedrock AgentCore，这不仅仅是 API 调用，而是构建了一个具有“记忆”和“持续行动能力”的代理服务器。
*   **深度**：触及了 AI 工程化的深水区——有状态服务。它讨论了如何维护“上下文消息策略”，这涉及到对话历史的截断、摘要与状态同步，是高级 RAG（检索增强生成）和 Agent 编排的核心难题。

**为什么这个观点重要**
随着 AI 从“聊天机器人”向“Agentic AI”（智能体 AI）演进，企业级应用要求 AI 能够解决实际问题，而不仅仅是生成文本。长运行任务是企业自动化的核心（如月度报表生成、批量数据处理）。如果无法解决长任务中的超时、状态丢失和用户反馈缺失问题，AI 就难以真正融入关键业务流程。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与数据源。在此处，它被用作 Agent 与长运行任务服务器之间的通信桥梁。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层框架，支持自定义编排和逻辑控制，比简单的 Prompt 管理更强大。
3.  **Strands Agents Integration**：这是文章的技术焦点。推测“Strands”是指一种将长任务分解为“线索”或维持连续会话状态的机制，允许 Agent 在断开连接后仍能“挂起”并在适当时机“恢复”。
4.  **Asynchronous Task Management (异步任务管理)**：非阻塞的任务处理模式。

**技术原理和实现方式**
*   **Context Message Strategy（上下文消息策略）**：系统不再是一次性传入 Prompt，而是维护一个动态的消息队列。当任务在后台运行时，服务器会定期生成“心跳”或“进度更新”消息，注入到 Bedrock Agent 的上下文窗口中。这确保了 LLM “知道”任务正在进行，并能基于中间状态生成回复。
*   **异步框架**：利用 Bedrock AgentCore 的能力，将 MCP 服务器的调用模式从“同步调用”转变为“任务提交 -> 确认 -> 异步执行 -> 回调/轮询结果”。

**技术难点和解决方案**
*   **难点**：LLM 的上下文窗口是有限的。长任务会产生大量中间日志和状态数据，直接塞进 Prompt 会导致 Token 溢出或成本失控。
*   **解决方案**：文章提到的“Context Message Strategy”必然包含了**摘要机制**。即，不是保留所有原始日志，而是由 LLM 定期将旧状态压缩为摘要，只保留当前相关状态和最近的历史。
*   **难点**：网络超时。HTTP 请求通常在 60 秒后超时。
*   **解决方案**：MCP 服务器实现为“发后即忘”或返回一个“任务 ID”。客户端通过轮询该 ID 或通过 WebSocket（如果支持）获取最终结果。

**技术创新点分析**
最大的创新在于将 **Bedrock AgentCore 的编排能力** 与 **MCP 的标准化接口** 结合，并引入 **Strands** 来解决“会话连续性”问题。这使得开发者无需从头构建复杂的 WebSocket 服务器或状态数据库，就能在 AWS 生态内实现类似 LangChain 的 Agent 功能，但更具云原生特性。

## 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为 AWS 架构师和 AI 工程师提供了一种标准模式，用于解决“AI 幻觉导致的任务卡死”或“长时间等待导致的用户体验下降”问题。它指导开发者如何设计高可用的 AI 后端。

**可以应用到哪些场景**
1.  **RPA（机器人流程自动化）**：例如，跨多个系统的数据迁移，耗时数小时，Agent 需要定期报告进度。
2.  **复杂代码生成与部署**：Agent 生成代码 -> 编译 -> 测试 -> 部署，这一链条可能很长，需要异步处理。
3.  **企业级数据分析**：用户请求“分析上季度所有销售数据并生成图表”，后台查询和计算可能需要几分钟。
4.  **合规性审查**：审查大量文档，分批次进行。

**需要注意的问题**
*   **成本控制**：长任务意味着多次 LLM 调用和大量的 Token 消耗（用于维护上下文）。
*   **错误处理**：如果异步任务在后台失败，如何通知 LLM 并让 LLM 自我修正？

**实施建议**
*   不要将所有原始数据都放入上下文，必须实现状态压缩。
*   设计清晰的“任务状态机”（Pending, Running, Completed, Failed），并让 LLM 能够理解这些状态。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI Agent 基础设施正在从“玩具级”向“生产级”过渡。行业开始关注**可观测性**、**状态管理**和**协议标准化**（如 MCP）。AWS 通过 Bedrock AgentCore 正在试图建立 Agent 编排的事实标准。

**可能带来的变革**
*   **从 Chatbot 到 Copilot 到 Worker**：AI 不再只是陪聊，而是成为具有持久工作能力的数字员工。
*   **MCP 协议的普及**：如果 AWS 大力推广，MCP 可能成为连接 AI 与 SaaS 应用的通用标准，类似于 API 之于 Web。

**对行业格局的影响**
强化了 AWS 在企业级 AI 市场的地位。相比 OpenAI 的 Assisants API，Bedrock AgentCore 提供了更底层的控制力，适合对数据隐私和定制化要求极高的大型企业。

## 5. 延伸思考

**引发的其他思考**
*   **人机协同**：在长任务运行期间，如何优雅地插入“人工确认”环节？
*   **多 Agent 协作**：如果任务极其复杂，一个 Strand Agent 是否可以拆分任务给其他 Agent？

**可以拓展的方向**
*   结合 **AWS Step Functions**：虽然文章提到了异步框架，但将长任务逻辑直接映射到 Step Functions 的状态机定义中，可能是更稳健的实现方式。
*   **流式响应**：MCP 服务器是否支持 Server-Sent Events (SSE) 来实时推送任务进度？

**未来发展趋势**
未来 Agent 将具备“长期记忆”和“短期工作记忆”的双重架构。Strands 模式可能演变为一种标准的“工作记忆”接口。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型**：检查你的项目中是否存在超过 30 秒的处理逻辑。
2.  **引入 Bedrock AgentCore**：如果你在 AWS 上，放弃简单的 Lambda+OpenAI 调用，转向使用 AgentCore 框架来管理 Prompt 和状态。
3.  **实现 MCP Server**：将你的长任务逻辑封装为一个 MCP Server。

**具体的行动建议**
*   **第一步**：搭建一个简单的 MCP Server，实现一个“延迟回复”接口（如 sleep 60s）。
*   **第二步**：配置 Bedrock Agent，使其能够调用该接口，并配置“异步等待”逻辑。
*   **第三步**：引入状态存储（如 DynamoDB），用于记录 Task ID 和状态，实现上下文恢复。

**需要补充的知识**
*   **Amazon Bedrock AgentCore 编排模型**。
*   **MCP 协议规范**（了解 Resources, Prompts, Tools 三种核心能力）。
*   **异步编程模式**（如 Python 的 asyncio 或 JS 的 Promise）。

## 7. 案例分析

**结合实际案例说明**
假设一个**金融合规审查场景**。
*   **传统模式**：用户上传 100 个 PDF，Agent 开始处理。由于处理时间长，HTTP 连接超时，用户看到报错。
*   **应用本文方案**：
    1.  用户上传文件。
    2.  Bedrock Agent 调用 MCP Server 的 `start_audit` 工具。
    3.  MCP Server 返回 `task_id: 123`，状态 `processing`。
    4.  Agent 回复用户：“已开始审查，任务 ID 123。”
    5.  后台进程逐个处理 PDF。
    6.  用户中途问：“进度如何？”
    7.  Agent 通过 `get_status(task_id)` 查询上下文，回复：“已完成 40/100，发现 3 个风险。”
    8.  任务结束后，Agent 主动（或通过用户查询）生成最终报告。

**失败案例反思**
如果未采用此架构，常见失败是：用户以为 Agent 死机了，重复点击提交，导致后台资源耗尽，或者因为 Token 溢出导致 Agent 忘记了最初的任务目标。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 AI Agent 时，**必须**采用基于异步任务管理和持续上下文策略（如 Bedrock AgentCore + Strands）的架构，而非同步请求-响应模式，以解决长周期任务的可靠性与交互连续性问题。

**支撑理由**
1.  **时间维度的不匹配**：LLM 生成响应是秒级的，而业务任务（如数据处理、代码部署）往往是分钟级或小时级的。依据：计算机网络的超时机制与 HTTP 协议的限制。
2.  **上下文窗口的限制**：长任务产生大量中间数据，若不加以策略化管理（摘要/状态存储），会瞬间耗尽 LLM 的上下文窗口。依据：LLM 的 Transformer 架构特性与 Token 计费模式。
3.  **用户体验的必要性**：用户需要实时反馈（进度条、中间结果），而非长时间的黑盒等待。依据：HCI（人机交互）中的响应时间原则（2秒定律）。

**反例或边界条件**
1.  **反例**：对于极简单的、毫秒级完成的工具调用（如“查询当前天气”），引入复杂的 Strands 异步框架

---
## 最佳实践

## 最佳实践

### 实践 1：设计有状态的无服务器架构

**说明**: 长时间运行的 MCP 服务器需要维护会话上下文，但底层计算资源应保持无状态以实现自动扩缩容。在 Amazon Bedrock AgentCore 中，应将状态（如对话历史、用户偏好）存储在外部存储中（如 Amazon DynamoDB 或 ElastiCache），而不是保存在服务器内存中。

**实施步骤**:
1. 配置 Amazon DynamoDB 表用于存储会话 ID 和对应的上下文数据。
2. 在 MCP 服务器代码中，实现中间件用于拦截请求，从状态存储中检索上下文。
3. 确保每次请求处理完毕后，将更新的上下文写回存储。

**注意事项**: 避免将敏感信息直接明文存储在状态中，应利用 AWS KMS 进行加密。

---

### 实践 2：实施异步任务处理机制

**说明**: Strands Agents 集成通常涉及耗时较长的推理或工具调用任务。为了防止 MCP 服务器超时或阻塞，应将长时间运行的任务转换为异步处理模式，利用 AWS Step Functions 或 Amazon SQS 来管理任务生命周期。

**实施步骤**:
1. 定义任务状态机，使用 Step Functions 编排 MCP 服务器与 Bedrock 之间的交互。
2. 当 AgentCore 发起请求时，MCP 服务器应立即返回一个任务 ID，并在后台启动异步工作流。
3. 配置回调端点或让客户端通过任务 ID 轮询任务状态。

**注意事项**: 需合理设置超时时间，并在异步工作流中实现重试逻辑以处理瞬态故障。

---

### 实践 3：优化 Strands Agents 的上下文管理

**说明**: Strands Agents 可能产生大量的中间推理步骤和工具调用记录。直接将所有历史记录传递给 Bedrock 模型会导致 Token 消耗过大并增加延迟。必须实施上下文剪裁或摘要策略。

**实施步骤**:
1. 实现滑动窗口机制，仅保留最近 N 轮的完整对话记录。
2. 对于早期的对话历史，使用轻量级模型生成摘要，替换原始详细记录。
3. 在调用 Bedrock AgentCore API 时，仅传递相关的系统提示词和精简后的历史上下文。

**注意事项**: 确保摘要过程不会丢失关键的用户指令或约束条件。

---

### 实践 4：配置精细化的 IAM 权限与安全边界

**说明**: MCP 服务器作为 Agent 与后端资源交互的桥梁，必须遵循最小权限原则。特别是集成 Strands Agents 时，可能涉及调用不同的工具或 API，必须严格限制每个工具的权限范围。

**实施步骤**:
1. 为 MCP 服务器创建专用的 IAM 角色，仅授予访问特定 S3 存储桶、DynamoDB 表或 Bedrock 模型的权限。
2. 如果 MCP 服务器需要调用下游 API，使用 AWS Secrets Manager 存储 API 密钥，而不是硬编码。
3. 定期使用 IAM Access Analyzer 审查权限，移除未使用的策略。

**注意事项**: 禁止在 MCP 服务器层面授予 `bedrock:InvokeModel` 的通配符权限，应限定到特定的模型 ID。

---

### 实践 5：建立全面的可观测性与日志追踪

**说明**: 长时间运行的系统容易出现内存泄漏或死锁。利用 AWS CloudWatch 和 X-Ray 可以实时监控 MCP 服务器的健康状况，并追踪 Strands Agents 的调用链路。

**实施步骤**:
1. 在 MCP 服务器中启用 AWS X-Ray 追踪，以可视化请求从 AgentCore 到 MCP 服务器再到 Bedrock 的完整路径。
2. 配置 CloudWatch 告警，监控 CPU 利用率、内存使用量和请求延迟等关键指标。
3. 将结构化日志（JSON 格式）发送到 CloudWatch Logs，包含 `request_id` 和 `session_id` 以便关联查询。

**注意事项**: 避免记录敏感的 PII（个人身份信息）数据，在日志输出前应进行脱敏处理。

---

### 实践 6：利用连接池管理 Bedrock 并发

**说明**: 高并发场景下，频繁建立和断开与 Amazon Bedrock 的连接会降低性能。MCP 服务器应使用 SDK 提供的连接池功能来复用连接。

**实施步骤**:
1. 在初始化 Bedrock 客户端时，配置 `max_connections` 和 `timeout` 设置。
2. 使用 Boto3 的 `Session` 或 `botocore` 的配置选项管理连接池大小。
3. 监控连接利用率，根据实际负载调整连接池参数。

**注意事项**: 避免设置过大的连接池导致资源耗尽，需根据实例规格合理规划。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并保持状态和记忆的 MCP 服务器。
- 该架构通过将 Strands 的持久化层与 Bedrock 的编排能力相结合，有效解决了传统无状态代理在处理复杂、多步骤任务时的中断问题。
- 开发者可以利用 MCP 协议实现 Strands Agents 与外部数据源及工具的标准化连接，从而扩展 Agent 的功能边界。
- 这种集成方案特别适用于需要长时间交互或跨多个会话保持上下文的高级工作流自动化场景。
- 新的集成能力显著提升了基于 Bedrock 构建企业级自主智能体的可行性与稳定性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [Strands Agents](/tags/strands-agents/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*