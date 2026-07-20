---
title: Conformal Policy Control
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02196v1
aliases:
- /posts/20260304-arxiv_ai-conformal-policy-control-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f76a74095d1ee91be558e98bb70de7dbe58c4139de3d93e057c6969023b3d991
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 24
captured_at: '2026-07-18T04:26:23.368833Z'
source_capture_sha256: sha256:c4380a1c8eb098bd383cc0c4220c127b8373dec89111300c7cb7fe12c896ef7f
source_capture_chars_original: 1101
source_publication_excerpt_chars: 1101
observation_id: obs_162d0c6a2661d5c7387f67fd86d7b1ff0624e37c916c84e440b4f46ceb2df7ff
revision_id: rev_eb74d35f504ea4e5e2e327b4996b74f3f08be727433295385f85082994749260
event_id: evt_1f9f821d33549139959dce1c17123fab691db24ed5857aaafa8d7cd4d99267da
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02196v1](<https://arxiv.org/abs/2603.02196v1>)
- **作者**: Drew Prinster, Clara Fannjiang, Ji Won Park, Kyunghyun Cho, Anqi Liu, Suchi Saria, Samuel Stanton
- **分类**: cs.AI
- **论文时间**: 2026-03-02T18:54:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02196v1.pdf](<https://arxiv.org/pdf/2603.02196v1.pdf>)

## 来源摘要/节选

> An agent must try new behaviors to explore and improve. In high-stakes environments, an agent that violates safety constraints may cause harm and must be taken offline, curtailing any future interaction. Imitating old behavior is safe, but excessive conservatism discourages exploration. How much behavior change is too much? We show how to use any safe reference policy as a probabilistic regulator for any optimized but untested policy. Conformal calibration on data from the safe policy determines how aggressively the new policy can act, while provably enforcing the user's declared risk tolerance. Unlike conservative optimization methods, we do not assume the user has identified the correct model class nor tuned any hyperparameters. Unlike previous conformal methods, our theory provides finite-sample guarantees even for non-monotonic bounded constraint functions. Our experiments on applications ranging from natural language question answering to biomolecular engineering show that safe exploration is not only possible from the first moment of deployment, but can also improve performance.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
