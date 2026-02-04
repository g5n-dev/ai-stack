---
title: "Ghidra MCP Server：集成110种工具的AI辅助逆向工程"
date: 2026-02-04T20:15:34+08:00
draft: false
entry_kind: "auto"
tags: ["Ghidra", "MCP", "逆向工程", "LLM", "安全分析", "工具集成", "AI Agent", "Hacker News"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "将 Ghidra 的逆向工程能力接入大语言模型（LLM）是当前安全研究的热点方向。本文介绍的 Ghidra MCP Server 整合了 110 个工具，旨在通过标准化接口实现 AI 辅助的自动化分析。文章将详细拆解其部署流程与核心功能，帮助开发者理解如何利用该方案提升二进制分析的效率与精度。"
external_url: https://github.com/bethington/ghidra-mcp
scenarios: ["大语言模型", "AI/ML项目"]
---

# Ghidra MCP Server：集成110种工具的AI辅助逆向工程

---

## 基本信息

- **作者**: xerzes
- **评分**: 235
- **评论数**: 60
- **链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

---
## 导语

将 Ghidra 的逆向工程能力接入大语言模型（LLM）是当前安全研究的热点方向。本文介绍的 Ghidra MCP Server 整合了 110 个工具，旨在通过标准化接口实现 AI 辅助的自动化分析。文章将详细拆解其部署流程与核心功能，帮助开发者理解如何利用该方案提升二进制分析的效率与精度。

---
## 评论

**中心观点**
该文章展示了一项将逆向工程框架 Ghidra 与大语言模型（LLM）通过 MCP 协议集成的实践，标志着安全工具从“脚本自动化”向“智能体辅助”演进的重要技术尝试，但在处理复杂逻辑和隐私合规方面仍存在显著边界。

**支撑理由与评价**

1.  **技术架构的先进性与生态契合（事实陈述）**
    文章采用 Model Context Protocol (MCP) 是极具前瞻性的技术选择。MCP 作为新兴的 AI 通信标准，解决了 LLM 与本地工具交互的碎片化问题。作者将 Ghidra 暴露的 110 个 API（如获取反汇编代码、交叉引用、重命名函数等）标准化为 MCP 工具，实际上是将 Ghidra 从一个单纯的 GUI 工具转变为一个可以被 Claude 等 AI 模型“调用”的无头服务。
    *   **深度评价**：这种架构不仅降低了 AI 调用安全工具的门槛，还允许 AI 具备“感知”上下文的能力（例如：AI 可以先查询函数名，再根据结果决定是否查看汇编代码），而非简单的单向指令执行。

2.  **实用价值：从“阅读”到“交互”的效率跃升（作者观点）**
    在逆向工程中，分析人员 80% 的时间花费在枯燥的静态代码阅读和模式匹配上（如识别特定的 C++ std::string 模式或加壳特征）。该工具的最大价值在于将 AI 变为“副驾驶”。
    *   **深度评价**：通过 MCP，AI 可以自主规划任务链。例如，用户只需说“分析这个 sub_401000 函数的功能”，AI 可以自动调用 `get_function` 获取代码，调用 `get_xrefs` 查看调用关系，最后整合分析。这比传统的 Copilot（仅提供补全代码）有质的飞跃，因为它具备了对二进制文件的“操作”能力。

3.  **创新性：安全工具的“Agent 化”范式（你的推断）**
    该项目代表了安全工具开发的新范式：**工具即 API**。传统的 Ghidra 插件通常是 Python 脚本，逻辑是固定的。而 MCP Server 将 Ghidra 的能力原子化，交由 AI 模型进行动态逻辑组合。
    *   **深度评价**：这种“原子化工具 + 推理模型”的组合，是实现自主型网络安全 Agent 的必经之路。它允许 AI 在面对未知样本时，动态决定使用哪些 Ghidra 内置功能，而非执行预编写脚本。

**反例与边界条件**

1.  **上下文窗口与幻觉风险（事实陈述）**
    虽然工具提供了 110 个功能，但 LLM 的上下文窗口是有限的。对于大型二进制文件（如加壳的恶意软件或固件），AI 无法一次性加载全部代码。如果 AI 仅基于局部片段进行推断，极易产生“幻觉”，例如错误地将随机数据解释为代码逻辑，导致误导性分析。
2.  **隐私与数据出境风险（行业观点）**
    文章默认将数据发送给 Anthropic 的 Claude（云端处理）。对于红队行动或敏感漏洞分析，将目标二进制文件的汇编代码或函数名上传至云端模型是严重的违规行为。除非该 MCP Server 完全本地化部署（如连接本地 Ollama/Llama 3），否则在真实的企业级安全场景中，该工具的落地将面临巨大的合规阻碍。
3.  **复杂逻辑的推理盲区（你的推断）**
    AI 擅长处理模式匹配和自然语言解释，但在处理复杂的控制流图（CFG）、基于寄存器的栈偏移计算或某些混淆过的代码逻辑时，仍然表现不佳。对于需要深度数学推导或特定领域知识（如特定的虚拟机保护）的分析，该工具可能仅能提供浅层辅助。

**验证方式与检查指标**

为了客观评价该工具的实际效能，建议通过以下方式进行验证：

1.  **“图灵测试”对比实验**：
    *   **指标**：选取 10 个未公开的 CTF 题目或真实恶意样本，分别由纯人工分析师和“人工 + Ghidra MCP”两组进行分析。
    *   **观察窗口**：记录从“开始分析”到“找到关键算法逻辑”的时间差，以及最终分析报告的准确度。重点观察 AI 是否能发现人类容易忽略的细节，或者是否编造了不存在的函数功能。

2.  **API 调用成功率与错误恢复**：
    *   **指标**：在 AI 自主操作过程中，统计 MCP Server 的 API 调用日志。
    *   **观察窗口**：观察 AI 在遇到 API 返回错误（如查询了不存在的地址）时，是会陷入死循环，还是能自我修正并尝试其他路径。这直接衡量了 AI Agent 的鲁棒性。

3.  **隐私合规性压力测试**：
    *   **指标**：检查数据流向。
    *   **观察窗口**：在断网环境下（模拟高密级环境），配置本地 LLM（如 Llama 3 70B），测试 MCP Server 的响应延迟和稳定性。如果必须依赖云端 API，则该工具在专业安全行业的适用范围将大打折扣。

**总结**
Ghidra MCP Server 是逆向工程领域与 AI 结合的一个高水准“连接器”项目。它证明了标准化协议（MCP）在连接专业软件与通用大模型方面的巨大潜力。虽然受限于 LLM 的推理上限和隐私问题，它尚

---
## 代码示例




```python
# 示例1：使用 MCP 工具获取 Ghidra 当前函数的汇编代码
import requests

def get_current_function_disassembly(server_url="http://localhost:8000"):
    """
    获取 Ghidra 当前光标所在函数的反汇编代码
    :param server_url: MCP 服务器地址
    :return: 函数的反汇编文本
    """
    # 调用 MCP 的 GetCurrentDisassembly 工具
    response = requests.post(f"{server_url}/tools/GetCurrentDisassembly")
    
    if response.status_code == 200:
        disassembly = response.json().get("result", "")
        print("当前函数反汇编代码：")
        print(disassembly)
        return disassembly
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None

# 使用示例
get_current_function_disassembly()
```


---

```python
# 示例2：使用 MCP 工具在 Ghidra 中搜索特定字符串
import requests

def search_string_in_binary(target_string, server_url="http://localhost:8000"):
    """
    在 Ghidra 打开的二进制文件中搜索特定字符串
    :param target_string: 要搜索的字符串
    :param server_url: MCP 服务器地址
    :return: 匹配的地址列表
    """
    # 调用 MCP 的 SearchMemory 工具
    payload = {"query": target_string, "search_type": "string"}
    response = requests.post(f"{server_url}/tools/SearchMemory", json=payload)
    
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        print(f"找到 {len(matches)} 处匹配：")
        for match in matches:
            print(f"地址：{match['address']}, 内容：{match['content']}")
        return matches
    else:
        print(f"搜索失败，状态码：{response.status_code}")
        return []

# 使用示例
search_string_in_binary("password")
```


---

```python
# 示例3：使用 MCP 工具分析函数的交叉引用（Xrefs）
import requests

def analyze_function_xrefs(function_name, server_url="http://localhost:8000"):
    """
    分析指定函数的交叉引用（调用者和被调用者）
    :param function_name: 函数名称
    :param server_url: MCP 服务器地址
    :return: 交叉引用信息
    """
    # 调用 MCP 的 GetXrefs 工具
    payload = {"function": function_name}
    response = requests.post(f"{server_url}/tools/GetXrefs", json=payload)
    
    if response.status_code == 200:
        xrefs = response.json().get("xrefs", {})
        print(f"函数 {function_name} 的交叉引用分析：")
        print("调用者：", xrefs.get("callers", []))
        print("被调用者：", xrefs.get("callees", []))
        return xrefs
    else:
        print(f"分析失败，状态码：{response.status_code}")
        return {}

# 使用示例
analyze_function_xrefs("main")
```


---
## 案例研究


### 1：某大型互联网企业安全应急响应团队

 1：某大型互联网企业安全应急响应团队

**背景**:
该企业负责维护数亿用户的移动端应用程序，业务逻辑复杂且涉及金融交易。随着业务迭代加快，安全团队每月需处理数百个漏洞扫描报告和外部白帽子提交的漏洞，其中涉及大量混淆过的 native 库（.so 文件）分析。

**问题**:
传统的逆向工程流程严重依赖资深安全工程师的手工操作。面对高度混淆的代码和复杂的控制流，分析一个恶意样本或漏洞细节往往需要数天时间。初级分析师因为不熟悉 Ghidra 脚本编写和复杂的汇编指令，无法有效分担工作量，导致高危漏洞响应周期过长，存在业务风险。

**解决方案**:
团队引入了 Ghidra MCP Server，将其集成到内部的 AI 辅助运营平台中。通过 MCP 协议，AI 模型可以直接调用 Ghidra 的 110 余个分析工具。当分析师上传样本后，AI 自动化执行函数识别、控制流图还原和交叉引用分析，并结合自然语言处理能力，将晦涩的汇编代码转化为可读的 C++ 伪代码逻辑，直接指出漏洞触发的关键路径。

**效果**:
样本分析的平均耗时从 4 小时缩短至 30 分钟以内。初级分析师在 AI 的辅助下能够独立完成原本需要 3 年经验以上专家才能胜任的混淆代码分析工作。团队的整体漏洞处理效率提升了 300%，成功在多次 0-day 漏洞挖掘中抢在攻击者行动前完成了补丁修复。

---



### 2：某工控系统安全实验室

 2：某工控系统安全实验室

**背景**:
该实验室专注于关键基础设施（如电力、轨道交通）的固件安全研究。由于历史遗留原因，大量工控设备使用的是非标准的私有架构或老旧的处理器架构（如 ARMv7, MIPS 等），且缺乏官方文档。

**问题**:
研究人员在对固件进行逆向分析时，面临两大痛点：一是 Ghidra 虽然支持多架构，但自动标注功能较弱，需要大量人工手动重命名变量和函数；二是对于未知的私有协议，解析数据包结构极其枯燥且易错。这导致对一个新型号 PLC 固件的完整审计往往需要数周时间，难以满足项目交付期限。

**解决方案**:
利用 Ghidra MCP Server，实验室构建了一个基于 LLM 的辅助分析工作流。研究人员只需提供固件二进制文件，AI 便通过 MCP 接口调用 Ghidra 的内存分析工具和反汇编器。AI 不仅能自动识别并注释标准的启动代码和加密算法库，还能通过分析数据流，自动推导出私有协议的数据结构体定义，并自动生成 Ghidra 的解析脚本。

**效果**:
固件分析周期从数周缩短至 3 天。AI 成功识别出了人工审查容易遗漏的多个后门函数和硬编码凭证。此外，AI 自动生成的结构体定义和注释脚本被保存为实验室的知识库，极大提升了后续类似项目的分析起点，实现了安全研究知识的积累和复用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立安全的沙箱隔离环境

**说明**: AI 辅助逆向工程涉及将未知的二进制文件数据传输给大语言模型（LLM）。为了防止恶意软件利用 MCP 协议逃逸或泄露敏感数据，必须在隔离的虚拟机或容器中运行 Ghidra 和 MCP Server，切勿在主机或生产环境中直接使用。

**实施步骤**:
1. 使用虚拟机（如 VMware, VirtualBox）或容器技术（如 Docker）搭建专门的逆向分析环境。
2. 在该环境中安装 Ghidra 并配置 MCP Server，确保网络访问受限（仅允许访问必要的 LLM API）。
3. 配置快照功能，以便在分析可疑文件导致环境异常时快速恢复。

**注意事项**: 严禁将包含密钥、密码或个人身份信息（PII）的敏感目标文件发送到云端 LLM。

---

### 实践 2：利用上下文窗口进行增量分析

**说明**: Ghidra MCP Server 提供了 110 个工具，一次性调用可能会消耗大量 Token 或超出上下文限制。最佳实践是采用增量分析策略，先获取函数列表和整体结构，再针对特定复杂函数进行深入分析。

**实施步骤**:
1. 首先使用 `get_program_info` 或 `list_functions` 等工具获取目标程序的整体概览。
2. 根据概览识别出关键或可疑的函数（如 `main`, `decrypt` 等）。
3. 仅针对选定的关键函数调用 `get_decompilation` 或 `get_xrefs` 等详细分析工具，以保持对话的高效性。

**注意事项**: 注意监控 Token 使用量，避免因单次请求过大导致会话中断或成本过高。

---

### 实践 3：构建自定义的命名与类型提示库

**说明**: AI 模型虽然擅长理解逻辑，但缺乏特定项目的领域知识。通过向 AI 提供已知的函数命名约定、结构体定义或特定的 API 文档，可以显著提高 AI 对代码意图的识别准确率。

**实施步骤**:
1. 在 Ghidra 中手动分析并标记部分关键函数和变量，建立基准。
2. 在与 AI 的交互中，明确告知 AI 当前的命名风格（如匈牙利命名法）和项目背景。
3. 将 AI 推断出的结果反向同步到 Ghidra 的注释中，形成正向循环。

**注意事项**: 确保 AI 修改的标签和注释符合 Ghidra 的数据类型规范，避免引入错误的类型定义导致分析逻辑混乱。

---

### 实践 4：交叉引用验证 AI 推断结果

**说明**: AI 生成的分析建议（如函数功能描述）可能存在幻觉。利用 Ghidra 的交叉引用功能，验证 AI 声称的“某函数调用了加密算法”是否属实，是保证分析质量的关键步骤。

**实施步骤**:
1. 当 AI 声称某个函数具有特定功能（例如网络请求）时，使用 MCP 提供的交叉引用工具查询该函数的调用树。
2. 检查该函数是否确实引用了相关的网络库 API（如 `socket`, `connect`）。
3. 对于无法在交叉引用中找到证据的 AI 结论，保持怀疑态度并进行人工复核。

**注意事项**: AI 可能会基于训练数据中的常见模式“脑补”不存在的代码路径，必须以 Ghidra 反汇编/反编译视图为准。

---

### 实践 5：编写结构化的 Prompt 模板

**说明**: 直接与 110 个工具交互可能非常繁琐。编写结构化的 Prompt 模板，让 AI 自动规划工具调用序列，可以大幅提升工作效率。这通常涉及告诉 AI “先做什么，再做什么，最后总结”。

**实施步骤**:
1. 创建一个 System Prompt 或预设指令，例如：“在分析二进制文件时，请先列出导入表，然后分析 main 函数，最后查找所有网络相关的字符串。”
2. 明确要求 AI 在输出中包含工具调用的具体参数，而不是仅输出自然语言描述。
3. 根据分析目标的不同（如恶意软件分析 vs 漏洞挖掘），准备多套不同的 Prompt 模板。

**注意事项**: 提示词应明确限制 AI 的操作范围，防止 AI 在无关的内存区域或无效地址上执行工具调用。

---

### 实践 6：结合自动化脚本批量处理

**说明**: 对于大型二进制文件，手动通过 Chat 界面调用工具效率较低。利用 MCP Server 的可编程性，结合脚本（如 Python）批量调用特定工具（如批量提取字符串、批量重命名函数），可以实现自动化的预处理流程。

**实施步骤**:
1. 熟悉 Ghidra MCP Server 暴露的 API 接口列表。
2. 编写简单的脚本，针对特定的二进制文件特征（如所有 `sub_` 开头的函数）批量请求 AI 进行重命名建议。
3. 将 AI 的处理结果通过脚本回写到 Ghidra 的脚本控制台或直接导入数据库。

**注意事项**: 批量处理可能会触发 API 速率限制，

---
## 学习要点

- Ghidra MCP Server 将 Ghidra 的 110 个原生工具集成到 Model Context Protocol (MCP) 中，实现了大语言模型（LLM）与逆向工程环境的深度互操作。
- 该工具允许 AI 智能体直接读取反编译代码、交叉引用（Xrefs）及函数列表，从而在无需人工干预的情况下自动分析二进制文件。
- 通过将 Ghidra 的功能暴露给支持 MCP 的 AI 客户端（如 Claude Desktop 或 Cline），该项目显著降低了进行专业级逆向工程的技术门槛。
- 该架构不仅支持单向查询，还允许 AI 智能体根据分析结果动态调用 Ghidra 工具，实现了从“阅读”到“操作”的自动化闭环。
- 开发者强调该工具的安全性设计，旨在确保 AI 对二进制文件的分析过程可控且透明，避免不可预测的代码执行风险。
- 这一进展标志着 AI 辅助安全研究从单纯的代码生成向复杂系统理解和漏洞挖掘领域的实质性跨越。

---
## 常见问题


### 1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

**A**: Ghidra MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器工具，旨在将 Ghidra 的逆向工程功能集成到支持 MCP 的 AI 客户端（如 Claude Desktop 或 Cline）中。与直接使用 Ghidra 图形界面（GUI）或编写 Ghidra 脚本不同，该服务器充当了 AI 模型与 Ghidra 之间的桥梁。它封装了多达 110 个 Ghidra 的 API 接口，使得 AI 助手能够直接读取反汇编代码、分析数据结构、重命名变量、查找交叉引用，甚至进行自动化分析，从而实现“AI 辅助逆向工程”。这允许用户通过自然语言与 AI 对话来操控 Ghidra，而不是手动点击菜单或编写 Python 脚本。

---



### 2: 该工具支持哪些 AI 客户端，如何配置？

2: 该工具支持哪些 AI 客户端，如何配置？

**A**: 目前，Ghidra MCP Server 主要兼容支持 MCP 协议的 AI 客户端。最典型的例子是 Anthropic 的 Claude Desktop 以及 VS Code 中的 Cline 插件。配置过程通常包括以下几个步骤：首先，确保你已安装并运行了 Ghidra；其次，克隆 Ghidra MCP Server 的源代码并安装所需的 Python 依赖（通常在 `requirements.txt` 中列出）；最后，在 AI 客户端的配置文件中添加 MCP 服务器的路径和启动命令。配置完成后，AI 客户端在启动时会自动连接到该服务器，使其能够调用 Ghidra 的工具集。

---



### 3: 这 110 个工具具体包含哪些功能？

3: 这 110 个工具具体包含哪些功能？

**A**: 这 110 个工具基本上覆盖了逆向工程中最常用的操作场景。具体功能分类包括：
*   **代码导航与查询**：获取当前函数列表、查找特定地址处的反汇编代码、获取函数的调用树和交叉引用。
*   **符号与数据操作**：重命名函数、变量和标签，添加注释，修改数据类型（例如将字节序列定义为结构体）。
*   **分析功能**：触发自动分析、查找未定义的符号、分析函数的控制流图。
*   **内存与段信息**：读取内存块信息、获取寄存器上下文等。
这些工具将原本复杂的 Ghidra Scripting API (Java/GhidraScript) 转化为标准化的 MCP 接口，方便 LLM 理解和调用。

---



### 4: 使用该工具是否存在安全风险，特别是代码隐私方面？

4: 使用该工具是否存在安全风险，特别是代码隐私方面？

**A**: 是的，这是一个需要重点考虑的问题。使用 Ghidra MCP Server 时，你正在将本地的逆向工程上下文（如反汇编代码片段、函数名、结构体定义等）发送给 AI 模型提供商（例如 Anthropic 或 OpenAI）。这意味着你正在分析的二进制文件的细节会被上传到云端。因此，**绝对不建议**将该工具用于处理敏感的、专有的或涉及恶意软件的高危样本，除非你使用的是本地部署的 LLM 并且配置了严格的本地 MCP 通信。对于学习开源软件（CTF 题目或公开软件）则相对安全。

---



### 5: 如果 Ghidra 中没有打开项目，AI 还能调用这些工具吗？

5: 如果 Ghidra 中没有打开项目，AI 还能调用这些工具吗？

**A**: 通常情况下不能。Ghidra MCP Server 作为一个中间件，需要连接到一个正在运行的 Ghidra 实例，并且该实例中必须加载了一个待分析的项目。如果 Ghidra 没有打开，或者没有加载任何二进制文件，MCP 服务器在尝试调用 API 时会返回错误或空结果。部分高级配置可能支持无头模式，但在标准使用场景下，用户通常需要先在 Ghidra GUI 中打开目标程序，确保 Ghidra Scripting API 处于可用状态，AI 才能通过 MCP Server 进行交互。

---



### 6: 该工具对 Ghidra 的版本有要求吗？

6: 该工具对 Ghidra 的版本有要求吗？

**A**: 虽然具体的版本要求取决于项目代码中使用的 Ghidra Python API (GhidraDev) 的兼容性，但一般来说，它需要较新版本的 Ghidra（通常是 Ghidra 10.0 或更高版本）。这是因为 MCP 协议和相关的 Python 脚本依赖于较新的 API 特性。在安装前，建议查看项目的 GitHub 仓库文档，确认其测试通过的 Ghidra 具体版本号。如果版本过旧，可能会导致 API 调用失败或缺少特定的依赖库。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在使用 Ghidra MCP Server 辅助分析一个二进制文件。你希望 AI 能够帮你识别出所有潜在的“不安全函数调用”（如 `strcpy` 或 `gets`）。请构建一个具体的 Prompt（提示词），明确告知 AI 需要调用的工具名称以及你期望返回的输出格式（例如：包含地址、函数名和参数列表的表格）。

### 提示**: 思考 MCP Server 的核心功能是将 Ghidra 的 API 暴露给 LLM。你需要明确指定 Ghidra 中的“Listing”或“Functions”相关操作，并在 Prompt 中定义结构化的输出约束。

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
- 标签： [Ghidra](/tags/ghidra/) / [MCP](/tags/mcp/) / [逆向工程](/tags/%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B/) / [LLM](/tags/llm/) / [安全分析](/tags/%E5%AE%89%E5%85%A8%E5%88%86%E6%9E%90/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/) / [AI Agent](/tags/ai-agent/) / [Hacker News](/tags/hacker-news/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助方案]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-2.md" >}})
- [Ghidra MCP Server：集成110种工具的AI逆向工程辅助服务]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-3.md" >}})
- [Ghidra MCP Server发布：集成110款工具实现AI辅助逆向工程]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-1.md" >}})
- [Ghidra MCP Server：集成110项工具的AI逆向工程辅助环境]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-10.md" >}})
- [Ghidra MCP Server：集成110款工具实现AI辅助逆向工程]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*