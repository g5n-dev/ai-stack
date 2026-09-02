---
title: "Auditing Anonymous AI Models: A Four-Stage Protocol for Black-Box Identity Verification"
date: 2026-09-01T13:10:01+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:45e93f6b2a83ca951cf93190cad42a6be28249b4b879b25e9b0e8a1527a6e652"
source_payload_sha256: "sha256:04dcd1d7520ea1f75cca355039bd32de4933bed31aacbc1b4e545ab1adaac18f"
observation_id: obs_742dcdeb829acd52e055ac07bfdc95ff80e3826977ae1518ae02e957b1f60df2
event_id: evt_8241e8d2de066db8b415da7a227723b8e6782f69752ec51932f6c4a86846e55f
revision_id: rev_2f19d71e33403eb2afc810671ce6539e8b4338b7f6df7f4965f4104a4f59b341
source_published_at: 2026-08-31T17:48:24Z
first_seen_at: 2026-09-01T05:20:18Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:b3cb8d51048c4b7a0a940ceaa0fc80fea8da7e1f5d52c2e1cd876f6c8e445f1f"
description: "该内容提出一种四阶段黑盒审计协议，用于验证匿名模型的真实身份，通过平台快照回溯、配置指纹匹配、词汇器差异测试和行为探测四个步骤来判断模型是否与声明一致。"
external_url: http://arxiv.org/abs/2608.31142v1
parent_observation_id: null
last_seen_at: 2026-09-02T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.31142v1](http://arxiv.org/abs/2608.31142v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Yisen Xi

## 要点解读

### 这是什么
该内容提出一种四阶段黑盒审计协议，用于验证匿名模型的真实身份，通过平台快照回溯、配置指纹匹配、词汇器差异测试和行为探测四个步骤来判断模型是否与声明一致。

### 用在哪里
适用于模型发布平台内部审查、第三方合规审计以及需要确认匿名模型来源可信度的开发者与安全团队，尤其在模型以代号发布且缺少公开文档的情况下。

### 可以推断的
推测：随着模型发布渠道多样化，平台和监管方对匿名模型的身份验证需求将进一步增长。  
推测：协议采用仅依赖标准库的实现方式，说明其部署门槛低，易于在不同环境中复现和集成。

## 来源摘要/节选

> The 2025--2026 AI market has seen a wave of stealth releases: frontier models launched anonymously on developer platforms under codenames. For their users, identity determines data-handling terms, supply-chain risk, and capability expectations. No validated methodology exists for black-box identity verification of anonymous models: practitioner checklists lack accuracy evidence, and self-identification is untrustworthy by design. We propose a four-stage forensic audit protocol for API-served models. Stage 0 reconstructs launch-time configuration from archived platform snapshots (Internet Archive), exposing preview--production drift. Stage 1 fingerprints configuration (context, output ceiling, reasoning, modality) against the platform catalog. Stage 2 tests tokenizer identity with a cross-length differential that rejects short-prompt collisions. Stage 3 corroborates with behavioral probes. We test declaration consistency on 10 known-identity releases (7 exact, 2 precision-differences, 1 partial, 0 counter-directional), not end-to-end identification under anonymity. Identification is validated prospectively on a flagship case whose 2026-08-23 analysis pointed to the GLM-5.3 version line and whose official reveal confirmed those family and version-line inferences (deployment variant was not pre-asserted; Flash was consistent post-reveal), and on three Stage-0-only cases where the protocol produced a graded hypothesis or declined rather than guessed. A standard-library-only implementation is provided as supplementary material.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。