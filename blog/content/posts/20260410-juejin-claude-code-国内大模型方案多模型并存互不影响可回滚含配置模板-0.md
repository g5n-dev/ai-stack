---
title: Claude Code 国内大模型方案：多模型并存、互不影响、可回滚（含配置模板）
date: 2026-04-10 11:13:49+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7627006875628339238
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ed7fb76e15fe7c20fe96948cf1eca45d3e267282383fe23145cec3b7bafbd9e8
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:19:31.519006Z'
source_capture_sha256: sha256:efbd8296a1f9b964da1f5bab3f831619541b6f0dcaea0fcc5672bcd33189acb6
source_capture_chars_original: 1521
source_publication_excerpt_chars: 612
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_ddf34430b91fb2f8d2e5698dc90eeb9434589fc74ec1b403f7b01a26b2c4f095
revision_id: rev_3734b98770c36436d1fced8695a27dd3d03385ecae994a727cd99683316dd9a6
event_id: evt_75ceb3b3cabd7df68b1a382ef5e95b946626b408ba5391ab943d149493ac1aba
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-10T03:13:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7627006875628339238](<https://juejin.cn/post/7627006875628339238>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 💡大家好，我是可夫小子，一名内容创作者，关注AI和自媒体。
> 作为地表最强的编程 Agent：Claude Code，默认只能使用自家的Claude大模型，但由于 Anthropic 的服务条款，是不能在国内使用。一直与国内的开发者玩起了猫鼠游戏，动不动就来个封号套餐，让人又爱又恨。
> 你想换智谱/DeepSeek/MiniMax，却每次都要改 URL、Key、代理？
> 这篇我给一个
> 最轻量方案
> ：不用安装 Router，靠
> 多份 settings + alias
> 实现：
> 一键切换模型（命令级开关）
> 各项目配置互不影响（隔离）
> 出问题可秒回滚（稳定）
> 现在的方案
> 国内主要有的大模型厂家有，智谱、DeepSeek、MiniMax，这几家大模型的能力也层次不齐，但每家模型的请求地址、API Key 都不一样，有时候需要经常切换。
> 现在主流的方案有Claude Code Router、CC-Switch项目等，就是解决这一问题应运而生。
> 但为了这个切换功能还要专门安装一个软件，有点太重了。我使用安排软件的逻辑就是能不装软件就不装软件。我还要使用更丝滑的轻量的方案。以下是我的参考方案，大家可以参考使用。
> 我的方案
> 使用~/.claude/settings.json里面添加不同的json，在启动claude时，显示使用
> --settings
> 来实现各个模型的切换，然后通过 alias 做成一个短命令，就能实现快速切换。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
