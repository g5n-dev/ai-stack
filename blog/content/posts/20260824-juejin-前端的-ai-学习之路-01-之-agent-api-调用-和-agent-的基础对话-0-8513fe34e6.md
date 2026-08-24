---
title: "前端的 AI 学习之路 01 之 Agent API 调用 - 和 Agent 的基础对话"
date: 2026-08-24T23:59:33+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:c4f93f08ecbc0a063518074465f8dec99fc8f0cadf638276ee073a8bb169d824"
source_payload_sha256: "sha256:cf8bb33d4f16bbad2a3e51336f4fff872eaaae6731d1ab5e904ca48dd7450d51"
source_published_at: 2026-08-24T15:38:20Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:e55bf1b8adc5b612adce78da274d848b80579a8cdd4885a047942555d18fd393"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 45
description: "核心结论 LLM 调用按 Token 计费而非字符或消息条数，不同 Token 类型对应不同单价，output_tokens 通常比 input_tokens 贵约五倍。上下文窗口存在上限，历史消息是最大开销来源，需要通过摘要压缩或滑窗截断等策略控制用量。"
external_url: https://juejin.cn/post/7677441124443848713
observation_id: obs_8513fe34e6b0f11a99eb4403968ecf85997936c5d4d08ba8109b6df3598d6c74
revision_id: rev_b9e1a56276ebffbbb6478d7b20cbde7488f8d201185348858a61347ba2a950a5
event_id: evt_57bd32ad727dcc6723fb881ac671ea15b29fd1b206c7ed9c615b301b2d3bd9a2
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-24T15:55:40.341849Z
last_seen_at: 2026-08-24T15:59:33Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: Setsuna\_F\_Seiei
- **原始来源**: [https://juejin.cn/post/7677441124443848713](https://juejin.cn/post/7677441124443848713)
- **原文发布时间**: Mon, 24 Aug 2026 15:38:20 GMT

## 核心结论

LLM 调用按 Token 计费而非字符或消息条数，不同 Token 类型对应不同单价，output_tokens 通常比 input_tokens 贵约五倍。上下文窗口存在上限，历史消息是最大开销来源，需要通过摘要压缩或滑窗截断等策略控制用量。调用方式分为三种：invoke 适合后台批处理场景，stream 实现实时逐块输出，batch 支持并发处理多组独立对话并自带限流保护。生产环境必须配置重试和超时机制，重试策略应针对临时性错误（如 rate limit、timeout、5xx 状态码），业务错误不应重试。

## 能力机制

Token 是模型将文本切分后的最小语义单元。英文约四字符对应一个 Token，中文约两字符对应一个 Token，实际比例因分词器而异。上下文窗口总容量减去 system prompt、历史消息、当前输入、模型输出、thinking 和工具调用结果等占用后，剩余空间决定还能处理多少内容。当总 Token 接近 context window 的百分之七十五至九十时，需要触发上下文压缩防止模型遗忘早期信息或请求报错。

LangChain 中的消息由 SystemMessage、HumanMessage、AIMessage 和 ToolMessage 四种类型组成。SystemMessage 定义 Agent 行为规范，拥有最高优先级；HumanMessage 是用户输入；AIMessage 包含模型回答和工具调用意图；ToolMessage 回传工具执行结果，其 tool_call_id 必须与 AIMessage 中的对应 id 严格匹配。

Anthropic 提供 Prompt Cache 功能，将稳定内容（如 system 指令、长文档）标记缓存后，后续请求若前缀匹配可按原单价的十分之一计费。缓存规则要求前缀完全相同，最小粒度为一千零二十四个 Token，最多支持四个缓存断点，缓存有效期为五分钟。

## 快速开始

初始化模型并估算 Token 用量：

```javascript
import { ChatAnthropic } from '@langchain/anthropic';
import { TokenTextSplitter } from '@langchain/textsplitters';

const model = new ChatAnthropic({
  model: 'claude-sonnet-4-20250514',
  timeout: 30_000,
  maxRetries: 3
});

const splitter = new TokenTextSplitter({ chunkSize: 1000, chunkOverlap: 0 });
const chunks = await splitter.splitText('待估算文本');
console.log(`约 ${chunks.length} 个分块`);
```

使用模板构造消息列表：

```javascript
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { HumanMessage, SystemMessage } from '@langchain/core/messages';

const promptTemplate = ChatPromptTemplate.fromMessages([
  ['system', '回答用{format}，不超过{maxWords}字。'],
  ['human', '{question}']
]);

const messages = await promptTemplate.formatMessages({
  format: 'JSON',
  maxWords: 100,
  question: '什么是闭包'
});

const response = await model.invoke(messages);
console.log(response.content);
console.log(response.usage_metadata);
```

流式输出示例：

```javascript
const stream = await model.stream([new HumanMessage({ content: '解释上下文窗口' })]);
for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

批量调用示例：

```javascript
const batchInputs = [
  [new HumanMessage({ content: '问题一' })],
  [new HumanMessage({ content: '问题二' })]
];
const results = await model.batch(batchInputs);
```

## 适用边界

invoke 方式等待完整回答返回，首字延迟高，适合不要求实时显示进度的后台批处理和结构化数据提取场景。stream 方式逐块产出内容，首字延迟低，可中途中断，适合面向用户的交互界面。batch 方式并发执行多组独立请求，内置并发限制保护，适合批量分类、批量翻译等场景，与 Promise.all 循环 invoke 相比能复用 HTTP 连接池且避免打爆限流。

Token 预算策略需根据对话长度选择：十轮以内的短对话可全量保留历史消息；简单场景可采用滑窗截断仅保留最近若干轮；长对话平衡精度与成本时使用摘要压缩；超长对话（数百轮）采用向量检索按需召回。Prompt Cache 适用于包含两千 Token 以上稳定内容且存在多轮对话的场景。

重试机制仅适用于临时性故障，业务错误（参数错误、内容违规等导致的 4xx 响应）不应重试。自定义重试策略可配置指数退避，初始延迟、延迟因子和最大重试次数需根据下游服务的限流策略调整。

## 核验清单

调用前确认已设置超时参数和最大重试次数。监控 Token 用量应以模型返回的 usage_metadata 为准，不要自行估算。检查消息角色是否完整：SystemMessage 定义行为边界，HumanMessage 携带用户输入，AIMessage 记录模型输出和工具调用意图，ToolMessage 回传结果且 tool_call_id 匹配正确。使用 batch 方式时确认是否需要配置 maxConcurrency 避免触发限流。配置缓存前确认内容稳定不变且位于消息列表前缀。流式调用时需在循环中累积每个 chunk 的 usage 字段以获取准确总量。重试策略中明确指定仅对临时性错误重试，业务错误直接失败。

## 来源与核验

- [原始文章](https://juejin.cn/post/7677441124443848713)
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