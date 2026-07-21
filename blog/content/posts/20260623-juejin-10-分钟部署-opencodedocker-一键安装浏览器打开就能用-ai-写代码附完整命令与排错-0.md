---
title: 10 分钟部署 OpenCode：Docker 一键安装，浏览器打开就能用 AI 写代码（附完整命令与排错）
date: 2026-06-23 09:57:11+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- AI Agent
- Docker
categories:
- AI 工程
scenarios:
- AI/ML项目
- 云原生/容器
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7653694379728158783
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:0771abd064445fd62e036e0544af92ac3abe0fef9d6e395540adb860d3a3366f
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:21:44.952633Z'
source_capture_sha256: sha256:26dccc5bb467aeb5b35f0ff5af07737ed90b555db4c0291462b7120400364523
source_capture_chars_original: 6000
source_publication_excerpt_chars: 642
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_c8158ed750ab33b9e8b979d5cc63de91369994b2b369a712fc282146a3a11035
revision_id: rev_14cd585dbfb1a605b9e36a1c86c40028543aff6f72d97cd5bfd1a19da4a6be80
event_id: evt_a6c2f8a95c9fc72a4b2dd79ed3f7e4e1b4209867ce481fc94b32942e3ad4ec88
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-23T01:57:11Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7653694379728158783](<https://juejin.cn/post/7653694379728158783>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 本文基于
> openeuler/opencode
> 镜像，WSL 与 Linux 服务器双场景实测
> 想在浏览器里用 AI 帮你写代码、改项目？
> OpenCode
> 是一款开源 AI 编码代理，支持终端 TUI、Web 界面和 IDE 扩展等多种使用方式。本文带你完成一次完整的
> OpenCode Docker 部署
> ：从环境准备到在浏览器里用自然语言生成第一个 hello-world 主页，全程约 10 分钟，零基础可跟做。
> 关于 OpenCode 的更多能力，请参阅
> OpenCode 中文文档
> 。国内用户拉取官方镜像（如
> ghcr.io/anomalyco/opencode
> ）可能较慢或超时，本文使用
> 轩辕镜像
> 加速的
> openeuler/opencode
> ——由 openEuler 基础设施 SIG 维护，经
> docker.xuanyuan.run
> 提供 Docker 镜像加速，下文命令均已实测通过。
> 一、环境准备：Docker 一键安装
> 开始之前，请确保机器上已安装 Docker。若尚未安装，可使用轩辕镜像提供的一键脚本（适用于 Linux 及常见国内云服务器）：
> bash &lt;\(wget -qO- https://xuanyuan.cloud/docker.sh\)
> 安装完成后，执行以下命令验证：
> docker --version
> docker compose version
> 若本机已有 Docker，可跳过此步。更多安装与镜像加速配置，可参考
> 轩辕镜像使用手册
> 。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
