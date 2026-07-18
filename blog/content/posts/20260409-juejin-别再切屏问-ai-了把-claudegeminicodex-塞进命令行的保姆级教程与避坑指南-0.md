---
title: 别再切屏问 AI 了！把 Claude、Gemini、Codex 塞进命令行的保姆级教程与避坑指南
date: 2026-04-09 19:37:54+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 命令行工具
categories: []
scenarios:
- 命令行工具
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7626641759687786506
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:ce15095e52444604fff20b262a43e9d7f1d64a59cfa819ad71a9fae7c781f471
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 49
captured_at: '2026-07-18T04:19:31.264608Z'
source_capture_sha256: sha256:5f1f82ebd73a010e38dfcdaf6b03052eb095f7870af04e8e9cbb4c4204fc4221
source_capture_chars_original: 2946
source_publication_excerpt_chars: 768
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7626641759687786506](<https://juejin.cn/post/7626641759687786506>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 现在网上各种CLI都很火，GUI反而是慢慢的退出大众视野，为什么大家开始喜欢终端里使用AI呢？抱着这个态度，我基本上把市面上主流的CLI都安装了一遍，随便把安装教程也梳理了一遍。
> 在我刚开始折腾 CLI，选择的是
> Claude Code
> ，但是后面、
> Gemini CLI
> 、
> Codex CLI
> 我也在后面的日子安装并体验了，而且都跑了一段时间。但是我可能和其他的文章不一样，这篇文章不聊跑分，也不争谁最强，我只讲 3 件事：怎么装、怎么判断它真的能用、我现在大概怎么分。你如果想第一时间使用上CLI，那这篇文章绝对可以当你的第一轮上手参考资料。
> 基础环境确认
> 对于新手，尤其是小白，我一般不建议上来就复制命令。CLI 这类工具最烦的不是安装命令本身，而是基础环境和知道为什么会错的解决方案。
> 首先先确认 4 件事：
> 机器上有没有安装的
> node
> 和
> npm
> 当前 shell 的
> PATH
> 正不正常
> 账号和订阅有没有到位
> 网络环境是否稳定，会不会影响登录流程
> 先跑这几个最基础的检查命令：
> node -v
> npm -v
> which
> node
> which
> npm
> echo
> $SHELL
> 如果这里已经报
> command not found
> ，那后面先别装 CLI，先把 Node 环境补齐。
> 如果 Node 和 npm 都有，但你后面装完还是跑不起来，十有八九是
> PATH
> 没刷进去，或者 shell 没重新加载。
> 注意： CLI 装不上，不一定是命令错了。很多时候是 Node 版本太旧、PATH 没生效，或者你当前终端压根没吃到新环境。如果不会使用nvm的可以参考教程安装：
> nvm安装教程
> 开始安装
> 其实我相信网上各种各样的安装教程肯定已经满天飞了，我这里就不啰嗦直接使用最直接的方式讲解安装，中间也会插入一些踩坑和注意事项。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
