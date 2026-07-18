---
title: 那个霸榜的Pony Alpha现身了：智谱GLM-5硬刚Claude Opus
date: 2026-02-12 15:02:46+08:00
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
external_url: https://juejin.cn/post/7605711582429970483
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:eaece9618a9db400700820ea895f84c42979b754896239283282020df71cac18
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 39
captured_at: '2026-07-18T04:17:14.996734Z'
source_capture_sha256: sha256:4b5f2d00abc656cd5bad1793870fbc5c1e4ec2f89d495bf76b93c04889de78b4
source_capture_chars_original: 1690
source_publication_excerpt_chars: 794
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605711582429970483](<https://juejin.cn/post/7605711582429970483>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 还记得前段时间在OpenRouter榜单上那个神秘兮兮、一度登顶热度榜的“Pony Alpha”吗？当时圈子里都在猜是哪家巨头又憋了个大招，是OpenAI的暗桩？还是Anthropic的新马甲？
> 2026年2月12日，谜底揭晓。不是硅谷的科技新贵，而是来自北京海淀的智谱AI。
> 这不仅仅是一次简单的版本号更迭。GLM-5的发布，实际上宣告了国产大模型从“能聊天”正式跨越到了“能干活”的工程化阶段。我看完了智谱长达几十页的技术报告和Github上的代码库，剔除掉那些公关辞令，这就带大家看看这台名为GLM-5的机器到底成色几何。
> 参数怪兽与“瘦身”哲学
> 先看最吓人的数字：744B。
> 是的，GLM-5的总参数量高达7440亿。这是什么概念？上一代GLM-4.5才355B，直接翻了一倍多。但别被这个数字劝退，这里面藏着智谱的技术鸡贼（褒义）：它采用了MoE（混合专家）架构，虽然块头大，但真正跑起来的“激活参数”只有40B。
> 这意味着什么？意味着它拥有巨型模型的知识储备，跑起来却只有中型模型的能耗。而且，智谱这次非常务实地集成了DeepSeek的Sparse Attention（稀疏注意力机制）。这个技术动作很关键，它解决了长文本“吞金兽”的问题，让200K的上下文窗口不再是摆设，而是真正用得起的生产力工具。
> 至于预训练数据，28.5T tokens。比前代涨了24%。在这个数据枯竭的年代，还能榨出这么多高质量token，本身就是护城河。
> 真的能写代码吗？
> 程序员最关心的Coding能力，这次GLM-5是奔着“砸场子”去的。
> 在SWE-bench-Verified这个目前公认最硬核的编程测试里，GLM-5拿下了77.8分。
> 为了让大家有个直观概念：Google的Gemini 3 Pro被它甩在身后，而目前公认的“代码之神”Claude Opus 4.5，分数在80分左右。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
