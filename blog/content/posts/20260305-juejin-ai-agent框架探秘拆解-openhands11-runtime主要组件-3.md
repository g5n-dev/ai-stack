---
title: AI Agent框架探秘：拆解 OpenHands（11）--- Runtime主要组件
date: 2026-03-05 22:28:24+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- 大语言模型
- Python
- Docker
categories:
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7613569620952350720
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:2a2d16592c645ef6716275edf555432adfe8318fa0cd1046d73e8995f3bf4002
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:18:36.360295Z'
source_capture_sha256: sha256:3654ba9cb1bd9085e8617253fe2c4c106aef9f87cd19eae91122a6aa9a415c45
source_capture_chars_original: 4124
source_publication_excerpt_chars: 765
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_d3519ddc02e63842c5253b8081a5bd38f31f8430e2f8580799feca99bc6e1c14
revision_id: rev_6402fe78c2966b2f6031129d9826340364e8884c15915950e000f926bc79e01b
event_id: evt_11ca8f955e9f16294a129f5a5d3b7b0be1f221fc9e63d64113ae19ad7d118875
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-05T14:28:24Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7613569620952350720](<https://juejin.cn/post/7613569620952350720>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> AI Agent框架探秘：拆解 OpenHands（11）--- Runtime主要组件
> 0x00 概要
> 0x01 三大组件
> 0x02 数据流
> 0x03 插件系统
> 3.1 sandbox\_plugins
> 3.2 Plugin 基类
> 3.3 JupyterPlugin
> 3.4 AgentSkillsPlugin
> 0x04 执行系统
> 4.1 调用
> 4.2action\_execution\_client.py
> 4.3 action\_execution\_server.py
> 4.4 流程图
> 4.5 代码
> 0x05 环境
> 5.1 调用
> 5.2 核心特色
> 5.3 流程图
> 5.4 代码
> 0xFF 参考
> 0x00 概要
> 本篇继续对 runtime 的解读，主要介绍 插件、执行系统和环境这三个组件。
> 因为本系列借鉴的文章过多，可能在参考文献中有遗漏的文章，如果有，还请大家指出。
> 0x01 三大组件
> 本篇要介绍的几个组件如下：
> ActionExecutor：在 Runtime 中执行动作的核心组件
> ActionExecutor 初始化时会根据配置加载指定的插件。插件注册到 ActionExecutor 的插件字典。
> 当接收到动作请求时，ActionExecutor 会调用相应的方法执行动作。
> 对于浏览动作，ActionExecutor 会使用 BrowserEnv 来处理。
> 如果涉及插件，ActionExecutor 会通过插件系统处理
> AgentSkillsPlugin：提供智能体技能功能的插件
> AgentSkillsPlugin 是一个插件，继承自 Plugin 基类。
> Runtime 初始化时，插件会被加载到插件字典中。 插件通过 PluginRequirement 机制被注册到系统中。
> 特定动作触发时调用相应插件功能。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
