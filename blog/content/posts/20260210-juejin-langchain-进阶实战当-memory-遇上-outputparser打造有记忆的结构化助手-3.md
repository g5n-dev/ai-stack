---
title: LangChain实战：结合Memory与OutputParser构建有记忆的结构化助手
date: 2026-02-10 21:20:19+08:00
draft: false
entry_kind: auto
tags:
- LangChain
- LLM
- RAG
- Prompt
- OutputParser
- Memory
- 结构化输出
- 多轮对话
categories:
- AI 工程
- 后端
source: juejin
description: 这是一篇关于 LangChain 进阶实战的简洁总结： 核心主题：结合 Memory（记忆）与 OutputParser（输出解析），打造既有记忆又能输出结构化数据的
  AI 助手。 1. 背景与痛点 当前的 LLM 应用开发常面临两个极端的困境： * **“记性好的话痨”**：类似 ChatBot，拥有良好的上下文记忆
external_url: https://juejin.cn/post/7605051978872078355
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
aliases:
- /posts/20260211-juejin-langchain-进阶实战当-memory-遇上-outputparser打造有记忆的结构化助手-3/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: NEXT06
- **链接**: [https://juejin.cn/post/7605051978872078355](https://juejin.cn/post/7605051978872078355)

---
## 导语

在构建 LLM 应用时，开发者往往需要在“上下文连贯性”与“输出结构化”之间做出取舍。LangChain 的 Memory 组件擅长维持对话状态，而 OutputParser 则能确保数据格式规范。本文将探讨如何将两者结合，通过实战案例展示如何构建既具备长期记忆能力，又能输出精准结构化数据的智能助手，帮助读者突破单一功能的限制，提升应用落地的可控性与实用性。

---
## 描述

在当前的 LLM 应用开发中，我们经常陷入两个极端的场景： 记性好的话痨：类似于 ChatBot，能记住上下文，聊天体验流畅，但输出全是不可控的自然语言。 一次性的 API：类似于信息提取工具，能返回

---
## 摘要

这是一篇关于 LangChain 进阶实战的简洁总结：

### 核心主题：结合 Memory（记忆）与 OutputParser（输出解析），打造既有记忆又能输出结构化数据的 AI 助手。

#### 1. 背景与痛点
当前的 LLM 应用开发常面临两个极端的困境：
*   **“记性好的话痨”**：类似 ChatBot，拥有良好的上下文记忆能力，对话流畅，但输出全是不可控的自然语言，难以直接被程序调用。
*   **“一次性的 API”**：类似信息提取工具，能通过 OutputParser 强制输出标准的 JSON/结构化数据，但往往是“无状态”的，无法记住之前的对话内容，交互体验差。

#### 2. 解决方案
文章提出将 LangChain 的 **Memory 组件** 与 **OutputParser 组件** 相结合。
*   **目标**：让 AI 助手在具备多轮对话能力（Memory）的同时，始终返回符合预定 Schema（结构）的数据（OutputParser）。
*   **价值**：既保留了对话的连贯性，又确保了下游系统（如数据库、API）能稳定地解析和使用返回结果。

#### 3. 实现逻辑
实现这一功能的核心在于处理**提示词**与**历史记录**的格式冲突：

1.  **冲突点**：OutputParser 需要在提示词末尾插入格式指令（如“必须以 JSON 输出”），而 Memory 组件通常只保存人类和 AI 的对话文本。
2.  **解决步骤**：
    *   **构建提示词**：将 System Prompt、格式指令和用户输入合并。
    *   **注入记忆**：将历史对话注入到提示词中，让模型能“看到”上下文。
    *   **挂载解析器**：使用 `RunnablePassthrough.assign` 等机制，确保模型输出先经过 OutputParser 处理成结构化对象，然后再传回给 Memory 模块保存。

#### 4. 关键结论
*   **技术细节**：在保存历史记录到 Memory 时，通常需要保存原始字符串而非解析后的对象，或者自定义 Memory 的处理逻辑。
*   **最终效果**：打造出一个“懂事”的助手——它能记住你的需求（Memory），并在每次回答时都乖乖交出标准格式的数据（

---
## 常见问题


### 1: 为什么 LangChain 的 Memory 组件与 OutputParser 结合使用时会报错？

1: 为什么 LangChain 的 Memory 组件与 OutputParser 结合使用时会报错？

**A**: 这是最常见的问题之一。原因在于标准 Memory 组件（如 `ConversationBufferMemory`）默认将历史记录作为字符串注入到 Prompt 中。然而，`OutputParser` 通常需要 LLM 返回特定格式的字符串（如 JSON），并且会在 Prompt 中添加格式指令。

当 LLM 试图同时满足“输出 JSON 格式”和“像人类一样自然对话”这两个冲突的指令时，往往会失败，或者输出的 JSON 被包裹在对话文本中，导致解析器无法识别。

解决方法是使用 `MessagesPlaceholder` 替代简单的字符串历史记录，并确保 Prompt 模板明确告诉 LLM：尽管有历史对话，但**当前**的输出必须是严格的 JSON 格式。

---



### 2: 如何在保留对话历史的同时，强制 LLM 输出符合 Pydantic 模型的结构化数据？

2: 如何在保留对话历史的同时，强制 LLM 输出符合 Pydantic 模型的结构化数据？

**A**: 要实现这一点，你需要构建一个支持历史消息记录的 Prompt Template。具体步骤如下：

1.  **定义 Pydantic 模型**：首先定义你想要的数据结构（例如 `PersonalInfo`）。
2.  **设置 Parser**：使用 `PydanticOutputParser` 从模型中提取格式指令。
3.  **构建 Prompt**：在创建 `PromptTemplate` 时，使用 `partial_variables` 预填格式指令。
4.  **关键步骤**：在 Prompt 模板中，必须包含一个 `MessagesPlaceholder(variable_name="chat_history")`，而不是简单的 `{history}`。这允许 LangChain 传入消息对象列表而非拼接好的字符串，从而保持上下文的完整性。
5.  **链式调用**：将 RunnablePassthrough.assign 用于处理历史记录，然后传递给 Prompt。

---



### 3: 当 LLM 输出的格式不符合 OutputParser 的要求时（例如多说了几句废话），如何处理？

3: 当 LLM 输出的格式不符合 OutputParser 的要求时（例如多说了几句废话），如何处理？

**A**: 这是实战中非常头疼的问题。如果 LLM 在 JSON 代码块前后添加了解释性文字，标准的 Parser 会直接抛出错误。

有几种解决方案：
2.  **使用自定义 Parser**：如果上述方法无效，可以编写一个简单的自定义解析函数，利用正则表达式提取 JSON 部分，然后再交给 Pydantic 解析。
3.  **使用带纠错能力的链**：LangChain 提供了 `OutputFixingParser`，它可以在解析失败时，将错误信息和原始结果回传给 LLM，要求 LLM 修正格式。

---



### 4: 在长对话中，Memory 占用的 Token 越来越多，导致超过上下文限制或成本过高，怎么优化？

4: 在长对话中，Memory 占用的 Token 越来越多，导致超过上下文限制或成本过高，怎么优化？

**A**: 简单的 `ConversationBufferMemory` 会无限制地存储历史。对于结构化输出场景，建议使用以下更高级的 Memory 类型：

1.  **ConversationBufferWindowMemory**：只保留最近 `k` 轮对话，丢弃更早的记忆。
2.  **ConversationSummaryMemory**：使用 LLM 将过去的对话总结为一段简短的摘要，随着对话进行不断更新摘要。这能显著减少 Token 消耗。
3.  **TokenBufferMemory**：基于 Token 数量而非对话轮数来保留历史，确保总 Token 数不超过设定阈值。

---



### 5: 如何验证 OutputParser 提取出的结构化数据是否符合业务逻辑？

5: 如何验证 OutputParser 提取出的结构化数据是否符合业务逻辑？

**A**: Pydantic 模型本身提供了数据验证功能（如类型检查、必填字段）。但针对业务逻辑验证，你可以利用 Pydantic 的 **Validators**。

例如，如果你要求用户输入年龄，模型提取了数字，但你想确保年龄是合理的（如 0-120 之间），你可以在 Pydantic 模型中添加 `@field_validator` 或 `@root_validator`。如果 LLM 输出的数据不符合验证逻辑，Pydantic 会抛出 `ValidationError`，你可以在代码中捕获该错误并提示用户重新输入，或者让 LLM 重试。

---



### 6: LangChain 的 LCEL (LangChain Expression Language) 语法中，如何优雅地将 Memory 传入链中？

6: LangChain 的 LCEL (LangChain Expression Language) 语法中，如何优雅地将 Memory 传入链中？

**A**: 在 LCEL 语法中，不再像旧版 Chain 那样直接在初始化时传入 `memory` 参数。你需要显式地处理历史记录。

通常的做法是使用 `RunnableWithMessageHistory`。你需要：
1.  定义一个基本的链（Prompt + Model + Parser）。
2.  实现一个历史记录管理函数（根据 `session_id` 存取消息）。
3.  使用 `RunnableWithMessageHistory` 包装这个链，并指定 `input_messages_key` 和 `history_messages_key`。

这样，每次调用时，包装器会自动从存储中提取历史，填入 Prompt 的 `MessagesPlaceholder` 中，执行结构化输出，并自动保存新的交互到历史中。

---
## 引用

- **掘金原文**: [https://juejin.cn/post/7605051978872078355](https://juejin.cn/post/7605051978872078355)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [LangChain](/tags/langchain/) / [LLM](/tags/llm/) / [RAG](/tags/rag/) / [Prompt](/tags/prompt/) / [OutputParser](/tags/outputparser/) / [Memory](/tags/memory/) / [结构化输出](/tags/%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA/) / [多轮对话](/tags/%E5%A4%9A%E8%BD%AE%E5%AF%B9%E8%AF%9D/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [Kirara-AI：支持多平台接入的多模态聊天机器人框架]({{< relref "posts/20260127-github_trending-lss233-kirara-ai-2.md" >}})
- [基于大模型的多平台聊天机器人：支持微信飞书钉钉接入]({{< relref "posts/20260131-github_trending-zhayujie-chatgpt-on-wechat-0.md" >}})
- [LangBot：生产级多平台智能体机器人开发平台]({{< relref "posts/20260131-github_trending-langbot-app-langbot-7.md" >}})
- [ChatGPT-on-WeChat：接入大模型的多平台聊天机器人]({{< relref "posts/20260131-github_trending-zhayujie-chatgpt-on-wechat-0.md" >}})
- [LangBot：生产级多平台智能 IM 机器人开发平台]({{< relref "posts/20260131-github_trending-langbot-app-langbot-7.md" >}})
*本文由 AI Stack 自动生成，提供深度内容分析。*
