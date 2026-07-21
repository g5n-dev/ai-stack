---
title: "WorkBuddy 加 WorkRally，AI 帮你拍短剧的全流程拆解，附保姆级教程"
date: 2026-07-20T02:13:23+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:81db9adba19875190232b2d2776c330dc1009364b53f8aa220ba5eb3de051cce"
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:dddd9f78485f30f4288ee3fec2ca1d3a67c6539da094703d3ca92cacdf0e1d17"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
description: "核心结论 WorkRally是腾讯混元团队推出的AI漫画和视频创作平台，其核心定位是面向短剧、短番、条漫等需要角色一致性和分镜连贯性的内容场景。该平台通过角色多视图生成技术解决了AI视频创作中的一致性难题，并提供命令行接口支持自动化工作流。"
external_url: https://juejin.cn/post/7663690608759210018
observation_id: obs_446fb4e87d33d654fdf403ad6f0de20162b5327703ef89300a181b0bde97e7d3
revision_id: rev_2ff9f652d5c2d515f2ba4869cb6fe13f06e3cd691c00110678923408d74b06f7
event_id: evt_1cffabd3d330b39309fac31d58a0845651f589a6612f70440b3665fc2d410c19
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-19T18:13:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 小虎AI生活
- **原始来源**: [https://juejin.cn/post/7663690608759210018](https://juejin.cn/post/7663690608759210018)
- **原文发布时间**: Sun, 19 Jul 2026 11:27:31 GMT

## 核心结论

WorkRally是腾讯混元团队推出的AI漫画和视频创作平台，其核心定位是面向短剧、短番、条漫等需要角色一致性和分镜连贯性的内容场景。该平台通过角色多视图生成技术解决了AI视频创作中的一致性难题，并提供命令行接口支持自动化工作流。

从来源描述的操作实例来看，用户上传一张照片后，系统可自动完成角色设定、多场景分镜图生成、视频片段合成及配音剪辑，形成完整的四场景短剧初稿。整个流程在三个多小时内完成，消耗约300体验积分。

来源指出平台目前仍处于需要打磨初稿的阶段，尚未达到一键成片的成熟度。行业竞争态势明确，可灵、Vidu等国产平台及Seedance 2.0、Grok视频生成等功能均在快速迭代中。

## 能力机制

**角色一致性系统**

平台支持用户上传单张照片自动生成多视图角色设定图，包含正面、侧面、背面视角。该角色形象在后续生成的所有图片和视频中保持一致，包括面部特征、服装样式和表情特征。来源将此功能描述为解决“AI视频最大痛点”的核心能力。

**积分消耗模式**

新用户注册后账户积分为零，需联系客服获取新用户体验积分。来源描述其通过客服渠道在十分钟内获得300积分。平台定价为10积分折合1元人民币。生成一张图片约消耗15积分，生成一段5秒视频约消耗50积分。

**命令行接口**

平台提供CLI（命令行接口）供开发者使用。来源提到该接口包含33个API命令，支持与AI编程助手配合实现自动化调用。CLI可安装至本地目录，理论上可与外部AI助手系统集成形成工作流。

**内容生成流程**

从来源描述的完整流程看，系统可自动执行以下步骤：基于输入照片生成角色设计图、编写多场景故事脚本、为每个场景生成配套分镜图片、将分镜图片转换为视频片段、进行配音合成和最终剪辑。

## 快速开始

**注册与积分获取**

访问workrally.qq.com，使用微信扫码完成注册。注册后账户初始积分为零，需联系平台客服申请新用户体验积分。来源提到可通过扫描客服二维码完成积分申领。

**CLI安装**

来源描述了通过外部AI助手完成CLI安装的流程，将平台提供的open-api相关工具整理为skill并安装至本地development/skills目录。具体安装命令需参考官方文档。

**基础操作路径**

用户上传人物照片作为角色素材，向AI助手描述所需的短剧主题和场景数量，系统自动执行角色生成、分镜设计、视频生成及合成流程。来源中的示例为生成四个场景的校园主题短剧，耗时约三小时完成初稿。

## 适用边界

**适用的内容类型**

平台专门面向需要角色一致性的连续内容场景，包括短剧、短番、条漫等形式。来源强调该平台不追求单次炫酷视频生成，而是专注于连贯内容的创作需求。

**当前能力限制**

来源明确指出初稿“还比较粗糙，有些细节要打磨”，说明生成内容的精细度尚需提升。5秒视频片段的生成模式限制了单次输出的时长。自动生成的脚本和旁白内容尚无自定义控制能力，用户对叙事细节的把控有限。

**成本考量**

300体验积分约合30元人民币，可完成四场景短剧的完整流程验证。对于持续性内容生产，来源未提供正式定价体系的详细信息，无法评估规模化使用的成本结构。

**集成场景**

CLI接口的存在使得平台具备与外部系统对接的可行性，但来源未提供API认证方式、调用频率限制或正式环境变量配置的具体信息。

## 核验清单

- 确认目标内容是否属于短剧、条漫等需要角色一致性的连贯场景
- 核实CLI安装路径是否与本地开发环境兼容
- 确认已通过客服获取体验积分并了解正式积分购买方式
- 验证生成角色与上传照片的一致性保持效果
- 检查自动生成脚本是否符合内容调性要求
- 评估初稿精细度是否满足基本展示需求
- 了解5秒视频片段的拼接方式和时长扩展方案
- 确认CLI所需的环境变量和认证方式（如有）
- 比对可灵、Vidu等替代平台的功能差异与适用场景

## 来源与核验

- [原始文章](https://juejin.cn/post/7663690608759210018)
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