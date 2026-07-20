---
title: Large Language Models Generate Harmful Content Using a Distinct, Unified Mechanism
date: 2026-04-13 23:58:28+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2604.09544v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8ceac493ca20a21e1ad49403662a8fca42bb19d1850186828583380bcb6825a8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:29:12.103286Z'
source_capture_sha256: sha256:8b80657e5b37d7cfb612fb5a7f1e768142afdf57cdf07d60d40bfa547509a03e
source_capture_chars_original: 1458
source_publication_excerpt_chars: 1458
observation_id: obs_becba6d38c6ff796db9e748cb6ea24d5c08874d5d70b49b50812cce583e04a64
revision_id: rev_17ad040464516d811bfe6d9a1bae5b8d3dad7ee1b08725a3d137916ae5852892
event_id: evt_1dceaf42bb592ba23829687e2a2ac59e5abaf9f9d55ca03d4e4fd5daf58794ac
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.09544v1](<https://arxiv.org/abs/2604.09544v1>)
- **作者**: Hadas Orgad, Boyi Wei, Kaden Zheng, Martin Wattenberg, Peter Henderson, Seraphina Goldfarb-Tarrant, Yonatan Belinkov
- **分类**: cs.CL
- **论文时间**: 2026-04-10T17:58:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.09544v1.pdf](<https://arxiv.org/pdf/2604.09544v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) undergo alignment training to avoid harmful behaviors, yet the resulting safeguards remain brittle: jailbreaks routinely bypass them, and fine-tuning on narrow domains can induce \`\`emergent misalignment'' that generalizes broadly. Whether this brittleness reflects a fundamental lack of coherent internal organization for harmfulness remains unclear. Here we use targeted weight pruning as a causal intervention to probe the internal organization of harmfulness in LLMs. We find that harmful content generation depends on a compact set of weights that are general across harm types and distinct from benign capabilities. Aligned models exhibit a greater compression of harm generation weights than unaligned counterparts, indicating that alignment reshapes harmful representations internally--despite the brittleness of safety guardrails at the surface level. This compression explains emergent misalignment: if weights of harmful capabilities are compressed, fine-tuning that engages these weights in one domain can trigger broad misalignment. Consistent with this, pruning harm generation weights in a narrow domain substantially reduces emergent misalignment. Notably, LLMs harmful generation capability is dissociated from how they recognize and explain such content. Together, these results reveal a coherent internal structure for harmfulness in LLMs that may serve as a foundation for more principled approaches to safety.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
