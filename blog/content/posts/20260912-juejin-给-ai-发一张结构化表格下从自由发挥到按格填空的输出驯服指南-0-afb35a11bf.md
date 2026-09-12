---
title: "🍔 给 AI 发一张结构化表格（下）：从\"自由发挥\"到\"按格填空\"的输出驯服指南"
date: 2026-09-12T17:24:29+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:71feb95e931e9b8d4e853840715383167e6fba396631aec632250850354b8459"
source_payload_sha256: "sha256:5ab6b69ee7bccffbb226a555278458a42f9a58d703ec588b064e6169215c9843"
source_published_at: 2026-09-12T08:59:15Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:667aeb7df341e0edb8e4018bf129237e48e27dc5d8416522d640288d5f318a92"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
description: "核心结论 LLM 默认输出自由文本，而非结构化 JSON。直接调用 会因 markdown 包裹或格式偏差而失败。将 LLM 驯服为结构化输出是一个渐进过程：从手搓正则剥除外衣，到 LangChain OutputParser 体系，再到 Zod Schema 类型约束，最后到 Tool Call 原生能力，约束强度…"
external_url: https://juejin.cn/post/7684195084155076617
observation_id: obs_afb35a11bf4252447cc9a51ad3e7717f7e50a6ca4681c9449e9158d614bfe7cd
revision_id: rev_ca2923793156a9f4cfdbf5a38e7d98905e96f72b6b688dc4a088ffa4dfecdebb
event_id: evt_3b4004f0aafc5716c76f99835caf0a23bb90ae72ca6a2132703a4ab24f47aa2a
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-12T09:20:57.809465Z
last_seen_at: 2026-09-12T09:24:29Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 默\_笙
- **原始来源**: [https://juejin.cn/post/7684195084155076617](https://juejin.cn/post/7684195084155076617)
- **原文发布时间**: Sat, 12 Sep 2026 08:59:15 GMT

## 核心结论

LLM 默认输出自由文本，而非结构化 JSON。直接调用 `JSON.parse()` 会因 markdown 包裹或格式偏差而失败。将 LLM 驯服为结构化输出是一个渐进过程：从手搓正则剥除外衣，到 LangChain OutputParser 体系，再到 Zod Schema 类型约束，最后到 Tool Call 原生能力，约束强度逐级提升。核心目的是为下游业务提供字段名固定、类型精确、结构可靠的数据。

## 能力机制

第一级手搓正则通过 `/```json\s*([\s\S]*?)\s*```/` 捕获 markdown 代码块内的 JSON 字符串，需手动处理 ` ```json ``` ` 包裹、try/catch 异常及多种格式变体。

第二级 JsonOutputParser 是 LangChain 基础解析器，`parser.getFormatInstructions()` 在 prompt 中追加格式约束文本，`parser.parse()` 内部完成 markdown 剥离与 JSON.parse 转换，但仅保证返回合法 JSON，不约束字段名和类型。

第三级 StructuredOutputParser.fromNamesAndDescriptions 通过字段名加描述的方式固定输出结构，强制 LLM 使用指定字段名，避免用同义中文替代。类型仍依赖描述约束。

第四级 StructuredOutputParser.fromZodSchema 以 Zod Schema 定义精确类型系统，支持 z.string()、z.number()、z.array()、z.object() 及嵌套结构，配合 .describe() 向 LLM 传递字段语义。parse() 内部执行 Zod 运行时验证，类型不符会抛错。

第五级 Tool Call 利用 LLM 原生工具调用能力，`model.bindTools([{name, description, schema}])` 绑定工具后，LLM 直接在 response.tool_calls[0].args 中返回结构化参数，无需 getFormatInstructions() 和 parse() 步骤，可靠性高于 prompt 约束。

## 快速开始

```javascript
// 第二级：JsonOutputParser
import { JsonOutputParser } from '@langchain/core/output_parsers';
const parser = new JsonOutputParser();
const prompt = `描述任务 ${parser.getFormatInstructions()}`;
const result = await parser.parse(response.content);

// 第三级：固定字段名
import { StructuredOutputParser } from '@langchain/core/output_parsers';
const parser = StructuredOutputParser.fromNamesAndDescriptions({
    name: '姓名',
    birth_year: '出生年份'
});

// 第四级：Zod Schema 精确类型
import { z } from 'zod';
import { StructuredOutputParser } from '@langchain/core/output_parsers';
const schema = z.object({
    name: z.string().describe('姓名'),
    birth_year: z.number().describe('出生年份')
});
const parser = StructuredOutputParser.fromZodSchema(schema);

// 第五级：Tool Call
import { z } from 'zod';
const schema = z.object({ name: z.string(), birth_year: z.number() });
const modelWithTool = model.bindTools([{ name: 'extract', schema }]);
const response = await modelWithTool.invoke('任务描述');
const result = response.tool_calls[0].args;
```

环境变量名称按需配置，不在示例中展示。

## 适用边界

JsonOutputParser 适用于仅需合法 JSON、不关心字段名的场景。fromNamesAndDescriptions 适用于需要固定字段名但类型要求宽松的场景。fromZodSchema 适用于类型严格、结构复杂、需运行时验证的生产环境。Tool Call 适用于模型已支持 tool calling 能力的场景，可靠性最高但依赖模型特性。

手搓正则适合临时调试或无 LangChain 依赖的简单场景，不建议在生产代码中维护。OutputParser 体系的优势在于通用性，任何返回文本的 LLM 均可使用；Tool Call 的优势在于可靠性和简洁性，但受限于模型能力。

## 核验清单

开发阶段需确认：prompt 中的格式约束指令已通过 getFormatInstructions() 自动添加；parser.parse() 能够正确处理 markdown 包裹的响应；使用 Zod Schema 时验证 birth_year 等数值字段返回的是数字而非字符串；数组字段如 awards 返回的是对象数组而非字符串拼接。

生产阶段需确认：模型是否支持 tool calling，是则优先采用 bindTools 方案；异常处理已覆盖 LLM 返回非 JSON 格式的兜底逻辑；复杂嵌套结构的字段名和类型与下游消费端定义一致；测试用例覆盖字段名错误、类型错误、结构缺失等失败场景。

## 来源与核验

- [原始文章](https://juejin.cn/post/7684195084155076617)
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