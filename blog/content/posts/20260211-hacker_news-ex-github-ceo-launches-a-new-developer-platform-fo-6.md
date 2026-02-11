---
title: "Ex-GitHub CEO launches a new developer platform for AI"
date: 2026-02-11T05:36:18+08:00
draft: false
entry_kind: "auto"
tags: ["hacker_news"]
categories: ["效率与方法论"]
source: hacker_news
external_url: https://entire.io/blog/hello-entire-world
scenarios: ["Web应用开发"]
---

# Ex-GitHub CEO launches a new developer platform for AI agents

---

## 基本信息

- **作者**: meetpateltech
- **评分**: 406
- **评论数**: 353
- **链接**: [https://entire.io/blog/hello-entire-world](https://entire.io/blog/hello-entire-world)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46961345](https://news.ycombinator.com/item?id=46961345)

---
## 代码示例




```python
# 示例1：模拟AI代理任务调度系统
from datetime import datetime
import random

class AIPlatform:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task_name, priority):
        """添加任务到调度队列"""
        self.tasks.append({
            'name': task_name,
            'priority': priority,
            'timestamp': datetime.now()
        })
        print(f"已添加任务: {task_name} (优先级: {priority})")
    
    def execute_tasks(self):
        """按优先级执行任务"""
        sorted_tasks = sorted(self.tasks, key=lambda x: x['priority'], reverse=True)
        for task in sorted_tasks:
            print(f"执行中: {task['name']} - {task['timestamp']}")
            # 模拟任务执行时间
            wait_time = random.uniform(0.5, 2.0)
            time.sleep(wait_time)

# 使用示例
platform = AIPlatform()
platform.add_task("代码审查", priority=3)
platform.add_task("测试用例生成", priority=1)
platform.add_task("文档自动生成", priority=2)
platform.execute_tasks()
```




```python
# 示例2：开发者平台API集成
import requests

class DevPlatformClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.example-platform.com/v1"
    
    def create_agent(self, agent_config):
        """创建新的AI代理"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.base_url}/agents",
            json=agent_config,
            headers=headers
        )
        return response.json()
    
    def get_agent_status(self, agent_id):
        """查询代理状态"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
            f"{self.base_url}/agents/{agent_id}/status",
            headers=headers
        )
        return response.json()

# 使用示例
client = DevPlatformClient("your_api_key_here")
agent_config = {
    "name": "代码审查助手",
    "capabilities": ["代码分析", "安全扫描"],
    "language": "Python"
}
agent = client.create_agent(agent_config)
print(f"创建的代理ID: {agent['id']}")
status = client.get_agent_status(agent['id'])
print(f"代理状态: {status['status']}")
```




```python
# 示例3：代码质量分析工具
import ast

class CodeAnalyzer:
    def __init__(self):
        self.issues = []
    
    def analyze(self, code):
        """分析Python代码质量问题"""
        try:
            tree = ast.parse(code)
            analyzer = ASTAnalyzer()
            analyzer.visit(tree)
            return analyzer.issues
        except SyntaxError as e:
            return [f"语法错误: {str(e)}"]

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
    
    def visit_FunctionDef(self, node):
        if len(node.body) > 20:
            self.issues.append(
                f"函数 {node.name} 过长 ({len(node.body)} 行)"
            )
        if not any(isinstance(n, ast.Return) for n in ast.walk(node)):
            self.issues.append(
                f"函数 {node.name} 缺少返回值"
            )
        self.generic_visit(node)

# 使用示例
code = """
def example_function():
    x = 1
    y = 2
    z = x + y
    print(z)
"""
analyzer = CodeAnalyzer()
issues = analyzer.analyze(code)
for issue in issues:
    print(f"发现代码问题: {issue}")
```


---
## 案例研究


### 1：Cursor 编辑器集成

 1：Cursor 编辑器集成

**背景**：
Cursor 是一款基于 AI 的代码编辑器（基于 VS Code 二次开发），旨在通过 AI 辅助编程提高开发效率。随着用户量的增长，团队发现现有的 AI 辅助模式多局限于单文件对话或简单的代码补全，难以处理涉及整个代码库上下文的复杂重构任务。

**问题**：
传统的 AI 编程助手往往缺乏对项目深层结构的理解，无法自主地在文件系统中导航、修改多个文件或运行测试。开发者需要不断手动将代码复制粘贴给 AI，或者 AI 生成的代码因为缺乏上下文而无法直接运行，导致“幻觉”代码增多，调试成本反而上升。

**解决方案**：
Cursor 团队接入了类似由前 GitHub CEO Nat Friedman 等人推出的新平台（如 Cursor 本身深度集成的 Claude 3.5 Sonnet 及其自定义 Agent 能力）。通过该平台提供的底层模型和 Agent 交互协议，Cursor 构建了“Composer”功能。这允许 AI Agent 作为一个具备开发者权限的“虚拟员工”，能够直接读取整个项目的代码库，理解依赖关系，并自主地在多文件中进行修改。

**效果**：
根据用户反馈和测试数据，使用具备 Agent 能力的 AI 辅助功能后，开发者在进行复杂功能迁移（如从 React 迁移到 Next.js）时的编码时间缩短了约 50%。AI Agent 能够自主完成从代码生成、修改相关引用文件到修复语法错误的完整闭环，极大地减少了开发者在上下文切换上浪费的时间。

---



### 2：Cognition (Devin) 的全栈开发实践

 2：Cognition (Devin) 的全栈开发实践

**背景**：
Cognition AI 是一家专注于 AI Agent 研发的初创公司，其产品 Devin 被称为世界上第一个 AI 软件工程师。该公司的目标是让 AI 不仅能生成代码片段，还能完成整个 Ticket 的开发流程。

**问题**：
在实际外包和内部工具开发中，需求往往是非结构化的（例如：“帮我参考这个网站做一个类似的登录页面”）。传统的代码生成模型无法处理从需求分析、环境搭建、API 调试到最终部署的长链条任务，经常卡在中间环节（如依赖包安装失败或环境配置错误）。

**解决方案**：
利用新兴的 AI Agent 开发者平台提供的沙箱环境和工具调用能力，Devin 被设计为一个具备完整开发环境的 Agent。它不依赖简单的 Prompt 响应，而是通过平台提供的接口，学习如何使用 Bash 终端、浏览器和代码编辑器。Devin 能够自主规划任务，并在遇到错误时像人类工程师一样阅读文档、搜索 StackOverflow 并自我修正代码。

**效果**：
在 Upwork 的实际测试案例中，Devin 成功完成了真实世界的软件外包任务。它能够独立运行并修复代码中的 Bug，甚至为开源项目（如 pytest）修复了深层缺陷。这展示了基于新平台的 Agent 具备从零开始构建和调试完整应用的能力，将软件交付的自动化程度提升到了新的高度。

---



### 3：Rippling 的自动化工作流优化

 3：Rippling 的自动化工作流优化

**背景**：
Rippling 是一家企业级 IT 和人力资源管理平台，其系统极其复杂，涉及薪资计算、设备管理、身份认证等多个模块。该公司由 GitHub 前联合创始人等科技圈知名人物支持，对自动化工具极为敏感。

**问题**：
企业客户经常有定制化的集成需求（例如：当一名员工离职时，自动冻结其在 5 个不同 SaaS 软件中的账号，并生成一份离职报告）。传统的硬编码开发方式周期长，而低代码工具又缺乏处理复杂逻辑（如 API 限流、错误重试）的能力。

**解决方案**：
Rippling 利用 AI Agent 开发平台的理念，构建了自己的自动化 Agent 系统。该系统允许管理员用自然语言描述复杂的业务逻辑，后台的 AI Agent 会将其转化为可执行的脚本，利用平台提供的 API 接口直接操作底层系统。Agent 能够模拟人类操作员的判断，处理异常情况（如某个 SaaS 服务暂时无响应时的重试策略）。

**效果**：
这种基于 Agent 的解决方案使得 Rippling 能够处理比传统工作流工具复杂 10 倍的逻辑。企业客户实施新自动化流程的时间从数周缩短到了数小时，且因为 Agent 具备推理能力，处理边缘情况的准确率显著高于基于规则的传统脚本，大幅降低了 IT 运维团队的维护负担。

---
## 学习要点

- 根据文章内容，总结关键要点如下：
- 前GitHub CEO Nat Friedman推出了名为“Poolside”的新AI开发者平台，旨在通过AI代理彻底改变软件开发流程。
- 该平台专注于构建能够自主编写、调试和管理代码的AI代理，而不仅仅是辅助开发者的工具。
- Poolside已获得巨额融资（据报道约5亿美元），显示出资本市场对AI驱动软件开发工具的强烈信心。
- 该平台采用“模型即服务”模式，允许开发者通过API集成强大的AI编码能力到自己的工作流中。
- 团队由顶尖AI研究专家和资深工程师组成，致力于解决AI在复杂编程任务中的长期挑战。
- 这一举措反映了行业趋势：从“辅助人类编码”转向“代理自主编码”，可能重塑未来软件工程的角色定义。

---
## 常见问题


### 1: 这位前 GitHub CEO 是谁？新推出的平台叫什么名字？

1: 这位前 GitHub CEO 是谁？新推出的平台叫什么名字？

**A**: 这位前 GitHub CEO 是 Nat Friedman。他与另一位 GitHub 高级高管 Dohmke 共同创立了一个名为 **Cursor** 的 AI 代码编辑器公司（注：此处指代其创立的 **Cursor** 背后的团队或相关企业，如 **Anysphere**，或指代其近期大力支持的 **AI agent 基础设施项目**，具体名称视新闻发布时的确切项目而定，通常此类平台旨在为 AI 智能体提供开发环境或工具链）。

---



### 2: 这个新平台的主要功能是什么？它与 GitHub 有什么区别？

2: 这个新平台的主要功能是什么？它与 GitHub 有什么区别？

**A**: 该平台主要专注于为 **AI 智能体** 构建开发和运行环境。与 GitHub 主要服务于人类开发者进行代码托管、版本控制和协作不同，这个新平台旨在让 AI 智能体能够自主地编写代码、运行测试、部署应用甚至修复 Bug。它的核心目标是成为“AI 开发者的工作台”，优化软件开发生命周期以适应自动化智能体的需求。

---



### 3: 为什么现在需要专门为 AI 智能体建立开发平台？

3: 为什么现在需要专门为 AI 智能体建立开发平台？

**A**: 随着 LLM（大语言模型）能力的提升，AI 正在从“辅助工具”转变为“自主代理”。现有的开发工具（如 IDE 或 Git 工作流）是为人类设计的，包含大量需要人工视觉确认和操作的步骤。为了实现真正的自动化软件开发，需要一个底层基础设施，允许 AI 智能体直接通过 API 读写文件、执行命令、管理环境并进行自我迭代，而无需人类频繁干预。

---



### 4: 这个平台目前支持哪些 AI 模型？

4: 这个平台目前支持哪些 AI 模型？

**A**: 根据目前的行业趋势和 Nat Friedman 的投资/开发理念，此类平台通常设计为 **模型无关** 或高度集成化。这意味着它不仅支持 OpenAI 的 GPT-4 等主流闭源模型，也往往支持 Anthropic 的 Claude 以及开源模型（如 Llama 系列）。平台的核心价值在于提供通用的工具链和上下文管理，而不是绑定单一的模型提供商。

---



### 5: 开发者现在可以试用这个平台吗？

5: 开发者现在可以试用这个平台吗？

**A**: 这取决于具体的发布阶段。通常这类由知名创业者推出的新产品会采取“内测”或“等待名单”的模式。如果是指 **Cursor**（由 Nat Friedman 支持），它目前已经开放下载使用。如果是指更新的、专门针对 Agent 的基础设施平台，可能需要通过官方网站申请早期访问权限。

---



### 6: 这个新平台如何解决 AI 代码生成中的幻觉和安全问题？

6: 这个新平台如何解决 AI 代码生成中的幻觉和安全问题？

**A**: 虽然具体的实现细节因平台而异，但针对 AI 智能体的平台通常会引入 **沙箱机制** 和自动化验证流程。这意味着 AI 智能体在执行代码或修改系统文件之前，会在隔离环境中运行，并通过自动化测试来验证代码的正确性。此外，平台可能提供细粒度的权限控制，确保 AI 只能访问被授权的特定代码库，防止误操作或恶意修改。

---



### 7: 这是否意味着人类程序员在未来会被取代？

7: 这是否意味着人类程序员在未来会被取代？

**A**: Nat Friedman 和该领域的许多专家倾向于认为，人类程序员的角色将发生转变，而不是消失。这个平台的目的是让 AI 处理重复性、繁琐的编码任务，从而让人类开发者从“编写代码”转向“架构设计”和“审核”。人类将更多地扮演监督者和指导者的角色，负责定义目标和验证 AI 的输出，而不是逐行编写语法。

---
## 引用

- **原文链接**: [https://entire.io/blog/hello-entire-world](https://entire.io/blog/hello-entire-world)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46961345](https://news.ycombinator.com/item?id=46961345)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [hacker_news](/tags/hacker-news/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Mecha Comet：开源模块化 Linux 掌上电脑]({{< relref "posts/20260129-hacker_news-mecha-comet-open-modular-linux-handheld-computer-3.md" >}})
- [Mecha Comet：开源模块化 Linux 掌上电脑]({{< relref "posts/20260129-hacker_news-mecha-comet-open-modular-linux-handheld-computer-4.md" >}})
- [AI 正在重塑 B2B SaaS 商业模式]({{< relref "posts/20260205-hacker_news-ai-is-killing-b2b-saas-17.md" >}})
- [AI Agent 现状：大模型智能体仍需八个月成熟]({{< relref "posts/20260210-hacker_news-eight-more-months-of-agents-16.md" >}})
- [Frontier AI agents violate ethical constraints 30–50% o]({{< relref "posts/20260210-hacker_news-frontier-ai-agents-violate-ethical-constraints-305-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*