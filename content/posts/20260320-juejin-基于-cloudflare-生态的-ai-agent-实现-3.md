---
title: 基于 Cloudflare 生态的 AI Agent 实现
date: 2026-03-20 04:08:50+08:00
draft: false
entry_kind: auto
tags:
- AI Agent
- Cloudflare
- 大模型
- 智能助手
- 博客开发
- Workers
- RAG
- 全栈
categories:
- AI 工程
- 系统与基础设施
source: juejin
description: 总结 本文介绍了作者在2026年新年夜晚，基于Cloudflare生态实现AI Agent的构思过程。 **核心要点：** 1. **技术背景**：利用Cloudflare生态系统的服务和工具来构建AI
  Agent 2. **时间契机**：2026年新年期间，窗外烟花绽放的夜晚 3. **动机来源**：作者拥有运行近十
external_url: https://juejin.cn/post/7618852263628701759
scenarios:
- AI/ML项目
- RAG应用
---

# 基于 Cloudflare 生态的 AI Agent 实现

---

## 基本信息

- **作者**: Surmon
- **链接**: [https://juejin.cn/post/7618852263628701759](https://juejin.cn/post/7618852263628701759)

---

## 导语

本文探讨在 Cloudflare 生态下构建 AI Agent 的完整方案，涵盖从边缘函数到数据流管理的关键环节。利用 Cloudflare Workers、Durable Objects 与 AI Gateway，可实现低延迟、高可用的智能代理服务。读者将获得项目结构设计、代码实现细节以及性能调优的实战经验。

---

## 描述

您提供的内容已经是中文。如果您是希望把它转换成**繁体中文**，或者想要在中文的基础上进行润色、调整语气和格式，请告诉我您的具体需求。

---

## 摘要

### 总结

本文介绍了作者在2026年新年夜晚，基于Cloudflare生态实现AI Agent的构思过程。

**核心要点：**

1. **技术背景**：利用Cloudflare生态系统的服务和工具来构建AI Agent
2. **时间契机**：2026年新年期间，窗外烟花绽放的夜晚
3. **动机来源**：作者拥有运行近十年的个人博客
4. **目标愿景**：为博客打造一个真正“有用”的智能助手，而非仅作装饰

这段开场白表明，作者希望将传统博客与前沿AI技术结合，通过Cloudflare平台实现实用性的智能交互功能。

---

## 学习要点

- 在 Cloudflare Workers 上部署 Workers AI，使 AI Agent 能够在边缘节点快速响应，实现低延迟和全球化扩展。
- 使用 Durable

---

## 常见问题

### Cloudflare 生态的 AI Agent 是什么？它和传统 AI 服务有什么不同？

Cloudflare 生态的 AI Agent 是指基于 Cloudflare Workers、Workers AI、Durable Objects、Workers KV、Queues 等原语构建的、可在边缘网络运行的智能代理。与传统的 AI 服务（如直接调用 OpenAI、Azure AI）相比，它具备以下优势：

1. **边缘部署**：代码运行在全球 200+ 个 PoP 上，延迟更低，尤其适合实时交互场景。
2. **弹性伸缩**：Workers 按请求计费，天然支持无服务器弹性伸缩，无需预置服务器。
3. **状态保持**：Durable Objects 提供了轻量、事务性的对象存储，可在同一实例内部维护对话状态；Workers KV 适合存放全局配置或粗粒度的缓存。
4. **异步任务**：Cloudflare Queues 允许把耗时任务（如大模型推理）放到后台 Worker 处理，防止请求超时。
5. **安全与治理**：可利用 Cloudflare Access、API Token、Rate Limiting、DDoS 防护等企业级安全功能。
6. **统一计费**：Workers 请求、AI 模型使用量、存储均可在 Cloudflare 账单中统一管理。

### 如何在 Cloudflare Workers 中调用 Workers AI 实现自然语言处理？

Workers AI 提供了在边缘运行的轻量化模型（如 `llama-2-7b-chat-int8`）。调用步骤如下：

1. **绑定 AI 资源**
   在 `wrangler.toml` 中声明 `ai` 绑定：
   ```toml
   [ai]
   binding = "AI"
   ```
2. **安装 Workers AI SDK（可选）**
   ```bash
   npm install @cloudflare/workers-ai
   ```
3. **在 Worker 代码中调用模型**
   ```typescript
   import { AI } from "@cloudflare/workers-ai";

   export interface Env {
     AI: AI;
   }

   export default {
     async fetch(request: Request, env: Env): Promise<Response> {
       const prompt = await request.text();
       // 使用 Workers AI 的对话模型
       const answer = await env.ai.run("@cf/meta/llama-2-7b-chat-int8", {
         messages: [{ role: "user", content: prompt }],
       });
       return new Response(JSON.stringify(answer), {
         headers: { "Content-Type": "application/json" },
       });
     },
   };
   ```
4. **返回结构化结果**
   大多数模型返回 `{ response: string, ... }`，可以在前端解析并展示。
5. **错误处理**
   - 使用 `try/catch` 捕获 `Error`（如模型不可用、配额耗尽）。
   - 通过 `env.ai.slots()` 检查当前模型槽位使用情况，及时限流或切换模型。

### AI Agent 如何维护会话状态？应该使用 Durable Objects 还是 Workers KV？

选择持久化方案时，需要根据 **状态大小**、**访问频率**、**事务需求** 来决定：

| 场景 | 推荐方案 | 说明 |
|------|----------|------|
| 需要在单个用户的多轮交互中保存完整对话历史 | Durable Objects（DO） | DO 提供 **单实例、事务性** 的对象存储，可直接在内存中保存对话数组，利用 `this.storage.put/get` 持久化。 |
| 只保存轻量配置（如用户 ID、会话标记） | Workers KV | KV 写入/读取延迟稍高（< 10 ms），适合 **全局只读或低频写入** 的数据。 |
| 需要跨多 Worker 共享状态 | Workers KV + 缓存 | 将状态写入 KV，前端 Worker 在处理请求时先从 KV 读取并缓存到本地变量，以降低读取次数。 |
| 需要原子操作或乐观锁 | Durable Objects | DO 的 `storage.transaction` 支持在同一对象内部进行原子读写。 |

**实现示例（Durable Objects）**：

```typescript
export class ChatSession implements DurableObject {
  private state: { messages: Array<{role: string; content: string}> };

  constructor(private state: DurableObjectState) {
    // 初始化或从持久化存储读取
    this.state = state.storage.get("messages") ?? [];
  }

  async fetch(request: Request): Promise<Response> {
    const { messages } = await request.json();
    this.state.messages = messages;
    await this.state.storage.put("messages", this.state.messages);
    return new Response("OK");
  }
}
```

> 小贴士：在 DO 中尽量保持内存状态，只有在请求结束后才一次性写入 `storage`，可以显著降低存储 I/O 成本。

### 如何处理需要多轮交互或长时间运行的任务？使用 Cloudflare Queues 有哪些注意事项？

AI 代理经常需要在 **多轮对话** 中调用大模型或执行后台计算。使用 Cloudflare Queues

---

## 引用

- **掘金原文**: [https://juejin.cn/post/7618852263628701759](https://juejin.cn/post/7618852263628701759)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AI Agent](/tags/ai-agent/) / [Cloudflare](/tags/cloudflare/) / [大模型](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [智能助手](/tags/%E6%99%BA%E8%83%BD%E5%8A%A9%E6%89%8B/) / [博客开发](/tags/%E5%8D%9A%E5%AE%A2%E5%BC%80%E5%8F%91/) / [Workers](/tags/workers/) / [RAG](/tags/rag/) / [全栈](/tags/%E5%85%A8%E6%A0%88/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [本地AI Agent Memory系统建设：存储策略与检索注入机制]({{< relref "posts/20260315-juejin-本地-ai-agent-memory-系统建设方案-1.md" >}})
- [Kirara-AI：支持多平台接入的多模态聊天机器人框架]({{< relref "posts/20260130-github_trending-lss233-kirara-ai-2.md" >}})
- [Vercel AI SDK 子代理：解决复杂 Agent 系统上下文爆炸问题]({{< relref "posts/20260213-juejin-vercel-ai-sdk-使用指南-子代理-subagents-1.md" >}})
- [Amazon Bedrock AgentCore 浏览器更新：新增代理、配置文件及扩展支持]({{< relref "posts/20260214-blogs_podcasts-customize-ai-agent-browsing-with-proxies-profiles--1.md" >}})
- [AI智能体自主性评估的实践方法]({{< relref "posts/20260219-hacker_news-measuring-ai-agent-autonomy-in-practice-17.md" >}})
