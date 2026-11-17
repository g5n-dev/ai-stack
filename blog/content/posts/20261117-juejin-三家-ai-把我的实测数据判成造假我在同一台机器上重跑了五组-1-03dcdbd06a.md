---
title: "三家 AI 把我的实测数据判成造假，我在同一台机器上重跑了五组"
date: 2026-11-17T11:53:45+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:462733aea958fdfcabfcd231af1147d2a257512b159aed6f900c7c2be781a2dc"
source_payload_sha256: "sha256:67fca4c13a288167f2c9e61a3d09979e807bf82e69adf61128702fbb3283054c"
source_published_at: 2026-11-16T15:52:56Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:406a0df17fbe5051a4890de8befe8cc8061967ca20eea2f71315185b0ff9e961"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 31
description: "核心结论 来源在 9.13.12、同一台机器上以冷进程重跑了 AI 提出的六项质疑，结果均能复现：百万位数据的 文件为 250000 字节，内存统计为 4132 字节，回读耗时约 9.6～9.7 秒； 未改变相关状态； 拒绝 bytes； 仅能从 导入。"
external_url: https://juejin.cn/post/7708682938187743270
observation_id: obs_03dcdbd06a23e57d869aa4d487dc0bc2830e1e7123acdba6f79f4e8d7a1aee76
revision_id: rev_bc340e1cf1e26c0d116ace55f3f540252e5839bd361d73cf55781d05d9d4a171
event_id: evt_89585abd3f4bc8d3cf4040a8521f99cce2a4bbb8ae0fa8f06cc67d632dcf5c4b
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-11-17T03:51:19.902935Z
last_seen_at: 2026-11-17T03:53:45Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 贝壳690
- **原始来源**: [https://juejin.cn/post/7708682938187743270](https://juejin.cn/post/7708682938187743270)
- **原文发布时间**: Mon, 16 Nov 2026 15:52:56 GMT

## 核心结论

来源在 `bool-hybrid-array` 9.13.12、同一台机器上以冷进程重跑了 AI 提出的六项质疑，结果均能复现：百万位数据的 `.bha` 文件为 250000 字节，内存统计为 4132 字节，回读耗时约 9.6～9.7 秒；`optimize()` 未改变相关状态；`cjx.encode` 拒绝 bytes；`GPU_opt` 仅能从 `core` 导入。

这些数字说明内存中的稀疏索引与磁盘上的位图格式是两种不同表示：`.bha` 按位图存储，落盘大小遵循 `ceil(N/4)`，不因 True 稀疏而缩小。`optimize()` 在当前版本中也没有表现出 README 所述的自动优化效果。

另有两条重要边界：小尺寸样本可能出现文件头未对齐、读回对象类型不符；GPU 功能因缺少可用 CUDA 与 cupy 环境，来源没有给出任何性能结论。

## 能力机制

`forest` 根据运行时 `sys.path` 动态枚举可导入模块，而不是维护固定依赖表。可见名称多数是 `LazyImport` 代理，星号导入只写入代理，首次访问才解析并导入模块。本轮测得 654 个可见名称，其中 643 个代理；另一轮为 664/568，说明数量会随已安装包、工作目录和路径变化。已安装的 numpy 等模块可直接使用，未安装的 jieba 在访问时抛出 `NameError`。

`cjx` 面向纯文本，接口严格要求 `encode` 接收 str、`decode` 接收 bytes，不进行隐式类型转换。六组往返测试均通过，但压缩体积普遍大于 zlib；空串输入返回 0 字节，而 zlib 产生 8 字节头。来源据此认为其文本专用性明确，但当前样本不足以支持替代 zlib。

`GPU_opt` 的实际名称与 README 中的 `GPU_obt` 不一致，并且没有从包顶层导出。调用依赖 cupy 后端；来源环境未安装 cupy，调用在 Cython 的 numpy 初始化阶段触发 `ImportError`。

## 快速开始

以下仅列出来源已确认的调用方式，不包含未经提供的安装命令。

```python
from bool_hybrid_array import *

a = BoolHybridArr([i % 1000 == 0 for i in range(1000000)])
print(a.memory_usage(detail=True)["总占用(字节)"])
```

按来源的落盘流程生成文件后，可检查文件大小：

```python
import os
print(os.path.getsize("b1.bha"))
```

检查惰性导入及名称解析：

```python
from bool_hybrid_array.forest import *
import bool_hybrid_array.forest as F

names = [n for n in dir(F) if not n.startswith("__")]
print(len(names))
print(sum(
    1 for n in names
    if type(getattr(F, n)).__name__ == "LazyImport"
))
```

验证文本压缩往返：

```python
x = cjx.encode("Hello CJX！" * 100)
print(len(x))
print(cjx.decode(x)[:15])
```

定位 GPU 入口：

```python
from bool_hybrid_array.core import GPU_opt
GPU_opt()
```

最后一条在来源环境中会因缺少 cupy 报错，不应将其视为性能测试步骤。

## 适用边界

来源事实表明，`.bha` 的存储估算应基于位长度而非稀疏比例；100 位、1000 位和 3000000 位分别对应 25、250 和 750000 字节。内存统计则反映运行时结构，不能直接用于推算文件大小。

`optimize()` 的结果应通过前后对比确认。来源构造了一万条、每百条一个 True 的稀疏数据，调用前后 `repr` 相同，总占用均为 532 字节，“是否需要优化”均为“是”，与 README 描述不一致。

工程上，若输入包含日志、缓存键或配置片段中的 bytes，需要先确认其文本编码再调用 `cjx`；这是对严格接口约束的适配，不代表库会自行转换类型。使用 `forest` 时也不应把名称总数写成稳定常量。GPU 加速则必须单独验证 cupy、CUDA 与后端加载情况。

## 核验清单

1. 冷进程执行，避免复用先前构造的对象。
2. 构造百万位稀疏数据，确认内存统计为 4132 字节，其中密集区 96、稀疏区 4036。
3. 完成来源中的落盘流程后，用 `os.path.getsize` 确认 `b1.bha` 为 250000 字节。
4. 扫描长度 1 至 300 万的多个样本，核对文件大小是否严格符合 `ceil(n/4)`。
5. 对稀疏数据分别打印 `repr` 与 `memory_usage(detail=True)`，再比较 `optimize()` 前后的状态。
6. 分别向 `cjx.encode` 和 `cjx.decode` 传入错误类型，确认异常及类型信息。
7. 统计 `forest` 的可见名称与 `LazyImport` 数量，并结合 `sys.path` 和已安装包解释差异。
8. 检查包顶层是否存在 `GPU_opt`，并从 `bool_hybrid_array.core` 导入；缺少 cupy 时只记录导入错误，不推断加速幅度。

## 来源与核验

- [原始文章](https://juejin.cn/post/7708682938187743270)
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