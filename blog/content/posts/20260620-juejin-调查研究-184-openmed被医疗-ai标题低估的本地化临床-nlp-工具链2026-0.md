---
title: 调查研究-184 OpenMed：被“医疗 AI“标题低估的本地化临床 NLP 工具链（2026）
date: 2026-06-20 09:14:01+08:00
draft: false
entry_kind: auto
tags:
- 掘金
- 自然语言处理
- Python
- Swift
categories:
- AI 工程
scenarios:
- AI/ML项目
- 自然语言处理
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7652719984766402614
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:396caef89a7eff8257c9120ac2738873694492b8aa14b2073729bb4c8611eff9
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 49
captured_at: '2026-07-18T04:21:44.073217Z'
source_capture_sha256: sha256:2d38ee26cb0d8f99451d09af966a51b15672b538a17e67e6b3e7fa250417e316
source_capture_chars_original: 4540
source_publication_excerpt_chars: 800
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
observation_id: obs_fbb66d8bce55ee60882b27ec86a029978243952ca7c1da03d6f8ed512bab0332
revision_id: rev_25e005bbffb45bbc4b95f00c97a245683696cd8e7fa4bd7aeb9cf7a0129c79cb
event_id: evt_4de91637b646e3b4ea98cd99d44113c419b33e49d07726eeac16b47d93f7f700
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-06-20T01:14:01Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: observed
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7652719984766402614](<https://juejin.cn/post/7652719984766402614>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> OpenMed 调研：被"医疗 AI"标题低估的本地化临床 NLP 工具链（2026）
> TL;DR
> 场景
> ：医疗 AI 系统接入，需要解决临床文本结构化、PII/PHI 检测、去标识化、批处理和本地部署
> 结论
> ：OpenMed 当前最有价值的不是"医疗问答"，而是医疗文本基础设施组件；定位是中间件层而非诊断层
> 产出
> ：OpenMed 能做什么/不能做什么的边界、推荐接入架构、模型加载安全规范、中文场景评估清单
> 版本矩阵
> 功能
> 状态
> 说明
> 临床 NER（疾病/药物/基因/解剖实体）
> ✅ 已验证
> v1.3.0 起跨平台，PyTorch + MLX 双后端
> PII 检测（姓名/电话/SSN/邮箱）
> ✅ 已验证
> v1.3.0（2026-04-29）Faker-backed 脱敏，PyTorch/MLX 全平台
> 多语言隐私过滤（16 语言）
> ✅ 已验证
> v1.4.0（2026-05-11）OpenMed Multilingual Privacy Filter
> Nemotron-PII 模型族
> ✅ 已验证
> v1.3.0 起新增 PyTorch/MLX artifacts
> privacy-filter trust boundary 修复
> ✅ 已验证
> v1.5.2（2026-05-27）发布，限制 trust\_remote\_code=True 触发条件
> 端侧推理 Apple Silicon MLX
> ✅ 已验证
> v1.3.0 起 MLX 8-bit/全精度版本，OpenMedKit/Swift 同源
> 中文临床病历 NER
> ⚠️ 待验证
> 官方材料未重点覆盖中文，需自建评估集
> Assertion 否定/怀疑识别
> ⚠️ 待验证
> 当前模型擅长实体抽取，否定/时态需后处理
> FHIR / ICD-10 / SNOMED CT 映射
> ❌ 暂不支持
> 需后处理层做术语标准化
> 临床决策/诊断推理
> ❌ 暂不支持…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
