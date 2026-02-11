---
title: "LangChain 进阶实战：当 Memory 遇上 OutputParser，打造有记忆的结构化助手"
date: 2026-02-11T00:15:26+08:00
draft: false
entry_kind: "auto"
tags: ["LangChain", "LLM", "Memory", "OutputParser", "结构化输出", "Prompt工程", "上下文管理", "实战案例"]
categories: ["AI 工程", "大模型"]
source: juejin
description: "在当前的 LLM 应用开发中，我们经常陷入两个极端的场景： 记性好的话痨：类似于 ChatBot，能记住上下文，聊天体验流畅，但输出全是不可控的自然语言。 一次性的 API：类似于信息提取工具，能返回"
external_url: https://juejin.cn/post/7605051978872078355
scenarios: ["AI/ML项目", "大语言模型", "后端开发"]
---

# LangChain 进阶实战：当 Memory 遇上 OutputParser，打造有记忆的结构化助手

---

## 基本信息

- **作者**: NEXT06
- **链接**: [https://juejin.cn/post/7605051978872078355](https://juejin.cn/post/7605051978872078355)

---
## 描述

在当前的 LLM 应用开发中，我们经常陷入两个极端的场景： 记性好的话痨：类似于 ChatBot，能记住上下文，聊天体验流畅，但输出全是不可控的自然语言。 一次性的 API：类似于信息提取工具，能返回

---
## 学习要点

- LangChain 的 `ConversationBufferMemory` 默认将历史记录作为字符串注入，导致无法与结构化输出（如 Pydantic 模型）直接兼容，这是构建结构化助手的核心痛点。
- 解决该痛点的最佳方案是自定义 `Memory` 的 `save_context` 逻辑，强制将历史消息存储为 `HumanMessage` 和 `AIMessage` 对象列表，而非原始字符串。
- 在构建 `PromptTemplate` 时，必须使用 `MessagesPlaceholder` 变量来接收对象化的历史消息，确保其格式符合 Chat Model 的输入标准。
- 将 `OutputParser` 的 `get_format_instructions()` 方法输出直接嵌入 Prompt 中，能够强制模型在保持上下文记忆的同时，始终输出符合 JSON Schema 的结构化数据。
- 在处理结构化输出时，应使用 `RunnablePassthrough.assign` 来优雅地组合历史记录与新输入，确保数据流在进入 LLM 前保持格式正确。
- 对于复杂的提取任务，可以在 Prompt 中提供少量示例，以引导模型在多轮对话中准确识别和提取关键信息，减少幻觉。
- 这种“对象化 Memory + 模板约束”的组合模式，是开发具备长期记忆且输出标准化的生产级 AI 应用的通用架构。

---
## 常见问题


### 1: 为什么在 LangChain 中结合使用 Memory 和 OutputParser 时会报错？

1: 为什么在 LangChain 中结合使用 Memory 和 OutputParser 时会报错？

**A**: 这是一个非常常见的类型不匹配问题。Memory 组件（特别是用于保存对话历史的组件）通常返回的是字符串或 HumanMessage/AIMessage 对象列表。然而，OutputParser 期望接收一个特定的、结构化的字符串输入以便进行解析。当 Memory 将上一次的对话（可能是一个复杂的对象结构）直接注入到 Prompt 中，或者与当前的输入混合时，可能会导致 LLM 返回的内容无法被 OutputParser 正确解析，或者在传递给 Parser 之前数据格式就已经出错。解决方法通常是在 PromptTemplate 中明确如何格式化历史消息，或者使用能够处理消息列表的特定 Parser。

---



### 2: 如何让 LLM 在保持对话记忆的同时，始终返回符合特定格式的 JSON 数据？

2: 如何让 LLM 在保持对话记忆的同时，始终返回符合特定格式的 JSON 数据？

**A**: 要实现这一点，你需要构建一个包含历史记录变量和格式化指令的 PromptTemplate。具体步骤如下：
1.  **初始化 Memory**：使用 `ConversationBufferMemory` 或类似组件，并设置 `return_messages=True`（推荐使用消息对象而非字符串，以便 LLM 更好理解上下文）。
2.  **定义 Parser**：实例化一个 `OutputParser`（如 `PydanticOutputParser` 或 `SimpleJsonOutputParser`），并获取其格式指令（`get_format_instructions()`）。
3.  **构建 Prompt**：在创建 PromptTemplate 时，必须包含两个部分：一个是用于插入 `history`（对话历史）的占位符，另一个是用于插入 `format_instructions`（解析器格式指令）的占位符。
4.  **组装 Chain**：将 Memory、Prompt、LLM 和 Parser 连接起来。关键在于确保 Prompt 明确告诉 LLM：“参考历史对话，并根据以下格式指令输出 JSON”。

---



### 3: 使用 `StructuredChatMemory` 与普通 Memory 配合 OutputParser 有什么区别？

3: 使用 `StructuredChatMemory` 与普通 Memory 配合 OutputParser 有什么区别？

**A**: 普通的 Memory（如 `ConversationBufferMemory`）主要是忠实地记录和回放对话历史。而 `StructuredChatMemory`（或类似的针对结构化输出的内存机制）通常专门用于处理包含“结构化输出工具调用”的对话。它的核心区别在于，它不仅能记住对话内容，还能记住 LLM 之前是如何调用特定工具或生成特定结构数据的。如果你正在构建一个需要多次交互且每次都需要返回结构化数据（例如分步骤收集用户信息）的助手，使用支持结构化历史的 Memory 类可以更稳定地维持上下文逻辑，防止 LLM 在后续对话中丢失对输出格式的约束。

---



### 4: 当 LLM 输出的格式不符合 OutputParser 的要求时（例如输出了废话而非 JSON），该如何处理？

4: 当 LLM 输出的格式不符合 OutputParser 的要求时（例如输出了废话而非 JSON），该如何处理？

**A**: 这是实战中最大的痛点之一。如果 LLM 因为记忆过载或指令不清而输出了非结构化文本，OutputParser 会抛出 `OutputParserException`。
**解决方案**：
1.  **使用 `OutputFixingParser`**：这是一个包装器，当内部的 Parser 失败时，它会将错误信息和错误的输出传回给 LLM，要求 LLM 修复并重新生成符合格式的输出。
3.  **Few-Shot Prompting**：在 Memory 之外，在 Prompt 中提供几个标准的“问答示例”，展示如何既回答问题又保持 JSON 格式。

---



### 5: 在长对话场景下，Memory 占用的 Token 过多导致 OutputParser 失效率变高，怎么优化？

5: 在长对话场景下，Memory 占用的 Token 过多导致 OutputParser 失效率变高，怎么优化？

**A**: 随着 Memory 变长，LLM 的注意力分散，容易忽略格式指令。优化策略包括：
1.  **摘要 Memory**：使用 `ConversationSummaryMemory` 或 `ConversationBufferWindowMemory`。不要把所有历史都塞进去，而是只保留最近的几轮对话，或者之前的对话摘要。这能减少 Token 消耗，并让 LLM 更专注于当前的格式指令。
2.  **动态指令注入**：确保 `format_instructions` 始终位于 Prompt 的末尾或最显眼的位置，不要被长篇的历史记录淹没。

---



### 6: LangChain 中的 `PydanticOutputParser` 如何与 Memory 配合定义动态的数据结构？

6: LangChain 中的 `PydanticOutputParser` 如何与 Memory 配合定义动态的数据结构？

**A**: `PydanticOutputParser` 依赖于定义好的 Pydantic 模型。在大多数情况下，数据结构是固定的。如果你需要根据对话历史动态改变输出结构（例如第一轮问名字，第二轮问年龄，结构不同），这通常不通过改变 Parser 定义来实现，而是通过 Prompt Engineering。你可以定义一个包含所有可能字段的“全集” Pydantic 模型，然后在 Prompt 中指示 LLM：“根据上下文，只填充当前阶段需要的字段，其他字段置空”。这样 Parser 结构保持不变，但输出的内容会随 Memory 中的上下文动态变化。

---



### 7: 如何调试 Memory 和 OutputParser 结合时的中间过程？

7: 如何调试 Memory 和 OutputParser 结合时的中间过程？

**A**: 调试此类复杂 Chain 的最佳方法是设置 `verbose=True`，或者使用 LangSmith。
1.

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7605051978872078355](https://juejin.cn/post/7605051978872078355)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [LangChain](/tags/langchain/) / [LLM](/tags/llm/) / [Memory](/tags/memory/) / [OutputParser](/tags/outputparser/) / [结构化输出](/tags/%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA/) / [Prompt工程](/tags/prompt%E5%B7%A5%E7%A8%8B/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [实战案例](/tags/%E5%AE%9E%E6%88%98%E6%A1%88%E4%BE%8B/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [LangChain实战：结合Memory与OutputParser构建有记忆的结构化助手]({{< relref "posts/20260210-juejin-langchain-进阶实战当-memory-遇上-outputparser打造有记忆的结构化助手-3.md" >}})
- [Context Graphs与Agent Traces技术解析]({{< relref "posts/20260204-blogs_podcasts-ainews-context-graphs-and-agent-traces-2.md" >}})
- [Context Graphs与Agent Traces：解析AI系统的上下文与追踪技术]({{< relref "posts/20260205-blogs_podcasts-ainews-context-graphs-and-agent-traces-5.md" >}})
- [利用AI高效编写高质量代码的实践方法]({{< relref "posts/20260206-hacker_news-how-to-effectively-write-quality-code-with-ai-3.md" >}})
- [利用AI高效编写高质量代码的实践指南]({{< relref "posts/20260206-hacker_news-how-to-effectively-write-quality-code-with-ai-5.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*