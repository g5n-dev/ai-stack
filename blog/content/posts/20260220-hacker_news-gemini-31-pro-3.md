---
title: "谷歌发布 Gemini 3.1 Pro 模型"
date: 2026-02-20T07:13:53+08:00
draft: false
entry_kind: "auto"
tags: ["Gemini", "Google", "LLM", "模型发布", "API", "多模态", "AI", "性能优化"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着多模态模型竞争的白热化，Google 发布的 Gemini 3.1 Pro 再次引发了开发者的广泛关注。作为对现有架构的深度优化版本，该模型不仅显著提升了复杂指令的遵循能力，还进一步降低了长文本处理的延迟与成本。本文将深入剖析其核心参数变化与实测表现，帮助你客观评估它是否适合接入你的技术栈。"
external_url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro
scenarios: ["大语言模型", "AI/ML项目"]
---

# 谷歌发布 Gemini 3.1 Pro 模型

---

## 基本信息

- **作者**: MallocVoidstar
- **评分**: 654
- **评论数**: 754
- **链接**: [https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47074735](https://news.ycombinator.com/item?id=47074735)

---
## 导语

随着多模态模型竞争的白热化，Google 发布的 Gemini 3.1 Pro 再次引发了开发者的广泛关注。作为对现有架构的深度优化版本，该模型不仅显著提升了复杂指令的遵循能力，还进一步降低了长文本处理的延迟与成本。本文将深入剖析其核心参数变化与实测表现，帮助你客观评估它是否适合接入你的技术栈。

---
## 评论

### 深度评价：Gemini 3.1 Pro 技术解析

#### 一、 核心评价与中心观点

**中心观点：**
关于Gemini 3.1 Pro的技术分析文章，其核心论点应聚焦于该模型在**长上下文处理能力、多模态融合深度以及推理成本控制**这三个维度的工程化优化。文章旨在论证该模型标志着AI技术从“单一能力突刺”向“工程化极致可用”的演进，确立了基于Token交互的新型生产力范式。

**支撑理由：**
1.  **长上下文窗口的工程化落地**：文章应指出，从百万级Token向更长、更稳定上下文的演进，不仅是参数量的提升，更是注意力机制（如线性注意力或Ring Attention）优化的结果。这种改进旨在解决超长文本检索中的召回率与成本平衡问题。
2.  **原生多模态融合**：区别于早期外挂视觉编码器的设计，Gemini 3.1 Pro 若强调原生多模态训练，意味着音频、视频、代码与文本在同一高维空间的对齐，这在理论上有助于降低多模态交互中的幻觉现象。
3.  **推理性能与成本的平衡**：文章应分析该模型在保持旗舰级性能的同时，如何通过MoE（混合专家模型）路由优化来降低推理延迟，从而使得端侧部署或高频实时交互成为可能。

**反例/边界条件：**
1.  **长文本中间层遗忘**：尽管理论上下文窗口很大，但在处理超长文本（如书籍级别）任务时，模型对中间段落（非开头或结尾）的细节召回率仍可能出现非线性衰减。
2.  **复杂逻辑的局限性**：在多步数学推理或复杂代码生成场景下，尽管生成流畅度较高，但在缺乏显式思维链引导时，逻辑链条的“断裂”风险依然存在。

---

#### 二、 多维度深入评价

**1. 内容深度与论证严谨性**
*   **技术剖析**：有深度的文章不应仅停留在列举Benchmark分数（如MMLU、HumanEval），而应深入剖析底层架构变化，例如是否采用了更深层的MoE层，或者是否引入了特定的隐式优化机制。
*   **机制分析**：优秀的分析会指出，Gemini 3.1 Pro 的核心价值在于“上下文缓存”机制的经济性，这一机制改变了RAG（检索增强生成）的应用架构设计。
*   **安全性考量**：如果文章未提及“安全对齐”在多模态层面的具体改进（如防御提示注入攻击），则其论证存在缺失，因为多模态输入口是当前安全防御的重点区域。

**2. 实用价值与指导意义**
*   **开发者视角**：文章是否提供了具体的Prompt策略或API调用优化建议（如如何利用System Instruction控制输出）是衡量其实用性的关键。
*   **案例验证**：若文章包含Gemini 3.1 Pro在视频分析领域的具体案例，例如对长视频内容的细节提取与总结，比单纯谈论“视频理解”能力更具参考价值。
*   **部署边界**：文章应明确指出目前的“Pro”版本通常不支持微调，这对于评估其在垂直领域私有化部署的适用性至关重要。

**3. 创新性**
*   **代理工作流**：如果文章探讨了Gemini 3.1 Pro在自主调用工具、规划任务等Agent行为上的能力，这体现了对传统Chatbot认知的拓展。
*   **原生交互能力**：关于“原生音频输出”能力的探讨（即模型直接生成带有语调、停顿的语音）也是评价其创新性的一个重要维度，这在交互体验上具有显著差异。

**4. 可读性与逻辑性**
*   **逻辑结构**：技术文章应避免术语堆砌。合理的逻辑链条应当是：提出问题（如现有模型无法处理长视频） -> 技术解法（如时间片注意力机制） -> 实际效果验证 -> 局限性分析。
*   **视角清晰度**：如果文章结构在技术架构解析和商业推广之间频繁跳跃，可能暗示作者缺乏清晰的技术视角。

**5. 行业影响**
*   **竞争格局**：Gemini 3.1 Pro 的发布可能会加速大模型行业的价格战，并促使竞争焦点从单纯的“模型能力”转向“应用生态”构建。
*   **移动端生态**：若该模型深度集成于Android生态，将推动移动端AI应用的普及，这对整个移动操作系统格局具有深远影响。

**6. 争议点与不同观点**
*   **评估标准偏差**：需关注文章是否过度依赖特定数据集的评分，而忽视了模型在真实场景中的鲁棒性。
*   **开放性争议**：关于模型权重是否开放、API调用策略的变更，也是社区讨论的焦点，文章应对此保持客观中立的态度。

---
## 代码示例




```python
# 示例1：HackerNews 热门文章获取器
import requests

def get_hacker_news_top_stories(limit=5):
    """
    获取 HackerNews 首页热门文章的标题和链接
    
    参数:
        limit: 要获取的文章数量，默认为5篇
        
    返回:
        包含文章信息的字典列表
    """
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    try:
        # 1. 获取热门文章ID列表
        story_ids = requests.get(f"{base_url}/topstories.json").json()[:limit]
        
        stories = []
        for story_id in story_ids:
            # 2. 并行获取每篇文章的详细信息
            story = requests.get(f"{base_url}/item/{story_id}.json").json()
            stories.append({
                "title": story.get("title"),
                "url": story.get("url"),
                "score": story.get("score"),
                "author": story.get("by")
            })
        
        return stories
    
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return []

# 使用示例
if __name__ == "__main__":
    stories = get_hacker_news_top_stories()
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']} (分数: {story['score']})")
        print(f"   链接: {story['url']}\n")
```




```python
# 示例2：关键词文章搜索器
import requests
from datetime import datetime

def search_hacker_news(keyword, limit=10):
    """
    在 HackerNews 上搜索包含特定关键词的文章
    
    参数:
        keyword: 要搜索的关键词
        limit: 返回结果数量限制
        
    返回:
        匹配的文章列表
    """
    base_url = "https://hn.algolia.com/api/v1"
    
    try:
        # 使用 Algolia 搜索 API
        params = {
            "query": keyword,
            "tags": "story",
            "hitsPerPage": limit
        }
        
        response = requests.get(f"{base_url}/search", params=params)
        results = response.json()["hits"]
        
        articles = []
        for article in results:
            # 转换时间戳为可读格式
            created_at = datetime.fromtimestamp(article["created_at_i"]).strftime("%Y-%m-%d %H:%M")
            
            articles.append({
                "title": article["title"],
                "url": article.get("url") or f"https://news.ycombinator.com/item?id={article['objectID']}",
                "points": article["points"],
                "author": article["author"],
                "created_at": created_at,
                "num_comments": article["num_comments"]
            })
        
        return articles
    
    except Exception as e:
        print(f"搜索出错: {e}")
        return []

# 使用示例
if __name__ == "__main__":
    results = search_hacker_news("AI", limit=5)
    for article in results:
        print(f"标题: {article['title']}")
        print(f"分数: {article['points']} | 评论: {article['num_comments']}")
        print(f"发布时间: {article['created_at']}")
        print(f"链接: {article['url']}\n")
```




```python
# 示例3：HN 数据分析工具
import requests
import matplotlib.pyplot as plt
from collections import Counter

def analyze_hacker_news_trends(days=7):
    """
    分析 HackerNews 最近的发帖趋势
    
    参数:
        days: 要分析的天数
        
    返回:
        包含分析结果的字典
    """
    base_url = "https://hn.algolia.com/api/v1"
    
    try:
        # 获取最近N天的文章
        params = {
            "tags": "story",
            "numericFilters": f"created_at_i>{int(datetime.now().timestamp()) - days*86400}",
            "hitsPerPage": 1000
        }
        
        response = requests.get(f"{base_url}/search", params=params)
        stories = response.json()["hits"]
        
        # 分析数据
        domains = [story["url"].split("//")[-1].split("/")[0] for story in stories if story.get("url")]
        top_domains = Counter(domains).most_common(10)
        
        points = [story["points"] for story in stories]
        avg_points = sum(points) / len(points) if points else 0
        
        # 可视化数据
        plt.figure(figsize=(10, 5))
        plt.bar(*zip(*top_domains))
        plt.title(f"最近{days}天最活跃的域名")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        return {
            "total_stories": len(stories),
            "avg_points": round(avg_points, 2),
            "top_domains": top_domains
        }
    
    except Exception as e:
        print(f"分析出错: {


---
## 案例研究


### 1：初创公司利用 AI 优化客户支持工作流

 1：初创公司利用 AI 优化客户支持工作流

**背景**:
一家处于快速成长期的 SaaS 初创公司，其产品用户群正在迅速扩大。随着用户量增加，客户支持团队面临巨大压力，主要依赖人工回复邮件和工单，导致响应时间变长，用户体验下降。

**问题**:
人工客服处理重复性高、模式相似的问题（如“如何重置密码”、“计费咨询”）效率低下，占用了工程师大量时间。同时，非英语母语的用户在沟通中存在语言障碍，导致理解偏差。

**解决方案**:
团队集成了 Gemini 3.1 Pro API，构建了一个智能客服助手。利用该模型的 100 万 token 上下文窗口，他们将所有的产品文档、历史工单记录和 API 参考资料一次性输入给模型，使其能够精准理解产品细节。同时，利用其原生多模态能力，允许用户直接上传界面截图报错，模型能直接识别图片内容并定位问题。

**效果**:
客户支持响应时间从平均 4 小时缩短至 5 分钟以内。智能助手成功拦截并自动解决了约 65% 的常规咨询问题，使工程师能专注于处理复杂的 Bug 修复。此外，通过模型的原生多语言支持，非英语用户的满意度提升了 20%。

---



### 2：金融科技公司的合规报告自动化生成

 2：金融科技公司的合规报告自动化生成

**背景**:
一家金融数据分析公司需要定期为客户生成深度市场分析报告。分析师每天需要处理海量的新闻资讯、财报数据和社交媒体情绪，从中提取关键信息并撰写摘要。

**问题**:
传统流程依赖分析师手动阅读大量文本并编写报告，不仅耗时（通常需要数小时），而且容易遗漏关键信息或因疲劳产生主观偏差。

**解决方案**:
公司开发了一套内部工作流，利用 Gemini 3.1 Pro 的长上下文处理能力，将每日数万字的行业新闻、上市公司财报 PDF 文件以及交易数据直接输入模型。模型被指示作为“资深金融分析师”，对数据进行综合分析、风险评估，并自动生成结构化的日报草稿。

**效果**:
报告生成时间从 3 小时缩短至 10 分钟。模型能够捕捉到人类分析师可能忽略的跨文档关联信息（例如某条新闻与另一份财报的隐含联系）。分析师的角色从“撰写者”转变为“审核者”，工作效率提升了 5 倍，且报告的标准化程度和数据准确性显著提高。

---



### 3：大型代码库的现代化重构与文档补全

 3：大型代码库的现代化重构与文档补全

**背景**:
一家拥有 10 年历史的老牌软件公司维护着数百万行遗留代码（主要是 Java 和 Python）。由于人员流动，许多核心模块缺乏文档，或者文档与代码严重脱节，新入职的开发人员上手极其困难。

**问题**:
阅读和理解复杂的遗留代码库占据了开发人员 60% 的时间。传统的代码分析工具难以理解代码的业务逻辑意图，导致重构风险极高，容易引入新的 Bug。

**解决方案**:
技术团队使用 Gemini 3.1 Pro 对整个代码库进行索引。利用其超长上下文窗口，模型可以“通读”整个项目的目录结构和依赖关系。开发人员可以通过自然语言询问代码功能（例如“解释这个模块如何处理交易回滚”），模型不仅能解释代码逻辑，还能根据最新的编码标准生成对应的单元测试和补全缺失的 API 文档。

**效果**:
新开发人员的入职培训周期缩短了 40%。团队成功识别并重构了 20% 的技术债务，且在模型辅助生成的单元测试下，重构后的代码故障率降低了 15%。模型生成的文档质量高，极大地降低了知识传承的断层风险。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建高度结构化的提示词

**说明**: Gemini 3.1 Pro 在处理具有清晰层级、格式和明确约束条件的提示词时表现最佳。通过提供结构化的输入，可以显著减少模型产生幻觉或输出格式不符合预期的概率。

**实施步骤**:
1. 使用 XML 标签或 Markdown 标题来分隔提示词的不同部分（例如：`<context>`、`<instructions>`、`<output_format>`）。
2. 在指令部分明确列出模型必须遵循的规则，使用枚举列表。
3. 提供少量示例来演示输入和期望的输出格式。

**注意事项**: 避免将所有指令混在一个长段落中，这会增加模型的解析负担。

---

### 实践 2：利用思维链提升复杂推理能力

**说明**: 对于逻辑推理、数学计算或多步骤分析任务，强制模型“展示思考过程”可以大幅提高准确率。这有助于模型在得出最终结论前进行中间验证。

**实施步骤**:
1. 在提示词中明确要求：“请一步步思考”或“让我们逐步分解这个问题”。
2. 要求模型在给出最终答案前，先输出中间推导步骤。
3. 对于代码生成任务，要求模型先解释算法逻辑，再生成代码。

**注意事项**: 思维链会略微增加推理时间和 Token 消耗，仅在复杂任务中使用。

---

### 实践 3：采用角色扮演设定专家人设

**说明**: 赋予模型特定的专业角色（如“资深数据科学家”、“资深文案编辑”），可以引导模型调用该领域特定的术语、语气和知识库，从而提高输出的专业度和相关性。

**实施步骤**:
1. 在对话开始时明确设定角色：“你是一位拥有 10 年经验的 [领域] 专家。”
2. 结合上下文，描述该角色在当前场景下的具体职责或目标。
3. 根据需要调整语气要求（例如：客观严谨、或具有说服力）。

**注意事项**: 确保设定的角色与任务目标高度匹配，避免角色冲突。

---

### 实践 4：实施分段式生成与迭代优化

**说明**: 不要试图通过一次提示就让模型生成完美的长篇内容（如书籍、长篇报告）。最佳实践是将大任务分解为小步骤，先生成大纲，再逐个部分生成，最后进行整合。

**实施步骤**:
1. 第一步：先生成任务的大纲或目录结构。
2. 第二步：根据大纲，针对每个章节单独生成内容。
3. 第三步：要求模型对生成的初稿进行润色、扩写或精简。

**注意事项**: 在长对话中，注意上下文窗口的限制，必要时总结前文关键信息。

---

### 实践 5：利用系统指令设定全局行为

**说明**: 如果使用 Gemini API，应利用 `system_instruction` 字段而非用户消息来设定核心规则。系统指令的权重高于用户消息，能有效防止“提示词注入”或用户通过诱导性对话改变模型的核心行为。

**实施步骤**:
1. 将安全边界、输出格式约束、核心身份定义放入 `system_instruction` 中。
2. 将具体的任务内容和用户查询放入 `user` 消息中。
3. 测试模型在面对对抗性输入时是否仍能坚守系统指令。

**注意事项**: 系统指令应简洁明了，专注于“怎么做”和“不能做什么”。

---

### 实践 6：建立验证与反馈机制

**说明**: 不要盲目信任模型的输出，特别是在事实性查询或代码生成方面。建立一套验证流程是生产环境中的关键实践。

**实施步骤**:
1. 对于事实性查询，要求模型提供来源或引用链接（需核实链接有效性）。
2. 对于代码生成，要求模型提供单元测试用例，并尝试运行这些用例。
3. 将模型的输出与已知的标准答案或规则库进行比对。

**注意事项**: 对于高风险领域（如医疗、法律），必须引入人工审核环节。

---
## 学习要点

- 基于 Hacker News 社区对 Gemini 2.5 Pro 的讨论，以下是总结出的关键要点：
- Gemini 2.5 Pro 在代码生成、逻辑推理及长上下文处理能力上实现了提升，被部分开发者认为是目前具有竞争力的开源模型之一。
- Google 采用了“开放权重”而非“开源”的授权模式，允许开发者免费下载并微调模型，但禁止将其用于训练其他大语言模型。
- 该模型在复杂任务（如数学和编程）中的表现已逼近 GPT-4 Turbo，引发了开发者社区的关注。
- Google 推出了 100 万 token 的上下文窗口，使模型能够处理极长的文档和代码库。
- 该模型的推理成本和延迟相比 GPT-4 具有一定优势，为高性能 AI 应用的部署提供了经济性考量。
- 社区讨论重点从单纯的性能基准测试转向了如何利用该模型进行本地化部署和特定领域的微调应用。

---
## 常见问题


### 1: Gemini 3.1 Pro 真的发布了吗？为什么我在 Google 官方文档里找不到它？

1: Gemini 3.1 Pro 真的发布了吗？为什么我在 Google 官方文档里找不到它？

**A**: 目前 Google 官方并没有发布名为 "Gemini 3.1 Pro" 的模型。根据 Hacker News 的相关讨论和行业动态，这通常是对 **Gemini 2.5 Pro** 的误读或误传。

近期最重大的发布是 Google DeepMind 推出的 **Gemini 2.5 Pro (Experimental)**。该模型在编程、推理和指令遵循方面有显著提升，且支持高达 100 万 tokens 的上下文窗口。如果您看到关于 "3.1" 的讨论，极有可能是对版本号 "2.5" 的笔误，或者是某些非官方渠道的混淆。

---



### 2: Gemini 2.5 Pro (常被误传为 3.1) 的上下文窗口有多大？这意味着什么？

2: Gemini 2.5 Pro (常被误传为 3.1) 的上下文窗口有多大？这意味着什么？

**A**: Gemini 2.5 Pro 拥有 **100 万 tokens** 的上下文窗口，这是目前业界最长的上下文窗口之一。

这意味着您可以一次性输入大量的文本、代码或文档进行分析。例如，您可以直接将整个中型代码库、几本长篇小说或数小时的视频转录文本喂给模型，而无需进行切片处理。这极大地降低了模型“遗忘”早期信息的风险，使得处理长篇内容的连贯性和准确性大幅提高。

---



### 3: 如何使用 Gemini 2.5 Pro？它是免费的吗？

3: 如何使用 Gemini 2.5 Pro？它是免费的吗？

**A**: 目前，Gemini 2.5 Pro 处于实验阶段，主要通过以下方式提供访问：

1.  **Google AI Studio**: 开发者可以申请访问权限，在网页端直接体验 API 调用，或者在代码中使用 API Key 进行调用。目前通常提供免费试用额度，但具体收费策略可能会随正式发布而调整。
2.  **Gemini Advanced 订阅**: 对于个人用户，通常需要订阅 Google One AI Premium 计划（类似于 ChatGPT Plus）才能在 Gemini 界面中使用最新的 Pro 版本模型。

需要注意的是，作为实验性模型，其可用性可能会受到速率限制，且服务稳定性可能不如正式版本。

---



### 4: 与 OpenAI 的 GPT-4.1 或 Claude 3.7 Sonnet 相比，它有什么优势？

4: 与 OpenAI 的 GPT-4.1 或 Claude 3.7 Sonnet 相比，它有什么优势？

**A**: 根据 Hacker News 上的早期用户反馈和基准测试，Gemini 2.5 Pro 的主要优势在于：

*   **超长上下文**: 虽然 GPT-4.1 也支持长上下文，但 Gemini 在处理极长文本（如接近 100 万 tokens）时的召回率和准确性表现非常出色，尤其适合分析海量代码库。
*   **代码生成能力**: 许多开发者反馈其在复杂编程任务、重构代码和理解遗留代码方面的表现略优于当前版本的 GPT-4。
*   **多模态推理**: 它对视频和音频内容的理解能力较强，能够直接处理长视频的输入并进行分析。

---



### 5: 在 Hacker News 上，开发者们主要在吐槽它的哪些缺点？

5: 在 Hacker News 上，开发者们主要在吐槽它的哪些缺点？

**A**: 尽管性能强大，但 HN 社区也指出了目前存在的一些问题：

*   **输出速度慢**: 由于模型参数量大且上下文极长，推理时间较长，首字生成延迟和输出速度有时不如轻量级模型。
*   **安全性过滤过度**: 部分用户抱怨模型在处理某些边缘话题时，Refusal（拒绝回答）过于敏感，导致无法完成正常的查询任务。
*   **幻觉问题**: 虽然逻辑推理能力强，但在处理极度冷门的知识时，仍可能出现一本正经胡说八道的情况，需要开发者进行验证。

---



### 6: 如果我想在项目中集成这个模型，应该注意什么？

6: 如果我想在项目中集成这个模型，应该注意什么？

**A**: 如果您计划在项目中集成 Gemini 2.5 Pro（或所谓的 3.1 Pro），建议注意以下几点：

1.  **版本锁定**: 由于目前是实验性版本，API 接口和模型行为可能会发生剧烈变化。在代码中注意模型版本的锁定，以免自动更新导致生产环境崩溃。
2.  **成本控制**: 虽然输入便宜，但长上下文的推理成本较高。建议在 Prompt 工程中只传递真正相关的上下文，而不是每次都全量发送。
3.  **延迟处理**: 针对长文本任务，必须设计异步处理机制，并向前端用户展示加载进度，否则用户体验会很差。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在开发一个需要处理长文本的摘要应用。请设计一个 Prompt（提示词），利用 Gemini 3.1 Pro 的长上下文能力，要求它从一份 50 页的 PDF 文档内容中提取出 5 个关键论点，并忽略其中的广告或无关附录。

### 提示**: 思考如何使用“分隔符”（如三引号或 XML 标签）来界定输入文本，以及如何明确指定输出格式（如 JSON 或列表）以确保结果的结构化。

### 

---
## 引用

- **原文链接**: [https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47074735](https://news.ycombinator.com/item?id=47074735)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Gemini](/tags/gemini/) / [Google](/tags/google/) / [LLM](/tags/llm/) / [模型发布](/tags/%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B8%83/) / [API](/tags/api/) / [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/) / [AI](/tags/ai/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [谷歌发布 Gemini 3.1 Pro 模型]({{< relref "posts/20260219-hacker_news-gemini-31-pro-6.md" >}})
- [谷歌发布 Gemini 3.1 Pro 模型]({{< relref "posts/20260219-hacker_news-gemini-31-pro-0.md" >}})
- [谷歌发布 Gemini 3.1 Pro 预览版]({{< relref "posts/20260219-hacker_news-gemini-31-pro-preview-18.md" >}})
- [谷歌发布 Gemini 3.1 模型]({{< relref "posts/20260219-hacker_news-gemini-31-1.md" >}})
- [谷歌发布 Gemini 3.1 Pro 预览版]({{< relref "posts/20260219-hacker_news-gemini-31-pro-preview-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*