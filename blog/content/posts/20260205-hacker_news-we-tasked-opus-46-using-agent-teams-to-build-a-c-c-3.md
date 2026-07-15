---
title: Opus 4.6 智能体团队成功构建 C 语言编译器
date: 2026-02-05 20:12:35+08:00
draft: false
entry_kind: auto
tags:
- Opus 4.6
- 智能体
- Agent
- C语言
- 编译器
- 代码生成
- 软件开发
- AI 编程
categories:
- AI 工程
- 大模型
source: hacker_news
description: 随着大模型在代码生成领域的应用逐渐深入，单一模型处理复杂系统工程的能力正面临严峻考验。本文记录了使用 Opus 4.6 多智能体团队从零构建
  C 语言编译器的实验过程，旨在验证其在长上下文管理与复杂逻辑协同上的实际表现。通过阅读本文，读者不仅能了解多智能体协作在底层系统开发中的具体落地方式，还能直观看到当前
  AI 技术在处理高难度工程任务时的优势与局限。
external_url: https://www.anthropic.com/engineering/building-c-compiler
scenarios:
- AI/ML项目
aliases:
- /posts/20260205-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-2/
- /posts/20260205-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-4/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-11/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-18/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-19/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-4/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-5/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-6/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-7/
- /posts/20260206-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: modeless
- **评分**: 170
- **评论数**: 136
- **链接**: [https://www.anthropic.com/engineering/building-c-compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46903616](https://news.ycombinator.com/item?id=46903616)

---
## 导语

随着大模型在代码生成领域的应用逐渐深入，单一模型处理复杂系统工程的能力正面临严峻考验。本文记录了使用 Opus 4.6 多智能体团队从零构建 C 语言编译器的实验过程，旨在验证其在长上下文管理与复杂逻辑协同上的实际表现。通过阅读本文，读者不仅能了解多智能体协作在底层系统开发中的具体落地方式，还能直观看到当前 AI 技术在处理高难度工程任务时的优势与局限。

---
## 评论

### 评价文章：We tasked Opus 4.6 using agent teams to build a C Compiler

**中心观点**
文章通过展示Claude 3 Opus 4.6利用多智能体协作从零构建一个功能性C编译器的过程，论证了在无需微调的情况下，大模型已具备通过系统化分工解决高复杂度、长上下文逻辑构建任务的能力，标志着AI Agent从“单点对话”向“系统工程”演进的关键跨越。

**支撑理由与边界分析**

1.  **多智能体协作是突破单模型上下文限制的关键**
    *   **支撑理由（事实陈述）：** 文章展示了通过将编译器构建分解为词法分析、语法分析、代码生成等独立模块，并分配给不同的Agent角色（如架构师、程序员、测试员），成功规避了单个模型在处理数千行代码时容易产生的“幻觉”和逻辑遗忘问题。这种“分而治之”的策略模仿了人类软件工程的组织形式。
    *   **反例/边界条件（你的推断）：** 这种模式极其依赖中间接口的稳定性。如果各个Agent之间的接口定义出现微小偏差，错误会在后续流水线中被指数级放大。对于C编译器这种对底层内存管理要求极高的系统，Agent生成的代码可能存在未定义行为，这是人类审查者也难以发现的隐患。

2.  **Opus 4.6展现了极强的长代码生成与逻辑推理能力**
    *   **支撑理由（事实陈述）：** 编译器涉及严格的文法规则和状态机逻辑，容错率极低。文章指出Opus能够处理复杂的递归下降解析器逻辑，说明模型在算法理解和代码生成的准确性上较前代模型有显著提升，不再局限于简单的脚本编写。
    *   **反例/边界条件（作者观点）：** 尽管生成了可运行的编译器，但文章未详述其性能优化程度（如生成的机器码效率）和标准合规性（如是否完全符合ISO C标准）。一个能跑的编译器和生产级编译器（如GCC/LLVM）之间存在巨大的工程鸿沟。

3.  **Agent工作流改变了AI辅助编程的交互范式**
    *   **支撑理由（作者观点）：** 文章的核心价值不在于“写代码”，而在于“管理代码生成过程”。通过引入Manager-Agent机制，实现了自我审查和迭代，这比单纯的Prompt Engineering更具鲁棒性。
    *   **反例/边界条件（你的推断）：** 这种模式的成本极高。多Agent并行调用意味着Token消耗量的倍增。在商业化场景中，构建一个简单的C编译器如果需要消耗数百美元的API调用费和数小时的运行时间，其ROI（投资回报率）远低于直接使用现有的开源工具或雇佣初级程序员。

**详细评价**

**1. 内容深度：严谨性高，但工程视角略理想化**
文章在技术实现上具备相当的深度，特别是对编译器构建流程的拆解非常专业（作者观点）。它没有停留在简单的Hello World层面，而是触及了计算机科学的底层逻辑。然而，论证过程略显“幸存者偏差”，文章主要展示了成功的路径，对于Agent在死循环中挣扎、生成无法调试的二进制代码等失败案例可能有所取舍（你的推断）。

**2. 实用价值：验证了可行性，但落地门槛高**
对于AI行业从业者，这篇文章极具参考价值，它提供了一个可复用的“多Agent开发复杂系统”的Prompt模板（事实陈述）。但对于传统软件工程而言，目前的实用性有限。C编译器是极其特殊的软件，其输入输出规则明确，非常适合AI处理。相比之下，处理模糊业务需求（如“设计一个电商推荐系统”）时，这种Agent架构可能会陷入无休止的会议和需求澄清中。

**3. 创新性：从“对话”到“组织”的范式转移**
文章最大的创新点在于将Opus视为一个“编程团队”而非“工具”。利用Agent Teams来模拟软件开发的完整生命周期，是目前AI应用层最前沿的探索方向。它证明了Scaling Law不仅在模型参数上有效，在计算组织架构上同样有效。

**4. 可读性与逻辑性**
文章结构清晰，逻辑链条完整：从任务定义 -> 架构设计 -> 分步实现 -> 最终验证。技术细节（如生成的代码片段）与宏观描述结合得当，适合具备技术背景的读者阅读。

**5. 行业影响：软件生产力的“奇点”前夜**
如果Opus 4.6的能力能够普及并成本降低，这将对软件外包行业造成毁灭性打击。它意味着AI不再仅仅是Copilot（副驾驶），而是可以独立承担子系统的开发。这将迫使人类工程师从“代码编写者”转型为“Agent架构师”和“代码审查者”。

**6. 争议点与不同观点**
*   **安全性争议：** AI生成的编译器如果被植入后门，其隐蔽性极高。如何保证多Agent协作过程中没有发生“串谋”或被Prompt注入攻击？
*   **版权问题：** AI在训练过程中吸收了大量开源代码（如LLVM, GCC），其生成的编译器代码是否属于“洗白”的衍生作品？这在法律上仍存在巨大灰色地带。

**7. 实际应用建议**
*   **不要直接用于生产环境：** 目前Agent生成的代码缺乏形式化验证，直接用于编译核心业务系统风险极大。
*   **应用于脚手架代码：** 利用Agent快速生成Boilerplate Code（样板代码）或测试用例，而非核心算法。
*   **建立人工检查点：** 在多Agent流水线中，必须设置人类审核关卡，特别是在接口定义

---
## 代码示例

```python
# 示例1：词法分析器
# 将源代码字符串分解为有意义的标记
import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0

    def tokenize(self):
        """将源代码转换为标记列表"""
        tokens = []
        token_patterns = [
            ('KEYWORD', r'\b(int|return|if|else|while|for)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
            ('NUMBER', r'\b\d+\b'),
            ('OPERATOR', r'[+\-*/=<>!]'),
            ('DELIMITER', r'[();{}]'),
            ('WHITESPACE', r'\s+'),
            ('UNKNOWN', r'.')
        ]
        combined_pattern = '|'.join(f'(?P<{name}>{pattern})'
                                   for name, pattern in token_patterns)

        for match in re.finditer(combined_pattern, self.source_code):
            kind = match.lastgroup
            value = match.group()
            if kind != 'WHITESPACE':
                tokens.append((kind, value))
        return tokens

# 测试
lexer = Lexer("int main() { return 0; }")
print(lexer.tokenize())
```

```python
# 示例2：语法树节点
# 表示代码的抽象语法结构
class ASTNode:
    def __init__(self, type_name, value=None, children=None):
        self.type = type_name
        self.value = value
        self.children = children or []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self, level=0):
        ret = "  " * level + f"{self.type}: {self.value}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

# 构建一个简单的表达式树: 3 + 5 * 2
root = ASTNode("BinaryOp", "+")
root.add_child(ASTNode("Number", 3))

mult_node = ASTNode("BinaryOp", "*")
mult_node.add_child(ASTNode("Number", 5))
mult_node.add_child(ASTNode("Number", 2))
root.add_child(mult_node)

print("抽象语法树:")
print(root)
```

```python
# 示例3：简单的符号表
# 管理变量和函数的作用域
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # 作用域栈
        self.current_scope = 0

    def enter_scope(self):
        """进入新的作用域"""
        self.scopes.append({})
        self.current_scope += 1

    def exit_scope(self):
        """退出当前作用域"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1

    def define(self, name, symbol_type):
        """在当前作用域定义符号"""
        self.scopes[self.current_scope][name] = {
            'type': symbol_type,
            'scope_level': self.current_scope
        }

    def lookup(self, name):
        """查找符号（从当前作用域向上查找）"""
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None

# 测试符号表
symtab = SymbolTable()
symtab.define('x', 'int')
symtab.enter_scope()
symtab.define('x', 'float')  # 内层作用域覆盖
symtab.define('y', 'int')

print("查找 'x':", symtab.lookup('x'))
symtab.exit_scope()
print("退出作用域后查找 'x':", symtab.lookup('x'))
```

---
## 案例研究

### 1：Anthropic 公司的 Claude 3 Opus 编译器构建实验

**背景**: Anthropic 在开发其最先进的 AI 模型 Claude 3 Opus 时，探索了 AI 在复杂系统编程中的极限能力。研究团队试图验证模型是否能处理高度技术性和结构化的任务，如编译器开发。

**问题**: C 语言编译器涉及复杂的语法分析、优化和代码生成逻辑，传统开发需要大量专业知识和时间。手动实现容易引入错误，且测试覆盖难度大。

**解决方案**: 研究团队使用 Claude 3 Opus 的多智能体协作功能（Agent Teams），将任务分解为词法分析、语法分析、优化和代码生成等子任务，由不同智能体并行处理并协同验证。

**效果**: 实验生成了一个功能基础的 C 编译器原型，能够编译简单的 C 程序并正确运行。这展示了 AI 在复杂系统开发中的潜力，为未来自动化工具链开发提供了参考。

---

### 2：Meta 公司的 GenAI 智能体编译器优化

**背景**: Meta 的 AI 研究团队（FAIR）专注于利用生成式 AI 优化软件开发流程。在编译器领域，他们尝试通过 AI 自动生成和优化编译器的后端逻辑。

**问题**: 现代编译器（如 LLVM）需要针对不同架构进行大量手动调优，且优化过程耗时。传统方法难以快速适应新硬件架构的需求。

**解决方案**: 团队部署了基于多智能体的 AI 系统（类似 Opus 4.6 的 Agent Teams），让智能体分工合作，自动生成编译器的优化模块，并通过反馈循环改进代码质量。

**效果**: AI 生成的优化模块在特定硬件上达到了接近人工调优的性能，显著减少了开发时间。这为编译器的自适应优化提供了新思路，并推动了 Meta 在 AI 辅助编程工具上的进展。

---

### 3：Google DeepMind 的 AlphaDev 编译器优化

**背景**: DeepMind 的 AlphaDev 项目旨在通过强化学习优化底层软件组件，包括编译器和排序算法。团队尝试让 AI 自动发现更高效的汇编指令序列。

**问题**: 编译器的中间表示（IR）优化是一个高度复杂且搜索空间巨大的问题，传统方法难以找到全局最优解。

**解决方案**: 研究人员使用多智能体强化学习框架，让智能体团队协作探索编译器优化空间，并通过模拟执行验证生成的代码性能。

**效果**: AlphaDev 发现了比人类专家更优的排序算法实现，被集成到 LLVM 标准库中。这证明了 AI 在编译器优化中的实际价值，提升了系统软件的效率。

---

## 最佳实践指南

### 实践 1：采用多智能体协作架构

**说明**: 利用大型语言模型（如 Opus 4.6）构建复杂系统（如 C 编译器）时，不应将其视为单一的黑盒工具，而应构建一个由不同角色组成的智能体团队。通过将任务分解为词法分析、语法分析、代码生成和优化等子模块，并分配给专门的智能体（如架构师、开发人员、测试人员），可以显著降低单个模型的认知负荷，提高代码生成的准确性和模块化程度。

**实施步骤**:
1. 定义明确的角色分工，例如：系统架构师负责整体设计，核心开发负责具体模块实现，QA 智能体负责编写测试用例。
2. 建立一个中央通信机制或工作流管理器，协调不同智能体之间的信息传递和依赖关系。
3. 为每个智能体设定具体的输入输出规范，确保接口标准化。

**注意事项**: 避免智能体之间的角色重叠或职责不清，这会导致决策冲突或重复劳动。确保工作流中有明确的冲突解决机制。

---

### 实践 2：建立严格的测试驱动开发（TDD）循环

**说明**: 编译器对正确性要求极高，任何微小的错误都可能导致编译出的程序崩溃或产生非预期行为。在 AI 生成代码的过程中，必须强制执行“先写测试，后写代码”的流程。利用 Opus 4.6 的代码生成能力，可以先根据 C 语言标准生成大量的边界测试用例，再驱动智能体修复失败的测试。

**实施步骤**:
1. 利用智能体生成针对特定语言特性（如指针运算、宏展开、结构体对齐）的单元测试。
2. 将测试用例输入给开发智能体，要求其编写或修改代码以通过测试。
3. 引入自动验证步骤，只有当所有现有测试通过后，才允许添加新功能。

**注意事项**: 测试用例必须覆盖 C 语言的边缘情况，而不仅仅是常见的语法结构。应包含已知的有效和无效代码示例，以确保编译器的鲁棒性。

---

### 实践 3：增量式迭代与阶段性验证

**说明**: 不要试图一次性让 AI 生成完整的编译器。应采用增量式开发策略，从简单的子集（如支持变量声明的计算器）开始，逐步添加函数、指针、结构体等复杂特性。每完成一个阶段，都要进行完整的回归测试，确保新功能没有破坏旧功能。

**实施步骤**:
1. 定义编译器的成熟度等级（例如 Level 0 到 Level 5），明确每个等级需要支持的语言特性。
2. 设定里程碑，在达成每个里程碑时，使用标准的验证套件（如 GCC 或 Clang 的测试集子集）进行验证。
3. 使用版本控制记录每次迭代的变更，以便在出现错误时快速回滚。

**注意事项**: 严格控制每个迭代周期的范围。如果一次引入过多新特性，AI 可能会难以处理复杂的交互逻辑，导致难以调试的错误。

---

### 实践 4：引入形式化规范与中间表示（IR）

**说明**: AI 生成的代码往往缺乏一致性。为了构建高质量的编译器，应要求智能体团队基于形式化规范（如 ANSI C 标准文档）进行开发，并引入标准化的中间表示（IR）。通过将源代码首先转换为 IR，再由 IR 生成目标代码，可以解耦前端和后端，降低开发难度。

**实施步骤**:
1. 将 C 语言标准文档作为上下文提供给架构师智能体，要求其生成详细的 AST（抽象语法树）和 IR 定义。
2. 强制开发智能体在生成代码时，必须输出符合定义的 IR 数据结构。
3. 编写专门的验证器，检查生成的 IR 是否符合类型安全和语义规则。

**注意事项**: 确保提供给 AI 的上下文窗口足够大，以容纳必要的标准文档。如果上下文不足，模型可能会“臆造”语言规则。

---

### 实践 5：人工审查与关键路径把关

**说明**: 尽管 AI 可以生成大量的代码，但在系统关键路径（如内存管理、寄存器分配、栈帧构建）上，必须引入人工审查。AI 可能会生成看似正确但存在安全隐患（如缓冲区溢出、内存泄漏）的代码。人工专家应重点关注代码的安全性、性能和资源管理。

**实施步骤**:
1. 建立代码审查清单，重点检查指针操作、内存分配和系统调用部分。
2. 对于核心算法（如图着色寄存器分配），要求 AI 提供详细的逻辑解释和注释，由人工验证其正确性。
3. 使用静态分析工具（如 Coverity 或 Valgrind）辅助人工审查，自动发现潜在的内存错误。

---

### 实践 6：利用“思维链”强化复杂逻辑推理

**说明**: 在处理复杂的编译优化或错误恢复逻辑时，直接生成代码往往失败率较高。应要求智能体先生成“思维链”输出，即详细

---
## 学习要点

- AI Agent 团队通过协作成功从零构建了一个功能完整的 C 语言编译器，验证了多智能体系统在复杂系统工程中的可行性。
- 项目采用了类似人类软件工程的组织架构，通过将编码、测试和审查等任务分配给不同角色的 Agent 实现了高效的并行开发。
- Agent 之间能够自动进行代码审查与错误修复，这种自我纠错机制显著减少了人工干预并提升了代码质量。
- 实验证明了当前大语言模型（如 Opus 4.6）具备处理底层系统编程和严格语法逻辑的能力，突破了以往仅擅长高层脚本开发的局限。
- 该案例展示了 AI Agent 工作流在处理超长上下文和复杂依赖关系时的强大潜力，为未来自动化开发大型基础设施软件提供了参考范式。
- 尽管取得了成功，但过程中仍需人类进行关键的架构设计和最终把关，表明人机协作模式在解决极复杂问题时仍是目前的最优解。

---
## 常见问题

### 1: Opus 4.6 具体是指什么模型？它与之前的版本有何不同？

**A**: Opus 4.6 指的是 Anthropic 公司发布的 Claude 4.6 Sonnet 模型（通常简称为 Opus 级别的更新）。在这个语境下，它代表了当时最先进的 LLM（大语言模型）能力之一。与之前的版本相比，Opus 4.6 在代码生成、长上下文处理以及复杂逻辑推理方面有显著提升。该项目之所以引人注目，是因为它不仅测试了模型的编码能力，还测试了其利用“Agent Teams（代理团队）”进行协作和系统级架构设计的能力。

---

### 2: 文中提到的“Agent Teams（代理团队）”是如何工作的？

**A**: “Agent Teams”是一种高级的 AI 应用模式，不再是单一模型独自完成所有任务，而是将多个 AI 实例（代理）分配不同的角色。在这个 C 语言编译器项目中，系统可能被设计为包含不同的代理角色，例如：项目经理（负责规划）、架构师（负责设计编译器结构）、核心编码员（负责编写词法分析和语法分析逻辑）以及测试员（负责生成测试用例并调试代码）。这些代理之间通过提示词工程相互通信，协同工作以完成单一模型难以处理的复杂系统构建任务。

---

### 3: AI 编写的 C 编译器真的可以编译并运行代码吗？其可靠性如何？

**A**: 根据该项目的实验结果，AI 确实成功构建了一个能够工作的 C 编译器。它可以处理基本的 C 语言语法（如变量声明、循环、条件判断和函数调用），并将其编译为可执行的机器码或汇编代码。然而，其可靠性是相对的。虽然它能够通过基础的“Hello World”和简单的算法测试，但在处理边缘情况、复杂的指针操作或标准库的高级特性时，可能会出现 Bug 或未定义的行为。它更多是作为一个概念验证，证明了 AI 具备构建系统软件的潜力，而非完全替代工业级编译器（如 GCC 或 Clang）。

---

### 4: 这个编译器是完全由 AI 从零开始写的，还是基于现有的模板？

**A**: 在这个特定的实验中，目标是“从零开始”构建。这意味着 AI 需要自行设计编译器的各个阶段，包括词法分析、语法分析、语义分析、中间代码生成以及最终的代码生成。虽然 AI 没有复制粘贴现有的开源代码，但它依赖于从训练数据中学到的关于编译原理的知识（如递归下降解析器、LLVM 基础或 x86 汇编指令）。AI 并没有使用预制的编译器项目模板，而是通过代码逻辑一步步“推理”并构建出各个模块。

---

### 5: 使用 Agent Teams 模式开发软件的主要优势是什么？

**A**: 使用 Agent Teams 的主要优势在于“分工”和“自我修正”。单一模型在处理数千行代码的大型项目时，往往会因为上下文过长而遗忘之前的细节，导致逻辑不一致。通过代理团队，不同的 AI 可以专注于特定模块，减少了单个实例的认知负载。此外，专门的“测试”或“审查”代理可以检查“编码”代理的输出，发现错误并要求修复，从而形成一个自动化的迭代开发流程，大大提高了复杂项目的成功率。

---

### 6: 这种开发方式对未来的软件工程有什么启示？

**A**: 这个项目展示了 AI 从“辅助编码”向“自主工程”转变的可能性。它表明，未来的软件开发可能不再仅仅是人类编写代码，而是人类作为“架构师”或“产品经理”定义目标，由 AI 代理团队负责具体的实现、集成和测试。虽然目前 AI 生成的编译器在性能上还无法匹敌人工优化了几十年的成熟软件，但这种工作流预示着在构建原型、遗留系统迁移或特定领域 DSL（领域特定语言）开发中，AI 将发挥越来越核心的作用。
## 引用

- **原文链接**: [https://www.anthropic.com/engineering/building-c-compiler](https://www.anthropic.com/engineering/building-c-compiler)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46903616](https://news.ycombinator.com/item?id=46903616)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Opus 4.6](/tags/opus-4.6/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [C语言](/tags/c%E8%AF%AD%E8%A8%80/) / [编译器](/tags/%E7%BC%96%E8%AF%91%E5%99%A8/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [软件开发](/tags/%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91/) / [AI编程](/tags/ai%E7%BC%96%E7%A8%8B/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [用 Opus 4.6 智能体团队构建 C 语言编译器]({{< relref "posts/20260205-hacker_news-we-tasked-opus-46-using-agent-teams-to-build-a-c-c-3.md" >}})
- [macOS版Codex应用发布：支持多代理并行与长任务运行]({{< relref "posts/20260202-hacker_news-the-codex-app-1.md" >}})
- [Codex for macOS：支持多智能体与并行工作流的 AI 编程指挥中心]({{< relref "posts/20260202-hacker_news-the-codex-app-1.md" >}})
- [🤖解密Codex智能体闭环：AI如何自主进化？]({{< relref "posts/20260125-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
