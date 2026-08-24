---
title: "ai agent -- Memory汇总"
date: 2026-08-24T22:05:15+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:8af466d040c670e13f2b804d14b4880b418888418c1ff7972cb95abbb3bb6993"
source_payload_sha256: "sha256:4f8f8b3f0e2c8677ea103b687fd38bc3dc4d62c27888a552d38de38ff151fdfe"
source_published_at: 2026-08-24T12:37:17Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:153b449cfb87ad25076e9bc1c770b0e87f744971a08271ed174b9f4edb6a2490"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 20
description: "核心结论 LangChain的Memory机制用于解决大模型无状态问题，通过持久化对话历史实现上下文感知。LangChain采用monorepo分层架构，核心包为 ，各集成包仅依赖core而非主包。老版API已迁移至 。对话历史的存储方式包括内存与文件系统两种，消息处理策略主要有截断、总结、检索三种。"
external_url: https://juejin.cn/post/7677397089275330600
observation_id: obs_a8b018dd5c7a974d0aff8250899a945c143eb449f6af9fff67e652b0031dc91c
revision_id: rev_d30e8a26089c2acf0101e99194be07b48c48f2f70ae0b67f1b2c1008ae95e2ca
event_id: evt_94cca59498f542154b700a4629625d71205baf88a50bb5ddec025a72aea54350
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-24T14:02:15.184012Z
last_seen_at: 2026-08-24T14:05:15Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: snow来了
- **原始来源**: [https://juejin.cn/post/7677397089275330600](https://juejin.cn/post/7677397089275330600)
- **原文发布时间**: Mon, 24 Aug 2026 12:37:17 GMT

## 核心结论

LangChain的Memory机制用于解决大模型无状态问题，通过持久化对话历史实现上下文感知。LangChain采用monorepo分层架构，核心包为`@langchain/core`，各集成包仅依赖core而非主包。老版API已迁移至`@langchain/classic`。对话历史的存储方式包括内存与文件系统两种，消息处理策略主要有截断、总结、检索三种。Memory存储存在上限，不会无限增长。

## 能力机制

Message类型包含四种：SystemMessage定义系统行为、HumanMessage承载用户输入、AIMessage为大模型回复、ToolMessage携带工具执行结果。每次与大模型交互时，将这些消息一并传入，大模型即可基于历史进行响应。

LangChain包结构中，`@langchain/core`是共同依赖项，`langchain`主包提供createAgent、initChatModel等高层API，`@langchain/openai`等集成包只依赖core不依赖主包，可实现轻量调用。

内存存储使用InMemoryChatMessageHistory类，文件存储使用FileSystemChatMessageHistory类，通过filePath和sessionId标识不同会话的历史记录。消息处理方面，截断可按数量或Token数执行，使用trimMessages函数配合js-tiktoken编码器计算Token消耗。总结策略在消息数量达到阈值后触发，将历史消息聚合后清空存储，仅保留最新消息与总结摘要。

## 快速开始

安装依赖包：

```bash
pnpm install dotenv @langchain/core @langchain/openai @langchain/community langchain
```

环境变量配置OPENAI_API_KEY、OPENAI_BASE_URL、MODEL_NAME。

初始化内存存储示例：

```javascript
import {ChatOpenAI} from '@langchain/openai';
import {InMemoryChatMessageHistory} from '@langchain/core/chat_history';
import {HumanMessage, SystemMessage} from '@langchain/core/messages';

const history = new InMemoryChatMessageHistory();
await history.addMessage(new HumanMessage("用户输入"));
const messages = await history.getMessages();
```

初始化文件存储示例：

```javascript
import {FileSystemChatMessageHistory} from '@langchain/community/stores/message/file_system';

const history = new FileSystemChatMessageHistory({
  filePath: './file-history.json',
  sessionId: 'session_001',
});
```

截断处理示例：

```javascript
import {trimMessages} from '@langchain/core/messages';
import {getEncoding} from 'js-tiktoken';

const enc = getEncoding('cl100k_base');
const trimmed = await trimMessages(messages, {
  maxTokens: 50,
  tokenCounter: async(msgs) => /* 计算逻辑 */,
  strategy: 'last',
});
```

## 适用边界

内存存储适用于单次会话进程内的短期记忆，进程结束后数据丢失。文件存储实现跨会话持久化，通过sessionId区分不同用户或对话场景。

截断策略中，按数量截断使用数组slice保留最近N条消息。按Token数截断使用cl100k_base编码器，适用于OpenAI GPT-4、GPT-3.5-turbo及部分Embedding模型的分词规则。总结策略在消息量较大时压缩历史，将重要信息聚合为单条摘要，降低后续调用的上下文长度与成本。

检索策略将消息存入向量数据库，按语义相似度召回相关历史记录，适用于需要从大量历史中精准匹配特定主题的场景。

## 核验清单

代码导入应从`@langchain/core`获取InMemoryChatMessageHistory、trimMessages、HumanMessage、AIMessage、SystemMessage等基础组件。涉及文件存储时从`@langchain/community/stores/message/file_system`导入FileSystemChatMessageHistory。老版API调用需从`@langchain/classic`导入。

存储实现需明确选择内存或文件方案，内存方案无持久化保证，文件方案需配置有效的filePath与sessionId。消息处理应根据实际场景选择截断、总结或检索，截断需配置合理的maxTokens或数量阈值。

Token计数使用cl100k_base编码器时需引入js-tiktoken依赖，通过encode方法获取Token序列。环境变量使用API_KEY时通过process.env访问，绝不硬编码密钥值。

## 来源与核验

- [原始文章](https://juejin.cn/post/7677397089275330600)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [6.结构化输出](/posts/20260718-juejin-6%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA-0-80d50ad8af/)
- [GitHub Copilot for JetBrains 架构拆解：Provider / Endpoint / Skills / Sandbox / Polic](/posts/20260718-juejin-github-copilot-for-jetbrains-%E6%9E%B6%E6%9E%84%E6%8B%86%E8%A7%A3provider-endpoint-0-2a917f4cdc/)
- [从 Token 到 RAG：我这一周搭起的大模型基础认知地图](/posts/20260718-juejin-%E4%BB%8E-token-%E5%88%B0-rag%E6%88%91%E8%BF%99%E4%B8%80%E5%91%A8%E6%90%AD%E8%B5%B7%E7%9A%84%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E8%AE%A4%E7%9F%A5%E5%9C%B0%E5%9B%BE-0-cd9514ced7/)
- [从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？](/posts/20260718-juejin-%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80%E6%89%8B%E6%92%B8-agent-%E7%B3%BB%E5%88%97-%E7%AC%AC-1-%E7%AF%87%E4%B8%80%E4%B8%AA-coding-agent-%E6%98%AF%E4%BB%80%E4%B9%88-0-b0628f7a64/)
- [从BFF到SSE：我在Vue项目里藏了个“AI翻译官”](/posts/20260719-juejin-%E4%BB%8Ebff%E5%88%B0sse%E6%88%91%E5%9C%A8vue%E9%A1%B9%E7%9B%AE%E9%87%8C%E8%97%8F%E4%BA%86%E4%B8%AAai%E7%BF%BB%E8%AF%91%E5%AE%98-0-9ec70466e8/)