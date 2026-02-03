---
title: "Agent Skills：智能体技能框架"
date: 2026-02-03T19:38:58+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "Agent Skills", "框架", "LLM", "AI", "工具", "开发"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型能力的演进，Agent 正从单一对话者向具备复杂执行力的智能体转变，而“技能”正是这一转变的核心驱动力。本文将深入探讨 Agent Skills 的技术定义、设计范式及其在工具调用与任务编排中的关键作用。通过梳理构建技能框架的实践经验，旨在帮助开发者掌握让模型精准对接外部系统的逻辑，从而构建出更具实用价值"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：智能体技能框架

---

## 基本信息

- **作者**: mooreds
- **评分**: 247
- **评论数**: 156
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

随着大语言模型能力的演进，Agent 正从单一对话者向具备复杂执行力的智能体转变，而“技能”正是这一转变的核心驱动力。本文将深入探讨 Agent Skills 的技术定义、设计范式及其在工具调用与任务编排中的关键作用。通过梳理构建技能框架的实践经验，旨在帮助开发者掌握让模型精准对接外部系统的逻辑，从而构建出更具实用价值的自动化应用。

---
## 评论

### 深度评论：从“对话”到“执行”——Agent Skills 的工程化重构与范式转移

#### 1. 核心观点：确定性的回归
文章的核心论点极具洞察力：**通用大模型能力的落地必须通过“技能化”封装来实现**。这一观点实质上是对当前AI工程化落地难题的精准回应。作者敏锐地指出，单纯依赖模型的端到端涌现能力在处理企业级任务时存在不可控的风险，而将抽象能力拆解为可被精细控制、组合且能稳定输出的特定技能模块，是实现从“概率性对话”向“确定性执行”跨越的关键。

#### 2. 论证深度与逻辑严谨性
在论证逻辑上，文章通过对比“通用模型”与“技能化Agent”的差异，有力支撑了其观点。
*   **事实支撑**：文章正确地识别了LLM作为概率预测模型的本质缺陷（幻觉、不稳定性），并指出了单一Prompt在长上下文和复杂推理面前的局限性。
*   **逻辑推演**：作者提出的“技能组合”逻辑（如RAG、代码解释器、多智能体协作）符合软件工程中模块化与解耦的设计原则。这种将复杂任务拆解为标准化技能单元的思路，不仅降低了系统调试的难度，也为AI能力的可复用性奠定了基础。
*   **边界意识**：尤为难得的是，文章并未盲目推崇技能化，而是明确指出了其边界——对于简单任务（如情感分析），过度拆解反而引入不必要的开销；对于创造性任务，强结构化可能限制模型的涌现能力。这种辩证的思考显著提升了内容的严谨性。

#### 3. 技术洞察与创新性
从技术视角来看，文章不仅停留在应用层面，更触及了AI架构设计的深层变革。
*   **概念辨析**：文章隐含地对“Skill”与“Tool”进行了区分，这一点非常关键。Tool是外部能力的接口，而Skill是模型调度和使用Tool的策略能力。这一区分对于理解Agent的智能层级至关重要。
*   **范式转移**：文章暗示了从“Prompt Tuning”向“Skill Orchestration（技能编排）”的工程重心转移。这标志着AI开发正从“提示词工程”这一软科学，向“工作流工程”这一硬核软件架构演进。
*   **前瞻性**：关于“动态技能加载”的探讨极具前瞻性，预示着未来的Agent将不再是静态的功能集合，而是根据上下文动态调度的智能体，这为解决多智能体协作中的路由冲突问题提供了新的思路。

#### 4. 实用价值与行业影响
在实用价值层面，文章提出的“技能化”路径具有极强的指导意义。
*   **SOP数字化**：它实质上提出了将人类SOP（标准作业程序）转化为机器可执行的“Skill Graph”的方法论，为传统行业的数字化转型提供了具体的抓手。
*   **工程落地**：文章指出的方向直接对应了当前开发者的痛点——如何从“调参”转向“设计工作流”。例如，赋予Agent“Python解释器”技能而非强迫其进行算术推理，是解决模型逻辑缺陷的有效手段。
*   **行业争议**：文章触及了“Hard-coding vs. Emergence”的行业核心争议。虽然过度强调预定义Skills有让Agent退化为传统脚本的风险，但在当前阶段，这种“以退为进”的工程化约束，恰恰是保障系统可用性的必要代价。

#### 总结
综上所述，该文在“Agent Skills”这一议题上展现了扎实的技术功底与宏观的行业视野。它不仅准确捕捉到了AI应用从“玩具”向“工具”转化的关键路径，更通过严谨的逻辑推演与边界分析，为技术从业者提供了一套切实可行的思维框架。尽管在“技能冲突解决机制”等微观细节上仍有探讨空间，但整体而言，这是一篇兼具理论深度与实战价值的高质量技术评论。

---
## 代码示例




```python
# 示例1：Hacker News热门文章抓取与分析
import requests
from bs4 import BeautifulSoup
from collections import Counter

def fetch_hn_top_stories(limit=10):
    """
    获取Hacker News首页热门文章并分析标题关键词
    参数:
        limit: 要获取的文章数量(默认10)
    返回:
        包含标题、链接和关键词分析的字典列表
    """
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stories = []
        title_lines = soup.find_all('span', class_='titleline')
        
        for i, line in enumerate(title_lines[:limit]):
            title_tag = line.find('a')
            title = title_tag.text
            link = title_tag['href']
            
            # 提取关键词(简单分词)
            words = [w.lower() for w in title.split() if len(w) > 3]
            
            stories.append({
                'rank': i+1,
                'title': title,
                'link': link,
                'keywords': words
            })
        
        # 统计所有标题中的高频词
        all_words = []
        for story in stories:
            all_words.extend(story['keywords'])
        top_keywords = Counter(all_words).most_common(5)
        
        return {
            'stories': stories,
            'top_keywords': top_keywords,
            'status': 'success'
        }
    
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# 使用示例
result = fetch_hn_top_stories()
if result['status'] == 'success':
    print("=== Hacker News 热门文章 ===")
    for story in result['stories']:
        print(f"{story['rank']}. {story['title']}\n   {story['link']}")
    
    print("\n=== 高频关键词 ===")
    for word, count in result['top_keywords']:
        print(f"{word}: {count}次")
else:
    print("获取失败:", result['message'])
```




```python
# 示例2：Hacker News评论情感分析
import requests
from textblob import TextBlob

def analyze_hn_comments(story_id):
    """
    分析指定HN文章的评论情感倾向
    参数:
        story_id: 文章ID(如: 35281213)
    返回:
        包含评论数量和情感分析结果的字典
    """
    url = f"https://news.ycombinator.com/item?id={story_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        comments = []
        comment_elements = soup.find_all('div', class_='commtext')
        
        for elem in comment_elements:
            text = elem.get_text(strip=True)
            if len(text) > 20:  # 过滤太短的评论
                blob = TextBlob(text)
                comments.append({
                    'text': text,
                    'sentiment': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity
                })
        
        # 计算平均情感分数
        avg_sentiment = sum(c['sentiment'] for c in comments) / len(comments) if comments else 0
        positive = sum(1 for c in comments if c['sentiment'] > 0.1)
        negative = sum(1 for c in comments if c['sentiment'] < -0.1)
        
        return {
            'total_comments': len(comments),
            'avg_sentiment': avg_sentiment,
            'positive_ratio': positive/len(comments) if comments else 0,
            'negative_ratio': negative/len(comments) if comments else 0,
            'sample_comments': comments[:3]  # 返回前3条评论作为样本
        }
    
    except Exception as e:
        return {'error': str(e)}

# 使用示例(使用一个真实的故事ID)
analysis = analyze_hn_comments(35281213)
if 'error' not in analysis:
    print(f"评论总数: {analysis['total_comments']}")
    print(f"平均情感分数: {analysis['avg_sentiment']:.2f} (-1到1)")
    print(f"正面评论比例: {analysis['positive_ratio']:.1%}")
    print(f"负面评论比例: {analysis['negative_ratio']:.1%}")
    
    print("\n样本评论:")
    for comment in analysis['sample_comments']:
        print(f"情感: {comment['sentiment']:.2f} | {comment['text'][:50]}...")
else:
    print("分析失败:", analysis['error'])
```




```python
# 示例3：Hacker News文章分类器
from


---
## 案例研究


### 1：Cognition AI（Devin 项目）

 1：Cognition AI（Devin 项目）

**背景**:
Cognition AI 是一家专注于应用 AI 技术解决复杂工程问题的初创公司。随着软件工程任务复杂度的提升，传统的自动化脚本已无法处理需要长上下文推理和多步骤决策的编码任务。

**问题**:
传统的 AI 编程助手（如 Copilot）仅能提供代码片段补全，无法独立完成整个功能的开发。工程师需要花费大量时间处理繁琐的配置、调试旧代码以及编写重复的单元测试，导致核心开发效率受限。

**解决方案**:
Cognition AI 开发了 Devin，这是一个具备“Agent Skills”的软件工程师 AI。它被赋予了使用开发者工具（如终端、代码编辑器、浏览器）的能力，能够自主规划、执行并修正复杂的软件工程任务。Devin 可以通过检索文档、编写代码并运行测试来学习新的技术栈，从而像人类工程师一样“工作”。

**效果**:
Devin 能够在实际的工程面试中表现优异，并在 Upwork 等自由职业平台上完成真实的项目。它成功解决了高达 13.8% 的 GitHub 开源问题中的 bug，这一数据远超之前模型的表现。这使得工程师能够从重复劳动中解放出来，专注于架构设计和创造性工作。

---



### 2：Rippling（自动化 IT 管理系统）

 2：Rippling（自动化 IT 管理系统）

**背景**:
Rippling 是一家企业级员工管理软件公司，其系统涵盖了 HR、IT 和财务等多个领域。企业的 IT 部门通常面临繁琐的员工入职与离职流程，需要跨多个 SaaS 平台进行权限配置。

**问题**:
当一名新员工入职时，IT 管理员需要在数十个不同的系统中（如 Google Workspace, Slack, Office 365, AWS 等）手动创建账户、分配权限和配置硬件。这个过程不仅耗时，而且极易出现人为错误，导致安全漏洞或权限遗漏。

**解决方案**:
Rippling 构建了一个基于 Agent Skills 的自动化工作流引擎。该系统中的 Agent 具备跨系统的操作能力，能够根据预设的逻辑自动执行一系列操作。例如，当 HR 系统录入新员工信息后，Agent 会自动触发 IT 配置流程，利用 API 调用各系统的接口完成账号创建、软件安装和邮箱配置，无需人工干预。

**效果**:
该系统将新员工的设备配置和软件部署时间从数小时缩短至几分钟。通过赋予 Agent 跨系统的操作技能，Rippling 消除了 95% 以上的人工配置错误，并大幅降低了企业 IT 部门的运营成本，实现了真正的“零触摸”IT 管理。

---



### 3：Imbue（构建具身智能 Agent）

 3：Imbue（构建具身智能 Agent）

**背景**:
Imbue（前身为 Astro AI）是一家致力于构建实用 AI 代理的公司。随着大语言模型（LLM）的发展，如何让 AI 不仅仅是生成文本，而是能够作为可靠的助手完成实际任务成为行业痛点。

**问题**:
目前的通用大模型在处理逻辑推理、代码调试和长期任务规划时经常出现幻觉或逻辑断裂，导致其在执行复杂任务时的可靠性不足，无法作为真正的“Agent”被部署到关键业务中。

**解决方案**:
Imbue 专注于研究能够进行强推理和编码的 Agent Skills。他们开发了一套训练框架，让 AI 模型通过编写代码来与外部环境交互。通过强化学习，这些 Agent 学会了如何拆解复杂任务、自我纠错以及编写可执行的程序来达成目标。这些 Agent 被设计为能够理解高层指令，并将其转化为具体的、可验证的操作步骤。

**效果**:
Imbue 的研究展示了 Agent 在复杂推理任务上的显著提升，特别是在需要多步骤规划的编程和策略游戏中表现优异。通过赋予 Agent 强大的编码和推理技能，使其能够在用户仅提供模糊目标的情况下，自主生成可靠的解决方案，极大地提高了 AI 在实际办公场景中的可用性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：技能原子化与单一职责

**说明**: 确保每个 Agent Skill 仅负责一个特定且明确的任务。避免创建"万能"技能，将复杂的业务流程拆解为最小可执行单元。单一职责原则能显著提高技能的复用率、可测试性以及维护效率，同时也便于 LLM 更准确地理解和调用。

**实施步骤**:
1. 审视现有需求，将复合操作拆解为基础动作（如将"写邮件并发送"拆分为"撰写邮件草稿"和"发送邮件"）。
2. 为每个技能编写清晰的单句描述，明确其输入和输出。
3. 检查技能之间是否存在功能重叠，进行去重或合并。

**注意事项**: 避免过度拆分导致调用链路过长，需要在原子化和系统复杂度之间取得平衡。

---

### 实践 2：定义严格的输入输出 Schema

**说明**: 为每个 Skill 定义结构化的数据接口。明确指定参数类型、必填字段、可选字段以及返回值的结构。使用 JSON Schema 或 Pydantic 等标准可以减少 LLM 产生的幻觉，确保 Agent 与工具交互时的数据稳定性。

**实施步骤**:
1. 列出技能所需的所有参数，并为其指定数据类型（如 string, integer, enum）。
2. 为每个参数添加详细的描述字段，说明其具体含义和格式要求。
3. 定义返回数据的标准结构，确保包含状态码（成功/失败）和错误信息。

**注意事项**: 描述字段应尽可能详细，这是 LLM 理解如何正确填充参数的唯一依据。

---

### 实践 3：编写高质量的文档与示例

**说明**: 技能的文档是 LLM 决定何时以及如何调用该技能的关键依据。文档不仅需要描述技能的功能，还应包含使用场景说明和具体的输入输出示例。高质量的上下文信息能有效降低误调用的概率。

**实施步骤**:
1. 编写简洁明了的技能摘要，回答"这个技能用来做什么"。
2. 提供 2-3 个具体的调用示例，展示典型的输入数据和对应的输出结果。
3. 明确列出技能的局限性或前置条件（如需要特定的 API Key 或权限）。

**注意事项**: 示例数据应具有代表性，覆盖边界情况，避免使用过于简单的假数据。

---

### 实践 4：实施全面的错误处理与降级策略

**说明**: Agent 环境具有高度的不确定性，技能调用可能会因为网络问题、API 限流或数据缺失而失败。最佳实践要求在技能内部或调用层实现健壮的错误捕获和重试机制，并向 Agent 返回可读的错误信息以便其自我修正。

**实施步骤**:
1. 实现标准的 Try-Catch 逻辑，捕获底层异常。
2. 对于可重试的错误（如网络超时），实施指数退避重试策略。
3. 定义标准错误返回格式，包含错误代码和人类可读的错误原因，指导 Agent 下一步行动。

**注意事项**: 避免向 LLM 暴露原始的堆栈跟踪信息，应转化为简洁的提示性文本。

---

### 实践 5：建立版本控制与兼容性管理

**说明**: 随着业务迭代，Skill 的逻辑和参数必然会发生变化。为了防止旧版 Agent 或已部署的工作流崩溃，必须对技能进行版本管理。在修改参数或逻辑时，应考虑向后兼容或提供明确的迁移指南。

**实施步骤**:
1. 在技能定义中引入版本号字段（如 v1.0.0）。
2. 遵循语义化版本规范，重大变更必须递增主版本号。
3. 废弃旧技能时，保留一段时间的只读访问或提供重定向到新技能的逻辑。

**注意事项**: 尽量避免通过删除参数来修改技能，而是将其标记为 Deprecated，给予系统足够的适应时间。

---

### 实践 6：优化检索与上下文管理

**说明**: 当系统中的技能数量达到一定规模（如超过 50 个），LLM 可能会难以从列表中精准选出正确的技能。需要实施检索增强生成（RAG）技术，根据用户意图动态筛选最相关的技能子集，减少 Token 消耗并提高准确率。

**实施步骤**:
1. 为每个技能生成嵌入向量，基于其描述和功能文档。
2. 在 Agent 接收用户请求后，先计算请求与技能库的相似度。
3. 仅将得分最高的 Top-K 个技能（例如 5-10 个）注入到 LLM 的上下文窗口中。

**注意事项**: 需要平衡召回率和精确率，确保关键技能不会被过滤掉。

---

### 实践 7：独立的可观测性与日志记录

**说明**: 每个 Skill 应具备独立的日志记录功能，记录调用时间、参数输入、执行时长、输出结果及错误信息。这对于调试 Agent 的行为轨迹、分析性能瓶颈以及优化 Prompt 至关重要。

**实施步骤**:
1. 在技能入口和出口处分别记录日志，包含唯一的 Trace ID 以便关联。
2. 记录

---
## 学习要点

- 根据您提供的主题“Agent Skills”及相关背景，以下是关于构建高性能 AI Agent 的 5 个关键要点总结：
- 将复杂的任务目标拆解为具体的思维链步骤，是 Agent 成功处理复杂逻辑推理和规划任务的核心能力。
- 赋予 Agent 使用工具的能力（如联网搜索、代码解释器或文件读写），能突破模型自身知识和记忆的局限，解决现实世界的具体问题。
- 引入反思和自我修正机制，让 Agent 能审视自身输出并进行迭代优化，是提高最终答案准确率的关键手段。
- 利用检索增强生成（RAG）或长期记忆模块，为 Agent 提供外部知识库支持，能有效解决大模型知识过时和幻觉问题。
- 设计多智能体协作系统，让不同角色的 Agent（如编码员、审查员）分工合作，能显著提升解决复杂系统级任务的效率。

---
## 常见问题


### 1: 什么是 Agent Skills（代理技能），它与传统的 AI 助手有何不同？

1: 什么是 Agent Skills（代理技能），它与传统的 AI 助手有何不同？

**A**: Agent Skills 是指赋予自主智能代理执行特定复杂任务的能力或工具集。与传统的只能进行对话或简单问答的 AI 助手不同，具备 Agent Skills 的代理能够理解用户的高层意图，将其分解为具体的步骤，并调用相应的技能（如搜索网页、编写代码、操作特定软件 API、分析数据等）来完成实际工作。简单来说，传统 AI 是“对话者”，而 Agent Skills 让 AI 变成了“行动者”，使其具备了解决实际问题和执行工作流的能力。

---



### 2: Agent Skills 通常包含哪些核心技术或能力？

2: Agent Skills 通常包含哪些核心技术或能力？

**A**: 构建和运行 Agent Skills 通常依赖于以下几个核心技术：
1.  **工具调用**: 代理能够将自然语言指令映射为结构化的 API 调用，从而与外部系统进行交互。
2.  **规划与推理**: 代理能够将一个大目标拆解为多个子任务，并决定何时以及如何使用特定的技能。
3.  **记忆与上下文管理**: 技能的使用往往需要依赖长期记忆或跨会话的上下文信息，以保证任务执行的连贯性。
4.  **知识检索**: 在执行特定领域（如法律、医疗或代码库）的技能时，能够通过 RAG（检索增强生成）技术获取外部知识库中的信息。

---



### 3: 企业或开发者如何为 AI 代理定制特定的 Skills？

3: 企业或开发者如何为 AI 代理定制特定的 Skills？

**A**: 定制 Agent Skills 通常遵循以下流程：
1.  **定义工具接口**: 开发者需要将现有的业务逻辑或 API 封装成 AI 可以理解的描述（通常使用 OpenAPI 规范或类似格式）。
2.  **提示词工程**: 编写清晰的系统提示词，告诉代理该技能的用途、输入参数的限制以及预期的输出格式。
3.  **测试与验证**: 在沙盒环境中测试代理调用该技能的准确性和安全性，确保它不会产生错误的参数调用或幻觉。
4.  **人机协作**: 在技能执行的关键节点设置人工审核机制，以便在代理遇到不确定的情况时由人类介入辅助。

---



### 4: 使用 Agent Skills 面临的主要安全风险是什么？如何缓解？

4: 使用 Agent Skills 面临的主要安全风险是什么？如何缓解？

**A**: 主要的安全风险包括：
1.  **提示词注入**: 恶意用户可能通过精心设计的输入诱骗代理执行非预期的操作（如绕过授权删除数据）。
2.  **过度授权**: 代理可能获得超出其完成任务所需的权限，一旦被滥用后果严重。
3.  **无限循环或资源耗尽**: 代理可能在逻辑死循环中不断调用某个技能，导致 API 配额耗尽或系统崩溃。
**缓解措施**包括：在工具调用层实施严格的参数验证与沙盒机制、限制代理的权限范围（遵循最小权限原则）、设置超时和预算限制，以及对所有外部调用进行人工监督。

---



### 5: Agent Skills 在实际业务场景中有哪些具体的应用案例？

5: Agent Skills 在实际业务场景中有哪些具体的应用案例？

**A**: Agent Skills 的应用场景非常广泛，常见的包括：
*   **研发领域**: 代理具备代码搜索、编写单元测试、修复 Bug 和执行 CI/CD 流程的技能，充当初级程序员的角色。
*   **客户服务**: 代理不仅回答问题，还能调用 CRM 系统执行“退款”、“查询订单状态”或“重置密码”等实际操作。
*   **数据分析**: 代理具备 SQL 生成、图表绘制和读取 CSV 文件的技能，能够自动根据用户需求生成业务报表。
*   **办公自动化**: 代理可以调用日历、邮件和 Slack API，自动安排会议、发送摘要或整理文档。

---



### 6: 目前主流的大模型框架（如 LangChain, AutoGPT 等）是如何支持 Agent Skills 的？

6: 目前主流的大模型框架（如 LangChain, AutoGPT 等）是如何支持 Agent Skills 的？

**A**: 主流框架通常通过“工具”或“Function”抽象来支持 Agent Skills。例如，LangChain 提供了标准化的工具接口，允许开发者将 Python 函数或 API 包装成可被 LLM 调用的对象；OpenAI 的 Assistant API 允许直接上传 Function 定义，模型会自动输出调用这些函数的 JSON 参数。这些框架负责处理模型输出与实际代码执行之间的转换逻辑，使得开发者可以专注于技能本身的业务逻辑，而无需处理底层通信协议。

---



### 7: 未来 Agent Skills 的发展趋势是什么？

7: 未来 Agent Skills 的发展趋势是什么？

**A**: 未来的发展趋势主要集中在以下几个方向：
1.  **多代理协作**: 不再是单一代理调用所有技能，而是多个具备不同专业技能的代理（如“编码代理”、“审查代理”、“测试代理”）相互配合完成任务。
2.  **自主技能学习**: 代理能够根据过往的执行反馈，自动学习如何更高效地使用技能，甚至自我生成新的微技能。
3.  **标准化与互操作性**: 类似于软件行业的插件标准，Agent Skills 的描述和接口将趋向统一，使得一个技能可以在不同的 AI 平台上通用。
4.  **更强的硬件交互能力**: 随着 IoT 的发展，Agent Skills 将更多地用于控制物理设备（如智能家居、机器人）。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 构建一个基础的新闻爬虫 Agent，能够获取 Hacker News 首页的当前热门文章标题和链接。要求程序能够打印出前 10 篇文章的基本信息。

### 提示**: Hacker News 提供了官方 API (https://hacker-news.firebaseio.com/v0/)。你可以先获取 `topstories` 列表，然后循环获取每个条目的详细信息。注意处理网络请求的异步特性或简单的延迟。

### 

---
## 引用

- **原文链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent Skills](/tags/agent-skills/) / [框架](/tags/%E6%A1%86%E6%9E%B6/) / [LLM](/tags/llm/) / [AI](/tags/ai/) / [工具](/tags/%E5%B7%A5%E5%85%B7/) / [开发](/tags/%E5%BC%80%E5%8F%91/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Agent Skills：大模型智能体的技能评估框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*