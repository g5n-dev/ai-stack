---
title: "再也不用手动整理会议纪要！我给 Claude 封装了一套永久自动化 Skill"
date: 2026-07-19T23:19:40+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:f5446b76ba8b2f3724dd0032ee4bcefb8ea1b742f2d312187cc2255f16124487"
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:a79c5da5719e8b58324ced59539e209ae801309df44a61cc39f6f8e4ea5d869c"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 39
description: "核心结论 Skill 本质是将反复使用的长 Prompt 和固定工作流程打包成永久保存在本地的专属能力。存放在项目根目录 下的文件夹中，核心配置文件为 。封装后的 Skill 相比临时粘贴提示词，可省去每次对话重新定义角色、规范输出格式的重复操作。"
external_url: https://juejin.cn/post/7663518981036195874
observation_id: obs_357d5c1b0595dce4b6f1e7d5443e40d4afc7cca08ae086532e2ac6deda26a02a
revision_id: rev_dadffaa3b62930752f41d8010493e9f46a5c2c6e49a60b6de677003f6a68a87e
event_id: evt_026cf00998ffe99ff06390e65090cef1948456a9fd643cbf9102d11025889058
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-19T15:19:40Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: To\_OC
- **原始来源**: [https://juejin.cn/post/7663518981036195874](https://juejin.cn/post/7663518981036195874)
- **原文发布时间**: Sun, 19 Jul 2026 11:25:20 GMT

## 核心结论

Skill 本质是将反复使用的长 Prompt 和固定工作流程打包成永久保存在本地的专属能力。存放在项目根目录 `.claude/skills/` 下的文件夹中，核心配置文件为 `skill.md`。封装后的 Skill 相比临时粘贴提示词，可省去每次对话重新定义角色、规范输出格式的重复操作。

当某项工作每周重复 3 次以上、每次输入的指令高度同质化时，适合封装成 Skill。

## 能力机制

Skill 的核心载体包含两个部分：本地文件夹存放一类技能的全部配置文件，工具自动扫描 `.claude/skills/` 目录加载所有技能；`skill.md` 是核心配置文件，用 YAML 头部定义技能名称和功能描述，正文固化工作流程与输出规范。

Anthropic 提供 `skill-creator` 工具用于标准化生成 Skill 模板，避免手动编写 YAML 配置时出现格式错误。安装 `skill-creator` 后，通过对话描述需求，工具会自动生成完整文件夹结构和标准化 `skill.md` 配置，无需手动编写 YAML。

## 快速开始

**安装 skill-creator 基础技能**

在 Claude 会话中输入指令，将 `skill-creator` 安装到当前目录的 `.claude/skills` 文件夹。

**校验工具是否安装成功**

安装完成后，输入指令 `/skills` 查看本地所有已加载的 Skill，列表中出现 `skill-creator` 算部署成功。

**创建会议纪要技能**

工具加载完成后，向其传入完整需求描述，包括：输入源格式、处理步骤、输出固定结构、边界规则。例如说明技能需要根据用户提供的文字稿，生成结构化会议纪要，包含会议基本信息、会议目标、会议内容、行动项四大模块，不确定内容留空。

**调用已创建的技能**

将录音转写文本文件丢给 Claude，输入调用指令，工具会自动执行封装好的纪要处理流程。

## 适用边界

**适合封装 Skill 的场景**

每周重复 3 次以上且输入输出格式高度固定的工作；每次对话都要粘贴超过 5 行的固定提示词；有固定文件输入源的场景；输出有严格结构化要求的工作。

**不建议封装的场景**

偶发的临时提问或查询；需求每次完全不相同、没有统一输出规范；一次性任务，后续不会重复使用。

## 核验清单

安装后执行 `/skills` 命令，确认列表中出现目标 Skill。若列表找不到新安装的工具，先检查文件夹名称是否为纯英文且无特殊符号，确认 `.claude` 文件夹未被代码工具忽略。

确认 `.claude/skills/` 目录结构正确创建，`skill.md` 文件位于该目录下。调用技能后验证输出是否符合定义的结构化要求。

手动修改 `skill.md` 配置后需重新调用 `skill-creator` 重载，否则工具会读取缓存中的旧配置，修改不生效。

## 来源与核验

- [原始文章](https://juejin.cn/post/7663518981036195874)
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