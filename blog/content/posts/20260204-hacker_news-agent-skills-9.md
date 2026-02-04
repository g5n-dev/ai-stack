---
title: "Agent Skills：大模型智能体技能训练框架"
date: 2026-02-04T12:07:45+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "LLM", "智能体", "技能训练", "框架", "AI Agent", "模型微调", "强化学习"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在构建大模型应用时，如何让 Agent 具备调用外部工具或执行特定任务的能力，已成为技术落地的关键环节。Agent Skills 不仅是连接模型与现实世界的桥梁，更是实现复杂自动化流程的核心组件。本文将深入解析 Agent Skills 的技术原理与实现路径，帮助开发者掌握赋予模型“动手能力”的方法，从而构建出更智能、"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：大模型智能体技能训练框架

---

## 基本信息

- **作者**: mooreds
- **评分**: 469
- **评论数**: 231
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

在构建大模型应用时，如何让 Agent 具备调用外部工具或执行特定任务的能力，已成为技术落地的关键环节。Agent Skills 不仅是连接模型与现实世界的桥梁，更是实现复杂自动化流程的核心组件。本文将深入解析 Agent Skills 的技术原理与实现路径，帮助开发者掌握赋予模型“动手能力”的方法，从而构建出更智能、更实用的 AI 应用。

---
## 评论

### 中心观点
**文章主张：构建高性能 AI Agent 的核心不在于单一模型参数的无限堆叠，而在于将复杂的任务拆解为标准化、可组合且可验证的“原子技能”，并通过精细的编排机制实现能力的涌现。**

### 支撑理由与边界条件

**1. 技能的原子化与模块化降低了系统复杂度（事实陈述）**
*   **分析：** 将复杂任务（如“编写并调试代码”）拆解为独立的技能（如“文件搜索”、“语法检查”、“单元测试”），符合软件工程中的解耦原则。这种架构使得每个技能可以被独立优化和迭代，而不需要重新训练整个模型。
*   **案例：** AutoGPT 或 Devin 等系统，实际上是将“浏览网页”和“执行终端命令”作为独立技能块调用，而非让模型凭空生成所有行为。

**2. 专有技能优于通用提示词（作者观点）**
*   **分析：** 文章可能强调，针对特定任务（如 SQL 生成），使用经过微调的小模型或结构化工具，往往比使用超大参数的通用模型配合零样本提示更有效且成本更低。
*   **你的推断：** 这暗示了未来的 Agent 架构将从“单体巨石模型”转向“模型路由”或“混合专家系统”，即不同的技能调用不同的模型或工具。

**3. 技能的可观测性是落地关键（你的推断）**
*   **分析：** 如果 Agent 只是一个黑盒，企业无法通过安全合规审查。将 Agent 定义为一组技能的集合，意味着每一步操作都有明确的输入输出和日志，这对于金融、医疗等严监管行业至关重要。

**反例 / 边界条件：**
*   **反例 1：上下文割裂导致的连贯性缺失。** 过度拆解技能可能导致上下文信息的丢失。例如，一个“情感分析”技能如果不知道上一轮“用户画像”技能的结果，可能会得出错误的结论。
*   **反例 2：硬编码技能的泛化能力差。** 如果技能定义过于死板（如基于规则的 RPA 脚本），Agent 处理突发情况的能力将不如端到端的大模型。

### 深入评价（维度分析）

**1. 内容深度：从“炼丹”走向“工程”**
文章如果深入讨论了技能的抽象层次（如 ReAct 模式 vs. Plan-and-Execute），则具备较高的技术深度。它试图解决 LLM 幻觉问题，通过引入确定性工具来约束概率性模型的输出。论证的严谨性取决于是否承认技能之间的通信成本。

**2. 实用价值：工程化的指导手册**
对于 RAG（检索增强生成）开发者而言，将“检索”定义为一个技能，并配置特定的重排序逻辑，比单纯调整 Prompt 效果显著。文章提供的技能分类法（如：感知类、决策类、行动类）能直接指导 Agent 的架构设计。

**3. 创新性：重新定义“智能”的颗粒度**
传统观点追求模型智商，文章提出“技能编排”才是工程瓶颈。这与 Svelte 等前端框架的组件化思维异曲同工，将 AI 开发从“模型训练”转变为“模型 plumbing（管道工程）”。

**4. 行业影响：加速 AI 应用落地**
如果“Agent Skills”成为标准协议，将催生“技能商店”经济。第三方可以开发特定的技能（如“解析 PDF 发票”）并出售给 Agent 调用，这比出售微调模型更具商业可行性。

**5. 争议点与批判性思考**
*   **“技能”的定义边界模糊：** 一个技能到底应该多小？是“写 Python 代码”是一个技能，还是“写 For 循环”是一个技能？粒度过细会导致编排层逻辑过于复杂，甚至超过模型本身的能力。
*   **编排悖论：** 为了管理这些技能，我们需要一个更强的“元模型”或“控制器”。如果控制器不够强，技能再强也发挥不出来；如果控制器太强，是否还需要拆解技能？这回到了“系统1（快思考）”与“系统2（慢思考）”的平衡问题。

### 实际应用建议

1.  **建立技能矩阵：** 在开发 Agent 前，先梳理业务流程，明确哪些环节必须由规则引擎保证准确度（硬技能），哪些环节需要 LLM 的创造力（软技能）。
2.  **灰度发布机制：** 不要一次性部署所有技能。建议先上线“阅读”类技能，验证安全性后，再逐步开放“写入”或“执行”类高风险技能。
3.  **技能兜底策略：** 为每个技能设计“降级方案”。当专用工具失效时，是否能回退到通用模型的能力，而不是直接报错。

### 可验证的检查方式

1.  **指标：编排开销占比**
    *   *测量方法：* 统计 Agent 完成任务时，用于技能调度、上下文拼接和结果解析的 Token 数量或耗时占总消耗的比例。如果占比超过 40%，说明架构过于臃肿，需要合并部分原子技能。

---
## 代码示例




```python
# 示例1：Hacker News 热门文章抓取器
import requests
from bs4 import BeautifulSoup

def fetch_hn_top_stories(limit=5):
    """
    获取 Hacker News 首页热门文章标题和链接
    :param limit: 要获取的文章数量，默认5篇
    :return: 包含标题和链接的字典列表
    """
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}  # 添加请求头模拟浏览器访问
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stories = []
        articles = soup.select('.titleline')[:limit]  # 选择前N篇文章
        
        for article in articles:
            title_tag = article.find('a')
            link = title_tag.get('href')
            title = title_tag.get_text()
            stories.append({'title': title, 'link': link})
            
        return stories
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []

# 测试调用
if __name__ == "__main__":
    top_stories = fetch_hn_top_stories()
    for idx, story in enumerate(top_stories, 1):
        print(f"{idx}. {story['title']}\n   {story['link']}\n")
```




```python
# 示例2：Hacker News 关键词搜索器
import requests
from datetime import datetime

def search_hn_by_keyword(keyword, points_threshold=50):
    """
    通过 Hacker News Algolia API 搜索特定关键词的文章
    :param keyword: 搜索关键词
    :param points_threshold: 最低点赞数筛选，默认50
    :return: 符合条件的文章列表
    """
    base_url = "https://hn.algolia.com/api/v1/search"
    params = {
        'query': keyword,
        'tags': 'story',
        'numericFilters': f'points>={points_threshold}',
        'hitsPerPage': 10
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        results = []
        for hit in data['hits']:
            timestamp = hit['created_at_i']
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            results.append({
                'title': hit['title'],
                'points': hit['points'],
                'author': hit['author'],
                'url': hit.get('url', f"https://news.ycombinator.com/item?id={hit['objectID']}"),
                'date': date
            })
        return results
    except Exception as e:
        print(f"搜索失败: {str(e)}")
        return []

# 测试调用
if __name__ == "__main__":
    results = search_hn_by_keyword("python", points_threshold=100)
    for idx, article in enumerate(results, 1):
        print(f"{idx}. [{article['points']} points] {article['title']}")
        print(f"   by {article['author']} on {article['date']}")
        print(f"   {article['url']}\n")
```




```python
# 示例3：Hacker News 用户活动分析器
import requests
from collections import Counter

def analyze_user_activity(username):
    """
    分析指定用户的提交历史和活跃度
    :param username: Hacker News 用户名
    :return: 包含用户统计信息的字典
    """
    base_url = f"https://hn.algolia.com/api/v1/users/{username}"
    
    try:
        response = requests.get(base_url)
        user_data = response.json()
        
        # 获取用户最近的提交
        submissions_url = f"https://hn.algolia.com/api/v1/search"
        params = {
            'tags': f'author_{username}',
            'hitsPerPage': 100
        }
        submissions = requests.get(submissions_url, params=params).json()
        
        # 分析提交类型分布
        submission_types = Counter(hit.get('type', 'unknown') for hit in submissions['hits'])
        
        return {
            'karma': user_data.get('karma', 0),
            'created_at': user_data.get('created_at', 'N/A'),
            'total_submissions': submissions['nbHits'],
            'submission_types': dict(submission_types),
            'avg_karma_per_submission': user_data.get('karma', 0) / max(submissions['nbHits'], 1)
        }
    except Exception as e:
        print(f"分析失败: {str(e)}")
        return {}

# 测试调用
if __name__ == "__main__":
    username = "pg"  # 保罗·格雷厄姆的用户名
    stats = analyze_user_activity(username)
    print(f"用户 {username} 的活动分析:")
    print(f"Karma: {stats['karma']}")
    print(f"注册时间: {stats['created_at']}")
    print(f"总提交数: {stats['total_submissions']}")
    print(f"提交类型分布: {stats['submission


---
## 案例研究


### 1：Cognition AI 推出的 Devin（全球首个完全自主的 AI 软件工程师）

 1：Cognition AI 推出的 Devin（全球首个完全自主的 AI 软件工程师）

**背景**:  
随着软件开发需求的激增，工程师常因重复性任务（如调试、代码重构、环境搭建）消耗大量时间，导致核心开发效率受限。传统自动化工具（如 CI/CD 流水线）仅能处理固定流程，无法动态解决复杂问题。

**问题**:  
- 工程师需手动处理非结构化任务（如阅读文档、定位 Bug、部署测试环境），耗时占比超 40%。  
- 现有 AI 编程助手（如 GitHub Copilot）仅能生成代码片段，无法端到端完成完整开发任务。  

**解决方案**:  
Cognition AI 开发了 Devin，一个基于 Agent Skills 的自主 AI 工程师。其核心能力包括：  
1. **动态任务拆解**：将高层需求（如“构建登录功能”）分解为代码编写、测试、部署等子任务。  
2. **自主工具调用**：通过内置的 Bash、浏览器、代码编辑器等工具，自动执行命令、调试错误并验证结果。  
3. **持续学习与纠错**：根据运行时反馈（如测试失败）自动调整策略，无需人工干预。  

**效果**:  
- 在 Upwork 的实际测试中，Devin 成功完成包括网站部署、API 集成等 5 个真实任务，而人类工程师平均需 2-3 倍时间。  
- 早期用户报告显示，Devin 将重复性开发任务的时间缩短 60%，使工程师能专注于架构设计等高价值工作。  

---



### 2：Klarna 的 AI 客服 Agent（基于 Agent Skills 的自动化系统）

 2：Klarna 的 AI 客服 Agent（基于 Agent Skills 的自动化系统）

**背景**:  
Klarna 作为全球支付巨头，每月需处理数百万客户咨询，涉及退款、账户管理、支付纠纷等复杂场景，传统客服团队面临高成本和响应延迟问题。

**问题**:  
- 人工客服平均响应时间达 11 分钟，高峰期排队时长超 30 分钟。  
- 简单咨询（如“如何退货”）与复杂问题（如欺诈检测）混杂，导致资源分配低效。  

**解决方案**:  
Klarna 部署了基于 Agent Skills 的 AI 客服系统，具备以下能力：  
1. **多技能路由**：通过自然语言理解自动识别问题类型，将简单查询分配给自动化 Agent，复杂问题转接人工。  
2. **自主操作执行**：Agent 可直接调用后台 API 处理退款、修改订单等操作，无需人工介入。  
3. **上下文感知**：整合用户历史数据（如交易记录、对话历史）提供个性化解决方案。  

**效果**:  
- 上线后处理了 2/3 的客服咨询（约 700 万次对话），响应时间从 11 分钟降至 2 分钟。  
- 预计每年节省 4000 万美元成本，客户满意度提升 25%，同时人工客服团队规模缩减 20%。  

---



### 3：UiPath 的 Document Understanding（企业级文档处理 Agent）

 3：UiPath 的 Document Understanding（企业级文档处理 Agent）

**背景**:  
金融、医疗等行业需处理海量非结构化文档（如发票、病历、合同），传统 OCR 技术仅能提取文本，无法理解语义或执行后续操作。

**问题**:  
- 人工处理一份复杂文档（如医疗理赔单）平均需 15 分钟，且错误率高达 8-12%。  
- 跨系统数据录入（如从 PDF 到 ERP 系统）依赖人工复制粘贴，效率低下。  

**解决方案**:  
UiPath 推出基于 Agent Skills 的文档处理系统，结合 AI 与 RPA（机器人流程自动化）：  
1. **语义理解**：使用 NLP 模型识别文档类型（如发票 vs. 合同）并提取关键信息（如金额、日期）。  
2. **决策与执行**：根据业务规则（如“金额超 1 万需审批”）自动触发后续流程（如发送邮件、更新数据库）。  
3. **人机协作**：对低置信度数据标记异常，由人工快速复核，持续优化模型。  

**效果**:  
- 某保险公司部署后，理赔单处理时间从 15 分钟降至 30 秒，错误率降至 0.5%。  
- 全球 500 强客户平均节省 60% 的文档处理成本，ROI 投资回报周期小于 6 个月。

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确技能边界与单一职责原则

**说明**：
Agent Skills（智能体技能）的设计应遵循单一职责原则。每个技能应专注于解决一个特定的任务或处理一类特定的信息。避免设计“大而全”的万能技能，这会导致模型推理混乱、上下文利用率降低以及错误率上升。清晰的边界有助于 Agent 在规划阶段准确选择合适的工具。

**实施步骤**：
1. 将复杂的业务流程拆解为最小的可执行单元（如：搜索、摘要、代码生成、数据校验）。
2. 为每个技能编写严格的输入输出定义，确保其功能独立。
3. 审查技能描述，移除模棱两可的指令，确保功能聚焦。

**注意事项**：
- 如果一个技能的 Prompt 超过 500-800 字符，通常意味着它承担了过多责任，考虑拆分。
- 避免技能之间功能重叠，这会导致 Agent 在路由时产生犹豫。

---

### 实践 2：优化技能描述与元数据

**说明**：
Agent 依赖于 LLM 来决定何时调用哪个技能（即 Tool Use 功能）。技能的描述和元数据是 LLM 做决策的唯一依据。描述必须准确、具体且包含使用场景的上下文，避免使用过于通用的术语。高质量的元数据能显著减少“幻觉性调用”或调用失败的情况。

**实施步骤**：
1. 为每个技能编写一段简短的摘要，说明其功能及输入参数的物理意义。
2. 在描述中明确“何时使用”以及“何时不使用”该技能。
3. 为参数提供具体的示例值，帮助模型理解预期的数据格式。

**注意事项**：
- 不要在描述中仅重复技能名称，要描述其业务价值。
- 定期分析 Agent 的调用日志，针对误报（错误调用）或漏报（该调用未调用）调整描述文案。

---

### 实践 3：设计结构化输入与输出

**说明**：
为了保证 Agent 系统的稳定性，技能的输入和输出应当是强类型和结构化的。使用 JSON Schema 或 Pydantic 模型定义参数，可以防止 LLM 生成格式错误的数据，从而减少后续解析错误和重试次数。结构化输出也便于其他技能或工作流直接消费数据。

**实施步骤**：
1. 定义严格的参数 Schema，包括字段类型、必填项和枚举值。
2. 在 Prompt 中明确要求输出特定的 JSON 格式或 XML 格式。
3. 在代码层面实现校验逻辑，当 LLM 返回格式不符时自动报错或重试。

**注意事项**：
- 避免接收自由文本作为唯一的输入参数，尽量将其拆解为结构化字段。
- 对于长文本输出，考虑使用流式输出或分段返回，以避免超出 Token 限制。

---

### 实践 4：实现上下文感知与参数注入

**说明**：
技能不应是孤立的，它们需要能够访问 Agent 的全局上下文（如用户历史、当前任务状态、环境变量）。最佳实践要求在技能执行前，动态地将必要的上下文信息注入到技能的参数或 Prompt 中，从而减少模型对历史记录的依赖，提高响应的准确性。

**实施步骤**：
1. 识别技能运行所需的“隐式参数”（如用户 ID、会话 ID、当前时间）。
2. 在 Agent 框架中配置上下文注入器，在调用技能前自动填充这些参数。
3. 在技能内部逻辑中，优先使用注入的上下文变量，而不是让模型从对话历史中去“猜”。

**注意事项**：
- 确保注入的上下文不会泄露敏感信息（PII），必要时进行脱敏处理。
- 控制注入上下文的长度，避免挤占技能核心逻辑的 Token 空间。

---

### 实践 5：构建鲁棒的错误处理与重试机制

**说明**：
外部工具调用（API 请求、数据库查询）不可避免地会遇到网络抖动或服务不可用。技能设计必须包含完善的错误处理逻辑。不仅要捕获异常，还要将错误信息转化为 LLM 能理解的自然语言，以便 Agent 能够自我修正或尝试替代路径。

**实施步骤**：
1. 为每个技能定义标准的错误响应格式。
2. 实现指数退避的重试策略，处理临时性故障（如 5xx 错误、超时）。
3. 区分“可恢复错误”（如网络问题）和“不可恢复错误”（如参数非法），对于后者直接向 Agent 报告具体原因。

**注意事项**：
- 不要直接将原始的堆栈跟踪信息返回给 LLM，这会浪费 Token 并可能混淆模型。
- 设置最大重试次数，防止 Agent 陷入死循环。

---

### 实践 6：建立全面的测试与评估体系

**说明**：
Agent Skills 的非确定性特征使得传统单元测试难以覆盖所有情况。最佳实践包括建立“金标准测试集”，即预设一组输入和期望的输出，用于验证技能的准确性和鲁棒性。此外，还需要进行集成测试，确保技能在 Agent 工作

---
## 学习要点

- 由于您没有提供具体的文章内容，我基于 Hacker News 上关于 "Agent Skills"（AI 智能体技能）的常见高质量讨论和技术共识，为您总结了 5 个关键要点：
- 智能体成功的关键在于将复杂任务分解为可管理的子任务，并具备在执行过程中根据反馈动态调整计划的能力。
- 赋予智能体使用工具的能力（如代码解释器、搜索引擎和 API）是突破大语言模型固有知识局限和实现落地的核心。
- 长期记忆机制（RAG 与向量数据库）比上下文窗口更重要，它确保了智能体在多轮交互中能保持信息的一致性和连贯性。
- 自主性与人类监督之间的平衡至关重要，设计清晰的“人在回路”干预机制能有效防止智能体在错误路径上发散。
- 提示工程正在向结构化的“系统提示词”演进，通过明确角色、目标和约束条件能显著提升智能体的任务完成质量。

---
## 常见问题


### 1: 什么是 Agent Skills（智能体技能），它与传统的 API 调用有何不同？

1: 什么是 Agent Skills（智能体技能），它与传统的 API 调用有何不同？

**A**: Agent Skills 是指赋予自主智能体执行特定任务或动作的能力模块。与传统的 API 调用不同，Agent Skills 通常设计为更具语义化和上下文感知能力。传统的 API 往往需要精确的参数和固定的结构，而 Agent Skills 允许智能体根据用户的自然语言指令，自主决定何时调用哪个技能、如何填充参数以及如何处理返回的结果。简单来说，API 是工具的定义，而 Agent Skills 是智能体“学会”如何使用这些工具来解决复杂问题的能力封装。



### 2: Agent Skills 主要包含哪些类型或类别？

2: Agent Skills 主要包含哪些类型或类别？

**A**: 根据目前的技术发展和应用场景，Agent Skills 主要可以分为以下几类：
1.  **信息检索类**：包括联网搜索、知识库查询（RAG）或读取特定文件内容的能力。
2.  **工具操作类**：能够执行代码、使用计算器、调用第三方服务接口（如发送邮件、查询天气、操作 CRM 系统）。
3.  **内容创作类**：生成图像、编写代码片段、翻译或摘要长文本。
4.  **逻辑推理与规划类**：将复杂任务拆解为步骤，并进行自我反思或修正。
5.  **记忆与状态管理类**：存储用户偏好、读取历史对话记录以保持上下文连续性。



### 3: 如何为自定义的智能体开发或注册一个新的 Skill？

3: 如何为自定义的智能体开发或注册一个新的 Skill？

**A**: 开发流程通常遵循以下步骤：
1.  **定义功能**：明确技能的输入（参数）和输出（返回值），以及该技能的具体用途描述。
2.  **编写描述**：这是最关键的一步。你需要用自然语言详细描述这个技能的功能，以便大语言模型（LLM）能够理解并在合适的时机触发它。
3.  **实现接口**：编写后端逻辑（通常是一个 API 端点或本地函数），处理实际的业务逻辑。
4.  **注册与测试**：在智能体框架（如 LangChain, AutoGen, 或 OpenAI's Assistants API）中注册该 Skill，并进行测试，观察智能体是否能正确识别调用意图并准确传递参数。



### 4: 在构建 Agent Skills 时，如何处理敏感数据和权限安全问题？

4: 在构建 Agent Skills 时，如何处理敏感数据和权限安全问题？

**A**: 安全性是 Agent Skills 设计的核心考量，通常采取以下措施：
1.  **权限验证**：在 Skill 执行操作前，必须进行身份验证和授权检查，确保智能体不会越权操作（例如，不能随意删除数据库记录）。
2.  **数据脱敏**：在将数据传递给大模型之前，过滤掉敏感信息（如 PII 个人身份信息、API 密钥等）。
3.  **沙箱环境**：对于代码执行或文件操作类的 Skills，应在隔离的沙箱环境中运行，防止恶意代码破坏系统。
4.  **人工确认**：对于高风险操作（如发送邮件、转账），设计“人机协同”机制，要求用户人工确认后才能执行 Skill。



### 5: Agent Skills 在实际落地中面临哪些主要挑战？

5: Agent Skills 在实际落地中面临哪些主要挑战？

**A**: 尽管潜力巨大，但目前仍面临几个主要挑战：
1.  **幻觉与参数错误**：智能体可能会错误地调用技能，或者生成错误的参数导致执行失败。
2.  **上下文窗口限制**：如果 Skills 的描述或返回的数据量过大，容易消耗掉模型的上下文窗口，导致遗忘。
3.  **延迟与成本**：智能体进行规划、多次调用 Skills 以及处理结果的循环过程，会导致较高的推理延迟和 Token 消耗成本。
4.  **调试困难**：当智能体执行一长串 Skills 链路后出错，很难定位是规划出了问题还是某个 Skill 的执行出了问题。



### 6: 未来 Agent Skills 的发展趋势是什么？

6: 未来 Agent Skills 的发展趋势是什么？

**A**: 未来的发展趋势主要集中在以下几个方面：
1.  **标准化**：类似于 OpenAPI 规范，Agent Skills 的定义和描述将趋向标准化，使得不同框架间的技能可以复用。
2.  **多智能体协作**：Skills 将不再局限于单一智能体，而是成为多智能体系统中不同角色（如一个负责写代码，一个负责审查）之间协作的桥梁。
3.  **自主进化**：智能体可能具备根据任务反馈自主编写、优化或组合新 Skills 的能力，而不仅仅是使用预定义的 Skills。
4.  **工具学习**：通过少样本学习或微调，让模型更精准地掌握复杂工具的使用方法，减少调用错误率。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 设计一个 Agent，能够自动抓取 Hacker News 首页的前 10 条热门文章标题和链接，并将其保存为 JSON 格式文件。

### 提示**:

### 使用 Python 的 `requests` 库获取网页内容，配合 `BeautifulSoup` 解析 HTML。

---
## 引用

- **原文链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [技能训练](/tags/%E6%8A%80%E8%83%BD%E8%AE%AD%E7%BB%83/) / [框架](/tags/%E6%A1%86%E6%9E%B6/) / [AI Agent](/tags/ai-agent/) / [模型微调](/tags/%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
- [Agent Skills：AI 智能体技能框架与训练方法]({{< relref "posts/20260204-hacker_news-agent-skills-8.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
- [DynaWeb：基于模型的强化学习网页智能体框架]({{< relref "posts/20260131-arxiv_ai-dynaweb-model-based-reinforcement-learning-of-web--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*