---
title: "开源项目第178期：OptMem — 426 个 token 的提示词，给 AI Agent 跨会话的持久记忆"
date: 2026-08-07T21:41:07+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:c6a8dad20847a941c2c5a07e32da9ffbc50cd2260027a4bd15385785e96d029a"
source_payload_sha256: "sha256:53889742bdf65ddcfb6a094a64f75b396684fe4d4780b40151351006ad72855e"
source_published_at: 2026-08-07T13:10:58Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:4e74d6d05972e6908a21bf7b74f1b2692ccde786ff14decb6c11870f2ee83be5"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
description: "核心结论 OptMem是一个AI Agent跨会话持久记忆工具，通过一个Python脚本配合426个token的提示词实现，无需外部依赖。工具将记忆存储在本地文本文件，配合二叉树摘要结构控制token消耗。"
external_url: https://juejin.cn/post/7671100905954263076
observation_id: obs_7a441307a04c24f0ce288e91ce778c436a57d5b11018fa4aa2db093ea7a3a417
revision_id: rev_0e57c3f213b0b6c6451c0d018ef49affea725836ca760d36550c54a452e9d2f9
event_id: evt_bd8f58e93ed5c5c1f241d5a352465c6dba8c6d364c66b91ceda4b7df0f8d3bef
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-07T13:38:31.005235Z
last_seen_at: 2026-08-07T13:41:07Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 冬奇Lab
- **原始来源**: [https://juejin.cn/post/7671100905954263076](https://juejin.cn/post/7671100905954263076)
- **原文发布时间**: Fri, 07 Aug 2026 13:10:58 GMT

## 核心结论

OptMem是一个AI Agent跨会话持久记忆工具，通过一个Python脚本配合426个token的提示词实现，无需外部依赖。工具将记忆存储在本地文本文件，配合二叉树摘要结构控制token消耗。安装方式为一行命令，完成后需将提示词块添加到AGENTS.md或CLAUDE.md中，使Agent在会话开始时自动加载历史记忆。核心设计理念是LOG.txt作为唯一真相来源，TREE/目录仅为可重建的缓存。

## 能力机制

工具在~/.optmem/memory/目录下管理三层结构。LOG.txt采用追加写入模式，每条记忆包含序号、时间戳和内容，固定宽度格式使单条记录可通过序号实现O(1)寻址。TREE/目录存放二叉树摘要节点，每两个相邻节点合并生成上一层摘要，形成树状压缩结构。TREE/内所有内容均可从LOG.txt完整重建。

`memo wake`命令在会话启动时执行，输出分层记忆视图：近期记忆以原始形式精确展示，较早记忆以逐级摘要形式压缩展示。摘要合并任务通过`memo nap`命令在Agent工作时内联执行，而非后台进程处理。六条核心命令分别承担加载记忆、记录事实、处理合并、全文搜索、展开摘要、删除节点等功能。

提示词块强制Agent将wake作为第一个操作，定义触发记录的时刻类型包括决策确定、事实发现、用户偏好、已知坑点，并禁止子Agent执行记忆操作。记录内容限制在280字节以内以保持原子性。

## 快速开始

安装命令适用于macOS和Linux环境，通过脚本自动部署memo命令并创建~/.optmem/目录。Windows用户需参考项目中的WINDOWS.md文档。安装完成后执行memo wake命令获取Memory块内容，将该块添加到项目根目录的AGENTS.md或全局配置~/.claude/CLAUDE.md中。环境变量MEMORY_DIR可指定记忆存储路径，实现通过Dropbox、iCloud或git仓库跨设备同步。

## 适用边界

该工具适用于个人开发者或单项目场景，核心优势在于记忆文件的完全透明性——用户可直接用文本编辑器查看Agent记录的所有内容。正则搜索功能要求精确词匹配，无法进行语义模糊检索。与向量数据库相比，OptMem省去服务器和嵌入模型搭建成本，每次会话加载固定token预算，但不支持百万级记忆的语义检索能力。二叉树摘要虽通过上下文注入部分弥补语义匹配问题，但仍存在记录用词与查询表述不一致时检索失败的可能。工具在会话开始时必然消耗token预算加载记忆，无论当次会话是否需要访问旧记录。

## 核验清单

安装后memo命令可用且无Python第三方依赖，~/.optmem/memory/目录结构包含LOG.txt、TREE/子目录和config配置文件。执行memo wake输出包含## Memory标记的Markdown格式内容。memo note命令记录内容不超过280字节。memo recall命令支持正则表达式搜索。memo nap命令处理二叉树节点的摘要合并任务。配置MEMORY_DIR环境变量后记忆文件路径相应变更。LOG.txt采用追加模式，写入后内容不被修改或删除。

## 来源与核验

- [原始文章](https://juejin.cn/post/7671100905954263076)
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