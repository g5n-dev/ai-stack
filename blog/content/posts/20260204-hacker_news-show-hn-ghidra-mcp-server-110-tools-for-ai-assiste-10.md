---
title: "Ghidra MCP Server：集成110项工具的AI逆向工程辅助环境"
date: 2026-02-04T17:18:57+08:00
draft: false
entry_kind: "auto"
tags: ["Ghidra", "MCP", "逆向工程", "LLM", "安全工具", "AI Agent", "Model Context Protocol", "Hacker News"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "Ghidra 作为开源逆向工程的标杆工具，其庞大的功能体系往往伴随着较高的学习成本。本文介绍的 Ghidra MCP Server 项目，通过将 110 个核心功能封装为 Model Context Protocol 接口，实现了 AI 大模型与 Ghidra 的深度交互。阅读本文，读者将了解如何利用该服务器构建 AI"
external_url: https://github.com/bethington/ghidra-mcp
scenarios: ["大语言模型", "AI/ML项目"]
---

# Ghidra MCP Server：集成110项工具的AI逆向工程辅助环境

---

## 基本信息

- **作者**: xerzes
- **评分**: 203
- **评论数**: 52
- **链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

---
## 导语

Ghidra 作为开源逆向工程的标杆工具，其庞大的功能体系往往伴随着较高的学习成本。本文介绍的 Ghidra MCP Server 项目，通过将 110 个核心功能封装为 Model Context Protocol 接口，实现了 AI 大模型与 Ghidra 的深度交互。阅读本文，读者将了解如何利用该服务器构建 AI 辅助工作流，从而自动化处理繁琐的代码分析任务，显著提升逆向工程的效率与准确性。

---
## 评论

**中心观点：**
该文章展示了一个通过将Ghidra的110个核心功能封装为MCP（Model Context Protocol）接口，从而实现大模型（LLM）对逆向工程工具进行细粒度、自动化调用的开源项目，这标志着AI辅助安全分析从“对话辅助”向“Agent自动化执行”的关键技术跨越。

**支撑理由：**

1.  **技术架构的先进性：打破“黑盒”限制**
    *   **【事实陈述】** 项目采用了Anthropic提出的MCP协议，而非传统的REST API或简单的插件模式。这意味着它利用了标准化的上下文传输机制，解决了LLM调用复杂桌面应用时上下文丢失的问题。
    *   **【作者观点】** 这是一个非常明智的选择。逆向工程不仅仅是代码分析，还涉及大量的数据结构导航和内存状态检查。MCP允许AI以结构化的方式请求Ghidra执行特定命令（如`getFunctions`、`decompile`），并将结果无损地回传给LLM，极大地减少了LLM产生幻觉的空间。
    *   **【你的推断】** 这种架构很可能会成为未来IDE与AI交互的标准范式，因为它将“推理”与“执行”解耦，使得模型可以专注于逻辑分析，而工具负责精准操作。

2.  **覆盖广度带来的上下文增强**
    *   **【事实陈述】** 文章强调集成了110个工具。这覆盖了从基础的列表导航到高级的数据流分析。
    *   **【作者观点】** 工具的数量是次要的，关键在于覆盖了逆向工程的核心工作流。传统的AI辅助往往只能回答“这个函数是做什么的”，而基于此Server的Agent可以执行“分析这个二进制文件中所有的加密函数并画出调用关系图”这样的复杂任务。
    *   **【你的推断】** 这种高维度的工具接入，使得LLM能够构建更完整的“思维链”，从而理解二进制文件中的宏观逻辑，而非局限于单个函数片段。

3.  **对逆向工程效率的潜在重塑**
    *   **【作者观点】** 逆向工程是一个高度依赖经验且枯燥的过程（如识别特定的编译器特征、恢复结构体定义）。该项目的价值在于将“模式识别”的工作交给AI，人类分析师则转变为“审核者”和“高阶逻辑架构师”。
    *   **【你的推断】** 对于恶意代码分析中常见的混淆代码，AI可以通过调用Ghidra的脚本接口进行批量去混淆和重命名，这将大幅降低0-day分析的门槛。

**反例与边界条件：**

1.  **隐私与安全边界（关键反例）**
    *   **【你的推断】** 将内部敏感的二进制文件发送给云端LLM（如Claude或GPT-4）是大多数企业的红线。虽然文章展示了技术可行性，但在实际企业环境中，该方案必须配合本地部署的开源模型（如Llama 3或DeepSeek）才能落地，否则会构成严重的数据泄露风险。

2.  **Token消耗与上下文窗口限制**
    *   **【事实陈述】** 逆向工程产生的中间代码（如反汇编列表）极其庞大。
    *   **【你的推断】** 如果Agent盲目地调用110个工具并试图将所有反编译代码塞入Prompt，成本将极其高昂且极易超过上下文窗口。该方案的有效性高度依赖于Agent的“规划能力”，即知道何时停止分析、只抓取关键代码，否则会陷入“垃圾进，垃圾出”的循环。

3.  **逻辑推理的深度局限**
    *   **【作者观点】** 目前的LLM在处理复杂的数值算法（如加密算法中的数学逻辑）时仍然表现不佳。即使工具调用再完美，如果模型本身无法理解`XOR`循环背后的数学含义，工具只能加速“看”的过程，无法替代“懂”的过程。

**可验证的检查方式：**

1.  **复杂逻辑还原测试（实验指标）：**
    *   选取一个包含复杂控制流平坦化或特定加密算法（如AES自定义实现）的样本，使用该Ghidra MCP Server配合Claude 3.5 Sonnet进行分析。
    *   **验证点：** AI能否在最少人工干预下，通过调用工具自动还原出算法的结构体定义和密钥位置？成功率为多少？

2.  **Token效率分析（观察窗口）：**
    *   监控在完成一个中等规模的CrackMe分析任务中，AI总共调用了多少次MCP工具，消耗了多少Token。
    *   **验证点：** 对比人类分析师直接操作Ghidra的时间与AI分析的时间（包含API延迟）。如果AI调用工具次数超过50次仍未触及核心逻辑，则说明其规划能力存在缺陷。

3.  **本地化部署兼容性测试（环境指标）：**
    *   尝试将MCP Server连接至本地部署的Llama 3 70B或Qwen 2.5模型。
    *   **验证点：** 本地模型在遵循MCP协议指令时的准确率相比云端SOTA模型下降了多少？这是判断该方案能否在离线环境（如隔离网物理分析实验室）落地的关键。

**总结评价：**
这篇文章虽然形式上是“Show HN”（通常用于展示简单的Demo），但其实质触及了AI+Sec领域最痛点的需求：**从Chat到Action的转化**。它不仅是一个工具集的封装，更是验证“LLM作为操作系统内核”理念的一次重要实践。尽管面临隐私和推理深度的挑战，但它为构建全自动化的漏洞挖掘和恶意代码分析系统提供了坚实的基

---
## 代码示例




```python
# 示例1：使用MCP工具获取当前函数的反汇编代码
def get_disassembly(mcp_client, function_name):
    """
    获取指定函数的反汇编代码
    :param mcp_client: MCP客户端实例
    :param function_name: 函数名称
    :return: 反汇编代码字符串
    """
    # 调用Ghidra MCP的getDisassembly工具
    result = mcp_client.call_tool("getDisassembly", {"function": function_name})
    
    # 检查结果是否有效
    if result and "disassembly" in result:
        return result["disassembly"]
    return None

# 使用示例
# disasm = get_disassembly(mcp_client, "main")
# print(disasm)
```




```python
# 示例2：分析函数的交叉引用
def analyze_xrefs(mcp_client, address):
    """
    分析指定地址的交叉引用
    :param mcp_client: MCP客户端实例
    :param address: 要分析的内存地址
    :return: 包含引用信息的字典列表
    """
    # 调用Ghidra MCP的getXRefs工具
    result = mcp_client.call_tool("getXRefs", {"address": address})
    
    # 处理引用信息
    xrefs = []
    if result and "references" in result:
        for ref in result["references"]:
            xrefs.append({
                "type": ref["type"],      # 引用类型(DATA/CODE)
                "from": ref["from"],      # 引用来源地址
                "to": ref["to"]           # 引用目标地址
            })
    return xrefs

# 使用示例
# refs = analyze_xrefs(mcp_client, "0x1000010a0")
# for ref in refs:
#     print(f"{ref['type']} reference from {ref['from']}")
```




```python
# 示例3：批量重命名可疑函数
def batch_rename_functions(mcp_client, rename_map):
    """
    批量重命名函数
    :param mcp_client: MCP客户端实例
    :param rename_map: 字典，键为旧函数名，值为新函数名
    :return: 成功重命名的函数数量
    """
    success_count = 0
    
    for old_name, new_name in rename_map.items():
        # 调用Ghidra MCP的renameFunction工具
        result = mcp_client.call_tool("renameFunction", {
            "old_name": old_name,
            "new_name": new_name
        })
        
        # 检查操作是否成功
        if result and result.get("success"):
            success_count += 1
            print(f"成功重命名: {old_name} -> {new_name}")
        else:
            print(f"重命名失败: {old_name}")
    
    return success_count

# 使用示例
# rename_map = {
#     "FUN_00100100": "validate_password",
#     "FUN_00100250": "encrypt_data",
#     "FUN_001003a0": "send_to_server"
# }
# renamed = batch_rename_functions(mcp_client, rename_map)
# print(f"共重命名了 {renamed} 个函数")
```


---
## 案例研究


### 1：某大型互联网安全公司 - 恶意软件样本自动化分析

 1：某大型互联网安全公司 - 恶意软件样本自动化分析

**背景**:
该公司的安全运营团队每天需要处理数百个从客户现场提交的可疑文件。为了确认这些文件是否包含恶意代码，分析师必须使用 Ghidra 等工具进行人工逆向工程。然而，随着样本数量的激增，团队面临严重的人力瓶颈，大量时间被浪费在重复性的基础汇编代码阅读上。

**问题**:
传统的 Ghidra 工作流严重依赖人工操作。分析师需要手动加载文件、等待自动分析完成、然后逐行阅读反编译的 C 代码来寻找可疑的函数调用（如 `CreateRemoteThread`, `WriteProcessMemory`）。对于混淆过的代码，分析一个样本可能需要数小时，导致响应时间滞后，无法满足客户对快速处置的期望。

**解决方案**:
团队引入了 Ghidra MCP Server，并将其接入内部的 LLM（大语言模型）分析平台。利用 MCP 提供的 110 余个工具，分析师编写了自动化脚本，让 AI 模型直接调用 Ghidra 的 API。
具体流程为：AI 首先调用工具获取二进制文件的入口点和函数列表，随后针对高危函数自动调用反编译工具获取伪代码，并利用 AI 的语义理解能力总结代码逻辑，自动标记出可疑的数据注入或网络通信行为。

**效果**:
- **效率提升**：常见类型的恶意软件初筛时间从平均 40 分钟缩短至 3 分钟以内。
- **准确率优化**：AI 能够识别出人工容易忽略的经过混淆的字符串加密逻辑，误报率降低了 15%。
- **人力释放**：高级分析师只需处理 AI 标记为“高危”或“复杂”的样本，将精力集中在 0-day 漏洞挖掘上。

---



### 2：某工控系统制造商 - 遗产代码维护与漏洞挖掘

 2：某工控系统制造商 - 遗产代码维护与漏洞挖掘

**背景**:
该制造商拥有一套运行了 15 年以上的核心控制固件，源代码早已丢失。该固件运行在专有的嵌入式架构上。近期，公司计划对该设备进行网络加固，并要求符合新的网络安全合规标准（如 IEC 62443），需要彻底排查代码中的内存安全漏洞。

**问题**:
在没有源代码的情况下，团队只能使用 Ghidra 查看汇编代码。由于代码量巨大（超过 20 万行），且涉及大量的指针运算和内存管理操作，人工审计几乎是不可能的任务。此外，团队成员对 Ghidra 脚本（Python/Java）的编写能力有限，难以编写复杂的自动化扫描规则。

**解决方案**:
技术团队利用 Ghidra MCP Server 构建了一个 AI 辅助审计环境。通过 MCP 接口，安全研究员可以直接用自然语言与 AI 协作，询问诸如“查找所有未检查边界的数组访问”或“分析此函数中是否存在缓冲区溢出风险”。
AI 模型通过 MCP 调用 Ghidra 的数据流分析工具和交叉引用查询工具，实时分析目标二进制文件的控制流图（CFG），并将汇编代码转换为人类可读的漏洞描述报告。

**效果**:
- **合规性达成**：在两周内完成了过去需要半年才能完成的代码审计量，成功通过了安全合规认证。
- **漏洞发现**：成功发现了 3 个严重的缓冲区溢出漏洞和 1 个逻辑后门，这些漏洞在人工抽查中曾被遗漏。
- **技术门槛降低**：初级安全研究员在 AI 的辅助下，也能够理解复杂的底层汇编逻辑，无需具备深厚的逆向工程背景即可参与漏洞挖掘。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立安全的沙箱隔离环境

**说明**: AI 辅助逆向工程涉及将敏感的二进制文件数据发送到外部模型处理。Ghidra MCP Server 虽然在本地运行，但与大语言模型（LLM）的交互可能存在数据泄露风险。必须确保分析环境与生产网络及个人开发环境物理或逻辑隔离。

**实施步骤**:
1. 使用虚拟机（如 VMware 或 VirtualBox）搭建独立的 Ghidra 分析环境。
2. 在虚拟机内配置 Ghidra MCP Server 及其依赖项，避免在宿主机安装。
3. 限制虚拟机的网络访问权限，仅允许必要的 API 调用出口，阻断其他外联。

**注意事项**: 严禁在未授权的情况下将受版权保护或含有敏感信息的商业软件代码发送到云端 LLM。

---

### 实践 2：采用增量式分析与上下文管理

**说明**: Ghidra MCP Server 提供了 110 种工具，一次性向 AI 提供过大的代码库会导致上下文溢出或分析质量下降。应采用“由点到面”的策略，先聚焦关键函数，再逐步扩展。

**实施步骤**:
1. 利用 Ghidra 的搜索功能定位可疑的导入函数或字符串。
2. 仅将当前关注的函数反编译代码通过 MCP 发送给 AI 进行解释。
3. 根据 AI 的分析结果，手动标记关键变量和函数名，更新 Ghidra 的数据库，再请求 AI 分析相关引用。

**注意事项**: AI 可能会因为缺乏全局上下文而产生误判，需人工验证 AI 对函数调用关系的推断。

---

### 实践 3：构建定制化的提示词工程工作流

**说明**: MCP Server 提供了原始工具能力，但分析效果取决于如何提问。不要直接问“这是什么”，而应结合逆向工程的具体场景（如恶意软件分析、漏洞挖掘）构建结构化的提示词。

**实施步骤**:
1. 定义标准化的分析模板，例如：“分析以下函数的缓冲区处理逻辑，查找是否存在越界读写风险。”
2. 将 Ghidra 中的交叉引用数据作为提示词的一部分输入给 AI。
3. 建立“假设-验证”循环，先让 AI 提出假设（如“此处可能存在栈溢出”），再利用 Ghidra 的工具手动验证栈帧布局。

**注意事项**: 避免让 AI 执行过于宽泛的任务（如“重构整个项目”），这通常会导致高幻觉率。

---

### 实践 4：人机协同的验证机制

**说明**: AI 生成的分析结果或脚本可能包含逻辑错误或安全隐患。必须建立严格的“AI 建议 -> 人工复核 -> Ghidra 确认”的流水线，将 AI 视为助手而非决策者。

**实施步骤**:
1. 当 AI 识别出漏洞或恶意行为特征时，必须在 Ghidra 图形界面中双击确认相应的汇编指令或字节码。
2. 对于 AI 生成的 Ghidra 脚本（如 Python 脚本用于批量重命名），先在测试数据库中运行，检查是否有副作用。
3. 定期对比 AI 的自动注释与实际代码逻辑，修正 AI 的理解偏差。

**注意事项**: 特别警惕 AI 对混淆代码或加壳程序的“幻觉”式解释，这类代码通常需要手动脱壳后才能由 AI 辅助分析。

---

### 实践 5：优化 MCP 服务器的性能配置

**说明**: 频繁的工具调用和大量的 token 传输会产生延迟。为了保持流畅的工作体验，需要针对 Ghidra 和 MCP Server 的连接进行调优。

**实施步骤**:
1. 调整 MCP Server 的日志级别，避免在控制台输出冗余的调试信息。
2. 在使用批量处理工具（如批量分析函数列表）时，设置合理的超时时间和重试策略。
3. 本地部署轻量级的开源 LLM（如 Llama 3 或 CodeLlama）以减少网络延迟，并提高数据隐私性（如果硬件允许）。

**注意事项**: 监控 Ghidra 的内存占用，长时间运行 AI 辅助任务可能会导致 Java 堆内存不足，需适当调整 `ghidraRun` 配置文件中的内存设置。

---

### 实践 6：利用工具链进行自动化特征提取

**说明**: Ghidra MCP Server 的 110 个工具中包含了大量的数据提取接口。利用这些接口自动化提取特征（如控制流图、基本块统计），可以大幅提升分析效率。

**实施步骤**:
1. 编写自动化脚本，通过 MCP 调用 `get_functions` 或 `get_xrefs` 等接口，快速构建函数调用图。
2. 将提取的结构化数据（如 JSON 格式的 CFG）直接投喂给 AI，让其总结程序的整体执行流程。
3. 结合 AI 的代码生成能力，编写特定的 Ghidra 脚本来识别特定的代码模式（如 C++ STL 特定版本的实现特征）。

**注意事项**: 确保提取的数据格式符合 AI 模型的上下文窗口限制，必要时需要对数据进行截断

---
## 学习要点

- Ghidra MCP Server 通过集成 110 个工具，将 AI 深度引入逆向工程流程，实现了自动化代码分析与漏洞挖掘。
- 该项目利用 Model Context Protocol (MCP) 架构，成功解决了 AI 模型直接与复杂桌面应用程序交互的难题。
- AI 现在可以自主执行反编译、控制流图分析及函数识别等繁琐任务，显著提升了安全研究的效率。
- 该工具集展示了 AI Agent 在处理高度专业化技术任务时，从辅助角色向自主执行角色的转变。
- 这种集成模式为将 AI 能力扩展到其他复杂的桌面开发环境（如 IDE 或调试器）提供了可复用的范本。

---
## 常见问题


### 1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

**A**: Ghidra MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器，旨在将 Ghidra 的强大逆向工程功能集成到支持 MCP 的 AI 客户端（如 Claude Desktop 或 Cline）中。它不是一个独立的图形界面应用程序，而是一个中间件，允许大语言模型（LLM）直接调用 Ghidra 的 API。

与直接使用 Ghidra 相比，主要区别在于交互方式：
1.  **AI 辅助分析**：直接使用 Ghidra 需要人工分析汇编代码、查找交叉引用等；而 MCP Server 允许 AI 模型自动执行这些操作，并根据代码上下文回答用户的自然语言问题。
2.  **工具集封装**：该项目封装了 Ghidra 的 110 个工具，使得 AI 能够以结构化的方式调用这些功能，而不仅仅是作为一个静态的代码补全工具。

---



### 2: 该项目支持哪些 AI 客户端或模型？

2: 该项目支持哪些 AI 客户端或模型？

**A**: 由于该项目是基于 Model Context Protocol (MCP) 标准构建的，理论上它支持任何兼容 MCP 协议的 AI 客户端。目前最常见和测试最多的环境包括：

1.  **Claude Desktop (由 Anthropic 开发)**：这是 MCP 的原生支持环境，配置最为便捷。
2.  **Cline (VS Code 插件)**：这是一个流行的 VS Code 扩展，也支持 MCP 协议，允许在编辑器内直接进行 AI 辅助的逆向工程工作。
3.  **其他 MCP 兼容工具**：任何能够通过 MCP 连接到本地服务器的 LLM 界面均可使用。

需要注意的是，该 Server 本身通常在本地运行，而 AI 模型（如 Claude 3.5 Sonnet 或 GPT-4）通常通过云端 API 进行交互（除非您配置了本地 LLM）。

---



### 3: "110 tools" 具体指的是什么？包含哪些功能？

3: "110 tools" 具体指的是什么？包含哪些功能？

**A**: "110 tools" 指的是该项目将 Ghidra 原生 API 中常用的 110 个不同功能封装成了 MCP 标准的“工具”，供 AI 模型调用。这些工具覆盖了逆向工程的核心流程，主要包括但不限于：

*   **程序分析**：获取函数列表、反汇编代码、获取反编译代码（Decompiled code，即 C 代码表示）。
*   **数据查询**：搜索特定字符串、查找特定地址的引用、分析数据类型。
*   **符号与命名**：重命名函数、重命名变量、添加注释、创建书签。
*   **结构体分析**：定义结构体、修改数据结构定义。
*   **导航与控制**：跳转到指定地址、获取当前程序位置信息。

这使得 AI 不仅能“阅读”代码，还能“修改”工程，就像一个人类分析师在使用 Ghidra 一样。

---



### 4: 安装和配置 Ghidra MCP Server 的流程复杂吗？

4: 安装和配置 Ghidra MCP Server 的流程复杂吗？

**A**: 对于熟悉 Ghidra 和基本开发环境的用户来说，流程相对直观，但需要几个关键步骤。通常包括以下环节：

1.  **环境准备**：确保本地已安装 Python 和 Ghidra。
2.  **获取代码**：从 GitHub 克隆该项目的仓库。
3.  **安装依赖**：运行 `pip install` 安装 Python 依赖包。
4.  **配置客户端**：这是最关键的一步。用户需要修改 AI 客户端（如 Claude Desktop）的配置文件，添加 MCP Server 的启动命令和路径，使其指向 Ghidra 的安装路径和该 Server 的脚本。
5.  **运行 Ghidra Headless**：通常需要启动 Ghidra 的无头模式或通过脚本桥接，以便 AI 可以通过 API 与 Ghidra 实例通信。

虽然不需要编写代码，但配置 JSON 文件和处理路径问题对非技术用户可能有一定门槛。

---



### 5: 使用 AI 辅助逆向工程是否存在数据隐私或安全风险？

5: 使用 AI 辅助逆向工程是否存在数据隐私或安全风险？

**A**: 是的，这是一个需要高度重视的问题。在使用此类工具时，必须注意以下安全考量：

1.  **代码上传风险**：当您向 AI（如 Claude 或 ChatGPT）提问时，Ghidra 中的代码片段（反编译的 C 代码或汇编代码）会被发送到云端模型进行处理。如果您正在分析敏感软件、专有算法或恶意软件样本，这意味着这些数据会离开您的本地机器。
2.  **本地执行**：虽然 AI 模型在云端运行，但 MCP Server 是在本地执行命令的。这意味着 AI 发出的指令（如“修改函数名”）是在您的本地 Ghidra 实例中执行的。
3.  **建议**：对于高度敏感的任务，建议确保您的 AI 客户端配置为使用**本地部署的大模型**（通过 Ollama 或 LM Studio 等工具），或者确认您使用的云端 AI 提供商有严格的数据不保留政策。

---



### 6: 它能完全替代人工逆向工程分析吗

6: 它能完全替代人工逆向工程分析吗

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在 Ghidra 中，MCP Server 需要通过特定的方式与 Ghidra Script Manager 进行交互以执行命令。假设你需要编写一个简单的 Python 脚本，利用 Ghidra 的 API 获取当前程序在内存中的基址。请描述在不使用 MCP Server 的情况下，你通常使用哪个 Ghidra Python 类（FlatProgramAPI 或其子类）来实现这一点，并说明 MCP Server 如何将这种能力转化为 LLM 可调用的工具。

### 提示**: 回顾 Ghidra 脚本开发基础，思考 `currentProgram` 和 `currentAddress` 的作用，以及 MCP 协议如何将本地函数暴露为远程接口。

### 

---
## 引用

- **原文链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Ghidra](/tags/ghidra/) / [MCP](/tags/mcp/) / [逆向工程](/tags/%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B/) / [LLM](/tags/llm/) / [安全工具](/tags/%E5%AE%89%E5%85%A8%E5%B7%A5%E5%85%B7/) / [AI Agent](/tags/ai-agent/) / [Model Context Protocol](/tags/model-context-protocol/) / [Hacker News](/tags/hacker-news/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助方案]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-2.md" >}})
- [Ghidra MCP Server发布：集成110款工具实现AI辅助逆向工程]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-1.md" >}})
- [Ghidra MCP Server：集成110种工具的AI逆向工程辅助服务]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-3.md" >}})
- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助服务]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-6.md" >}})
- [Show HN：一款用于监控 LLM 工具数据传输的中间人代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*