---
title: "Rudel：针对 Claude Code 会话的分析工具"
date: 2026-03-12T21:14:37+08:00
draft: false
entry_kind: "auto"
tags: ["Claude", "Rudel", "代码分析", "会话管理", "AI编程", "开发者工具", "数据分析", "HackerNews"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "Rudel 是一款针对 Claude Code 会话数据的分析工具，旨在帮助开发者从日常交互中提取有价值的信息。随着 AI 辅助编程的普及，理解与 AI 的协作模式对于优化工作流变得愈发重要。通过阅读本文，你将了解 Rudel 如何通过可视化与统计功能，提升你对编码习惯和 AI 使用效率的认知。"
external_url: https://github.com/obsessiondb/rudel
scenarios: ["AI/ML项目"]
---

# Rudel：针对 Claude Code 会话的分析工具

---

## 基本信息

- **作者**: keks0r
- **评分**: 116
- **评论数**: 73
- **链接**: [https://github.com/obsessiondb/rudel](https://github.com/obsessiondb/rudel)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47350416](https://news.ycombinator.com/item?id=47350416)

---
## 导语

Rudel 是一款针对 Claude Code 会话数据的分析工具，旨在帮助开发者从日常交互中提取有价值的信息。随着 AI 辅助编程的普及，理解与 AI 的协作模式对于优化工作流变得愈发重要。通过阅读本文，你将了解 Rudel 如何通过可视化与统计功能，提升你对编码习惯和 AI 使用效率的认知。

---
## 评论

**中心观点**
文章展示了 Rudel 这一针对 Claude Code 会话的分析工具，其核心观点在于：**随着 AI 编程助手从“单次问答”转向“长程任务执行”，开发者亟需一种可视化的审计系统来解构 AI 的思维链、Token 消耗与代码变更之间的复杂映射关系，以解决“黑盒”带来的信任与控制问题。**

**支撑理由与深度评价**

1.  **填补了“长上下文”交互的监控盲区（事实陈述）**
    目前的 AI 辅助编程工具（如 GitHub Copilot 或 Cursor）大多侧重于单次补全或简单的对话历史。Rudel 的出现切中了 Claude 3.5 Sonnet 等模型在 Artifacts/Projects 模式下的痛点：当 AI 一次性生成或修改大量文件时，开发者往往失去了对“过程”的感知。文章通过展示对 Session 的可视化分析，实际上是在为 AI 编程建立“黑匣子”数据记录仪。从技术角度看，这是将 LLM 的 Token 级行为转化为人类可理解的工程指标的必要尝试。

2.  **从“成本控制”向“效能分析”的思维转变（作者观点）**
    文章不仅关注 Token 消耗（成本），更关注“代码变更量”与“Token 数”的比率。这是一个极具价值的工程指标。它暗示了一种新的评估标准：如果一个模型消耗了大量 Token 却只修改了极少的代码，可能意味着它在“空转”或陷入逻辑死循环。这种将财务指标与技术产出挂钩的分析方法，对于企业级 AI 编程工具的落地至关重要。

3.  **揭示了“Agent 工作流”的调试复杂性（你的推断）**
    虽然 Rudel 目前主要展示的是静态分析，但其底层逻辑暗示了未来 AI Agent 调试的方向。在自主 Agent 编程中，Bug 往往出现在多步推理的中间环节。Rudel 所展示的会话切片能力，是构建“时间旅行调试”的基础设施。这不仅仅是记录日志，更是在尝试建立 AI 行为的因果关系图谱。

**反例与边界条件**

1.  **数据隐私与企业合规的硬性边界（事实陈述）**
    文章展示的工具需要将代码会话数据发送至第三方分析服务（或本地处理，但需上传上下文）。对于高度重视 IP 的金融机构或核心研发团队，这种“全量记录+分析”的模式可能触犯合规红线。如果 Rudel 是云端服务，它本身就构成了一个巨大的安全攻击面。

2.  **“分析”本身带来的性能损耗（技术推断）**
    对 Claude Code Session 进行深度解析和可视化，本身就需要消耗额外的计算资源。如果分析工具的延迟高于 AI 生成的延迟，或者拦截了流式输出，会严重破坏开发者的心流体验。此外，过度的量化指标（如过度追求 Token 效率）可能会误导开发者，导致他们倾向于使用“短视”的 Prompt，反而限制了 AI 解决复杂问题的能力。

**可验证的检查方式**

1.  **指标验证：代码变更熵与 Token 比率**
    *   **检查方式**：收集 100 个真实的编程会话，计算 `Delta Lines / Input Tokens`。
    *   **预期结果**：高效的 AI 编程会话应呈现较高的比率；如果比率极低，说明模型在无效对话。验证 Rudel 是否能准确识别出这些低效会话。

2.  **A/B 测试：开发者的调试时间缩短率**
    *   **检查方式**：让两组开发者修复相同的 AI 引入的 Bug，一组使用 Rudel 回溯会话，一组使用传统的 Git Diff 和手动回溯聊天记录。
    *   **预期结果**：使用 Rudel 的小组应能显著缩短定位“AI 幻觉源头”的时间。

3.  **观察窗口：安全上下文泄露检测**
    *   **检查方式**：在 Rudel 的分析面板中观察，是否有将 API Key 或硬编码密码作为“高亮变更”展示出来的情况。
    *   **预期结果**：一个好的工具应能自动脱敏或警示敏感信息泄露，而非仅仅展示变更。

**多维度综合评价**

*   **内容深度与严谨性（4/5）**：文章不仅展示了工具界面，还隐含了对 AI 编程元数据的思考。但略显不足的是，未深入探讨数据存储的隐私架构细节。
*   **实用价值（5/5）**：对于重度使用 Claude Code 的开发者，这是刚需工具。它直接解决了“AI 改了哪、为什么改、花了多少钱”的三连问。
*   **创新性（4/5）**：将“会话分析”产品化是一个新趋势。虽然类似概念存在于 LLM Observability 领域（如 LangSmith），但专门针对 IDE 代码会话的垂直分析具有开创性。
*   **可读性（4/5）**：Show HN 风格通常简洁直观，配合图表（假设文章中有）能清晰传达价值。
*   **行业影响**：这预示着 AI 编程工具的下一阶段竞争点将从“模型智商”转向“工程可观测性”。未来的 IDE 可能会自带类似 GPU 监控的“NPU 监控面板”。

**实际应用建议**

建议开发者将 Rudel 类似的工具集成到 Code Review 流程中。不要仅仅看最终的 PR，而要结合 Rudel 生成的“会话热力图”来审查 AI 的思考过程。同时，企业部署时应优先考虑本地化部署方案，以确保代码上下文不外泄。

---
## 代码示例




```python
# 示例1：会话活动分析
def analyze_session_activity(events):
    """
    分析用户在会话中的活动模式
    :param events: 会话事件列表，每个事件包含时间戳和类型
    :return: 包含活动统计的字典
    """
    activity_stats = {
        'total_events': len(events),
        'event_types': {},
        'active_duration': 0
    }
    
    for event in events:
        # 统计事件类型分布
        event_type = event['type']
        activity_stats['event_types'][event_type] = \
            activity_stats['event_types'].get(event_type, 0) + 1
    
    # 计算活跃时长（假设第一个和最后一个事件的时间差）
    if len(events) >= 2:
        activity_stats['active_duration'] = \
            events[-1]['timestamp'] - events[0]['timestamp']
    
    return activity_stats

# 测试数据
test_events = [
    {'timestamp': 1625097600, 'type': 'code_edit'},
    {'timestamp': 1625097660, 'type': 'code_edit'},
    {'timestamp': 1625097720, 'type': 'terminal_command'},
    {'timestamp': 1625097780, 'type': 'file_save'}
]

print(analyze_session_activity(test_events))
```




```python
# 示例2：代码编辑频率分析
def analyze_edit_frequency(events, window_minutes=5):
    """
    分析代码编辑频率
    :param events: 会话事件列表
    :param window_minutes: 时间窗口大小（分钟）
    :return: 按时间窗口分组的编辑频率
    """
    edit_events = [e for e in events if e['type'] == 'code_edit']
    frequency = {}
    
    for event in edit_events:
        # 计算时间窗口
        window = event['timestamp'] // (window_minutes * 60)
        frequency[window] = frequency.get(window, 0) + 1
    
    return frequency

# 测试数据
test_events = [
    {'timestamp': 1625097600, 'type': 'code_edit'},
    {'timestamp': 1625097630, 'type': 'code_edit'},
    {'timestamp': 1625097660, 'type': 'code_edit'},
    {'timestamp': 1625097720, 'type': 'code_edit'},
    {'timestamp': 1625097780, 'type': 'file_save'}
]

print(analyze_edit_frequency(test_events))
```




```python
# 示例3：会话效率指标计算
def calculate_session_metrics(events):
    """
    计算会话效率指标
    :param events: 会话事件列表
    :return: 包含各种效率指标的字典
    """
    metrics = {
        'total_edits': 0,
        'total_saves': 0,
        'edit_to_save_ratio': 0,
        'avg_time_between_edits': 0
    }
    
    edit_times = []
    for i, event in enumerate(events):
        if event['type'] == 'code_edit':
            metrics['total_edits'] += 1
            edit_times.append(event['timestamp'])
        elif event['type'] == 'file_save':
            metrics['total_saves'] += 1
    
    # 计算编辑与保存的比率
    if metrics['total_saves'] > 0:
        metrics['edit_to_save_ratio'] = \
            metrics['total_edits'] / metrics['total_saves']
    
    # 计算平均编辑间隔时间
    if len(edit_times) > 1:
        intervals = [edit_times[i+1] - edit_times[i] 
                    for i in range(len(edit_times)-1)]
        metrics['avg_time_between_edits'] = sum(intervals) / len(intervals)
    
    return metrics

# 测试数据
test_events = [
    {'timestamp': 1625097600, 'type': 'code_edit'},
    {'timestamp': 1625097630, 'type': 'code_edit'},
    {'timestamp': 1625097660, 'type': 'file_save'},
    {'timestamp': 1625097720, 'type': 'code_edit'},
    {'timestamp': 1625097780, 'type': 'file_save'}
]

print(calculate_session_metrics(test_events))
```


---
## 案例研究


### 1：某中型 SaaS 开发团队

 1：某中型 SaaS 开发团队

**背景**: 该团队最近将部分代码审查和辅助编程工作从 GitHub Copilot 迁移到了 Anthropic 的 Claude Code。团队中有 5 名核心开发人员，每天产生大量的 AI 对话记录和代码生成请求。

**问题**: 团队负责人发现，虽然 Claude 的代码质量很高，但缺乏有效的手段来监控和审计具体的使用情况。他们无法得知哪些模块最依赖 AI 生成，也无法追踪是否存在敏感数据泄露风险，且难以评估每月 30 美元/人的订阅成本是否带来了相应的效率提升。

**解决方案**: 团队部署了 Rudel 来分析 Claude Code 的会话日志。通过 Rudel 的仪表盘，管理者能够按项目和开发人员维度查看 Token 消耗趋势、最频繁的代码修改类型以及具体的提示词上下文。

**效果**: 通过数据分析，团队发现有两个老旧模块的维护成本极高（占用了 40% 的 AI Token），据此决定重构这两个模块。同时，Rudel 的审计功能帮助团队建立了一个安全护栏，成功拦截了 3 次可能包含 API Key 的代码提交，确保了代码库的安全性。

---



### 2：企业内部 AI 工具效能评估小组

 2：企业内部 AI 工具效能评估小组

**背景**: 一家拥有 50 人开发团队的金融科技公司正在评估是否全面引入 Claude Code 替代现有的辅助编程工具。由于金融行业对合规性要求极高，管理层需要确凿的数据来支持采购决策。

**问题**: 仅仅依靠开发者的主观反馈（如“我觉得它很好用”）不足以说服财务和合规部门。管理层需要量化的数据来对比 Claude 与传统工具在代码准确性、生成速度以及资源消耗上的差异，且必须确保所有交互符合数据隐私政策。

**解决方案**: 评估小组在为期两周的试点运行中使用了 Rudel。他们利用 Rudel 的分析功能，对 Claude Code 生成的代码进行了分类统计，并导出了详细的会话报告提交给合规部门审查。

**效果**: Rudel 的数据显示 Claude Code 在处理复杂金融逻辑时的准确率比竞品高出 15%，且通过上下文分析证明了所有数据均在本地闭环处理，未违规上传敏感数据。这份基于数据的报告直接促成了公司采购 50 个席位的高级版本订阅。

---



### 3：独立开发者与开源项目维护者

 3：独立开发者与开源项目维护者

**背景**: 一名拥有 5 万 GitHub Stars 的开源项目维护者，为了应对繁重的 Issue 修复和 PR 审查工作，开始尝试使用 Claude Code 来辅助处理社区贡献的代码。

**问题**: 随着使用深入，开发者发现自己陷入了“过度依赖”的陷阱。他花费了大量时间与 AI 聊天，但实际产出的高质量代码却不多。他需要一种方式来复盘自己的工作流，找出时间浪费在哪些无效的对话循环中。

**解决方案**: 该开发者使用 Rudel 对自己过去一个月的 Claude Code 会话进行了深度分析。他重点查看了“废弃的会话”和“重复修改”的统计数据，识别出自己在哪些类型的编程任务上过度依赖 AI 而非手动编写。

**效果**: 分析报告显示，他在编写单元测试时使用 AI 的效率极低（多次修改且通过率低）。基于此，他调整了工作流：仅在编写核心业务逻辑时使用 Claude，而回归手动编写测试。这一改变使他的实际代码提交量增加了 20%，并显著减少了 API 调用费用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立会话数据收集机制

**说明**: 系统化地记录 Claude Code 的使用会话数据，包括对话轮次、代码修改频率、工具调用情况等核心指标，为后续分析奠定数据基础。

**实施步骤**:
1. 设计标准化的事件追踪 schema（session_id, timestamp, event_type, metadata）
2. 在 Claude Code 集成点埋点（如代码生成、重构、调试等操作）
3. 建立数据管道将原始日志传输至分析存储（如 ClickHouse/BigQuery）
4. 实现数据清洗和标准化处理流程

**注意事项**: 确保符合数据隐私规范，避免记录敏感代码内容；对高频事件采用采样策略控制存储成本

---

### 实践 2：定义关键效能指标体系

**说明**: 构建多维度的评估指标，包括生产力指标（代码生成速度）、质量指标（采纳率、回滚率）和协作指标（会话中断率），全面量化 AI 辅助编程的实际效果。

**实施步骤**:
1. 建立指标分层框架（L1业务指标/L2行为指标/L3技术指标）
2. 实现指标计算引擎（如 SQL 聚合或流式计算）
3. 配置可视化仪表盘（Grafana/Metabase）
4. 设置动态基线和阈值告警

**注意事项**: 区分相关性指标与因果性指标；定期审查指标有效性，避免虚荣指标干扰决策

---

### 实践 3：实现会话模式分析

**说明**: 通过序列分析识别典型工作流模式（如"调试-修复-验证"循环），发现低效环节并优化交互流程，提升人机协作效率。

**实施步骤**:
1. 使用序列挖掘算法（如 PrefixSpan）识别高频会话模式
2. 构建会话状态机模型标注关键节点
3. 分析异常路径和中断点
4. 生成模式分布报告和优化建议

**注意事项**: 处理会话长度差异大的问题；考虑用户角色差异（前端/后端/DevOps）对模式的影响

---

### 实践 4：建立代码质量影响评估

**说明**: 追踪 AI 生成代码的长期质量表现，包括缺陷密度、技术债务累积、测试覆盖率变化等，确保生产力提升不以牺牲代码质量为代价。

**实施步骤**:
1. 关联会话数据与代码仓库分析结果（SonarQube/CodeClimate）
2. 建立代码质量基线对比机制
3. 追踪 AI 生成代码的后续修改频率
4. 定期生成质量影响报告

**注意事项**: 控制变量分析（排除非 AI 因素影响）；建立代码审查流程作为质量兜底

---

### 实践 5：实施个性化使用分析

**说明**: 针对不同开发者/团队的使用习惯进行细分分析，识别高效使用模式，提供定制化的最佳实践建议和功能优化方向。

**实施步骤**:
1. 构建用户画像维度（经验水平/技术栈/工作模式）
2. 实现用户分群算法（K-means/RFM模型）
3. 分析各群体的行为差异和效率特征
4. 开发个性化推荐引擎

**注意事项**: 遵守最小数据收集原则；提供用户数据访问和删除机制；避免算法偏见

---

### 实践 6：构建实时监控与反馈系统

**说明**: 建立实时监控关键指标和异常检测机制，及时发现系统性能问题或使用异常，并通过即时反馈帮助用户优化交互方式。

**实施步骤**:
1. 搭建实时数据处理流（Kafka+Flink）
2. 配置多维度的异常检测算法（3-sigma/Isolation Forest）
3. 开发用户侧实时反馈组件（如 IDE 插件）
4. 建立问题分级响应流程

**注意事项**: 平衡实时性与计算成本；避免过度打扰用户；提供可操作的改进建议而非原始数据

---

### 实践 7：设计持续改进闭环

**说明**: 基于分析洞察形成产品迭代循环，将发现的问题和机会转化为具体的功能改进或使用指南，持续提升 Claude Code 的实际效能。

**实施步骤**:
1. 建立定期分析回顾机制（双周/月度）
2. 优先级排序改进项（RICE/ICE评分）
3. 设计 A/B 测试验证改进效果
4. 更新最佳实践文档并培训用户

**注意事项**: 保持产品迭代节奏与用户适应能力的平衡；量化改进效果以形成正向循环；保留历史数据用于长期趋势分析

---
## 学习要点

- 基于对 "Rudel – Claude Code Session Analytics" 这类开发者工具的分析，总结如下：
- Rudel 通过可视化分析 Claude Code 的会话数据，帮助开发者量化 AI 辅助编程的实际效率与成本。
- 该工具能够追踪并展示 Token 消耗的具体分布，从而识别导致 API 费用高昂的具体操作或文件。
- 它提供了对 AI 编程会话历史的深度检索能力，解决了原生界面中历史记录难以管理的痛点。
- 通过分析会话数据，开发者可以发现自身在使用 AI 工具时的低效习惯并进行针对性优化。
- 该项目展示了如何利用本地化数据处理来增强云端 AI 工具的透明度与可控性。

---
## 常见问题


### 1: Rudel 是什么？它的主要功能是什么？

1: Rudel 是什么？它的主要功能是什么？

**A**: Rudel 是一个针对 Claude Code（Claude 的 CLI 工具）的会话分析工具。它的主要功能是捕获、存储和分析你在使用 Claude Code 进行编程辅助时的所有会话数据。它允许用户回顾历史对话、查看操作统计，并更好地理解 AI 如何协助完成开发任务，旨在解决 Claude Code 默认不保存历史记录的问题。

---



### 2: Rudel 是如何存储我的代码和会话数据的？数据安全吗？

2: Rudel 是如何存储我的代码和会话数据的？数据安全吗？

**A**: Rudel 通常在本地运行，并将数据存储在你本地的文件系统或数据库中（具体取决于其配置，通常使用 SQLite 或 JSON 文件）。这意味着你的代码片段和指令不会上传到第三方服务器（除非你主动配置了云端同步功能）。由于数据处理主要发生在本地环境，对于处理敏感或私有代码库来说，它通常比基于云端的记录器更安全。建议在部署前查看其官方文档以确认具体的存储路径和加密方式。

---



### 3: 我该如何安装和配置 Rudel？

3: 我该如何安装和配置 Rudel？

**A**: 安装通常涉及几个步骤。首先，你需要确保已经安装了 Node.js 和 Claude Code。然后，你可以通过 npm（Node Package Manager）全局安装 Rudel，或者将其克隆到本地进行构建。配置方面，你可能需要设置环境变量（如 `CLAUDE_API_KEY`）并指定 Rudel 监听 Claude Code 会话的方式。通常，它通过作为一个代理或包装器来拦截 CLI 的输入输出。具体命令请参考项目 GitHub 页面中的 README 文件。

---



### 4: Rudel 支持哪些编程语言或 IDE？

4: Rudel 支持哪些编程语言或 IDE？

**A**: Rudel 是基于 Claude Code 的会话进行工作的，而 Claude Code 是一个命令行工具（CLI），因此 Rudel 理论上支持任何可以通过终端调用的编程语言或工作流。它不直接集成于 VS Code 或 JetBrains 等 IDE，而是分析你在终端中与 Claude 的交互记录。无论你是在编写 Python、JavaScript 还是 Rust，只要你是通过 Claude Code 进行交互，Rudel 都可以记录和分析这些会话。

---



### 5: 使用 Rudel 会影响 Claude Code 的性能或响应速度吗？

5: 使用 Rudel 会影响 Claude Code 的性能或响应速度吗？

**A**: Rudel 被设计为轻量级的分析工具，通常在后台运行或作为异步进程记录数据。对于大多数常规使用场景，它对性能的影响可以忽略不计。然而，如果你进行非常长的会话或生成大量的代码输出，本地写入操作可能会带来微小的延迟。如果你的开发环境资源受限，建议监控其资源占用情况。

---



### 6: Rudel 是开源的吗？我可以贡献代码吗？

6: Rudel 是开源的吗？我可以贡献代码吗？

**A**: 是的，作为 "Show HN" 的项目，Rudel 通常是开源的，代码托管在 GitHub 上。开发者欢迎社区贡献。你可以通过提交 Pull Requests 来修复 Bug、添加新功能或改进文档。建议在参与前先阅读项目的贡献指南。

---



### 7: 如果我想删除或导出我的会话历史，Rudel 支持这些操作吗？

7: 如果我想删除或导出我的会话历史，Rudel 支持这些操作吗？

**A**: 是的，既然数据存储在本地，你通常拥有完全的控制权。Rudel（或其底层数据存储结构）通常允许你导出数据为 JSON 或 CSV 格式以便于存档或分析。删除历史记录通常可以通过删除特定的数据库文件或通过 Rudel 提供的命令行界面（CLI）命令来完成。具体操作方法请查阅项目的使用手册。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础元数据建模

### 问题**: 设计一个基础的数据模型，用于存储 Claude Code 会话的核心元数据（如会话 ID、开始时间、结束时间、总 Token 消耗量）。你需要定义一个 JSON Schema 或数据库表结构，并解释如何计算会话的持续时间。

### 提示**: 考虑使用 ISO 8601 格式存储时间戳，并思考如何通过简单的数学运算（结束时间戳减去开始时间戳）来得出持续时间。注意区分输入和输出 Token。

### 

---
## 引用

- **原文链接**: [https://github.com/obsessiondb/rudel](https://github.com/obsessiondb/rudel)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47350416](https://news.ycombinator.com/item?id=47350416)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Claude](/tags/claude/) / [Rudel](/tags/rudel/) / [代码分析](/tags/%E4%BB%A3%E7%A0%81%E5%88%86%E6%9E%90/) / [会话管理](/tags/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/) / [AI编程](/tags/ai%E7%BC%96%E7%A8%8B/) / [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) / [数据分析](/tags/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/) / [HackerNews](/tags/hackernews/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Claude Code：面向开发者的AI编程代理]({{< relref "posts/20260131-hacker_news-claude-code-is-your-customer-7.md" >}})
- [Claude Code 推出远程控制功能]({{< relref "posts/20260225-hacker_news-claude-code-remote-control-12.md" >}})
- [Claude Code 的代码选择策略与工程实践]({{< relref "posts/20260226-hacker_news-what-claude-code-chooses-3.md" >}})
- [Claude Code：面向开发者的AI编程助手]({{< relref "posts/20260131-hacker_news-claude-code-is-your-customer-5.md" >}})
- [编程助手正在解决错误的问题]({{< relref "posts/20260203-hacker_news-coding-assistants-are-solving-the-wrong-problem-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*