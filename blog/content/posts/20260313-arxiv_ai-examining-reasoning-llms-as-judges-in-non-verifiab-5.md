---
title: Examining Reasoning LLMs-as-Judges in Non-Verifiable LLM Post-Training
date: 2026-03-13 23:24:24+08:00
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
external_url: https://arxiv.org/abs/2603.12246v1
aliases:
- /posts/20260314-arxiv_ai-examining-reasoning-llms-as-judges-in-non-verifiab-5/
- /posts/20260315-arxiv_ai-examining-reasoning-llms-as-judges-in-non-verifiab-5/
- /posts/20260316-arxiv_ai-examining-reasoning-llms-as-judges-in-non-verifiab-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ae322790e3058151d092a0a17b13d846ef683b0fc8c8fa7e535baa7a4ad73484
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:28:07.966279Z'
source_capture_sha256: sha256:a62d7bf225014413fb320550b2db2d930e2c147e5f7f6faa87eac2b2afdccd40
source_capture_chars_original: 1380
source_publication_excerpt_chars: 1380
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12246v1](<https://arxiv.org/abs/2603.12246v1>)
- **作者**: Yixin Liu, Yue Yu, DiJia Su, Sid Wang, Xuewei Wang, Song Jiang, Bo Liu, Arman Cohan, Yuandong Tian, Zhengxing Chen
- **分类**: cs.AI
- **论文时间**: 2026-03-12T17:57:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12246v1.pdf](<https://arxiv.org/pdf/2603.12246v1.pdf>)

## 来源摘要/节选

> Reasoning LLMs-as-Judges, which can benefit from inference-time scaling, provide a promising path for extending the success of reasoning models to non-verifiable domains where the output correctness/quality cannot be directly checked. However, while reasoning judges have shown better performance on static evaluation benchmarks, their effectiveness in actual policy training has not been systematically examined. Therefore, we conduct a rigorous study to investigate the actual impact of non-reasoning and reasoning judges in reinforcement-learning-based LLM alignment. Our controlled synthetic setting, where a "gold-standard" judge \(gpt-oss-120b\) provides preference annotations to train smaller judges, reveals key differences between non-reasoning and reasoning judges: non-reasoning judges lead to reward hacking easily, while reasoning judges can lead to policies that achieve strong performance when evaluated by the gold-standard judge. Interestingly, we find that the reasoning-judge-trained policies achieve such strong performance by learning to generate highly effective adversarial outputs that can also score well on popular benchmarks such as Arena-Hard by deceiving other LLM-judges. Combined with our further analysis, our study highlights both important findings and room for improvements for applying \(reasoning\) LLM-judges in non-verifiable LLM post-training.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
