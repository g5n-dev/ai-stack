---
title: "别再被 AI 骗了：我把腾讯云 4 个 Skill 做成了个「AI 打假侦探」，过程的一个小配置坑惨了我"
date: 2026-08-17T07:37:17+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:68f66f231c95d593a58448dcb7afc9e1cc69da5c4f7a5cf131c6459debb15cc4"
source_payload_sha256: "sha256:471f2912a1c7c38700a72dd3f5a590c3606adde895967be5711ec036d7b1c1d2"
source_published_at: 2026-08-16T15:19:00Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:90add55d0e22737fd810c5ad63ad76081ad3c20d46561d8b9f8652b9fba7d918"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
description: "核心结论 腾讯云 AI Skills 支持图片、文本、视频三类 AI 生成内容检测，并提供人脸换脸防护接口。项目通过手动实现 TC3-HMAC-SHA256 签名调用腾讯云内容安全 API，绕过了官方 SDK 的体积依赖。"
external_url: https://juejin.cn/post/7674215005011951654
observation_id: obs_c5a61f632c8344449823edf4548a09123bf3237508b8ce817e70c47817240058
revision_id: rev_2934e68d4b0a2e97d977d8c811bb2a38be871466383c8600bfabfc8fab9568e6
event_id: evt_3015798fe405097c2d29f63c1ef064276677c4a6bbb39fa897ecb2d24ba67415
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-16T23:33:48.754997Z
last_seen_at: 2026-08-16T23:37:17Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: LucianaiB
- **原始来源**: [https://juejin.cn/post/7674215005011951654](https://juejin.cn/post/7674215005011951654)
- **原文发布时间**: Sun, 16 Aug 2026 15:19:00 GMT

## 核心结论

腾讯云 AI Skills 支持图片、文本、视频三类 AI 生成内容检测，并提供人脸换脸防护接口。项目通过手动实现 TC3-HMAC-SHA256 签名调用腾讯云内容安全 API，绕过了官方 SDK 的体积依赖。关键经验是：创建 Biztype 审核策略时必须指定「场景」字段，否则系统会对所有内容返回「真实」判定，导致检测功能形同虚设。项目代码已在 GitHub 开源。

## 能力机制

检测链路分为四个模块。图片识别调用 ims 的 ImageModeration 接口，传入 IMAGE_AIGC 参数，识别 Stable Diffusion、Midjourney 等生成图。文本识别调用 tms 的 TextModeration 接口，传入 TEXT_AIGC 参数，识别 AI 代写文章。视频识别采用 vm 异步两段式架构，识别 Veo3、混元、即梦等生成的视频。人脸换脸检测使用 faceid 防护盾接口。

返回结果结构统一为三个字段：Suggestion 表示处置建议（Block/Review/Pass），Label 表示内容标签（Normal 或 GeneratedContentRisk），Score 表示置信度评分（0-100）。

编排层由 WorkBuddy 负责，根据用户输入自动分流至对应脚本执行检测。作者放弃了腾讯云官方 SDK，改为用 Python 标准库手写 TC3-HMAC-SHA256 签名，并通过字节级比对确认签名实现正确。

## 快速开始

准备阶段需要在腾讯云控制台完成三项操作：创建 API 密钥获取 SecretId 与 SecretKey；在「LLM 内容审核」页面开通服务；进入「应用管理」分别为图片、视频、文本创建审核策略，创建时必须填写「场景」字段。

环境变量配置如下：

```
TENCENTCLOUD_SECRET_ID
TENCENTCLOUD_SECRET_KEY
TENCENTCLOUD_AIGC_RECOG_IMAGE_BIZ_TYPE
TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE
TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE
```

验证密钥有效性：

```
python scripts/detect.py check
```

执行检测的命令格式：

```
python scripts/detect.py image ./目标图片.jpg
python scripts/detect.py text ./目标文本.txt
python scripts/detect.py video "视频URL"
python scripts/detect.py auto ./任意文件
```

auto 参数支持自动识别文件类型并分流至对应检测脚本。

## 适用边界

检测能力受限于腾讯云内容安全服务的识别范围与场景配置完整性。当前支持的场景包括新闻、小说、百科、问答、博客、商业文案、论文、作文、日记等，不同场景使用对应的 AI 特征标准进行判断。策略未填写场景时，系统会跳过内容分析直接返回「真实」，因此场景配置是检测生效的前提条件。

SecretKey 仅在创建时显示一次，且长度为 32 位，不可重复查询。若密钥复制错误或被覆盖，需重新创建。图片 AI 识别、视频 AI 识别、文本 AI 识别三项服务需分别开通，缺一不可。

签名实现需要严格遵循 TC3-HMAC-SHA256 算法规范，若出现 AuthFailure.SignatureFailure 错误，建议通过官方 SDK 进行同密钥调用的交叉验证来定位问题来源。.env 文件与环境变量的优先级需要明确配置，否则可能存在失效旧密钥覆盖有效密钥的情况。

## 核验清单

部署前应逐项确认以下要点：API 密钥已正确配置且未过期；LLM 内容审核服务已开通并完成初始化；三个 Biztype 策略均已创建且「场景」字段已填写；签名算法实现与官方 SDK 进行了字节级比对验证；.env 文件与环境变量的优先级逻辑已确认；检测脚本可正常调用 API 并返回结果。验证环节建议先用已知 AI 生成内容测试，确认返回 Block 与 GeneratedContentRisk 标签后再投入正式使用。

## 来源与核验

- [原始文章](https://juejin.cn/post/7674215005011951654)
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