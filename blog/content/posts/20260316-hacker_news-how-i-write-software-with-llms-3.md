---
title: "利用大语言模型辅助软件开发的实践方法"
date: 2026-03-16T08:20:50+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "AI编程", "开发实践", "Prompt工程", "代码生成", "Copilot", "软件工程", "工作流"]
categories: ["AI 工程", "效率与方法论"]
source: hacker_news
external_url: https://www.stavros.io/posts/how-i-write-software-with-llms
scenarios: ["大语言模型", "AI/ML项目"]
---

# 利用大语言模型辅助软件开发的实践方法

---

## 基本信息

- **作者**: indigodaddy
- **评分**: 103
- **评论数**: 44
- **链接**: [https://www.stavros.io/posts/how-i-write-software-with-llms](https://www.stavros.io/posts/how-i-write-software-with-llms)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47394022](https://news.ycombinator.com/item?id=47394022)

---
## 代码示例




```python
# 示例1：自动生成API文档
def generate_api_doc(func):
    """
    自动为函数生成API文档
    :param func: 要生成文档的函数
    :return: 带有文档字符串的函数
    """
    # 获取函数名和参数
    func_name = func.__name__
    params = func.__code__.co_varnames[:func.__code__.co_argcount]
    
    # 生成文档字符串
    doc = f"函数: {func_name}\n参数:\n"
    for param in params:
        doc += f"  - {param}\n"
    
    # 添加文档到函数
    func.__doc__ = doc
    return func

# 使用示例
@generate_api_doc
def calculate_discount(price, discount_rate):
    return price * (1 - discount_rate)

print(calculate_discount.__doc__)
```




```python
# 示例2：智能代码补全
def smart_complete(code_context, partial_code):
    """
    基于上下文的智能代码补全
    :param code_context: 已有的代码上下文
    :param partial_code: 部分代码
    :return: 补全后的代码建议
    """
    # 简单的补全规则示例
    if "import" in partial_code:
        return "import os\nimport sys"
    elif "def " in partial_code:
        return "def function_name():\n    pass"
    elif "class " in partial_code:
        return "class ClassName:\n    def __init__(self):\n        pass"
    else:
        return "# 无法提供补全建议"

# 使用示例
context = "正在编写Python脚本"
partial = "def "
print(smart_complete(context, partial))
```




```python
# 示例3：代码质量检查
def check_code_quality(code):
    """
    检查代码质量并给出建议
    :param code: 要检查的代码字符串
    :return: 质量报告字典
    """
    report = {
        "issues": [],
        "suggestions": []
    }
    
    # 检查代码行长度
    for i, line in enumerate(code.split('\n'), 1):
        if len(line) > 79:
            report["issues"].append(f"第{i}行超过79字符")
    
    # 检查函数命名
    if "def " in code:
        if "def bad_name" in code:
            report["suggestions"].append("建议使用更具描述性的函数名")
    
    # 检查文档字符串
    if '"""' not in code and "'''" not in code:
        report["suggestions"].append("建议添加文档字符串")
    
    return report

# 使用示例
code_to_check = """
def bad_name(x):
    return x*2
"""
print(check_code_quality(code_to_check))
```


---
## 学习要点

- 基于Hacker News关于“如何利用LLM编写软件”的讨论，以下是总结出的关键要点：
- 将大型语言模型视为“初级开发者”或“结对编程伙伴”而非全能替代者，人类必须始终承担架构设计与最终代码审查的责任。
- 采用“自上而下”的交互方式，先让模型生成高层架构或伪代码，确认逻辑无误后再要求其填充具体的实现细节。
- 编写清晰、精确且包含上下文的提示词是获得高质量代码的关键，模糊的指令会导致模型产生幻觉或编写出难以维护的代码。
- 利用模型处理繁琐的“苦力活”，如编写单元测试、解释复杂代码、生成正则表达式或进行语法迁移，能显著提升开发效率。
- 在处理私有代码或敏感数据时，务必注意隐私保护，优先使用本地部署的开源模型或具备企业级隐私保障的工具。
- 不要盲目接受模型生成的代码，必须人工审查其中的安全漏洞、逻辑错误以及依赖库的兼容性。

---
## 常见问题


### 1: 在使用大语言模型（LLM）辅助编程时，如何有效地编写提示词以获得高质量的代码？

1: 在使用大语言模型（LLM）辅助编程时，如何有效地编写提示词以获得高质量的代码？

**A**: 编写有效的提示词是成功利用 LLM 的关键。首先，**上下文至关重要**。不要只说“写一个函数”，而应该提供具体的背景信息，例如函数的用途、预期的输入输出类型、以及它如何与现有代码库交互。其次，采用**迭代式交互**。如果生成的代码不完全符合要求，不要放弃，而是指出具体的问题（例如“变量名不符合规范”或“逻辑在边界条件下失败”）并要求模型修改。此外，**明确指定技术栈和约束条件**，比如“使用 Python 的 asyncio 库”或“不要使用外部依赖”。最后，对于复杂的任务，使用**思维链**提示，要求模型先解释逻辑再生成代码，可以显著提高代码的准确性。

---



### 2: LLM 生成的代码往往包含幻觉或安全漏洞，如何进行验证和测试？

2: LLM 生成的代码往往包含幻觉或安全漏洞，如何进行验证和测试？

**A**: 永远不要盲目信任 LLM 生成的代码。验证过程应包含几个步骤：首先是**代码审查**，像审查人类同事的代码一样，逐行检查逻辑，确保没有引入隐蔽的 Bug 或安全漏洞（如 SQL 注入或硬编码的密钥）。其次是**编写单元测试**，利用 LLM 生成测试用例是一个好主意，但必须由开发者确认测试逻辑的正确性，并运行测试以确保代码通过。对于关键业务逻辑，**人工调试**是必不可少的。此外，使用静态代码分析工具（如 linter 或 SAST 工具）来自动检测潜在的错误。如果 LLM 引用了不存在的库或 API（幻觉），必须通过查阅官方文档进行核实。

---



### 3: 在实际工作流中，应该将哪些任务分配给 LLM，哪些保留给人类开发者？

3: 在实际工作流中，应该将哪些任务分配给 LLM，哪些保留给人类开发者？

**A**: 为了最大化效率，应采用**人机协作**的模式。LLM 擅长处理**重复性、模板化或探索性**的任务，例如：编写样板代码、生成正则表达式、解释复杂的遗留代码、编写单元测试、或者尝试新的 API 用法。然而，**核心架构设计、系统安全性、业务逻辑的复杂决策**以及**对最终交付物的责任**必须由人类开发者保留。LLM 是一个“副驾驶”或“智能补全工具”，它可以加速开发过程，但不能替代对系统整体架构的把控和对业务需求的理解。开发者应专注于“做什么”和“为什么”，而让 LLM 辅助解决“怎么做”的语法实现细节。

---



### 4: 如何处理 LLM 生成代码的版权和许可合规性问题？

4: 如何处理 LLM 生成代码的版权和许可合规性问题？

**A**: 这是一个法律灰色地带，需要谨慎处理。首先，了解你所使用的 LLM 服务条款。大多数主流商业 LLM（如 GitHub Copilot 或 ChatGPT）通常声称其生成内容的所有权归用户所有，但这并不保证代码不侵犯现有版权。为了降低风险，**不要直接复制粘贴大段不明来源的代码**。其次，使用**代码扫描工具**检查生成的内容是否与开源库中的代码高度相似，特别是具有传染性许可证（如 GPL）的代码。最佳实践是将 LLM 生成的代码视为参考，进行重写和调整，以确保其原创性并符合公司的知识产权政策。对于敏感项目，建议限制使用基于公共数据训练的开放模型。

---



### 5: 随着项目规模扩大，如何避免 LLM 上下文窗口不足的问题？

5: 随着项目规模扩大，如何避免 LLM 上下文窗口不足的问题？

**A**: LLM 的上下文窗口（一次性能够处理的信息量）是有限的，处理大型项目时确实会遇到瓶颈。解决方法包括：**分块处理**，将大文件或系统拆分为模块，只向 LLM 提供相关的代码片段。**使用 RAG（检索增强生成）技术**，利用本地向量数据库索引代码库，根据问题动态检索最相关的代码片段作为上下文输入给 LLM，而不是一次性发送整个项目。另一种方法是**摘要压缩**，先让 LLM 阅读并总结单个模块的功能，然后在处理跨模块依赖时，仅使用这些摘要作为上下文。此外，利用支持长上下文的最新模型（如 128k 或 200k token 窗口的模型）也是一个直接的解决方案，尽管成本可能会增加。

---



### 6: LLM 辅助编程是否会降低开发者的基础编程能力？

6: LLM 辅助编程是否会降低开发者的基础编程能力？

**A**: 这种担忧是合理的，但取决于使用方式。如果开发者完全依赖 LLM 进行“复制粘贴”而不理解其背后的逻辑，确实会导致技能退化。为了避免这种情况，应将 LLM 视为**学习工具**而非单纯的替代品。当 LLM 生成代码时，开发者应当**深入探究其原理**，问“为什么这样写？”或“有没有更好的方法？”。利用 LLM 解释复杂概念或重构代码，实际上可以加速学习曲线。关键在于保持**主动思考**：开发者必须具备判断代码优劣的能力，这反过来又要求开发者不断巩固自己的基础知识。简而言之，用 LLM 来增强能力，而不是替代思考。

---



### 7: 目前有哪些主流的工具或插件可以集成到 IDE 中使用 LLM？

7: 目前有哪些主流的工具或插件可以集成到 IDE 中使用 LLM？

**A**: 目前市面上有许多成熟的工具可以将 LLM 能

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你需要让 LLM 为一个简单的计算器函数编写单元测试。请设计一个 Prompt，要求 LLM 生成覆盖“正常输入”、“边界条件”和“异常处理”的测试用例，且不包含具体的测试代码逻辑，只提供测试场景描述。

### 提示**:

### 明确告知 LLM 被测函数的输入输出规范。

---
## 引用

- **原文链接**: [https://www.stavros.io/posts/how-i-write-software-with-llms](https://www.stavros.io/posts/how-i-write-software-with-llms)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47394022](https://news.ycombinator.com/item?id=47394022)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [效率与方法论](/categories/%E6%95%88%E7%8E%87%E4%B8%8E%E6%96%B9%E6%B3%95%E8%AE%BA/)
- 标签： [LLM](/tags/llm/) / [AI编程](/tags/ai%E7%BC%96%E7%A8%8B/) / [开发实践](/tags/%E5%BC%80%E5%8F%91%E5%AE%9E%E8%B7%B5/) / [Prompt工程](/tags/prompt%E5%B7%A5%E7%A8%8B/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Copilot](/tags/copilot/) / [软件工程](/tags/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用AI高效编写高质量代码的实践方法]({{< relref "posts/20260206-hacker_news-how-to-effectively-write-quality-code-with-ai-3.md" >}})
- [利用AI高效编写高质量代码的实践方法]({{< relref "posts/20260207-hacker_news-how-to-effectively-write-quality-code-with-ai-15.md" >}})
- [超越智能体编码：AI 编程助手的演进方向]({{< relref "posts/20260208-hacker_news-beyond-agentic-coding-19.md" >}})
- [超越智能体编码：AI 编程助手的演进方向]({{< relref "posts/20260208-hacker_news-beyond-agentic-coding-7.md" >}})
- [编程助手致力解决错误问题]({{< relref "posts/20260203-hacker_news-coding-assistants-are-solving-the-wrong-problem-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*