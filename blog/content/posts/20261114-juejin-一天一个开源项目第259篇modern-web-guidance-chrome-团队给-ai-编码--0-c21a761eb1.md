---
title: "一天一个开源项目（第259篇）：Modern Web Guidance —— Chrome 团队给 AI 编码 Agent 的「现代 Web 最佳实践」外挂"
date: 2026-11-14T00:20:58+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:7df0d222ecc864bdefdb91e5f3027ccc3db8c304b4a244db99ff28025c8d507b"
source_payload_sha256: "sha256:5811b24d55a6fac8cdefab618634549d8799e1c28774c860b7299ebf25ea9abc"
source_published_at: 2026-11-13T15:24:10Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:caba46b0cbd3879335e7b31ddc59be85e73d1a03aa22804469cebd0321a5ca16"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
description: "核心结论 Modern Web Guidance 是 GoogleChrome 维护的 Web 开发 Skill，用于把平台知识、最佳实践和浏览器兼容性数据送入 AI 编码 Agent。它不修改模型，而是让 Agent 在处理 Web 平台问题时检索精选指南，从而减少旧式 JavaScript、重复造轮子和不必要依赖。"
external_url: https://juejin.cn/post/7707533858106884115
observation_id: obs_c21a761eb1d39789734d820ca15ea0b5b8194a7ee46a19711ecb5003d26ad0ae
revision_id: rev_bacb70e077107f38c2e59d4e0352fd08ca03b5f9626d868d08bb60f781045e32
event_id: evt_4cd86cdad538bfe6714e5c99b85bd110faad976c7b771092cb91c0a316fe5940
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-13T16:19:41.471751Z
last_seen_at: 2026-11-13T16:20:58Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 冬奇Lab
- **原始来源**: [https://juejin.cn/post/7707533858106884115](https://juejin.cn/post/7707533858106884115)
- **原文发布时间**: Fri, 13 Nov 2026 15:24:10 GMT

## 核心结论

Modern Web Guidance 是 GoogleChrome 维护的 Web 开发 Skill，用于把平台知识、最佳实践和浏览器兼容性数据送入 AI 编码 Agent。它不修改模型，而是让 Agent 在处理 Web 平台问题时检索精选指南，从而减少旧式 JavaScript、重复造轮子和不必要依赖。

项目采用先搜索、后取回的流程：`search` 用自然语言定位指南，`retrieve` 按指南 ID 返回代码模式、常见坑点和降级方案。检索使用离线、零依赖的嵌入模型与 BM25，无需联网或 API Key。

项目同时提供对照评测：以相同任务分别运行有指引和无指引模式，并用源码模式、计算样式、运行时 DOM 行为及无障碍状态评分。项目方公布的一组结果中，各 Agent 的通过率提升约 27 至 36 个百分点；这是项目自有任务与评分体系下的结果，不代表第三方基准或业务项目中的同等收益。

## 能力机制

指南覆盖约 250 个现代 Web 特性和 203 个开发场景，主题包括 CSS、HTML、JavaScript、可访问性、性能、安全、渐进式 Web 应用及 WebAssembly 等。其内容不仅介绍 API，还包含适用场景、已知问题和兼容策略。

项目通过两个只读发布仓库分工维护：`modern-web-guidance-src` 存放指南原稿、脚本、评测框架、示例应用和 CLI 工具；`GoogleChrome/modern-web-guidance` 存放编译后的 Skill 与插件配置。合并改动按周发布，并同步到 npm 包 `modern-web-guidance`。

新特性采用以兼容性为中心的规则：纯增量能力可渐进增强；关键行为需要轻量降级，自定义降级代码原则上控制在 50 行以内，或按条件加载 polyfill；指南会记录特定限制，例如 `fetchLater()` 的 64KB 负载配额。兼容性判断以 Baseline 数据为依据。

Origin Trial 或不稳定特性的指南可以被搜索，但默认不会直接取回，需开发者明确允许。该许可可写入项目级 `.mwgrc` 或用户级 `~/.mwgrc`，也可以提交到仓库供团队共享。允许某类指南不等于消除了兼容性风险。

评测框架会生成任务、标准答案和 Playwright 评分脚本，并先验证评分脚本能通过标准答案、在未修改的基础应用上失败。随后比较 Agent 在有无指引时的表现，以机会值衡量剩余提升空间，以提升值衡量通过率变化。效果弱的指南会被裁剪或改进。

## 快速开始

可直接试用以下命令：

```bash
npx modern-web-guidance@latest search "animate a dialog modal backdrop"
npx modern-web-guidance@latest retrieve "animate-to-from-top-layer"
npx modern-web-guidance@latest legacy-scan .
```

第一条按描述搜索指南，第二条按 ID 取回指南，第三条扫描当前目录中的旧式写法。

交互式安装与更新：

```bash
npx modern-web-guidance@latest install
npx modern-web-guidance@latest update
```

安装后，Agent 会在相关任务中启用 `modern-web-guidance` Skill，并按指南要求调用 CLI。项目也提供 Vercel Skills CLI、GitHub CLI、OpenAI Codex、Claude Code、GitHub Copilot CLI 等安装入口。

如需启用受门控的指南，可执行：

```bash
npx modern-web-guidance@latest set-allow-origin-trials
npx modern-web-guidance@latest set-allow-volatile-features
```

关闭匿名遥测使用环境变量 `DISABLE_TELEMETRY=1`，不涉及任何密钥配置。

## 适用边界

指南清单不是完整 Web 平台文档，未收录的问题仍依赖模型自身能力。项目评测由内容与任务同源的团队设计，任务、评分脚本和结果都会更新，因此不能把表中提升幅度外推到其他模型、业务代码或团队。

Origin Trial 和单引擎不稳定特性需要人工判断是否启用，许可后由使用方承担相应兼容性风险。CLI 可以离线检索，不等于使用 Agent 时所有推理数据都只在本机处理；Agent 本身的数据流向仍取决于所使用工具及部署方式。

项目默认收集匿名遥测，包括安装次数、Agent 名称、被检索的指南 ID 和 Agent 生成的搜索查询，不收集用户原始提示词。公司项目采用前应核对这一行为是否符合内部合规要求。

代码采用 Apache-2.0 许可证，指南内容采用 CC-BY 4.0。README 未明确标注 beta 或 stable，使用方需要自行评估成熟度。

## 核验清单

核验时建议先区分来源事实与工程判断：

- 运行 `search`、`retrieve` 和 `legacy-scan`，确认离线检索能定位与取回指南。
- 检查 `.mwgrc` 的提交范围，确认团队共享的门控许可是否与实际项目策略一致。
- 对照项目评测文档，核对任务、模型版本、评分脚本和统计日期，不只引用提升幅度。
- 在代表性业务代码上检查指南是否覆盖实际技术栈，并单独评估兼容性与降级成本。
- 确认 `DISABLE_TELEMETRY` 是否需要启用，同时审查 Agent 工具链的数据处理方式。
- 参与贡献前确认 Node.js `>=22.18.0`、pnpm、`pnpm preflight`、Google CLA 及内容授权流程。

## 来源与核验

- [原始文章](https://juejin.cn/post/7707533858106884115)
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