---
title: "Beyond F1: Evaluating Coverage and Failure Recovery in AI Model Security Scanners"
date: 2026-08-30T14:43:08+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8742510acfe9d43c54ecee9b7caba4f19cb18c18b7329f2689c90e70b49ed885"
source_payload_sha256: "sha256:e5d2607b61cc6fe584d06c710897f75928abd84f84b1011b825170de8ddb2142"
observation_id: obs_4a0116170e17dfd5eda88d4bcfded361714860b0cb9379778c858b710bd007f8
event_id: evt_718e1385e4e266b7129cc05bcb860ed92088543c5b23a0b248cf60ea789767d1
revision_id: rev_a15efee64513c2333f7a9300104d65410c04d6cfee8a2936f8c9c01368e79cf9
source_published_at: 2026-08-27T17:49:28Z
first_seen_at: 2026-08-30T06:51:49Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 81
interpretation_sha256: "sha256:9419588e819bbbbc2c19dc09028f8e43b528d5f090fe80f006028751af771628"
description: "该研究利用合成的 Pickle 与 PyTorch 样本库，对比了 ModelScan、ModelAudit 与 Fickling 在机器学习模型安全检查中的判断覆盖率、能否给出确定性结论以及准确性，并分析了工具之间的冗余情况。"
external_url: http://arxiv.org/abs/2608.27424v1
parent_observation_id: null
last_seen_at: 2026-08-30T06:39:24.571482Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27424v1](http://arxiv.org/abs/2608.27424v1)
- **发布域名**: arxiv.org
- **分类**: cs.CR
- **作者**: Qianlong Lan、Vinothini Pandurangan、Anuj Kaul 等

## 要点解读

### 这是什么
该研究利用合成的 Pickle 与 PyTorch 样本库，对比了 ModelScan、ModelAudit 与 Fickling 在机器学习模型安全检查中的判断覆盖率、能否给出确定性结论以及准确性，并分析了工具之间的冗余情况。

### 用在哪里
适用于在机器学习部署流程中需要挑选或评估静态安全扫描工具的团队，也适合对现有扫描方案进行基准测试和冗余分析的安全研究人员。

### 可以推断的
推测：在实际项目中，仅依赖单一工具的覆盖率可能遗漏部分恶意模型的风险。  
推测：工具组合使用可以在覆盖率上互补，尤其在某些工具分析失败时，其他工具仍可能提供可靠的检测结果。

## 来源摘要/节选

> Static scanners are increasingly used to identify executable or otherwise unsafe content in machine- learning artifacts, yet conventional evaluation metrics characterize only cases where a scanner yields a usable security judgment. We evaluate ModelScan, ModelAudit, and Fickling using a controlled, artifact-backed benchmark on a synthetic corpus of 170 Pickle and PyTorch focused artifacts across 145 specimen families, 135 of which have binary security ground truth and 10 of which are intentionally malformed without labels. We explicitly distinguish non-N/A coverage, analysis completion, definitive security decisions, non-security findings, and unsupported outcomes. On labeled families, ModelAudit produced definitive security decisions for all 135 families (100%), Fickling for 110 (81.5%), and ModelScan for 67 (49.6%). Conditional on making a definitive judgment, ModelScan achieved 100% precision, recall, and F1. Fickling identified no unique true- positive families beyond those found by the combination of ModelAudit and ModelScan. Furthermore, for the 48 malicious families where ModelScan failed to complete its analysis, both ModelAudit and Fickling generated detections consistent with ground truth. These findings underscore the need to separate judgment accuracy from judgment availability, as well as incremental detection coverage from tool-level redundancy.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。