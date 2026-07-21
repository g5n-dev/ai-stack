---
title: Langchain入门到精通0x09：Tool & Function Calling
date: 2026-03-13 03:05:25+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7616201064984428554
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:d1c61ed913b52baf991f26d5fcd91bb464ae7c7fa7cdd7dd79dd8187b7490172
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 42
captured_at: '2026-07-18T04:19:13.019863Z'
source_capture_sha256: sha256:b7507f32a9bd4743b4f3d74edbd46f05517d95e1d029700e0da2c044dc8ca48f
source_capture_chars_original: 2348
source_publication_excerpt_chars: 726
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_b9d16535ab7886b7a9f9c3aaa4fac6d9f9e151e2333a0ee8a1682d4c12b46831
revision_id: rev_cc9595d5bf1812a7ed50604e182c1101d4672ffd747fc0b80ef6a926939b4fd1
event_id: evt_89494d4d6c7d22758c0c45ad7eea9cc5f32116c558727fa07c91027fe17f9eb6
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-12T19:05:25Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7616201064984428554](<https://juejin.cn/post/7616201064984428554>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大模型的边界能力
> 我们先看看下面一段代码，AI大模型执行的结果是什么呢？
> # 通义千问大模型
> model
> = get\_lc\_model\_client\(\)
> output\_parser
> = JsonOutputParser\(\)
> resp
> = model.invoke\(
> "今天是几月几号？"
> \)
> print\(resp\)
> AI居然不知道，是不是大跌眼镜呢？ 我们尝试换一个模型（DeepSeek）试试:
> model
> = get\_ali\_model\_client\(\)
> 果然，虽然答出了一个日期，但并不是真实今天的日期。之前我们在
> 为啥需要RAG
> 讲过大模型的
> 时效性
> ：训练是有成本的，不可能随时更新训练。所以可能有些最近的知识可能其并不知道。
> 这就是大模型的
> 能力边界
> 之一，解决方案除了RAG技术之外便是 Tool了。
> Tool
> Tool（工具）
> ：这是 LangChain 中的一个
> 类
> 或
> 对象
> 。它封装了一个具体的功能（如 Python 函数），并包含了该功能的名称、描述和参数模式（Schema）。开发者通过
> @tool
> 装饰器或
> BaseTool
> 类来创建工具，告诉模型“我这里有什么能力”。其核心流程如下：
> 定义工具
> ：开发者预先将函数（如 get\_date\(\)）及其描述、参数格式告知LLM。
> 模型规划
> ：当用户提问（如“今天是几月几号？”），LLM并不直接回答，而是分析意图，
> 选择并规划
> 需要调用的工具，并严格按照格式生成一个结构化的调用请求。
> 外部执行
> ：你的程序
> 解析
> 这个结构化请求，
> 安全地
> 在本地或远端执行真正的函数，获得结果
> 整合回复
> ：将执行结果返回给LLM，由LLM组织成自然语言回复给用户（如“今天是3月12日。”）。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
