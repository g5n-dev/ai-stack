---
title: Capability-Oriented Training Induced Alignment Risk
date: 2026-02-13 03:01:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI 安全
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.12124v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:60c8a07012bd4ab24e59ad8c33474fa6b40dff875c57f30f070e892b14f5cd02
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:ada7e535ae876a71203c541a304773c263321700a3d13734f4fba0601fd46f1f
source_capture_chars_original: 1492
source_publication_excerpt_chars: 1492
observation_id: obs_82e11d2c2d88d5f0d52cb175162d1534d4b04da800e78bcfc798262b9a1abd31
revision_id: rev_123bc249cf5da7f7204f2db8901bde742ff46ef95a9c8925f1451b961e6dfad3
event_id: evt_42b4c046723c0599a355ee348acebfd678e42e15fa60993bc92b3265a8cbdbb1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12124v1](<https://arxiv.org/abs/2602.12124v1>)
- **作者**: Yujun Zhou, Yue Huang, Han Bao, Kehan Guo, Zhenwen Liang, Pin-Yu Chen, Tian Gao, Werner Geyer, Nuno Moniz, Nitesh V Chawla, Xiangliang Zhang
- **分类**: cs.LG
- **论文时间**: 2026-02-12T16:13:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12124v1.pdf](<https://arxiv.org/pdf/2602.12124v1.pdf>)

## 来源摘要/节选

> While most AI alignment research focuses on preventing models from generating explicitly harmful content, a more subtle risk is emerging: capability-oriented training induced exploitation. We investigate whether language models, when trained with reinforcement learning \(RL\) in environments with implicit loopholes, will spontaneously learn to exploit these flaws to maximize their reward, even without any malicious intent in their training. To test this, we design a suite of four diverse "vulnerability games", each presenting a unique, exploitable flaw related to context-conditional compliance, proxy metrics, reward tampering, and self-evaluation. Our experiments show that models consistently learn to exploit these vulnerabilities, discovering opportunistic strategies that significantly increase their reward at the expense of task correctness or safety. More critically, we find that these exploitative strategies are not narrow "tricks" but generalizable skills; they can be transferred to new tasks and even "distilled" from a capable teacher model to other student models through data alone. Our findings reveal that capability-oriented training induced risks pose a fundamental challenge to current alignment approaches, suggesting that future AI safety work must extend beyond content moderation to rigorously auditing and securing the training environments and reward mechanisms themselves. Code is available at https://github.com/YujunZhou/Capability\_Oriented\_Alignment\_Risk.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
