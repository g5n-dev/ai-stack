---
title: "Agent Skills：智能体技能框架与能力评估"
date: 2026-02-04T13:32:11+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "技能框架", "能力评估", "LLM", "AI Agent", "评测", "Agent Skills"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在 LLM 应用开发中，Agent 的核心价值在于通过调用工具解决复杂问题，而 Agent Skills 则是连接大模型与外部能力的关键组件。随着应用场景从单一问答转向多步骤任务协作，如何高效定义、管理与复用这些技能，已成为提升系统稳定性的技术重点。本文将梳理 Agent Skills 的技术原理与工程化实践，帮助开发"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：智能体技能框架与能力评估

---

## 基本信息

- **作者**: mooreds
- **评分**: 481
- **评论数**: 233
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

在 LLM 应用开发中，Agent 的核心价值在于通过调用工具解决复杂问题，而 Agent Skills 则是连接大模型与外部能力的关键组件。随着应用场景从单一问答转向多步骤任务协作，如何高效定义、管理与复用这些技能，已成为提升系统稳定性的技术重点。本文将梳理 Agent Skills 的技术原理与工程化实践，帮助开发者掌握构建模块化智能体的具体方法，从而在实际业务中实现更精准的工具调用与流程编排。

---
## 评论

### 深度评论

#### 中心观点
构建高效AI智能体的核心不在于单纯追求模型参数规模的堆叠，而在于通过精细化的技能抽象、编排与组合，实现大模型从“通才”向“专才”的能力跃迁。文章主张将复杂的任务拆解为标准化的技能单元，以解决大模型在实际落地中面临的幻觉、成本及可控性问题。

#### 支撑理由与边界条件

**1. 技能抽象显著降低了推理成本与幻觉率**
*   **理由**：将复杂任务拆解为特定的“Skills”（如Search、Code、SQL_Write），本质上是将大模型的推理空间收束。相比于端到端的Chain-of-Thought（CoT），特定技能配合RAG（检索增强生成）或Tool Use（工具调用），能显著减少无关Token生成，并利用外部工具校验中间结果，从而降低逻辑断裂风险。
*   **反例/边界条件**：对于高度依赖跨领域联想的创造性任务（如文学创作或头脑风暴），过度的技能拆解可能会割裂思维的连贯性，导致输出过于机械或缺乏灵感。

**2. 技能复用是构建Agent生态的基石**
*   **理由**：文章强调将Agent能力模块化，类似于软件工程中的微服务架构。一旦“数据分析”或“邮件撰写”被定义为标准技能，它们即可被跨项目、跨场景复用，这是Agent走向规模化生产的前提。
*   **反例/边界条件**：技能的标准化极具挑战。不同业务场景下的“写邮件”技能，其上下文、语气和约束条件差异巨大，通用技能往往难以直接落地，仍需大量特定调整。

**3. 技能编排比单点技能更具决定性**
*   **理由**：Agent的核心价值在于“规划”。单个技能（如使用Google搜索）价值有限，但通过Planner将“搜索”、“总结”、“翻译”串联起来解决复杂问题，才是Agent的精髓。若只谈技能而忽视编排逻辑，则舍本逐末。
*   **反例/边界条件**：在编排链条过长时，误差会累积。如果第一个技能返回了错误信息，后续的Skill编排会将其放大（级联效应），导致最终结果完全不可用。

#### 多维度深度评价

**1. 内容深度**
该文章触及了AI工程化的核心痛点，试图跳出“模型对战”的怪圈，转向“系统架构”的视角。
*   **严谨性评价**：文章若仅停留在“我们要有技能”的口号层面，则深度不足。深度探讨应当涉及技能的定义边界——一个Skill到底是一个Prompt Template，还是一个Fine-tuned LoRA，亦或是一个独立的API？目前行业对于Skill的粒度定义尚无标准，这是论证中常见的逻辑模糊地带。

**2. 实用价值**
对工程团队具有极高的指导意义。
*   **指导意义**：提示开发者不要试图用Prompt解决所有问题，而应将Agent开发视为传统软件开发：定义接口（输入/输出）、实现逻辑、异常处理。
*   **局限性**：文章往往低估了Skill维护的复杂性。维护100个高质量的Skill Prompt，其隐形成本可能比训练一个垂直领域小模型更高。

**3. 创新性**
*   **新观点**：提出了“Skill as a Service”或“Skill Router”的概念，即由一个路由模型来判断当前任务应该调用哪个技能。这比传统的硬编码If-Else更具智能性。
*   **批判**：这并非全新概念，某种程度上是对专家系统和现代RAG的旧瓶装新酒，但LLM的语义理解能力赋予了路由器前所未有的灵活性。

**4. 行业影响**
推动行业从“模型中心”向“应用中心”转移。这预示着未来AI人才的需求将从“炼丹师”转向“AI架构师”——即懂得如何拆解业务并映射为Agent技能栈的人。

**5. 争议点与不同观点**
*   **争议点**：**Native vs. Tooling**。OpenAI o1等模型的出现表明，通过强化学习提升模型的内生推理能力，可能比依赖外部工具调用（Skills）更有效。如果模型足够聪明，它可能不需要显式的“搜索技能”，而是自己推导出需要搜索并生成代码执行。
*   **观点**：Skills不是目的，而是模型能力的补丁。随着模型能力进化，部分低级技能（如简单的语法纠正）将被内化，而高级技能（如操作私有ERP系统）将长期存在。

---
## 代码示例




```python
# 示例1：从Hacker News获取热门文章标题
import requests

def get_hacker_news_top_stories(limit=5):
    """
    获取Hacker News当前热门文章标题
    :param limit: 要获取的文章数量，默认5篇
    :return: 包含文章标题和链接的列表
    """
    # Hacker News API端点
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        # 获取热门文章ID列表
        response = requests.get(top_stories_url)
        story_ids = response.json()[:limit]
        
        result = []
        for story_id in story_ids:
            # 获取每篇文章的详细信息
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            story_data = story_response.json()
            
            # 提取标题和链接
            result.append({
                "title": story_data.get("title", "无标题"),
                "url": story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}")
            })
        
        return result
    
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return []

# 测试代码
if __name__ == "__main__":
    stories = get_hacker_news_top_stories()
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}\n   {story['url']}\n")
```




```python
# 示例2：分析Hacker News文章评论情感
from textblob import TextBlob
import requests

def analyze_story_comments_sentiment(story_id):
    """
    分析指定Hacker News文章评论的情感倾向
    :param story_id: 文章ID
    :return: 评论情感分析结果
    """
    # 获取文章评论
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    story_data = requests.get(story_url).json()
    comment_ids = story_data.get("kids", [])
    
    if not comment_ids:
        return "该文章暂无评论"
    
    positive = 0
    negative = 0
    neutral = 0
    
    for comment_id in comment_ids[:10]:  # 限制分析前10条评论
        comment_url = f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json"
        comment_data = requests.get(comment_url).json()
        comment_text = comment_data.get("text", "")
        
        if not comment_text:
            continue
            
        # 使用TextBlob进行情感分析
        blob = TextBlob(comment_text)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0.1:
            positive += 1
        elif sentiment < -0.1:
            negative += 1
        else:
            neutral += 1
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "total": positive + negative + neutral
    }

# 测试代码
if __name__ == "__main__":
    # 使用一个示例文章ID
    sample_story_id = 12345  # 替换为实际的文章ID
    sentiment_result = analyze_story_comments_sentiment(sample_story_id)
    print(f"评论情感分析结果: {sentiment_result}")
```




```python
# 示例3：监控Hacker News关键词并自动通知
import requests
import time
from datetime import datetime

def monitor_hacker_news_keywords(keywords, check_interval=300):
    """
    监控Hacker News新文章中是否包含指定关键词
    :param keywords: 要监控的关键词列表
    :param check_interval: 检查间隔(秒)，默认5分钟
    """
    last_checked_ids = set()
    
    while True:
        try:
            # 获取最新文章ID
            new_stories_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
            response = requests.get(new_stories_url)
            current_ids = set(response.json()[:30])  # 检查最新30篇
            
            # 找出新增的文章
            new_ids = current_ids - last_checked_ids
            if not new_ids:
                time.sleep(check_interval)
                continue
                
            print(f"\n检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            for story_id in new_ids:
                # 获取文章详情
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_data = requests.get(story_url).json()
                title = story_data.get("title", "").lower()
                url = story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}")
                
                # 检查是否包含关键词
                for keyword in keywords:
                    if keyword.lower() in title:
                        print(f"发现匹配关键词 '{keyword}' 的文章:")
                        print(f"标题: {story_data['title']}")


---
## 案例研究


### 1：Cognition AI (Devin)

 1：Cognition AI (Devin)

**背景**:
Cognition AI 是一家专注于应用人工智能的初创公司，致力于通过完全自主的 Agent 改变软件工程的工作流程。随着软件开发需求的激增，传统的编码模式在处理重复性高、逻辑复杂的任务时效率受限。

**问题**:
软件工程师在日常工作中花费大量时间在环境配置、依赖库安装、代码调试和编写重复的单元测试上。现有的自动化工具（如 Copilot）仅能提供代码片段建议，无法独立完成端到端的工程任务，导致开发流程依然严重依赖人工介入。

**解决方案**:
Devin 是一个具备“Agent Skills”的 AI 软件工程师。它被设计为能够使用开发者工具（如命令行、代码编辑器、浏览器），并具备规划、推理和纠错能力。Devin 可以自主学习不熟悉的技术，在沙盒环境中执行任务，并能够根据用户的反馈修复 Bug。

**效果**:
在实际测试中，Devin 成功通过了 Upwork 的真实工程测试，能够完成从需求分析到代码部署的全过程。它不仅能够自动编写并部署代码，还能训练和微调其他 AI 模型。这标志着 AI Agent 从“辅助工具”向“独立工程师”的转变，极大地提升了软件开发的自动化水平。

---



### 2：Rabbit (R1)

 2：Rabbit (R1)

**背景**:
Rabbit 是一家硬件初创公司，其目标是重新定义人机交互方式，摆脱对屏幕和特定 App 的依赖。该公司发布了名为 R1 的便携式设备，试图解决现代智能手机中 App 生态割裂的问题。

**问题**:
用户在日常生活中需要打开无数个 App 来完成不同的服务（如听音乐、订车、买菜），每个 App 都有不同的界面和操作逻辑。现有的语音助手（如 Siri 或 Alexa）通常只能执行简单的指令，无法跨应用执行复杂的、多步骤的操作链。

**解决方案**:
Rabbit 开发了基于“Large Action Model”（LAM）的 Agent 技术。该系统不依赖于与各个 App 的 API 集成，而是通过“ teach mode”（教学模式）学习用户在特定 App 或网站上的操作界面和流程。Agent 掌握这些“Skills”后，可以直接通过自然语言指令，代替用户在后台点击界面、输入信息来完成操作。

**效果**:
R1 设备展示了 Agent Skills 在跨应用服务调度上的潜力。用户只需说“帮我订一杯拿铁”，Agent 就能自动跳转登录、选择口味、支付并完成订单。这种基于 UI 自动化的 Agent Skills 使得设备能够操作未经 API 开放的服务，实现了真正的意图导向计算。

---



### 3：Imbue (原 Neurala)

 3：Imbue (原 Neurala)

**背景**:
Imbue 是一家专注于构建具备推理能力的 AI Agent 的公司，近期获得了巨额融资以研发能够在复杂环境中自主决策的系统。其核心研究方向是如何让 AI 不仅会写代码，还能具备逻辑思考和解决实际问题的能力。

**问题**:
目前的 AI 模型虽然能生成流畅的文本或代码，但在面对需要多步推理、处理模糊指令或长期规划的复杂任务时，往往表现不佳（即“规划”能力的缺失）。企业级应用需要 Agent 能够在信息不完全的情况下做出稳健的决策，而不是仅仅模仿训练数据。

**解决方案**:
Imbue 构建了一个专门的 Agent 训练平台，重点优化 AI 的“元认知”能力，即自我反思和错误修正能力。他们开发了一系列 Agent Skills，使系统能够将一个复杂的宏大目标拆解为可执行的子任务，并在执行过程中根据结果动态调整策略。该系统特别强化了代码编写作为推理的基础，因为代码环境提供了明确的逻辑反馈。

**效果**:
Imbue 的 Agent 在内部基准测试中展现出了比通用大模型更强的逻辑推理和任务完成率。其技术价值在于能够处理那些传统 AI 无法解决的、需要严密逻辑的复杂工作流（如复杂的数据库查询、战略游戏模拟或自动化业务流程优化），为构建可靠的“AI 员工”奠定了基础。

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确技能边界与单一职责原则

**说明**: Agent Skills 的设计应遵循微服务化的思想，每个 Skill 应专注于解决一个特定领域的问题或执行一项明确的任务。避免创建过于庞大、功能混杂的“万能 Skill”。清晰的边界有助于提高调用的准确性，减少幻觉，并便于后续的维护和迭代。

**实施步骤**:
1. 列出 Agent 需要完成的所有任务清单。
2. 将复杂任务拆解为原子化的操作（例如：将“写文章并发布”拆分为“撰写草稿”、“校对语法”、“发布到平台”）。
3. 为每个原子操作定义独立的 Skill，并编写严格的描述。

**注意事项**: 避免在单个 Skill 中包含过多的逻辑判断分支，这会降低 LLM 的执行效率。

---

### 实践 2：编写结构化的输入输出规范

**说明**: 为了确保 Agent 能够正确调用 Skill 并处理返回结果，必须明确定义输入参数和输出数据的 Schema。使用 JSON Schema 或 Pydantic 模型可以强制数据类型的一致性，减少因格式错误导致的执行失败。

**实施步骤**:
1. 为每个 Skill 定义必需和可选的输入参数。
2. 规定输出数据的结构，避免返回非结构化的纯文本。
3. 在代码层面实现参数校验，如果 LLM 生成的参数不符合规范，应自动报错并重试。

**注意事项**: 输出描述应尽可能具体，例如要求输出“JSON 格式的对象列表”而不是“一段包含数据的文字”。

---

### 实践 3：优化文档与语义描述

**说明**: Skill 的描述文档是 LLM 理解并决定是否调用该 Skill 的唯一依据。描述不仅要包含功能简介，还应详细说明适用场景、不适用场景以及参数的具体含义。高质量的 Prompt 工程能显著提高 Agent 的路由准确率。

**实施步骤**:
1. 编写简洁明了的 Skill 名称（通常为动词+名词，如 `search_database`）。
2. 在描述中明确该 Skill 的“前置条件”和“预期效果”。
3. 提供少量示例（Few-Shot Examples）在文档中，展示正确的调用方式。

**注意事项**: 避免使用歧义词汇，描述中不要包含与功能无关的背景信息，以免干扰 LLM 的判断。

---

### 实践 4：实现全面的错误处理与重试机制

**说明**: 外部工具调用（API 请求、数据库查询等）往往存在不稳定性。Skill 必须具备健壮的错误处理能力，能够区分可重试的错误（如网络超时）和不可重试的错误（如权限拒绝），并向 Agent 返回有意义的错误信息以便其自我修正。

**实施步骤**:
1. 捕获所有底层异常，防止 Agent 进程崩溃。
2. 针对网络波动实施指数退避重试策略。
3. 将技术错误代码转化为 LLM 能理解的自然语言描述返回。

**注意事项**: 不要直接将原始的堆栈跟踪信息返回给 LLM，这会消耗大量 Token 且可能导致解析错误。

---

### 实践 5：引入缓存机制优化性能与成本

**说明**: 对于获取静态数据或重复性内容的 Skill（如查询用户资料、获取固定配置），引入缓存机制可以显著降低 API 调用成本和延迟，同时提高 Agent 的响应速度。

**实施步骤**:
1. 识别出具有幂等性的 Skill（即输入相同，输出永远相同的操作）。
2. 在 Skill 执行前先检查缓存层（如 Redis 或内存字典）。
3. 设置合理的缓存过期时间（TTL），以确保数据的时效性。

**注意事项**: 涉及到实时性要求极高的操作（如查询当前股价）不应使用缓存，或者缓存时间应控制在秒级。

---

### 实践 6：建立可观测性与日志记录

**说明**: 在 Agent 系统中，决策过程往往是黑盒。必须记录每次 Skill 调用的详细信息，包括调用时间、输入参数、返回结果、耗时以及错误信息，这对于调试和优化 Agent 行为至关重要。

**实施步骤**:
1. 在 Skill 的入口和出口埋点，记录完整的 Trace ID。
2. 将日志结构化存储，便于后续通过 ELK 或类似工具进行分析。
3. 监控成功率、平均响应时间等关键指标。

**注意事项**: 记录日志时需注意数据隐私，避免将敏感信息（PII）直接明文打印在日志中。

---
## 学习要点

- 基于您提供的来源（Hacker News）和主题（Agent Skills），以下是关于构建高性能 AI Agent 的 5-7 个关键要点总结：
- 工具使用与规划能力是 Agent 区别于传统 Chatbot 的核心分水岭**，Agent 必须具备调用外部 API 和将复杂任务拆解为可执行步骤的能力。
- RAG（检索增强生成）是解决 Agent 幻觉和知识时效性问题的关键技术**，通过挂载外部知识库可显著提升回答的准确性和可信度。
- 反思与自我修正机制能大幅提升 Agent 的任务完成质量**，允许模型检查自己的输出并根据错误进行迭代优化。
- 多智能体协作比单一 Agent 更能处理复杂任务**，通过让不同 Agent 扮演不同角色并相互辩论或协作，可以涌现出更优的解决方案。
- 人类反馈强化学习（RLHF）与对齐是确保 Agent 行为符合人类意图的必要手段**，这能防止模型在执行任务时产生有害或偏离目标的行动。
- 上下文窗口管理和记忆系统是维持长期对话与任务连续性的基础**，Agent 需要有效过滤和存储信息以避免遗忘关键指令。

---
## 常见问题


### 1: 什么是 Agent Skills（智能体技能），它与传统的 AI 提示词有什么区别？

1: 什么是 Agent Skills（智能体技能），它与传统的 AI 提示词有什么区别？

**A**: Agent Skills 是指赋予人工智能智能体执行特定任务或操作的能力。与传统的基于文本的提示词不同，Skills 通常涉及具体的工具调用、API 交互或结构化的工作流程。提示词更多是引导模型生成文本，而 Agent Skills 则允许智能体在环境中执行行动，例如检索实时数据、操作软件工具或调用外部服务。简单来说，提示词是“说”，而 Agent Skills 是“做”。

---



### 2: Hacker News 上关于 Agent Skills 的讨论主要集中在哪些技术趋势上？

2: Hacker News 上关于 Agent Skills 的讨论主要集中在哪些技术趋势上？

**A**: 根据 Hacker News 社区的讨论，关于 Agent Skills 的关注点主要集中在以下几个方面：首先是**工具调用**的标准化，即如何让 LLM 更准确、稳定地连接外部 API；其次是**自主性**，即智能体在没有人类持续干预的情况下规划和执行复杂任务的能力；最后是**多智能体协作**，讨论如何让具备不同技能的智能体协同工作以解决更复杂的问题。开发者们也经常分享关于减少 Skills 执行过程中幻觉和错误的实战经验。

---



### 3: 开发 Agent Skills 时面临的最大技术挑战是什么？

3: 开发 Agent Skills 时面临的最大技术挑战是什么？

**A**: 目前最大的挑战在于**可靠性与错误处理**。LLM 本质上是概率性的，它在生成 JSON 格式的参数或选择正确的工具时可能会出现微小的错误，导致整个 Skills 调用链失败。此外，**上下文窗口的限制**也是一个难题，因为智能体需要记住之前的操作结果和工具定义，这会迅速消耗 Token。开发者需要构建强大的反馈循环机制，让智能体能够根据工具执行的报错信息进行自我修正和重试。

---



### 4: 常见的 Agent Skills 架构模式有哪些？

4: 常见的 Agent Skills 架构模式有哪些？

**A**: 目前业界主流的架构模式主要包括三种：
1.  **ReAct 模式**：即推理+行动，智能体交替进行思考、规划行动步骤、观察结果，再进行下一步行动。
2.  **规划-执行模式**：将任务分为两个阶段，先由一个智能体制定详细的行动计划，再由另一个智能体或执行器具体调用 Skills 去实施。
3.  **工具注册模式**：类似于 LangChain 或 Semantic Kernel 的做法，将函数或 API 注册为工具，由 LLM 根据用户意图动态选择调用哪个 Skill。

---



### 5: 如何评估一个 Agent Skill 的性能是否达标？

5: 如何评估一个 Agent Skill 的性能是否达标？

**A**: 评估 Agent Skill 比评估单纯的文本生成要复杂。通常需要关注以下几个指标：
1.  **成功率**：在给定测试集下，Skill 调用是否成功返回了预期的结果，且没有抛出异常。
2.  **工具选择准确率**：智能体是否在正确的场景下选择了正确的 Skill。
3.  **参数填充准确率**：调用 API 时，生成的参数是否符合 Schema 定义且数值正确。
4.  **端到端效果**：最终是否解决了用户的实际问题。Hacker News 上也常讨论建立专门的“评估数据集”来模拟真实用户场景进行自动化测试。

---



### 6: Agent Skills 的安全性如何保障？

6: Agent Skills 的安全性如何保障？

**A**: 赋予 AI 智能体操作能力会带来新的安全风险。防范措施主要包括：**权限控制**，遵循最小权限原则，只授予智能体完成特定任务所需的最低权限；**沙箱机制**，在隔离的环境中执行不可信的代码或操作；**人工确认**，对于高风险操作（如删除文件、发送邮件、资金转账），必须引入人工审核环节，不能让智能体完全自主执行；以及**输入验证**，严格校验 LLM 传递给 API 的参数，防止注入攻击。

---



### 7: 未来 Agent Skills 的发展方向是什么？

7: 未来 Agent Skills 的发展方向是什么？

**A**: 社区普遍认为未来将朝着**更通用的标准化**发展，例如 OpenAI 的 Function Calling 或 OpenAPI 规范的普及，将降低开发 Skills 的门槛。另一个方向是**自我改进与学习**，智能体不仅能使用 Skills，还能根据执行结果反馈来优化自身的 Skills 使用策略。此外，**多模态 Skills** 也将成为趋势，即智能体能够处理图像、音频等多种数据格式的输入和输出，而不仅仅是文本。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 编写一个 Agent 工具（Tool），能够获取 Hacker News (HN) 首页当前的前 10 篇文章标题和对应的链接。要求能够处理网络请求异常，并在请求失败时返回友好的错误提示。

### 提示**: Hacker News 官方提供了官方 API（基于 Firebase），文档地址通常为 `https://github.com/HackerNews/API`。你需要先获取 `topstories` 列表，然后遍历 ID 获取具体 item 的详情。请使用 Python 的 `requests` 库或 `httpx` 库来实现。

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
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [技能框架](/tags/%E6%8A%80%E8%83%BD%E6%A1%86%E6%9E%B6/) / [能力评估](/tags/%E8%83%BD%E5%8A%9B%E8%AF%84%E4%BC%B0/) / [LLM](/tags/llm/) / [AI Agent](/tags/ai-agent/) / [评测](/tags/%E8%AF%84%E6%B5%8B/) / [Agent Skills](/tags/agent-skills/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
- [Agent Skills：AI 智能体的技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-3.md" >}})
- [Agent Skills：AI 智能体技能框架与训练方法]({{< relref "posts/20260204-hacker_news-agent-skills-8.md" >}})
- [Agent Skills：智能体技能评估与开源框架]({{< relref "posts/20260204-hacker_news-agent-skills-7.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*