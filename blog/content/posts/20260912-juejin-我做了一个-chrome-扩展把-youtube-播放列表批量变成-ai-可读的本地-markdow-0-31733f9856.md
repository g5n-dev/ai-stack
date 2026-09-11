---
title: "我做了一个 Chrome 扩展，把 YouTube 播放列表批量变成 AI 可读的本地 Markdown"
date: 2026-09-12T02:35:20+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:2699a3f22d344341f1411c7577431ebd567b751d03502b6277f346416cfa7f06"
source_payload_sha256: "sha256:0857d8f3872a188fcdaaecf40dd7a28123b8488a0096f213a4e6b35e3293d986"
source_published_at: 2026-09-11T14:51:41Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a7481f03251f61dd88c5311006ccdbca477053fdd5d022f388eeb75210fea27b"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
description: "核心结论 Transcriptly 是一款 Chrome 扩展，功能是将 YouTube 视频、播放列表和频道的字幕批量导出为本地 Markdown 文件。项目采用 MIT 协议开源，不依赖 YouTube Data API。"
external_url: https://juejin.cn/post/7684157530612138010
observation_id: obs_31733f9856e3a5a09ad2f18c6432758b431c5c6fad9ca01fbc8495794bbce690
revision_id: rev_3f106d982f8a3fde621d82ab7f53243c2ea80e3321ab340a355f98732f96d9d9
event_id: evt_09e950417c536eb0e02111f5ad2b96d70011b70e08596d67416c45a216cc8368
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-09-11T18:32:18.756507Z
last_seen_at: 2026-09-11T18:35:20Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 嘉琪coder
- **原始来源**: [https://juejin.cn/post/7684157530612138010](https://juejin.cn/post/7684157530612138010)
- **原文发布时间**: Fri, 11 Sep 2026 14:51:41 GMT

## 核心结论

Transcriptly 是一款 Chrome 扩展，功能是将 YouTube 视频、播放列表和频道的字幕批量导出为本地 Markdown 文件。项目采用 MIT 协议开源，不依赖 YouTube Data API。批量保存操作不需要注册账号，字幕数据通过浏览器能力直接写入用户指定的本地文件夹，不经过中间服务器。用户可以自主选择是否向公共字幕库贡献内容，该选项默认为关闭状态。

## 能力机制

Transcriptly 的处理流程为：用户进入 YouTube 视频、播放列表或频道页面后，勾选需要的目标视频，随后指定本地保存目录。扩展会依次打开各视频页面、读取可用字幕并生成独立的 Markdown 文件。

导出格式提供两种选择。Timeline 格式保留每段字幕对应的时间戳，用户点击时间标记可跳转回视频原位置，适合需要核对原文或引用来源的场景。Article 格式去除时间线干扰，将字幕整理为接近普通文章的结构，更便于连续阅读或交由 AI 工具进行总结和提取。

批量处理支持暂停、继续操作，并具备失败自动重试机制。处理上限未设置固定阈值，但实际性能受网络带宽、视频数量以及 YouTube 页面加载速度影响。

## 快速开始

用户通过 Chrome 应用商店安装扩展后，在带有字幕的 YouTube 视频页面点击浏览器工具栏中的 Transcriptly 图标即可预览并保存字幕。在播放列表或频道页面使用时，可进入批量选择模式一次保存多个视频。

安装方式为 Chrome 应用商店搜索安装，项目源码托管于 GitHub，采用 MIT 协议。

## 适用边界

Transcriptly 本身不提供 AI 知识库功能，也不绑定任何大模型服务。它属于知识工作流的“资料入口”阶段，仅负责将 YouTube 内容转换为开放格式的本地文件，后续处理由用户自行选择 Obsidian、Claude、ChatGPT、Cursor 等工具完成。

公共字幕库为可选功能，用户需要主动选择才会将字幕贡献至公开库，该功能与本地保存相互独立。即使不再使用 Transcriptly，已保存的 Markdown 文件仍可正常打开和编辑。

## 核验清单

使用前应确认目标视频已包含可用字幕，批量处理时会读取各视频页面提供的字幕数据。可通过扩展图标预览字幕内容后再执行保存操作。保存前需指定用于存放 Markdown 文件的本地文件夹路径。导出格式可根据后续使用场景选择 Timeline 或 Article。若需要将字幕纳入公共知识库，需在扩展设置中主动开启贡献选项。

## 来源与核验

- [原始文章](https://juejin.cn/post/7684157530612138010)
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