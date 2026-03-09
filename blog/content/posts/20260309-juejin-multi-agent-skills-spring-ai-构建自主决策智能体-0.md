---
title: "Multi-Agent 与 Skills 结合 Spring AI 构建自主决策智能体"
date: 2026-03-09T12:20:24+08:00
draft: false
entry_kind: "auto"
tags: ["Spring AI", "Multi-Agent", "LLM", "智能体", "函数调用", "自主决策", "RAG", "系统架构"]
categories: ["AI 工程", "后端"]
source: juejin
description: "随着大语言模型技术的演进，智能体已成为实现复杂任务自动化的重要方向。本文将探讨如何利用 Spring AI 框架，结合多智能体架构与技能化设计，构建具备自主决策能力的系统。通过解析核心组件与工程化实践，我们将展示如何让智能体精准感知环境并调用工具，帮助开发者掌握构建高可用 AI 应用的关键技术。"
external_url: https://juejin.cn/post/7614889731939811355
scenarios: ["AI/ML项目", "大语言模型", "RAG应用"]
---

# Multi-Agent 与 Skills 结合 Spring AI 构建自主决策智能体

---

## 基本信息

- **作者**: 雨中飘荡的记忆
- **链接**: [https://juejin.cn/post/7614889731939811355](https://juejin.cn/post/7614889731939811355)

---
## 导语

随着大语言模型技术的演进，智能体已成为实现复杂任务自动化的重要方向。本文将探讨如何利用 Spring AI 框架，结合多智能体架构与技能化设计，构建具备自主决策能力的系统。通过解析核心组件与工程化实践，我们将展示如何让智能体精准感知环境并调用工具，帮助开发者掌握构建高可用 AI 应用的关键技术。

---
## 描述

Multi-Agent + Skills + Spring AI 构建自主决策智能体

引言

随着大语言模型（LLM）的快速发展，智能体（Agent）技术成为 AI 应用开发的热点。智能体不仅能够理解自然语言，还能感知环境、做出决策并执行操作，从而完成复杂任务。本文将介绍如何基于 Spring AI 结合多智能体（Multi-Agent）架构与技能（Skills）机制，构建具备自主决策能力的智能体系统。

---

**目录**

1. **背景与概念**
   * 什么是智能体？
   * 为什么选择 Spring AI？
   * 多智能体与技能化设计的优势

2. **Spring AI 核心组件解析**
   * `ChatClient` 与模型抽象
   * 函数调用与工具绑定
   * 记忆组件

3. **构建具备“技能”的智能体**
   * 技能接口设计
   * 实现自定义技能（例如：搜索、计算）
   * 将技能注册到 Spring AI

4. **多智能体架构设计**
   * 单体智能体的局限
   * 多智能体协作模式（如：管理者-工作者模式）
   * 智能体间的通信与路由

5. **实战案例：构建自主决策系统**
   * 需求分析
   * 代码实现示例
   * 流程演示与测试

6. **总结与展望**

---

## 1. 背景与概念

### 什么是智能体？
在 LLM 时代，智能体通常指这样一个系统：
1.  **感知**：接收用户输入或环境信息。
2.  **大脑**：利用 LLM 进行推理、规划和决策。
3.  **行动**：调用外部工具或 API 执行具体操作。
4.  **反馈**：根据执行结果调整策略，直到目标达成。

### 为什么选择 Spring AI？
Spring AI 是 Spring 生态系统中用于构建 AI 应用的抽象层。它提供了：
*   **可移植性**：轻松切换不同的模型提供商（如 OpenAI、Azure、Ollama）。
*   **企业级集成**：与 Spring Boot 的无缝结合，便于管理配置、安全和依赖。
*   **函数调用支持**：强大的 Function Calling 能力，是实现“技能”的关键。

### 多智能体与技能化设计的优势
*   **专业化**：通过 Skills，我们可以为智能体装备特定的能力（如联网搜索、数据库查询），避免 LLM 产生幻觉。
*   **协作与解耦**：Multi-Agent 架构允许将复杂任务拆解，不同的 Agent 负责不同的子任务，提高系统的鲁棒性和可维护性。

---

## 2. Spring AI 核心组件解析

在开始编码之前，我们需要了解 Spring AI 的几个核心概念：

*   **ChatClient**：这是同步和流式与 AI 模型交互的入口。它支持提示词管理、输出解析等。
*   **Function Callback**：Spring AI 将 Java 方法注册为 LLM 可以调用的“函数”。当 LLM 判断需要某个特定信息时，它会触发该函数。
*   **ChatMemory**：智能体是“无状态”的，通过 ChatMemory 组件，我们可以让智能体记住对话历史，实现上下文连贯。

---

## 3. 构建具备“技能”的智能体

### 3.1 技能接口设计
首先，我们定义一个通用的技能接口。所有的工具（如查天气、读邮件）都将实现这个接口。

```java
public interface Skill {
    String getDescription(); // LLM 需要知道这个技能是做什么的
    String getName();        // 技能的唯一标识
}
```

### 3.2 实现自定义技能
假设我们要实现一个“计算器技能”和一个“搜索技能”。

**计算器技能:**
```java
import java.util.function.Function;

public class CalculatorSkill implements Function<CalculatorSkill.Request, CalculatorSkill.Response> {

    public record Request(String expression, String operation) {}
    public record Response(double result) {}

    @Override
    public Response apply(Request request) {
        // 简单的逻辑处理
        if ("add".equals(request.operation)) {
            // 解析并计算... (此处省略具体解析逻辑)
            return new Response(100.0); // 模拟返回
        }
        return new Response(0.0);
    }
}
```

### 3.3 将技能注册到 Spring AI
在 Spring AI 中，我们通过 `ChatClient` 的 builder 配置这些函数。

```java
List<FunctionCallback> toolCallbacks = List.of(
    FunctionCallbackWrapper.builder(new CalculatorSkill())
        .withDescription("执行基本的数学运算")
        .withName("CalculatorTool")
        .build()
);

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultFunctions(toolCallbacks) // 注册技能
    .build();
```

---

## 4. 多智能体架构设计

单一的通用智能体往往在处理复杂长流程任务时表现不佳。我们可以引入**多智能体系统**。

### 4.1 常见模式：管理者-工作者
*   **Manager Agent (Root)**：负责接收用户需求，进行任务拆解，并将子任务分发给下层 Agent。
*   **Worker Agent**：拥有特定的 Skill 集合（如专门负责代码生成、专门负责文档撰写）。它们只执行自己擅长的任务，并将结果返回给 Manager。

### 4.2 实现思路
我们可以利用 Spring 的 `ApplicationContext` 管理多个 Agent Bean。

```java
@Service
public class ManagerAgent {

    private final ChatClient chatClient;
    private final List<WorkerAgent> workers;

    // 构造函数注入各个 Worker

    public String orchestrate(String userQuery) {
        // 1. Manager 分析任务
        // 2. Manager 决定调用哪个 Worker (通过函数调用或路由逻辑)
        // 3. Worker 执行具体 Skill
        // 4. Manager 汇总结果并回复
    }
}
```

---

## 5. 实战案例：构建自主决策系统

**场景**：用户想要“帮我查询当前天气，如果下雨则建议我带伞，并生成一句早安文案”。

**系统架构**：
1.  **Manager**：理解意图，决定先查天气，再根据结果生成文案。
2.  **WeatherWorker**：拥有 `WeatherService` 技能。
3.  **CopyWriterWorker**：拥有 `CreativeWriting` 技能。

**代码逻辑简述**：
Manager 调用 LLM，LLM 识别出需要调用 `get_weather` 工具。
Spring AI 拦截该调用，执行 `WeatherService` 中的 Java 方法（如调用第三方 API）。
将真实天气数据（如“大雨”）返回给 LLM。
Manager 请求 CopyWriterWorker 基于此数据生成文案。

**演示输入**：
> "外面天气怎么样？"

**内部流程**：
`Manager` -> [LLM 决策] -> 调用 `WeatherSkill` -> 获得 "大雨" -> `Manager` -> 请求 `CopyWriterSkill` -> 生成 "大雨滂沱，记得带伞，早安！"

**最终输出**：
> "目前外面下着大雨。建议您出门时务必携带雨伞。早安，愿您有个美好的一天！"

---

## 6. 总结与展望

通过结合 **Spring AI** 的便捷性、**Skills** 的模块化以及 **Multi-Agent** 的协作能力，我们构建了一个具备初步自主决策能力的智能体。

*   **优势**：代码结构清晰，易于扩展新的技能，符合 Spring 开发者的习惯。
*   **未来方向**：引入更复杂的记忆机制（如向量数据库存储长期记忆），或者利用 LangGraph4j 等库实现更复杂的状态图编排，让智能体处理更加复杂的业务流。

---
## 评论

### 中心观点
该文章提出了一种**基于 Spring AI 框架，结合“技能”抽象与多智能体协作模式来构建具备自主决策能力 AI 系统**的技术范式，旨在降低 Java 生态中 LLM 应用开发的门槛并提升系统的模块化程度。

### 支撑理由与边界条件分析

**1. 技术生态的填补与工程化落地（事实陈述）**
*   **理由**：Spring AI 的出现填补了 Java/Python 在 AI 工程化领域的鸿沟。对于拥有庞大遗留系统的企业而言，文章提出的方案极具吸引力。它允许开发者利用现有的 Spring 生态知识（如依赖注入、配置管理）来构建 Agent，而非从零学习 Python 的 LangChain 或 LangGraph。
*   **反例/边界条件**：Java 的启动时间和动态性弱于 Python。在需要高频交互或极度灵活的“工具调用”场景下，基于 Spring 的 Agent 可能面临性能瓶颈或冷启动延迟问题。

**2. “技能”抽象的模块化价值（作者观点）**
*   **理由**：文章强调“Skills”概念，这实际上是对 Prompt Engineering 和 Tool Use 的工程化封装。将业务逻辑封装为独立的 Skill，符合软件工程中的单一职责原则，使得 Agent 的能力可以像乐高积木一样插拔，极大提升了系统的可维护性和复用性。
*   **反例/边界条件**：过度封装可能导致“上下文碎片化”。如果每个 Skill 都携带大量的系统提示词，多 Agent 协作时的上下文窗口消耗会呈指数级增长，可能导致 Token 成本激增或超出模型上下文限制。

**3. Multi-Agent 协作解决复杂问题（你的推断）**
*   **理由**：文章主张通过 Multi-Agent 模式实现自主决策。这符合当前 AI 研究的前沿趋势，即通过“群体智能”或“分工协作”来突破单一模型的幻觉限制和逻辑推理天花板。例如，让一个 Agent 负责代码生成，另一个负责代码审查，比单一 Agent 完成任务更稳健。
*   **反例/边界条件**：Multi-Agent 系统的调试难度极高（死循环、无限循环调用）。此外，Agent 间的通信开销（通过自然语言）远高于函数调用，在低延迟要求的实时业务场景（如高频交易、实时风控）中并不适用。

**4. 对自主决策能力的过度乐观（批判性观点）**
*   **理由**：文章标题提到“自主决策”，暗示系统具备高度自治性。
*   **反例/边界条件**：目前的 LLM 本质上是概率预测模型，不具备真正的“意志”或“长期记忆”。在涉及高风险决策（如医疗诊断、金融大额转账）时，必须引入“人在回路”机制，完全的自主决策在当前技术条件下是危险的。

### 维度评价

#### 1. 内容深度：**[中上]**
文章成功地将复杂的 AI 概念映射到了熟悉的 Spring 框架模式上，论证了工程落地的可行性。然而，在“Multi-Agent 如何进行冲突消解”以及“如何保证分布式 Agent 的一致性”等深层次架构问题上，可能仅停留在框架调用层面，缺乏深入的分布式系统理论支撑。

#### 2. 实用价值：**[高]**
对于广大的 Java 企业级开发者来说，这是一篇极具指导意义的文章。它提供了一条从“传统 Web 开发”平滑过渡到“AI 应用开发”的清晰路径，降低了技术转型的心理门槛和试错成本。

#### 3. 创新性：**[中]**
“Multi-Agent”和“Skills”并非新概念（AutoGPT, MetaGPT 等已提出），但将这一范式引入 Spring AI 生态并进行标准化封装，具有一定的工程创新意义。它更多是**工程架构层面的整合**，而非算法层面的突破。

#### 4. 可读性：**[优]**
基于 Spring 的命名规范和设计模式，使得文章对于 Java 程序员非常友好。逻辑结构通常遵循“问题-方案-代码示例”的模式，易于理解和复现。

#### 5. 行业影响：**[中等偏上]**
如果该方案被广泛采纳，将加速 AI 技术在传统金融、制造、政务等 Java 主导行业的渗透。它可能会催生一批基于 Spring AI 的企业级 Agent 开发平台，改变企业级中间件的市场格局。

#### 6. 争议点或不同观点
*   **框架锁定风险**：虽然 Spring AI 简化了开发，但深度绑定特定框架可能导致未来模型切换（如从 OpenAI 切换到私有化部署模型）时，面临适配层的重构工作。
*   **Java 是否适合 AI 开发？**：业界仍有观点认为 AI 的核心在于数据迭代和算法实验，Python 的动态特性在这一阶段仍不可替代，Java 更适合作为 AI 能力的“消费者”而非“构建者”。

#### 7. 实际应用建议
*   **从“单 Agent + 多 Skills”开始**：不要一开始就构建复杂的 Multi-Agent 系统。先构建一个具备丰富工具调用能力的单体 Agent，验证 LLM 的理解能力。
*   **关注 Token 成本**：在 Spring Boot 的配置中，务必加入对 Token 使用量的监控和拦截，避免 Agent 陷入“死循环对话”导致费用失控。
*   **工具调用的确定性**：确保封装的 Skill 具有清晰的输入输出 Schema，LLM 只有在理解工具功能的前提下才能做出正确决策。

### 可验证的检查方式

1.  **性能基准测试（指标）**：

---
## 学习要点

- 利用 Spring AI 的函数调用机制，将 LLM 大模型与业务代码解耦，实现智能体对特定技能的精准调用与执行。
- 引入“决策者”与“工作者”分离的多智能体架构，通过角色分工将复杂的规划任务拆解为可执行的子任务。
- 借助思维链提示工程引导模型进行逐步推理，有效弥补 LLM 在处理复杂逻辑时的幻觉与推理短板。
- 利用 AI 的上下文记忆机制（如 ChatMemory）维护对话历史，确保智能体在多轮交互中保持决策的连贯性。
- 结合 Spring Boot 的低门槛特性与 Java 生态系统的稳健性，降低了企业级 AI 应用开发的准入门槛与维护成本。
- 通过 Prompt 模板化管理，将业务逻辑与提示词分离，提升了系统在动态场景下的灵活性与可维护性。
- 构建自主决策智能体系统的核心在于实现从“感知”到“规划”再到“行动”的完整闭环，而非单纯依赖模型能力。

---
## 常见问题


### 1: 什么是 Multi-Agent（多智能体）架构，它与单体 Agent 有什么区别？

1: 什么是 Multi-Agent（多智能体）架构，它与单体 Agent 有什么区别？

**A**: Multi-Agent 架构是指由多个相对独立的 Agent 智能体组成的系统，这些 Agent 之间可以相互协作、通信或竞争以完成复杂任务。

与单体 Agent 的主要区别在于：
1.  **职责分离**：单体 Agent 通常由一个 LLM 处理所有任务，容易在复杂流程中迷失方向；而 Multi-Agent 将不同角色（如研究员、程序员、审查员）分配给不同的 Agent，每个 Agent 专注于特定的领域或技能。
2.  **协作与解耦**：Multi-Agent 通过“手递手”或共享记忆的方式协作，一个 Agent 的输出可以作为另一个 Agent 的输入，从而实现更复杂的逻辑推理和任务执行。
3.  **可扩展性**：当需要增加新功能时，Multi-Agent 只需添加新的 Agent 或定义新的 Skill，而不需要修改核心的单体逻辑。

---



### 2: 在 Spring AI 生态中，"Skills"（技能）具体指什么，它们是如何工作的？

2: 在 Spring AI 生态中，"Skills"（技能）具体指什么，它们是如何工作的？

**A**: 在 Spring AI 构建智能体的上下文中，Skills（技能）通常指代 Agent 可以调用的具体能力单元或工具。它们是将大模型的通用推理能力连接到具体业务逻辑的桥梁。

工作原理如下：
1.  **定义**：一个 Skill 通常是一个 Java 方法或函数，它被包装成 `FunctionCallback` 或类似的机制。
2.  **注册与描述**：开发者将这些 Skills 注册给 LLM，并提供描述性的元数据（例如：“这个工具可以查询当前天气”或“这个工具可以执行数据库插入”）。
3.  **动态调用**：当用户提问时，LLM 会根据语义判断是否需要调用某个 Skill。如果需要，LLM 会生成具体的参数请求，Spring AI 拦截该请求并执行对应的 Java 方法，最后将结果返回给 LLM 进行最终总结。这就是 Function Calling（函数调用）机制。

---



### 3: 如何利用 Spring AI 实现 Agent 的“自主决策”能力？

3: 如何利用 Spring AI 实现 Agent 的“自主决策”能力？

**A**: 自主决策的核心在于让 Agent 拥有“思考”和“规划”的能力，而不仅仅是机械地执行指令。在 Spring AI 中，通常通过以下方式实现：

1.  **Chat Memory（对话记忆）**：使用 `ChatMemory` 组件（如 InMemoryChatMemory 或 PersistentChatMemory）保存对话历史。这使得 Agent 能够理解上下文，基于之前的交互做出连贯的决策。
2.  **Prompt Engineering（提示词工程）**：在 System Prompt 中明确 Agent 的角色、目标、可用工具以及约束条件。通过精心设计的提示词，引导 LLM 进行“思维链”推理，即先分析问题，再规划步骤，最后执行。
3.  **Agent Loop（智能体循环）**：构建一个处理循环，Agent 执行动作后，系统观察环境反馈，再由 Agent 决定是继续执行、修正错误还是结束任务。这种反馈循环是实现自主性的关键。

---



### 4: Spring AI 相比于直接使用 Python（如 LangChain）构建 Agent 有哪些优势？

4: Spring AI 相比于直接使用 Python（如 LangChain）构建 Agent 有哪些优势？

**A**: Spring AI 主要面向 Java 生态，其优势主要体现在企业级应用开发中：
1.  **生态融合**：对于已经使用 Spring Boot（Java/Kotlin）构建的后端系统，Spring AI 提供了无缝集成。开发者可以直接复用现有的 Spring 组件（如 Security, Data JPA, Actuator），无需维护独立的 Python 服务。
2.  **依赖管理与自动配置**：利用 Spring 的自动配置机制，可以快速接入 OpenAI、Azure OpenAI、Hugging Face 等各种模型提供商，大大降低了配置复杂度。
3.  **类型安全与抽象**：Java 的强类型系统有助于在编写 Function Callback 时定义清晰的输入输出结构，Spring AI 提供的抽象层屏蔽了不同 AI 厂商 API 的差异，便于后续切换模型。
4.  **企业级特性**：天然支持微服务架构、配置中心（如 Spring Cloud Config）和监控，适合构建稳定、可扩展的生产级 AI 应用。

---



### 5: 在 Multi-Agent 系统中，如何处理不同 Agent 之间的通信和状态共享？

5: 在 Multi-Agent 系统中，如何处理不同 Agent 之间的通信和状态共享？

**A**: 通信和状态共享是 Multi-Agent 系统的难点，常见的解决方案包括：
1.  **消息传递**：Agent 之间通过定义好的消息格式进行通信。在 Spring AI 中，可以通过 Service 之间的调用，或者利用消息队列（如 Kafka/RabbitMQ）来实现异步通信。
2.  **共享记忆**：使用共享的 `ChatMemory` 或数据库存储全局状态。例如，一个“写作 Agent”生成的内容，存入共享向量数据库或数据库中，供“审核 Agent”读取和修改。
3.  **编排模式**：引入一个“Manager”或“Orchestrator” Agent，它不直接执行任务，而是负责任务的分发和结果的汇总。这种模式在 Spring AI 中可以通过定义一个工作流服务来实现，由该服务按顺序调用不同的 Agent Bean。

---



### 6: 构建 Multi-Agent 系统时，如何避免 Token 消

6: 构建 Multi-Agent 系统时，如何避免 Token 消

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7614889731939811355](https://juejin.cn/post/7614889731939811355)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Spring AI](/tags/spring-ai/) / [Multi-Agent](/tags/multi-agent/) / [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [函数调用](/tags/%E5%87%BD%E6%95%B0%E8%B0%83%E7%94%A8/) / [自主决策](/tags/%E8%87%AA%E4%B8%BB%E5%86%B3%E7%AD%96/) / [RAG](/tags/rag/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
- [利用 Amazon Bedrock AgentCore 构建统一智能系统]({{< relref "posts/20260220-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-13.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与个性化能力的活动助手]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-5.md" >}})
- [基于Spring AI构建类OpenClaw自主Agent的实现方案]({{< relref "posts/20260302-juejin-spring-ai-实战从零构建类-openclaw-的自主-agent-2.md" >}})
- [LangBot：生产级多平台智能体机器人开发平台]({{< relref "posts/20260201-github_trending-langbot-app-langbot-0.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*