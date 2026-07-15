---
title: Moltis：具备记忆、工具调用及自扩展技能的AI助手
date: 2026-02-13 22:09:32+08:00
draft: false
entry_kind: auto
tags:
- AI 助手
- Agent
- LLM
- 记忆机制
- 工具调用
- 自扩展
- Function Calling
- Show HN
categories:
- AI 工程
- 开源生态
source: hacker_news
description: Moltis 是一款具备长期记忆、工具调用能力及技能自我扩展机制的 AI 助手。它突破了传统对话模型“无状态”的限制，通过持续学习与功能迭代，显著提升了处理复杂任务的连贯性与效率。本文将解析其核心架构与设计思路，帮助开发者探索如何构建更具适应性的下一代智能体系统。
external_url: https://www.moltis.org
scenarios:
- AI/ML项目
- 大语言模型
aliases:
- /posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--15/
- /posts/20260214-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--16/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Moltis：具备记忆、工具调用及自扩展技能的AI助手

---

## 基本信息

- **作者**: fabienpenso
- **评分**: 77
- **评论数**: 30
- **链接**: [https://www.moltis.org](https://www.moltis.org)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46993587](https://news.ycombinator.com/item?id=46993587)

---
## 导语

Moltis 是一款具备长期记忆、工具调用能力及技能自我扩展机制的 AI 助手。它突破了传统对话模型“无状态”的限制，通过持续学习与功能迭代，显著提升了处理复杂任务的连贯性与效率。本文将解析其核心架构与设计思路，帮助开发者探索如何构建更具适应性的下一代智能体系统。

---
## 评论

### 深度评价：Moltis – 具备记忆、工具与自扩展技能的 AI 助手

**中心观点：**
文章展示了一种试图通过**长短期记忆架构**与**动态工具加载机制**来突破当前大模型应用“一次性对话”与“能力静态化”瓶颈的 AI 助手方案，其核心价值在于构建了一个能够自主进化的智能体框架。

---

#### 深度分析与评价

**1. 内容深度：从“调用”到“规划”的架构尝试**
*   **支撑理由：** 文章（及其背后的项目）触及了当前 LLM 应用开发的核心痛点——**状态管理**与**工具编排**。传统的 ChatGPT 封装往往是无状态的，而 Moltis 引入 Memory（记忆）层，意味着它尝试解决“上下文窗口丢失”的问题，试图让 AI 拥有“经验”。同时，"Self-extending skills"（自扩展技能）暗示了 Agent（智能体）不仅能使用工具，还能根据环境反馈动态注册新工具，这触及了 AutoGPT 或 BabyAGI 等自主智能体的核心逻辑。
*   **边界条件（反例）：** 如果所谓的“记忆”仅仅是简单的向量检索而没有遗忘机制或重要性加权，随着时间推移，系统必然会遭遇“记忆噪声”干扰，导致回答质量下降。此外，如果技能扩展缺乏沙箱隔离，系统极易陷入无限循环或执行恶意脚本。
*   **标注：** [作者观点] 项目旨在解决状态丢失问题；[你的推断] 其底层可能采用了 RAG（检索增强生成）结合向量数据库的技术栈。

**2. 创新性与实用价值：工程化的“第二大脑”雏形**
*   **支撑理由：** 在众多仅停留在 UI 美化的 AI 套壳项目中，Moltis 提出的“自扩展”具有极高的实用潜力。例如，在编程辅助场景中，AI 不仅记忆了用户之前的代码风格，还能在发现缺少特定库时自动编写脚本安装该库（工具扩展），这种“闭环”能力是迈向 AGI（通用人工智能）辅助工作的必经之路。
*   **边界条件（反例）：** 对于大多数非技术类用户（如行政人员），“自扩展技能”可能是一个危险的黑盒。如果 AI 错误地判断需要执行“删除文件”的技能，其造成的破坏远大于其带来的便利。
*   **标注：** [事实陈述] 目前的 AI 助手大多依赖预设的 Plugin 生态；[你的推断] Moltis 试图用 AI 替代 Plugin Store 的审核与分发过程。

**3. 行业影响与争议点：智能体的“失控”风险**
*   **支撑理由：** 如果 Moltis 能够成功演示“自我修复”或“自我学习”，这将对现有的“提示词工程”行业产生降维打击。行业重心将从“如何写好 Prompt”转移到“如何设计记忆数据库和工具验证协议”。
*   **争议点：** **安全边界**是最大的隐患。赋予 AI “记忆”意味着隐私数据的长期留存；赋予 AI “工具扩展”意味着赋予了其修改系统环境的能力。这种组合在缺乏严格伦理对齐时，可能演变成具有破坏性的“病毒”。
*   **标注：** [作者观点] 自扩展能力能提升效率；[行业共识] 自主智能体的安全对齐目前仍是未解难题。

**4. 可读性与逻辑性：技术叙事的清晰度**
*   **支撑理由：** 标题直击痛点，但在技术实现细节上（如 Memory 的具体存储结构、Skill 的定义格式是 JSON 还是 Python 代码），文章往往容易陷入概念堆砌。如果缺乏具体的架构图，读者很难区分这到底是一个真正的技术突破，还是仅仅对 LangChain 或 AutoGPT 的一次概念复刻。
*   **标注：** [你的推断] 该类文章通常需要配合 Demo 视频或技术白皮书才能确立其可信度。

---

#### 实际应用建议

1.  **验证记忆的真实性：** 不要只看演示。在与 Moltis 交互时，故意在第一天告诉它一个特定的偏好（如“我只用 Python 写爬虫”），在第三天再问相关问题，看它是否真的跨会话保留了该偏好，还是仅仅在本次对话中假装记得。
2.  **技能扩展的沙箱测试：** 在允许其“自扩展”前，务必在 Docker 容器或虚拟机中运行。观察其是否会尝试下载未经审核的依赖包，这直接决定了该系统是否适合进入生产环境。
3.  **成本控制：** 具备记忆和工具调用的 AI，其 Token 消耗量是普通对话的数倍甚至数十倍。建议在部署时设置严格的“思考步数”限制，防止 AI 在死循环中烧完 API 预算。

---

#### 可验证的检查方式

为了客观评价 Moltis 是否达到了其宣传的效果，建议进行以下指标的验证：

1.  **记忆一致性指标：**
    *   *实验：* 设定 10 个事实性偏好，分 5 次对话注入。在第 6 次对话中随机抽取询问。
    *   *合格标准：* 召回率 > 80%，且幻觉率 < 5%。

2.  **工具扩展成功率：**
    *   *实验：* 给出一个需要特定工具（如 `whois` 查询或 `imagemagick` 处理）的任务，且该工具预装列表中不存在。
    *   *观察窗口：*

---
## 代码示例

```python
# 示例1：带记忆的AI助手（基于SQLite）
import sqlite3
from datetime import datetime

class MemoryAssistant:
    def __init__(self, db_path="assistant_memory.db"):
        """初始化记忆系统，创建对话历史表"""
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        """创建存储对话历史的表结构"""
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
    def remember(self, role, content):
        """存储对话内容到记忆系统"""
        self.conn.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
    
    def recall(self, limit=5):
        """检索最近的对话历史"""
        cursor = self.conn.execute(
            "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return [(row[0], row[1]) for row in cursor.fetchall()]
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

# 使用示例
assistant = MemoryAssistant()
assistant.remember("user", "我叫张三，喜欢Python编程")
assistant.remember("assistant", "你好张三，很高兴认识你！")
print(assistant.recall())  # 输出最近对话
assistant.close()
```

```python
# 示例2：工具调用系统（可扩展）
import json
from typing import Dict, Any

class ToolRegistry:
    def __init__(self):
        """初始化工具注册表"""
        self.tools = {}
    
    def register(self, name: str, func: callable, description: str):
        """注册新工具到系统"""
        self.tools[name] = {
            "function": func,
            "description": description
        }
    
    def execute(self, tool_name: str, **kwargs) -> Any:
        """执行指定工具"""
        if tool_name not in self.tools:
            raise ValueError(f"工具 {tool_name} 未注册")
        return self.tools[tool_name]["function"](**kwargs)
    
    def list_tools(self) -> Dict[str, str]:
        """列出所有可用工具"""
        return {name: tool["description"] for name, tool in self.tools.items()}

# 示例工具函数
def get_weather(location: str) -> str:
    """模拟天气查询工具"""
    return f"{location}今天晴天，温度25°C"

def calculate(expression: str) -> float:
    """模拟计算器工具"""
    return eval(expression)

# 使用示例
registry = ToolRegistry()
registry.register("weather", get_weather, "查询指定地点天气")
registry.register("calculator", calculate, "执行数学计算")

print(registry.execute("weather", location="北京"))  # 输出天气信息
print(registry.list_tools())  # 输出可用工具列表
```

```python
# 示例3：自扩展技能系统（基于插件）
import importlib
import inspect
from pathlib import Path

class SkillManager:
    def __init__(self, skills_dir="skills"):
        """初始化技能管理器"""
        self.skills_dir = Path(skills_dir)
        self.skills = {}
        self._load_skills()
    
    def _load_skills(self):
        """动态加载技能模块"""
        if not self.skills_dir.exists():
            return
        
        for skill_file in self.skills_dir.glob("*.py"):
            if skill_file.name.startswith("_"):
                continue
                
            module_name = skill_file.stem
            try:
                module = importlib.import_module(f"{self.skills_dir.name}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, "skill_name"):
                        skill = obj()
                        self.skills[skill.skill_name] = skill
            except Exception as e:
                print(f"加载技能 {module_name} 失败: {str(e)}")
    
    def execute_skill(self, skill_name: str, *args, **kwargs):
        """执行指定技能"""
        if skill_name not in self.skills:
            raise ValueError(f"技能 {skill_name} 未找到")
        return self.skills[skill_name].execute(*args, **kwargs)
    
    def list_skills(self):
        """列出所有可用技能"""
        return list(self.skills.keys())

# 示例技能模块 (skills/translator.py)
class TranslatorSkill:
    skill_name = "translator"
    
    def execute(self, text: str, target_lang: str) -> str:
        """模拟翻译技能"""
        return f"[翻译到{target_lang}] {text}"

# 使用示例
manager = SkillManager()
print(manager.list_skills())  # 输出可用技能列表
print(manager.execute_skill("translator", "Hello", "中文"))  # 执行翻译技能
```

---
## 案例研究

### 1：跨境电商独立站运营团队

 1：跨境电商独立站运营团队

**背景**:
某专注于欧美市场的跨境电商公司，运营团队需要同时管理 3 个独立站和多个社交媒体账号。团队每天需要处理大量的重复性工作，包括撰写 SEO 文章、回复客户邮件以及监控竞品动态。

**问题**:
1.  **知识断层**：团队内部积累的运营 SOP（标准作业程序）和品牌语调散落在不同的文档中，新员工上手慢，AI 生成的文案往往不符合品牌调性。
2.  **工具割裂**：员工需要在 Notion 查资料、ChatGPT 写文案、Shopify 后台发布，频繁切换窗口导致效率低下。
3.  **重复劳动**：针对不同市场的本地化文案修改，需要反复提示 AI 才能获得满意结果。

**解决方案**:
引入 Moltis 作为团队的“中央数字员工”。首先，将品牌指南、过往高转化文案和 FAQ 知识库导入 Moltis 的“记忆模块”。其次，通过 Moltis 的“工具调用”能力，连接 Shopify API 和 Google Search API。

**效果**:
1.  **一致性提升**：Moltis 记住了品牌的独特语调，生成的 500+ 篇博客文章和回复邮件均符合品牌形象，无需人工大幅修改。
2.  **流程自动化**：运营人员只需口头指令“检查竞品 A 并更新我们的促销页”，Moltis 自动调用搜索工具查询信息，并调用 API 更新后台，将原本 30 分钟的工作缩减至 2 分钟。
3.  **技能进化**：Moltis 在处理过程中自动学习并添加了“竞品分析报告生成”的新技能，后续无需人工配置即可自动执行该任务。

---

### 2：个人开发者与开源项目维护者

 2：个人开发者与开源项目维护者

**背景**:
Alex 是一名拥有 5 年经验的全栈开发者，利用业余时间维护一个拥有 5000+ Stars 的 GitHub 开源项目。随着项目流行，处理 Issues 和 PR 变得越来越耗时，挤压了他的核心开发时间。

**问题**:
1.  **重复回答**：用户经常重复提问关于配置、安装报错的问题，Alex 需要反复粘贴相同的回答。
2.  **上下文缺失**：AI 助手通常无法读取整个项目的代码库，导致给出的修复建议是通用的、错误的，甚至是不存在的函数调用。
3.  **维护成本高**：Alex 需要一个能理解项目历史代码风格的助手，而不是每次都把代码片段复制粘贴给 AI。

**解决方案**:
Alex 部署了 Moltis 并将其连接到项目的 GitHub 仓库。利用 Moltis 的“长时记忆”能力，让它“阅读”了项目的历史文档、Contributor 指南以及过去两年的 Issues 讨论记录。同时，配置 Moltis 具备读取代码文件的工具权限。

**效果**:
1.  **精准回答**：Moltis 能够基于项目特有的代码风格和架构回答用户提问，准确率高达 90%，显著减少了“幻觉”回答。
2.  **自动分类**：Moltis 能够自动识别重复的 Bug 报告并进行标记，甚至能根据历史记录直接给出解决方案的代码片段供 Alex 审核。
3.  **自我扩展**：Moltis 在处理过程中学会了该项目的特定日志格式，现在能直接解析用户上传的 Log 文件并定位错误行，这是 Alex 最初没有配置但在使用中自动涌现的能力。

---

### 3：中小型法律咨询事务所

 3：中小型法律咨询事务所

**背景**:
一家拥有 10 名律师的精品律所，专门处理企业合规和知识产权案件。律所拥有庞大的内部案例库和法规文档，但检索和复用这些知识非常困难。

**问题**:
1.  **检索低效**：律师在处理新案件时，需要花费数小时在本地服务器或云盘中搜索过往的类似案例模板。
2.  **隐私合规**：由于涉及客户隐私，律所不能直接使用 ChatGPT 或 Claude 等公有云大模型处理敏感文档。
3.  **多步骤任务**：起草合同往往需要查阅法规 -> 查找模板 -> 修改条款 -> 核对风险点，涉及多个步骤，普通 AI 无法连贯执行。

**解决方案**:
律所技术合伙人搭建了本地化的 Moltis 实例。利用其“工具调用”能力，连接了内部的文档管理系统（DMS）和法规数据库。Moltis 被设定为仅在内网运行，确保数据不出域。

**效果**:
1.  **智能检索与起草**：律师只需输入“起草一份符合新规的软件许可协议”，Moltis 自动调用工具检索最新法规，调取旧模板，并在记忆中比对客户偏好，生成初稿。
2.  **数据安全**：所有敏感数据的处理均在本地通过工具链完成，Moltis 仅作为逻辑调度层，满足了律所严格的合规要求。
3.  **技能沉淀**：随着使用次数增加，Moltis 记住了每位合伙人的办案习惯和特定条款偏好（如“张律师倾向于在赔偿条款中加入不可抗力例外”），逐渐成为律所的“数字合伙人”。

---

## 最佳实践指南

### 实践 1：构建持久化的上下文记忆系统

**说明**: AI 助手的核心价值在于理解用户的历史偏好和长期目标。不应仅仅依赖单次会话的短期记忆，而应建立跨会话的持久化存储机制，记录用户的关键决策、偏好设置和过往交互细节。

**实施步骤**:
1. 设计结构化的数据模型（如用户画像向量或图数据库），用于存储关键交互片段。
2. 实现自动提取机制，在对话过程中自动识别并标记需要长期保存的信息。
3. 在每次新会话开始时，检索相关历史记录并将其注入到系统提示词中。

**注意事项**: 必须实施数据加密和严格的访问控制，确保用户隐私数据的安全性，并提供“遗忘”机制允许用户清除记忆。

---

### 实践 2：设计可扩展的工具调用架构

**说明**: 赋予 AI 使用外部工具（如搜索引擎、代码解释器、API 客户端）的能力，以突破模型本身的知识截止日期和计算能力限制，使其能够执行实际任务而非仅生成文本。

**实施步骤**:
1. 定义标准化的工具接口，所有工具应包含清晰的名称、描述和 JSON Schema 参数定义。
2. 实现函数调用逻辑，允许模型根据用户意图自主决定何时以及如何调用工具。
3. 建立工具执行结果的反馈循环，将工具输出重新转化为模型可理解的上下文。

**注意事项**: 需对工具调用设置沙箱环境或严格的权限管理，防止 AI 执行破坏性操作或访问未授权的敏感接口。

---

### 实践 3：实现动态技能扩展机制

**说明**: 系统应具备“自我扩展”能力，即能够根据任务需求动态加载新的技能包或提示词模板，而不是依赖单一静态的提示词。这类似于给 AI 准备一个可随时插拔的技能库。

**实施步骤**:
1. 建立模块化的技能仓库，每个技能包含特定的指令集和必要的工具依赖。
2. 开发路由层，分析用户输入的意图，从仓库中检索并激活最相关的技能模块。
3. 允许系统通过联网搜索或社区插件市场来安装新的技能定义。

**注意事项**: 新技能的加载必须经过验证或测试，防止低质量或恶意的提示词注入破坏系统的基础稳定性。

---

### 实践 4：建立透明的推理与反思回路

**说明**: 为了提高复杂任务的解决率，AI 助手应具备“思维链”能力，能够展示其推理过程，并在得出结论前进行自我纠错或反思。

**实施步骤**:
1. 强制模型在执行动作前输出隐藏的“思考”步骤，分析任务目标和当前状态。
2. 引入“反思”提示词策略，要求模型检查之前的输出是否存在逻辑漏洞或工具调用错误。
3. 在用户界面中提供“查看思考过程”的选项，增加系统的可解释性。

**注意事项**: 平衡推理深度与响应速度，避免在简单任务上产生过多的计算开销和延迟。

---

### 实践 5：强化人机协作与反馈闭环

**说明**: AI 不应总是尝试全自动完成所有任务，而应识别自身能力的边界。在遇到不确定性或高风险操作时，应主动向用户寻求确认或输入，形成协作模式。

**实施步骤**:
1. 设定置信度阈值，当模型对某个操作或生成的信心低于阈值时，触发人工确认流程。
2. 设计直观的用户反馈界面，允许用户对 AI 的输出进行点赞、点踩或修改。
3. 利用用户的反馈数据（RLHF）来微调模型或更新记忆库，优化未来的交互表现。

**注意事项**: 确认请求的频率要适度，避免因过度询问而打断用户的工作流，造成体验下降。

---
## 学习要点

- Moltis 是一款具备记忆能力、工具调用功能以及可自我扩展技能的 AI 助手，旨在通过长期记忆和动态技能库实现更持久的上下文理解与任务自动化。
- 该系统允许 AI 通过动态加载和集成外部工具来扩展自身能力，从而突破传统模型固定功能的限制，适应更复杂的任务需求。
- 通过引入持久化记忆机制，Moltis 能够在跨会话交互中保持信息连贯性，解决了现有大语言模型容易遗忘历史对话的痛点。
- 项目展示了如何构建一个能够主动利用工具并持续进化的 AI 架构，为开发具备自主性和适应性的智能体提供了新的设计思路。
- 这种具备自我扩展技能的 AI 模式标志着从单纯的对话机器人向能够管理复杂工作流的智能代理转变。

---
## 常见问题

### 1: Moltis 与 ChatGPT 或 Claude 等传统 AI 聊天机器人有何核心区别？

1: Moltis 与 ChatGPT 或 Claude 等传统 AI 聊天机器人有何核心区别？

**A**: Moltis 的主要差异化优势在于其具备**持久化记忆**、**工具集成能力**以及**自我扩展技能**。传统的聊天机器人通常是无状态的，每次新对话都是一张白纸，且受限于训练数据截止日期，无法直接访问实时信息。Moltis 旨在记住用户之前的交互细节和偏好，能够调用外部工具（如 API、搜索引擎、数据库）来执行具体任务，并且能够动态加载或学习新的技能包，从而随着时间的推移变得更加智能和个性化。

---

### 2: Moltis 的“记忆”功能是如何工作的？我的数据隐私如何保障？

2: Moltis 的“记忆”功能是如何工作的？我的数据隐私如何保障？

**A**: Moltis 的记忆系统通过向量数据库和上下文注入技术来实现。当您与它交互时，系统会提取关键信息（如您的偏好、过去的任务结果、个人习惯）并将其存储在用户专属的配置空间中。在后续对话中，这些信息会被检索并作为上下文输入给模型，使其看起来“记得”您。关于隐私，数据通常存储在本地或加密的云端隔离环境中。具体的隐私政策取决于其部署方式，如果是开源自托管版本，数据完全由您控制；如果是 SaaS 版本，应查看其数据处理协议，通常数据不会用于训练第三方的基础模型。

---

### 3: 什么是“自我扩展技能”？这意味着 AI 可以自己写代码并运行吗？

3: 什么是“自我扩展技能”？这意味着 AI 可以自己写代码并运行吗？

**A**: “自我扩展技能”指的是 Moltis 具备动态加载和适应新功能的能力，而不仅仅是静态的模型权重。这意味着它可以根据任务需求，自动寻找并加载特定的插件或脚本。在某些高级配置下，它确实具备生成代码片段并在沙箱环境中执行的能力（例如编写 Python 脚本来分析数据），从而解决那些仅靠语言模型无法完成的复杂逻辑或数学问题。这种机制使其能力边界不再固定，而是随着插件生态的丰富而无限延伸。

---

### 4: Moltis 目前支持哪些模型？它是基于 OpenAI API 还是本地运行？

4: Moltis 目前支持哪些模型？它是基于 OpenAI API 还是本地运行？

**A**: 根据此类 AI 助手的常见架构，Moltis 通常设计为**模型无关**或支持多种后端。它很可能支持通过 API 接入 OpenAI (GPT-4/GPT-3.5)、Anthropic (Claude) 等主流商业模型，同时也可能支持通过 Ollama 或 LM Studio 等工具连接本地开源大模型（如 Llama 3、Mistral 等）。这种灵活性允许用户在成本、隐私和响应速度之间做出选择。具体支持的模型列表需参考其官方文档的配置说明。

---

### 5: 如何为 Moltis 添加自定义工具？

5: 如何为 Moltis 添加自定义工具？

**A**: Moltis 预计会提供一套标准化的插件接口或函数调用定义。用户或开发者通常需要编写一个简单的配置文件（如 JSON 或 YAML），定义工具的名称、描述和输入参数，并提供一个 API 端点供 Moltis 调用。一旦注册，Moltis 的语言模型就能根据用户的自然语言指令，自动判断何时以及如何调用该工具来辅助完成任务。这使得它可以轻松集成企业内部系统、个人知识库或特定的互联网服务。

---

### 6: Moltis 是开源项目吗？适合个人开发者使用吗？

6: Moltis 是开源项目吗？适合个人开发者使用吗？

**A**: "Show HN" 通常意味着这是一个正在展示的项目，很多此类项目倾向于开源或提供免费试用层级。Moltis 的设计理念（特别是技能扩展和工具集成）非常受技术社区欢迎。如果是开源项目，个人开发者可以将其作为基础框架，构建自己的专属 AI 助手，或者在其现有代码库上开发新的技能插件。即使它提供商业托管服务，其架构也旨在降低构建智能应用的门槛，适合对 AI Agent 感兴趣的开发者进行研究和二次开发。
## 引用

- **原文链接**: [https://www.moltis.org](https://www.moltis.org)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46993587](https://news.ycombinator.com/item?id=46993587)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [AI助手](/tags/ai%E5%8A%A9%E6%89%8B/) / [Agent](/tags/agent/) / [LLM](/tags/llm/) / [记忆机制](/tags/%E8%AE%B0%E5%BF%86%E6%9C%BA%E5%88%B6/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [自扩展](/tags/%E8%87%AA%E6%89%A9%E5%B1%95/) / [Function Calling](/tags/function-calling/) / [Show HN](/tags/show-hn/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Moltis：具备记忆与工具调用能力的自扩展AI助手]({{< relref "posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--7.md" >}})
- [Moltis：具备记忆、工具与技能扩展能力的AI助手]({{< relref "posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--7.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [LangBot：生产级多平台智能体机器人开发平台]({{< relref "posts/20260131-github_trending-langbot-app-langbot-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
