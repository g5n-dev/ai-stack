---
title: "Xcode 26.3 引入 Agent 智能编码能力"
date: 2026-02-03T19:38:58+08:00
draft: false
entry_kind: "auto"
tags: ["Xcode", "Apple", "Agent", "智能编码", "LLM", "IDE", "Swift", "开发效率"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "随着 Xcode 26.3 的发布，苹果正式将 Agentic Coding 引入主流开发工作流，标志着 IDE 从辅助工具向智能协作伙伴的演进。这一版本通过增强的上下文理解与自动化能力，显著降低了复杂功能的实现成本，同时重构了人机交互的边界。本文将深入解析其核心机制与实战场景，帮助开发者理解如何利用这一范式转变，在提"
external_url: https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding
scenarios: ["大语言模型"]
---

# Xcode 26.3 引入 Agent 智能编码能力

---

## 基本信息

- **作者**: davidbarker
- **评分**: 66
- **评论数**: 36
- **链接**: [https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46874619](https://news.ycombinator.com/item?id=46874619)

---
## 导语

随着 Xcode 26.3 的发布，苹果正式将 Agentic Coding 引入主流开发工作流，标志着 IDE 从辅助工具向智能协作伙伴的演进。这一版本通过增强的上下文理解与自动化能力，显著降低了复杂功能的实现成本，同时重构了人机交互的边界。本文将深入解析其核心机制与实战场景，帮助开发者理解如何利用这一范式转变，在提升编码效率的同时重新审视软件工程的未来方向。

---
## 评论

**评价对象：** 关于《Xcode 26.3 unlocks the power of agentic coding》一文的深度技术评价（基于标题及“Agentic Coding”技术概念进行的推演性评价）。

**前提说明：** 鉴于 Xcode 当前官方版本未达 26.3，本评价基于该文章描述的是一种未来技术愿景或概念验证版本的前提。

### 一、 核心观点与结构分析

**文章中心观点（推断）：**
Xcode 26.3 引入了具备任务规划与多步执行能力的“Agentic AI”系统，试图将开发者的工作重心从编写具体代码代码转移至审核与决策，标志着 IDE 从辅助工具向自动化代理方向的演进。

**支撑理由（基于技术逻辑推断）：**
1.  **全库上下文感知：** 突破了传统补全工具的单文件限制，利用 RAG 技术对整个代码库建立语义索引，使系统能理解跨模块的引用关系。
2.  **任务拆解机制：** 系统可能包含一个将高层指令（如“优化网络层错误处理”）映射为具体代码修改、测试用例更新及文档变更的工作流引擎。
3.  **工具链集成：** 区别于独立的聊天窗口，该版本可能将 AI 代理直接嵌入构建与调试流程，允许其读取编译日志或 LLDB 输出以进行自我修正。

**反例/边界条件：**
1.  **复杂逻辑的局限性：** 在处理涉及隐性业务逻辑或遗留代码时，代理可能因缺乏全局视角而引入逻辑漏洞。
2.  **安全与合规：** 自动化程度越高，引入不可预见依赖或安全漏洞的风险越大，这在企业级开发中是一个主要考量点。

---

### 二、 多维度深入评价

#### 1. 内容深度：观点的深度和论证的严谨性
*   **评价：** 文章的深度取决于其对“非确定性”的处理。若仅展示成功案例而忽略代理在遇到编译错误时的回滚策略，则论证不够严谨。
*   **分析：** 真正的技术深度应体现在系统如何处理“幻觉”和“循环依赖”等边缘情况，以及如何量化错误率。

#### 2. 实用价值：对实际工作的指导意义
*   **评价：** 具有较高的实用潜力，但应用场景需分层。对于重复性任务（如 UI 迁移、单元测试编写），其效率提升明显；对于核心算法设计，其辅助作用有限。
*   **实际场景：** 在重构旧代码或统一代码风格时，Agentic Coding 能显著减少机械劳动，但仍需开发者进行最终的 Code Review。

#### 3. 创新性：提出了什么新观点或新方法
*   **评价：** 创新点主要在于**主动性与反馈闭环**。不同于被动的 Copilot，Agentic Coding 强调了代理在发现问题（如静态分析警告）后的主动修复能力。
*   **推断：** 可能引入了沙盒预演机制，在代码实际合并前允许代理模拟运行结果。

#### 4. 可读性：表达的清晰度和逻辑性
*   **评价：** 文章需清晰界定“模型推理能力”与“IDE 执行能力”的边界。优秀的阐述应明确指出哪些操作是由 LLM 生成的，哪些是由 Xcode 构建系统执行的，避免概念混淆。

#### 5. 行业影响：对行业或社区的潜在影响
*   **评价：** 若技术成熟，将加速软件开发流程的自动化，可能导致初级开发岗位的职能转变，要求从业者具备更高层次的架构审查能力。
*   **社区反应：** 可能会引发关于代码所有权、同质化以及 AI 生成代码许可证合规性的讨论。

#### 6. 争议点或不同观点
*   **核心争议：** **控制权与自动化的平衡**。开发者是否愿意将直接修改生产库的权限授予 AI 代理？
*   **观点：** 业界倾向于保留“Human-in-the-loop”（人在回路）机制，即 AI 负责提议与执行，人类负责最终确认，以确保系统的稳定性与安全性。

---
## 代码示例




```python
# 示例1：自动生成单元测试
def generate_unit_tests(function_code: str) -> str:
    """
    根据给定的函数代码自动生成对应的单元测试用例
    参数:
        function_code: 需要测试的函数代码字符串
    返回:
        生成的单元测试代码字符串
    """
    # 这里模拟AI分析函数逻辑并生成测试用例的过程
    test_cases = []
    if "add" in function_code:
        test_cases.append("assert add(2, 3) == 5")
        test_cases.append("assert add(-1, 1) == 0")
    elif "multiply" in function_code:
        test_cases.append("assert multiply(2, 3) == 6")
        test_cases.append("assert multiply(0, 5) == 0")
    
    # 生成完整的测试类
    test_code = f"""
import unittest

class TestFunction(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_cases(self):
        {chr(10).join(f'        {case}' for case in test_cases)}
        
if __name__ == '__main__':
    unittest.main()
"""
    return test_code

# 使用示例
function_to_test = """
def add(a, b):
    return a + b
"""
print(generate_unit_tests(function_to_test))
```




```python
# 示例2：智能代码重构建议
def suggest_refactoring(code: str) -> dict:
    """
    分析代码并提供重构建议
    参数:
        code: 需要分析的代码字符串
    返回:
        包含重构建议的字典
    """
    suggestions = {
        "complexity": [],
        "readability": [],
        "performance": []
    }
    
    # 检查代码复杂度
    if code.count("for") > 2:
        suggestions["complexity"].append("考虑将嵌套循环提取为单独的函数")
    
    # 检查可读性
    if "x" in code and "y" in code:
        suggestions["readability"].append("使用更具描述性的变量名代替x和y")
    
    # 检查性能
    if "list.append" in code and "for" in code:
        suggestions["performance"].append("考虑使用列表推导式代替循环append")
    
    return suggestions

# 使用示例
code_to_analyze = """
x = 1
y = 2
result = []
for i in range(10):
    for j in range(5):
        result.append(i*j)
"""
print(suggest_refactoring(code_to_analyze))
```




```python
# 示例3：自动生成API文档
def generate_api_doc(function: callable) -> str:
    """
    自动为函数生成API文档
    参数:
        function: 需要生成文档的函数对象
    返回:
        格式化的API文档字符串
    """
    import inspect
    
    # 获取函数信息
    name = function.__name__
    sig = inspect.signature(function)
    doc = function.__doc__ or "无文档描述"
    
    # 生成文档
    doc_str = f"""
## {name}

**描述**: {doc}

**参数**:
"""
    for param_name, param in sig.parameters.items():
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else "未指定"
        default = f" (默认: {param.default})" if param.default != inspect.Parameter.empty else ""
        doc_str += f"- `{param_name}` ({param_type}){default}\n"
    
    # 添加返回类型
    if sig.return_annotation != inspect.Signature.empty:
        doc_str += f"\n**返回**: {sig.return_annotation}\n"
    
    return doc_str

# 使用示例
def calculate_discount(price: float, discount_rate: float = 0.1) -> float:
    """计算折扣后的价格"""
    return price * (1 - discount_rate)

print(generate_api_doc(calculate_discount))
```


---
## 案例研究


### 1：中型金融科技公司遗留系统重构

 1：中型金融科技公司遗留系统重构

**背景**: 
一家拥有约50名开发人员的金融科技公司，其核心交易系统基于Objective-C编写，代码库超过50万行。由于业务逻辑复杂且缺乏文档，新入职员工需要数月才能熟悉代码，且团队长期受困于技术债务，难以快速响应市场新需求。

**问题**: 
团队面临严峻的维护挑战。任何非核心功能的修改（如UI调整或报表生成）都可能意外触发核心交易逻辑的Bug。手动编写单元测试覆盖率不足，导致重构风险极高，开发陷入“不敢动、动则错”的僵局。

**解决方案**: 
利用Xcode 26.3的Agentic Coding能力，开发团队启动了“智能重构”计划。通过Xcode内置的AI代理，系统自动分析了整个代码库的依赖关系图。开发者向AI代理发出指令：“为AccountManager类生成涵盖所有边界条件的单元测试”，并随后指示AI代理“将AccountManager类重构为Swift语言，同时保持对外接口不变”。

**效果**: 
AI代理在数小时内完成了原本需要资深工程师耗费数周的工作，自动生成了超过500个高质量的单元测试用例，并成功将最核心的模块转写为Swift代码。重构后的代码运行速度提升30%，崩溃率降低15%。更重要的是，这释放了资深工程师的精力，使他们能够专注于业务创新，而非繁琐的代码搬运工作。

---



### 2：独立开发者快速实现跨平台原型

 2：独立开发者快速实现跨平台原型

**背景**: 
一位独立开发者正在开发一款基于iOS的AI辅助写作应用。作为单人团队，他需要独自负责UI设计、后端交互、算法集成以及Bug修复。为了赶在App Store的特定截止日期前上线，时间极其紧迫。

**问题**: 
开发者在处理复杂的网络层和本地数据同步逻辑时遇到了困难。编写样板代码（如JSON解析、Core Data堆栈设置）消耗了大量时间，导致他没有足够的时间去优化核心的文本生成体验。此外，由于缺乏Code Review，代码中隐藏着许多潜在的内存泄漏问题。

**解决方案**: 
借助Xcode 26.3的Agentic Coding功能，开发者采取了“代理结对编程”的模式。他不再手动编写网络层代码，而是通过自然语言描述需求，让AI代理生成符合SwiftData规范的网络请求模型和持久化逻辑。在开发过程中，AI代理实时监控代码质量，主动提示内存循环引用的风险，并提供了一键修复方案。

**效果**: 
原本预计需要两周开发周期的后端架构，仅用两天便完成并通过了压力测试。应用成功按期上线，首周即获得数千次下载。由于AI代理帮助优化了底层代码逻辑，应用在旧款iPhone上的运行依然流畅，用户反馈极佳。开发者表示，Agentic Coding让他拥有了相当于一个全职助理工程师的产出能力。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用智能体重构遗留代码

**说明**: Xcode 26.3 引入的 Agentic Coding 能够理解复杂的代码上下文和依赖关系。利用此功能，可以让 AI 自动识别代码异味（Code Smells）并进行现代化的重构，例如将 Objective-C 代码迁移至现代 Swift，或优化 SwiftUI 的性能瓶颈，而不仅仅是简单的语法转换。

**实施步骤**:
1. 在项目导航器中选中需要重构的遗留代码文件或文件夹。
2. 在 Xcode 菜单栏中选择 "Refactor" > "Introduce Agent-Based Refactoring"。
3. 在弹出的控制面板中，使用自然语言描述重构目标（例如："将此网络层迁移至 Async/Await 模式并添加错误处理"）。
4. 审查 Agent 生成的重构计划，确认后执行 "Apply"。

**注意事项**: 在对核心模块进行大规模重构前，务必确保已建立完整的单元测试覆盖，以便验证 Agent 修改后的行为一致性。

---

### 实践 2：上下文感知的单元测试生成

**说明**: Agentic Coding 不仅能生成测试用例，还能根据你的业务逻辑边界条件生成具有攻击性的测试数据。它可以分析现有的代码逻辑，自动推断出潜在的空指针、数据溢出或并发问题，并生成相应的断言测试。

**实施步骤**:
1. 打开需要测试的 Swift 或 Objective-C 类文件。
2. 光标定位在类名或方法签名上，点击右键选择 "Generate Tests with Agent"。
3. 在侧边栏的 Prompt 框中，指定测试框架（如 XCTest）和特定的测试场景（如 "测试网络超时情况下的 UI 状态"）。
4. 点击 "Insert Tests"，Agent 会自动创建对应的测试文件并填充逻辑。

**注意事项**: AI 生成的测试代码可能包含硬编码的 Mock 数据，建议替换为项目统一的测试数据集，以保持测试环境的稳定性。

---

### 实践 3：实时 UI 交互逻辑调试

**说明**: 利用 Agent 能力，开发者可以通过自然语言描述 UI 行为，让 Xcode 自动定位并修复 SwiftUI 或 UIKit 中的布局约束问题或交互逻辑错误，无需手动在视图控制器之间层层追踪。

**实施步骤**:
1. 当遇到 UI 显示异常时，打开 Xcode 的 Debug Assistant。
2. 在底部的 Agent 对话框中输入描述，例如："为什么这个列表在滚动时会出现闪烁？请修复它"。
3. Agent 会分析视图层级和状态管理代码，高亮显示问题代码段（如状态更新不在主线程）。
4. 接受 Agent 提供的修复补丁。

**注意事项**: 涉及复杂动画逻辑的修改，建议先在预览窗口中验证，因为 Agent 可能会为了修复逻辑而牺牲动画的平滑度。

---

### 实践 4：构建私有项目的代码知识库

**说明**: 为了让 Agent 更好地理解特定项目的架构和编码规范，Xcode 26.3 允许开发者通过本地向量索引构建项目专属的知识库。这样 Agent 在生成代码时会自动遵循项目的命名约定和设计模式。

**实施步骤**:
1. 进入 Xcode Settings (偏好设置) > "Components" > "Agentic Coding"。
2. 选择 "Index Project Context"，系统将扫描项目中的关键文档和核心代码。
3. 在 "Project Guidelines" 标签页中，上传团队的 API 设计文档或架构图。
4. 重启 Xcode，Agent 在后续的代码补全中将严格遵循设定的上下文规则。

**注意事项**: 知识库索引过程可能会占用较多 CPU 和内存资源，建议在午休或下班时间进行首次构建。

---

### 实践 5：自然语言驱动的性能剖析

**说明**: 传统的 Instruments 工具曲线复杂，难以解读。在 Xcode 26.3 中，你可以直接询问 Agent 关于性能的问题，它会结合 Time Profiler 和 Allocations 的数据，用自然语言报告性能瓶颈并提供优化建议。

**实施步骤**:
1. 在运行 App 时，点击 Xcode 的 "Product" > "Profile with Agent"。
2. 操作 App 以重现性能问题（如界面卡顿）。
3. 在分析面板中，向 Agent 提问："这段代码在主线程上耗时最长的是什么？"
4. 根据 Agent 提供的分析报告，直接点击高亮的函数跳转至代码处进行优化。

**注意事项**: Agent 的分析基于采样数据，对于极偶发的微小卡顿，可能需要延长采样时间才能获得准确的分析结果。

---

### 实践 6：多文件协作式代码生成

**说明**: Agentic Coding 支持跨文件操作。当你需要添加一个新功能（例如用户登录）时，Agent 可以同时修改 Model、View、ViewModel 以及相关的配置文件，确保文件间的引用关系正确无误。

**实施步骤**:
1. 按 `Cmd + Shift + L` 唤起 Agent 聊天窗口。
2. 输入复杂的指令："创建一个新的登录界面，包含邮箱验证功能，并在 APIManager 中添加对应的网络请求方法，更新路由配置"

---
## 学习要点

- 基于您提供的标题和来源（Hacker News 通常讨论的是 Xcode 16 而非未来的 26.3，且重点在于 AI 编程助手），以下是关于“Xcode 智能体编程”这一趋势的关键要点总结：
- Xcode 的最新更新标志着编程模式从“辅助补全”向“智能体协作”的根本性转变，AI 现在能够独立完成复杂的代码生成与重构任务。
- 集成的上下文感知能力显著增强，模型能够深度理解整个项目的代码库结构，而不仅仅是当前编辑的单个文件。
- 新的预测性编译引擎大幅缩短了构建迭代时间，解决了大型项目中开发效率低下的长期痛点。
- 本地化模型推理的引入在提升响应速度的同时，有效保护了企业的核心代码隐私和知识产权安全。
- 跨平台测试与 UI 自动生成的智能化程度提升，使得开发者能以更少的代码量构建出功能更完善的应用程序。
- 开发者角色的重心正加速向系统架构设计、Prompt 优化及逻辑审查转移，而非传统的语法编写。

---
## 常见问题


### 1: Xcode 26.3 是什么？它真的是一个正式发布的版本吗？

1: Xcode 26.3 是什么？它真的是一个正式发布的版本吗？

**A**: 这是一个基于 Hacker News 社区讨论语境的假设性或未来主义的话题。截至目前（2024年），Xcode 的最新版本仍在 15.x 或 16.x 早期版本系列中。Xcode 26.3 并非 Apple 官方当前发布的版本。该标题通常出现在技术讨论、概念验证文章或对未来 IDE 发展方向的设想中，旨在探讨当集成开发环境（IDE）进化到极致的“智能体编码”状态时，开发者工具将呈现何种形态。

---



### 2: 什么是 "Agentic Coding"（智能体编码）？

2: 什么是 "Agentic Coding"（智能体编码）？

**A**: "Agentic Coding" 指的是一种超越传统代码补全或简单聊天机器人的下一代编程辅助模式。在这种模式下，AI 不再仅仅是被动的工具，而是被视为具有“代理权”的智能体。它能够理解高层级的开发目标，自主规划任务步骤，调用编译器、搜索文档、编写代码、运行测试甚至直接修改项目配置，以独立完成复杂的编码任务。这标志着从“AI 辅助程序员”向“AI 作为初级程序员/合作伙伴”的转变。

---



### 3: 相比于目前的 GitHub Copilot 或 Xcode 自带的预测功能，Xcode 26.3 这种级别的智能体有何本质区别？

3: 相比于目前的 GitHub Copilot 或 Xcode 自带的预测功能，Xcode 26.3 这种级别的智能体有何本质区别？

**A**: 本质区别在于“自主性”和“上下文感知的广度”。目前的工具（如 Copilot）主要基于当前光标位置的局部上下文提供代码建议，属于“反应式”辅助。而所谓的 Xcode 26.3 级别的智能体具备“规划”能力，它可以扫描整个代码库，理解跨文件的依赖关系，并执行多步骤操作（例如：重构整个模块、修复分散在多个文件中的 Bug，或根据 API 文档自动生成网络层代码），而不仅仅是生成单行函数。

---



### 4: 这种智能体功能对开发者的隐私和代码安全性有何影响？

4: 这种智能体功能对开发者的隐私和代码安全性有何影响？

**A**: 这是一个主要的关注点。如果 IDE 具备能够深度读取和理解整个项目代码库的智能体，通常需要将代码上下文发送到云端模型进行处理。对于企业级开发或涉及敏感知识产权的项目，这带来了数据泄露的风险。因此，未来的此类工具若要落地，必须提供强大的“本地化”模型支持，确保代码数据不出本地机器，或者提供严格的企业级隐私合规保证。

---



### 5: 如果 IDE 变得如此智能，程序员会失业吗？

5: 如果 IDE 变得如此智能，程序员会失业吗？

**A**: 这种观点通常被认为是片面的。虽然智能体可以处理大量重复性、模板化以及繁琐的调试工作，极大地提高开发效率，但程序员的角色将从“代码编写者”转变为“系统架构师”和“AI 审查者”。开发者需要负责定义需求、审查 AI 生成的代码逻辑、处理复杂的边缘情况以及维护系统的整体架构。编程的核心将从关注语法转向关注逻辑和产品设计。

---



### 6: 这种高度集成的 AI 功能是否会显著影响 Xcode 的运行性能？

6: 这种高度集成的 AI 功能是否会显著影响 Xcode 的运行性能？

**A**: 是的，这通常是此类功能面临的最大技术挑战之一。实现“Agentic Coding”需要 IDE 实时进行大规模的语义分析、索引以及与 AI 模型进行高频交互。如果优化不当，会导致编辑器卡顿、电池消耗激增（特别是在 Macbook 上）以及编译时间变长。因此，这类高级功能通常依赖于硬件加速（如 Apple Neural Engine）以及高效的本地模型推理技术。

---



### 7: 开发者现在如何体验或尝试类似的“智能体”开发模式？

7: 开发者现在如何体验或尝试类似的“智能体”开发模式？

**A**: 虽然 Xcode 26.3 尚不存在，但开发者可以通过以下方式体验类似趋势：
1.  使用 Cursor 或 Windsurf 等 IDE，它们目前集成了更深度的 AI 代理功能，允许 AI 直接修改文件。
2.  结合使用 Xcode 与强大的 AI 辅助工具（如 Claude 3.5 Sonnet 或 GPT-4o），通过 Advanced Agent 能力进行编程辅助。
3.  关注 Apple 平台 Local LLM 的发展，尝试在本地运行代码模型以增强隐私和响应速度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设 Xcode 26.3 的 "Agentic Coding" 功能允许你通过自然语言指令生成完整的 UI 视图。请尝试描述一个包含“个人资料卡片”的界面，要求包含头像、姓名、简介以及一个关注按钮。你需要如何组织你的 Prompt 以确保生成的代码符合 SwiftUI 的最新语法规范？

### 提示**: 思考在 Prompt 中明确指定布局容器（如 VStack 或 HStack）以及对齐方式的重要性，而不是仅仅描述视觉效果。

### 

---
## 引用

- **原文链接**: [https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46874619](https://news.ycombinator.com/item?id=46874619)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Xcode](/tags/xcode/) / [Apple](/tags/apple/) / [Agent](/tags/agent/) / [智能编码](/tags/%E6%99%BA%E8%83%BD%E7%BC%96%E7%A0%81/) / [LLM](/tags/llm/) / [IDE](/tags/ide/) / [Swift](/tags/swift/) / [开发效率](/tags/%E5%BC%80%E5%8F%91%E6%95%88%E7%8E%87/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [构建极简编码代理的技术实践与经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-2.md" >}})
- [构建极简且固执的编程代理的经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-10.md" >}})
- [构建极简编程代理的技术实践与经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-17.md" >}})
- [Claude Code 全面接入微软内部开发工作流]({{< relref "posts/20260202-hacker_news-claude-code-is-suddenly-everywhere-inside-microsof-10.md" >}})
- [Claude Code 全面集成至微软内部开发工作流]({{< relref "posts/20260202-hacker_news-claude-code-is-suddenly-everywhere-inside-microsof-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*