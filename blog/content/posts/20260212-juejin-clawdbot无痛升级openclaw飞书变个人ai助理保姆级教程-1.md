---
title: clawdbot无痛升级openclaw，飞书变个人AI助理保姆级教程
date: 2026-02-12 10:28:19+08:00
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
external_url: https://juejin.cn/post/7605523224530010153
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:37777886da6a746f9c31ca053cbe6641f07dc4554f27cbe9813604a91777109e
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 35
captured_at: '2026-07-18T04:17:14.673159Z'
source_capture_sha256: sha256:93f267f5fe0a69939747577504f37b80a039822f70e1753994e1d062dc5a4693
source_capture_chars_original: 2876
source_publication_excerpt_chars: 783
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_64a9b541820a7704e7708618a344f66506b88961a954aa9f015f20c1feaf1283
revision_id: rev_35afe044557bc96479246311444aeed486d6b24c8a21b4427bf1d78c4b89c4f9
event_id: evt_a339b9759b4de435d19ec29380803bb31449b0e12dafcc542ec4c9a1e86608dc
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-12T02:28:19Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7605523224530010153](<https://juejin.cn/post/7605523224530010153>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 大家好，
> 我是阿星👋！
> 上期我们已经教大家如何用本机+clawdbot在飞书上部署个人助理。clawdbot接入飞书阿里云，立即拥有24小时AI助理贾维斯
> 但是clawdbot又改名为OpenClaw了旧的已经不维护了。
> 新版还加了webui功能可以可视化进行配置。所以我们肯定是要升级的。
> 而且新版还可以比较方便安装一下下面功能，还能做功能拓展：
> 在新版，你可以优先勾选以下几个最实用的技能
> 所以，如果你想实现下面这些功能，可以跟着下面步骤升级到
> 2026.2.9
> 📝 apple-notes
> /
> ⏰ apple-reminders
> : 这样你可以直接在飞书里跟机器人说“帮我记个笔记”或者“下午三点提醒我开会”。
> 🐙 github
> : 勾选这个可以让你通过机器人查询仓库动态或管理 Issue。
> 📸 camsnap
> : 很酷的功能，可以让机器人调用你 MacBook 的摄像头拍照并传给你（适合远程监控）。
> 📨 imsg
> : 允许机器人帮你收发 iMessage 短信。
> 🧩 clawhub
> : 核心组件，建议保留。
> 第一步：清理旧门户
> 🛑 先让旧机器人“下班”
> 在卸载之前，必须先停止正在运行的服务，否则进程占用会让你怀疑人生。
> clawdbot gateway stop
> 🗑️ 彻底卸载旧版 ClawdBot
> npm uninstall -g clawdbot
> 第二步：一键入驻新家
> 官方提供了一行代码的一键安装脚本，它会自动帮你把环境依赖（比如 Node 22+）都搞定：
> curl -fsSL https:
> //openclaw.ai/install.sh | bash
> 🔍 验明正身
> 安装完后，输入下面这行命令，看看新版本是不是已经在你的电脑里安装了：
> openclaw
> --version
> 如果显示类似
> 2026.2.9
> ，恭喜你，基础环境已就绪！…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
