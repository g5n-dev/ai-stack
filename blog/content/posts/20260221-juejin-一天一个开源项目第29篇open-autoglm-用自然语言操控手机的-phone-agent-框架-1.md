---
title: 一天一个开源项目（第29篇）：Open-AutoGLM - 用自然语言操控手机的 Phone Agent 框架
date: 2026-02-21 06:57:09+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Python
- JavaScript
categories:
- AI 工程
scenarios:
- AI/ML项目
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7608382961723588658
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:3c951c3d1a8ecfbaaa5121c1e2918f6ea907908b5214357be638ed2af336c4c9
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 55
captured_at: '2026-07-18T04:17:31.959625Z'
source_capture_sha256: sha256:82f8236ddedad7b4c10aa176dcf18c3b24bebf57503563763a969b9d7c3cb2a2
source_capture_chars_original: 3496
source_publication_excerpt_chars: 547
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_062543a90a667fbc72c5b41bb0f538f8a2033627d282dcb65d45d6058a8a1149
revision_id: rev_f46a3d3c299cdcb283d2ac06b29af7823db16ee0e07d460763da7d9a7dbaa22c
event_id: evt_8ac6a2244411e22b5a3675bcd01a394667ee921e62b25a8599cbe312e05c3848
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-20T22:57:09Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7608382961723588658](<https://juejin.cn/post/7608382961723588658>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 引言
> "打开美团搜索附近的火锅店」「给文件传输助手发一条：部署成功」——说完，手机自己动。"
> 这是"一天一个开源项目"系列的第29篇文章。今天带你了解的项目是
> Open-AutoGLM
> （
> GitHub
> ），由
> zai-org
> （智谱生态）开源。
> 你希望用自然语言控制手机：打开 App、搜索、点击、输入文字，而不必自己一步步操作。
> Open-AutoGLM
> 提供两件事：一是
> Phone Agent 框架
> （运行在电脑上的 Python 代码），通过
> ADB
> （Android）或
> HDC
> （鸿蒙）控制设备，循环执行「截图 → 视觉模型理解界面 → 输出动作（启动 App、点击坐标、输入等）→ 执行」；二是
> AutoGLM-Phone
> 系列视觉语言模型（9B 参数），针对手机界面做了优化，可直接用智谱 BigModel、ModelScope 的 API，或自建 vLLM/SGLang 服务。用户只需说一句如「打开小红书搜索美食」，Agent 即可自动完成整条流程，并支持敏感操作确认与登录/验证码时的人工接管。项目支持
> Android 7.0+
> 与
> HarmonyOS NEXT
> ，覆盖 50+ 安卓应用与 60+ 鸿蒙应用，并可与
> Midscene.js
> 等 UI 自动化工具集成。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
